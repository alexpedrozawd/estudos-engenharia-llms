"""Ajuste fino em miniatura, offline e determinístico (Cap. 15).

1. Calculadora de memória de treino (pesos, gradientes, estados do Adam e ativações).
2. LoRA de verdade, em escala de brinquedo: uma matriz base congelada W e um
   adaptador de posto baixo A·B treinado por gradiente; separa validação e para
   quando ela piora (parada antecipada).
3. Quantização int8 com escala única e por bloco, com o erro de volta.
4. Comparação antes/depois por fatia e manifesto de versão para refazer o ajuste.

Para treino real, use uma biblioteca de PEFT num modelo pequeno; mantenha estes
testes como regressão das contas e do protocolo (validação, parada, fatias).
"""
import hashlib
import json
import random
from typing import Dict, List, Sequence, Tuple

Matriz = List[List[float]]


# ---------- 1. Memória de treino (GB decimais: bilhões de parâmetros x bytes) ----------
def memoria_treino(n_bilhoes: float, metodo: str = "completo", bytes_peso: float = 2, bytes_estado: float = 2,
                   fracao_treinavel: float = 0.01, ativacoes_gb: float = 0.0) -> Dict[str, float]:
    """`metodo`: completo, lora ou qlora (no QLoRA, pesos congelados em 4 bits = 0,5 byte)."""
    # EXERCICIO-INICIO: pesos (QLoRA = 0,5 byte) + adaptador; gradiente e 2 estados do Adam só nos treináveis; some ativações; valide o método.
    if metodo not in {"completo", "lora", "qlora"}:
        raise ValueError(f"método desconhecido: {metodo}")
    peso = 0.5 if metodo == "qlora" else bytes_peso
    treinaveis = n_bilhoes if metodo == "completo" else n_bilhoes * fracao_treinavel
    pesos = n_bilhoes * peso + (0 if metodo == "completo" else treinaveis * bytes_peso)
    grad_e_adam = treinaveis * bytes_estado * 3          # 1 gradiente + 2 estados do Adam
    return {"pesos": round(pesos, 3), "grad_e_adam": round(grad_e_adam, 3), "ativacoes": ativacoes_gb,
            "total": round(pesos + grad_e_adam + ativacoes_gb, 3)}
    # EXERCICIO-FIM


# ---------- 2. LoRA em miniatura ----------
def _mul(a: Matriz, b: Matriz) -> Matriz:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _soma(a: Matriz, b: Matriz) -> Matriz:
    return [[x + y for x, y in zip(la, lb)] for la, lb in zip(a, b)]


def _prever(x: Sequence[float], m: Matriz) -> List[float]:
    return [sum(x[k] * m[k][j] for k in range(len(x))) for j in range(len(m[0]))]


def perda(dados: Sequence[Tuple[List[float], List[float]]], m: Matriz) -> float:
    return sum(sum((p - y) ** 2 for p, y in zip(_prever(x, m), alvo)) for x, alvo in dados) / len(dados)


def tarefa_sintetica(d: int = 4, n: int = 120, ruido: float = 0.05, semente: int = 15):
    """Base W e tarefa nova W + u·v (mudança de posto 1), com ruído; devolve W, treino e validação."""
    rng = random.Random(semente)
    w = [[rng.uniform(-1, 1) for _ in range(d)] for _ in range(d)]
    u = [[rng.uniform(-1, 1)] for _ in range(d)]
    v = [[rng.uniform(-1, 1) for _ in range(d)]]
    alvo_m = _soma(w, _mul(u, v))
    dados = []
    for _ in range(n):
        x = [rng.uniform(-1, 1) for _ in range(d)]
        dados.append((x, [y + rng.gauss(0, ruido) for y in _prever(x, alvo_m)]))
    corte = int(n * 0.9)                                    # 10% para validação, como no estudo de caso
    return w, dados[:corte], dados[corte:]


