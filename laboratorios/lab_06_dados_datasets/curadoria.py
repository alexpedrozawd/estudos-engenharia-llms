"""Curadoria determinística de conjuntos de avaliação da Aurora Educação (Cap. 6).

Tudo em biblioteca padrão e sem rede: validação de JSONL, deduplicação exata e
aproximada, amostragem estratificada e por reservatório, divisão por grupo sem
vazamento e manifesto de versão.
"""
import hashlib
import json
import random
import re
from collections import Counter
from typing import Dict, Iterable, List, Sequence, Tuple


def validar_jsonl(linhas: Iterable[str], obrigatorios: Sequence[str]) -> Tuple[List[Dict], List[str]]:
    """Valida cada linha como objeto JSON com os campos obrigatórios (schema-on-write)."""
    validos, erros = [], []
    for n, linha in enumerate(linhas, start=1):
        if not linha.strip():
            continue
        try:
            obj = json.loads(linha)
        except json.JSONDecodeError as exc:
            erros.append(f"linha {n}: JSON inválido ({exc.msg})")
            continue
        if not isinstance(obj, dict):
            erros.append(f"linha {n}: não é objeto")
            continue
        faltam = [c for c in obrigatorios if c not in obj or obj[c] in ("", None)]
        if faltam:
            erros.append(f"linha {n}: faltam {', '.join(faltam)}")
            continue
        validos.append(obj)
    return validos, erros


def normalizar(texto: str) -> str:
    texto = re.sub(r"[^\w\s]", "", texto.lower())
    return re.sub(r"\s+", " ", texto).strip()


def hash_texto(texto: str) -> str:
    return hashlib.sha256(normalizar(texto).encode("utf-8")).hexdigest()


def deduplicar_exatas(itens: Sequence[Dict], campo: str = "pergunta") -> Tuple[List[Dict], int]:
    """Mantém a primeira ocorrência de cada texto normalizado; devolve itens e removidos."""
    vistos, unicos = set(), []
    for item in itens:
        h = hash_texto(item[campo])
        if h not in vistos:
            vistos.add(h)
            unicos.append(item)
    return unicos, len(itens) - len(unicos)


def jaccard(a: str, b: str, n: int = 3) -> float:
    def ngramas(t: str):
        p = normalizar(t).split()
        if len(p) < n:
            return {tuple(p)}
        return {tuple(p[i:i + n]) for i in range(len(p) - n + 1)}
    x, y = ngramas(a), ngramas(b)
    return len(x & y) / len(x | y) if x | y else 1.0


def amostra_estratificada(itens: Sequence[Dict], chave: str, fracao: float,
                          minimo: int = 1, semente: int = 7) -> List[Dict]:
    """Sorteia dentro de cada estrato; garante `minimo` itens por estrato quando houver."""
    rng = random.Random(semente)
    grupos: Dict[str, List[Dict]] = {}
    for item in itens:
        grupos.setdefault(item[chave], []).append(item)
    amostra: List[Dict] = []
    for nome in sorted(grupos):
        g = grupos[nome]
        k = min(len(g), max(minimo, round(len(g) * fracao)))
        amostra.extend(rng.sample(g, k))
    return amostra


def reservatorio(fluxo: Iterable, k: int, semente: int = 7) -> List:
    """Amostragem por reservatório: k itens uniformes de um fluxo de tamanho desconhecido."""
    rng = random.Random(semente)
    res: List = []
    for n, item in enumerate(fluxo, start=1):
        if n <= k:
            res.append(item)
        else:
            j = rng.randint(1, n)
            if j <= k:
                res[j - 1] = item
    return res


def dividir_por_grupo(itens: Sequence[Dict], grupo: str, fracao_teste: float,
                      semente: int = 7) -> Tuple[List[Dict], List[Dict]]:
    """Divide por grupo (ex.: aluno) para que nenhum grupo apareça nos dois lados."""
    grupos = sorted({i[grupo] for i in itens})
    rng = random.Random(semente)
    rng.shuffle(grupos)
    n_teste = max(1, round(len(grupos) * fracao_teste))
    teste_g = set(grupos[:n_teste])
    treino = [i for i in itens if i[grupo] not in teste_g]
    teste = [i for i in itens if i[grupo] in teste_g]
    return treino, teste


def detectar_vazamento(ajuste: Sequence[Dict], teste: Sequence[Dict], campo: str = "pergunta",
                       limiar: float = 0.5) -> List[Tuple[str, str, float]]:
    """Lista pares (teste, ajuste, nota) com semelhança >= limiar."""
    achados = []
    for t in teste:
        melhor = max(ajuste, key=lambda a: jaccard(t[campo], a[campo]), default=None)
        if melhor is not None:
            nota = round(jaccard(t[campo], melhor[campo]), 3)
            if nota >= limiar:
                achados.append((t[campo], melhor[campo], nota))
    return achados


def manifesto(itens: Sequence[Dict], versao: str, origem: str, estrato: str,
              aceitador: str) -> Dict[str, object]:
    """Gera manifesto com contagens por estrato, sintéticos e hash do conteúdo."""
    corpo = "\n".join(json.dumps(i, ensure_ascii=False, sort_keys=True) for i in itens)
    return {
        "versao": versao,
        "origem": origem,
        "total": len(itens),
        "por_estrato": dict(sorted(Counter(i[estrato] for i in itens).items())),
        "sinteticos": sum(1 for i in itens if i.get("origem") == "sintetico"),
        "sha256": hashlib.sha256(corpo.encode("utf-8")).hexdigest()[:16],
        "aceitador": aceitador,
    }