def treinar_lora(w: Matriz, treino, validacao, r: int = 1, lr: float = 0.3, epocas: int = 500,
                 paciencia: int = 5, semente: int = 15) -> Dict[str, object]:
    """Treina só A (d×r) e B (r×d); W fica congelada. B começa em zero, então o ajuste parte do modelo base."""
    rng = random.Random(semente)
    d = len(w)
    a = [[rng.uniform(-0.5, 0.5) for _ in range(r)] for _ in range(d)]
    b = [[0.0] * d for _ in range(r)]
    # época 0 = modelo base: se o adaptador nunca superar a base na validação, fica B = 0 (sem ajuste)
    historico, melhor, melhor_ab, sem_melhora = [], perda(validacao, w), (a, b, 0), 0
    for epoca in range(1, epocas + 1):
        m = _soma(w, _mul(a, b))
        g = [[0.0] * d for _ in range(d)]                   # gradiente da perda em relação a ΔW = A·B
        for x, alvo in treino:
            erro = [p - y for p, y in zip(_prever(x, m), alvo)]
            for i in range(d):
                for j in range(d):
                    g[i][j] += 2 * x[i] * erro[j] / len(treino)
        bt = [list(col) for col in zip(*b)]
        at = [list(col) for col in zip(*a)]
        da, db = _mul(g, bt), _mul(at, g)
        a = [[a[i][k] - lr * da[i][k] for k in range(r)] for i in range(d)]
        b = [[b[k][j] - lr * db[k][j] for j in range(d)] for k in range(r)]
        pv = perda(validacao, _soma(w, _mul(a, b)))
        historico.append(pv)
        if pv < melhor - 1e-9:
            melhor, melhor_ab, sem_melhora = pv, (a, b, epoca), 0
        else:
            sem_melhora += 1
            if sem_melhora >= paciencia:
                break
    a, b, epoca_melhor = melhor_ab
    return {"A": a, "B": b, "melhor_epoca": epoca_melhor, "epocas_rodadas": len(historico),
            "val_antes": perda(validacao, w), "val_depois": melhor, "historico": historico,
            "parametros_treinaveis": 2 * d * r, "parametros_base": d * d}


def parada_antecipada(perdas_val: Sequence[float], paciencia: int = 1) -> int:
    """Época (1-based) com menor perda antes de `paciencia` épocas seguidas sem melhora."""
    # EXERCICIO-INICIO: guarde a menor perda de validação e sua época (base 1); pare após `paciencia` épocas sem melhora.
    melhor, idx, sem = float("inf"), 0, 0
    for i, v in enumerate(perdas_val, start=1):
        if v < melhor:
            melhor, idx, sem = v, i, 0
        else:
            sem += 1
            if sem >= paciencia:
                break
    return idx
    # EXERCICIO-FIM


# ---------- 3. Quantização ----------
def quantizar_int8(vetor: Sequence[float], bloco: int = 0) -> Tuple[List[int], List[float], float]:
    """Escala única (bloco=0) ou por bloco; devolve inteiros, escalas e erro máximo de volta."""
    # EXERCICIO-INICIO: por bloco: escala = max|x|/127 (ou 1.0); q = round(x/escala); devolva (valores, escalas).
    tam = bloco or len(vetor)
    q, escalas, erro = [], [], 0.0
    for ini in range(0, len(vetor), tam):
        parte = vetor[ini:ini + tam]
        escala = max(abs(x) for x in parte) / 127 or 1.0
        qs = [round(x / escala) for x in parte]
        erro = max(erro, max(abs(x - v * escala) for x, v in zip(parte, qs)))
        q.extend(qs)
        escalas.append(escala)
    return q, escalas, erro
    # EXERCICIO-FIM


# ---------- 4. Antes/depois por fatia e manifesto ----------
def comparar_por_fatia(registros: Sequence[Dict[str, object]], tolerancia: float = 0.0) -> Dict[str, object]:
    """registros: {fatia, base: 0/1, ajustado: 0/1}. Aponta fatias que pioraram além da tolerância."""
    fatias: Dict[str, List[Tuple[int, int]]] = {}
    for r in registros:
        fatias.setdefault(str(r["fatia"]), []).append((int(r["base"]), int(r["ajustado"])))
    tabela = {f: {"base": sum(b for b, _ in v) / len(v), "ajustado": sum(a for _, a in v) / len(v), "n": len(v)}
              for f, v in sorted(fatias.items())}
    pioras = [f for f, t in tabela.items() if t["ajustado"] < t["base"] - tolerancia]
    return {"tabela": tabela, "pioras": pioras, "aprovar": not pioras}


def manifesto(conjunto: Sequence[Dict[str, object]], modelo_base: str, adaptador: str, hiper: Dict[str, object]) -> Dict[str, str]:
    linhas = "\n".join(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in conjunto)
    return {"conjunto_sha256": hashlib.sha256(linhas.encode("utf-8")).hexdigest()[:16], "modelo_base": modelo_base,
            "adaptador": adaptador, "hiperparametros": json.dumps(hiper, sort_keys=True)}
