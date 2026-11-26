"""Pipeline de evals automatizados (Projeto 07): A vs B, juiz com inversão, Cohen's kappa e bootstrap pareado."""
from __future__ import annotations

import json
import os
import random
import sys
import time
from typing import Callable, Dict, List, Literal, Optional, Sequence

from pydantic import BaseModel, Field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402
from mercado_base import estatistica as est  # noqa: E402
from mercado_base.cliente_openai import gerar_estruturado  # noqa: E402

PROMPT_A = "Responda de forma breve à pergunta com base no contexto."
PROMPT_B = (
    "Você é o assistente da Aurora Educação (proposta didática). Responda com exatidão "
    "usando somente o contexto fornecido, cite explicitamente o rótulo [T1] quando usar uma "
    "informação e, se não houver apoio no contexto, responda exatamente: "
    "Não encontrei essa informação nos documentos."
)


class VereditoJuiz(BaseModel):
    vencedor: Literal["A", "B", "empate"]
    nota_a: int = Field(ge=1, le=5)
    nota_b: int = Field(ge=1, le=5)
    justificativa: str = Field(min_length=1, max_length=400)


SISTEMA_JUIZ = (
    "Você é um avaliador técnico rigoroso de respostas RAG. Compare a Resposta 1 e a Resposta 2 "
    "frente à pergunta e à resposta de referência. Penalize alucinações, omissões e falta de citação [T1] "
    "quando a referência citar. Responda estritamente no esquema JSON."
)


def carregar_casos(caminho: str | None = None) -> Dict[str, object]:
    alvo = caminho or os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados", "casos_eval.json")
    with open(alvo, encoding="utf-8") as f:
        return json.load(f)


def _inverter_rotulo(r: str) -> str:
    if r == "A":
        return "B"
    if r == "B":
        return "A"
    return "empate"


def julgar_com_inversao(
    cliente_juiz,
    pergunta: str,
    referencia: str,
    resp_a: str,
    resp_b: str,
) -> Dict[str, object]:
    """Julga (A, B) e (B, A) para neutralizar viés de posição; discordância consolida em empate."""

    # EXERCICIO-INICIO: chame o juiz em A/B e em B/A, desinverta o 2º rótulo e só aceite vencedor consistente.
    def _chamar(primeiro: str, segundo: str):
        msgs = [
            {"role": "system", "content": SISTEMA_JUIZ},
            {
                "role": "user",
                "content": (
                    f"Pergunta: {pergunta}\n"
                    f"Referência esperada: {referencia}\n\n"
                    f"Resposta A:\n{primeiro}\n\n"
                    f"Resposta B:\n{segundo}\n\n"
                    "Atribua nota_a (1-5), nota_b (1-5), vencedor ('A', 'B' ou 'empate') e justificativa."
                ),
            },
        ]
        return gerar_estruturado(cliente_juiz, msgs, VereditoJuiz, max_reparos=2, max_tokens=256)

    v1, meta1 = _chamar(resp_a, resp_b)
    v2, meta2 = _chamar(resp_b, resp_a)
    v2_mapeado = _inverter_rotulo(v2.vencedor)
    vies_posicao = v1.vencedor != v2_mapeado
    vencedor = "empate" if vies_posicao else v1.vencedor
    nota_a = round((v1.nota_a + v2.nota_b) / 2.0, 3)
    nota_b = round((v1.nota_b + v2.nota_a) / 2.0, 3)
    return {
        "vencedor": vencedor,
        "vencedor_direto": v1.vencedor,
        "vencedor_invertido_mapeado": v2_mapeado,
        "vies_posicao": vies_posicao,
        "nota_a": nota_a,
        "nota_b": nota_b,
        "justificativa": v1.justificativa,
        "reparos": int(meta1["reparos"]) + int(meta2["reparos"]),
        "tokens_entrada": int(meta1["tokens_entrada"]) + int(meta2["tokens_entrada"]),
        "tokens_saida": int(meta1["tokens_saida"]) + int(meta2["tokens_saida"]),
    }
    # EXERCICIO-FIM


def cohen_kappa(rotulos_a: Sequence[str], rotulos_b: Sequence[str]) -> float:
    """Calcula o coeficiente kappa de Cohen entre dois avaliadores categóricos."""
    # EXERCICIO-INICIO: kappa = (po − pe)/(1 − pe), com pe pela soma dos produtos das frequências marginais; valide os tamanhos.
    if len(rotulos_a) != len(rotulos_b) or not rotulos_a:
        raise ValueError("as listas de rótulos devem ter o mesmo tamanho (> 0)")
    n = len(rotulos_a)
    categorias = sorted(set(rotulos_a) | set(rotulos_b))
    po = sum(1 for a, b in zip(rotulos_a, rotulos_b) if a == b) / n
    pe = sum((rotulos_a.count(c) / n) * (rotulos_b.count(c) / n) for c in categorias)
    if abs(1.0 - pe) < 1e-12:
        return 1.0 if abs(po - 1.0) < 1e-12 else 0.0
    return round((po - pe) / (1.0 - pe), 4)
    # EXERCICIO-FIM


def bootstrap_pareado(
    escores_a: Sequence[float],
    escores_b: Sequence[float],
    *,
    n_amostras: int = 2000,
    alpha: float = 0.05,
    seed: int = 42,
) -> Dict[str, object]:
    """Testa ganho pareado (B - A) via bootstrap com intervalo de confiança bilateral."""
    # EXERCICIO-INICIO: diferenças pareadas, reamostragem com semente, IC por percentis e p-valor unilateral (fração de médias <= 0).
    if len(escores_a) != len(escores_b) or not escores_a:
        raise ValueError("escores_a e escores_b devem ter o mesmo tamanho (> 0)")
    if n_amostras < 10:
        raise ValueError("n_amostras deve ser >= 10")
    n = len(escores_a)
    diffs_obs = [float(b) - float(a) for a, b in zip(escores_a, escores_b)]
    rng = random.Random(seed)
    medias_boot: List[float] = []
    nao_positivos = 0
    for _ in range(n_amostras):
        soma = 0.0
        for _i in range(n):
            soma += diffs_obs[rng.randrange(n)]
        media_b = soma / n
        medias_boot.append(media_b)
        if media_b <= 0.0:
            nao_positivos += 1
    medias_boot.sort()
    idx_inf = max(0, min(n_amostras - 1, int((alpha / 2.0) * n_amostras)))
    idx_sup = max(0, min(n_amostras - 1, int((1.0 - alpha / 2.0) * n_amostras) - 1))
    ic_inf = round(medias_boot[idx_inf], 4)
    ic_sup = round(medias_boot[idx_sup], 4)
    return {
        "n": n,
        "n_amostras": n_amostras,
        "media_a": round(sum(escores_a) / n, 4),
        "media_b": round(sum(escores_b) / n, 4),
        "diferenca_media": round(sum(diffs_obs) / n, 4),
        "ic_inferior": ic_inf,
        "ic_superior": ic_sup,
        "p_valor_unilateral": round(nao_positivos / n_amostras, 4),
        "significativo": ic_inf > 0.0,
    }
    # EXERCICIO-FIM


def kappa_bootstrap(rotulos_a: Sequence[str], rotulos_b: Sequence[str], *, n_amostras: int = 2000,
                    alpha: float = 0.05, seed: int = 42) -> Dict[str, float]:
    """IC por percentis do kappa, reamostrando pares (com 40 pares a faixa ainda é larga)."""
    n = len(rotulos_a)
    rng = random.Random(seed)
    valores = []
    for _ in range(n_amostras):
        idx = [rng.randrange(n) for _ in range(n)]
        valores.append(cohen_kappa([rotulos_a[i] for i in idx], [rotulos_b[i] for i in idx]))
    valores.sort()
    return {"ic_inferior": valores[max(0, int(alpha / 2 * n_amostras))],
            "ic_superior": valores[min(n_amostras - 1, int((1 - alpha / 2) * n_amostras) - 1)]}


def _gerar_resposta(cliente, prompt_sistema: str, contexto: str, pergunta: str) -> str:
    usuario = f"Contexto:\n{contexto}\n\nPergunta: {pergunta}"
    if hasattr(cliente, "completar_chat"):
        r = cliente.completar_chat(
            [{"role": "system", "content": prompt_sistema}, {"role": "user", "content": usuario}],
            temperatura=0.0,
            max_tokens=180,
        )
        return r.conteudo.strip()
    return cliente.completar(usuario, sistema=prompt_sistema, temperatura=0.0, max_tokens=180).texto.strip()


def avaliar_prompts(
    dados: Dict[str, object],
    cliente_gerador,
    cliente_juiz,
    *,
    limiar_kappa: float = 0.60,
    n_bootstrap: int = 2000,
    seed: int = 42,
    ao_concluir_geracao: Optional[Callable[[], None]] = None,
) -> Dict[str, object]:
    """Calibra o juiz (Cohen's kappa), gera A vs B em lote, julga com inversão e decide por bootstrap."""
    casos = dados["casos_avaliacao"]
    geradas: List[tuple[Dict[str, object], str, str]] = []
    latencias_gerador_ms: List[float] = []
    for caso in casos:
        t0 = time.perf_counter()
        resp_a = _gerar_resposta(cliente_gerador, PROMPT_A, str(caso["contexto"]), str(caso["pergunta"]))
        latencias_gerador_ms.append(round((time.perf_counter() - t0) * 1000.0, 3))
        t0 = time.perf_counter()
        resp_b = _gerar_resposta(cliente_gerador, PROMPT_B, str(caso["contexto"]), str(caso["pergunta"]))
        latencias_gerador_ms.append(round((time.perf_counter() - t0) * 1000.0, 3))
        geradas.append((caso, resp_a, resp_b))

    if ao_concluir_geracao is not None:
        ao_concluir_geracao()

    pares_cal = dados["pares_calibracao"]
    rotulos_humanos: List[str] = []
    rotulos_juiz: List[str] = []
    vieses_cal = 0
    latencias_juiz_ms: List[float] = []
    for par in pares_cal:
        t0 = time.perf_counter()
        j = julgar_com_inversao(
            cliente_juiz,
            str(par["pergunta"]),
            str(par["referencia"]),
            str(par["resposta_a"]),
            str(par["resposta_b"]),
        )
        latencias_juiz_ms.append(round((time.perf_counter() - t0) * 1000.0, 3))
        rotulos_humanos.append(str(par["julgamento_humano"]))
        rotulos_juiz.append(str(j["vencedor"]))
        vieses_cal += int(bool(j["vies_posicao"]))

    kappa = cohen_kappa(rotulos_humanos, rotulos_juiz)
    juiz_calibrado = kappa >= limiar_kappa
    concordantes = sum(1 for h, j in zip(rotulos_humanos, rotulos_juiz) if h == j)
    por_origem: Dict[str, Dict[str, object]] = {}
    for origem in sorted({str(p.get("origem", "pre_rotulado")) for p in pares_cal}):
        idx = [i for i, p in enumerate(pares_cal) if str(p.get("origem", "pre_rotulado")) == origem]
        ok = sum(1 for i in idx if rotulos_humanos[i] == rotulos_juiz[i])
        por_origem[origem] = {"pares": len(idx), "kappa": cohen_kappa([rotulos_humanos[i] for i in idx],
                                                                      [rotulos_juiz[i] for i in idx]),
                              "concordancia": round(ok / len(idx), 4), "wilson95_concordancia": est.wilson(ok, len(idx))}

    resultados_casos: List[Dict[str, object]] = []
    notas_a: List[float] = []
    notas_b: List[float] = []
    placar = {"A": 0, "B": 0, "empate": 0}
    vieses_eval = 0

    for caso, resp_a, resp_b in geradas:
        t0 = time.perf_counter()
        julg = julgar_com_inversao(
            cliente_juiz,
            str(caso["pergunta"]),
            str(caso["referencia"]),
            resp_a,
            resp_b,
        )
        latencias_juiz_ms.append(round((time.perf_counter() - t0) * 1000.0, 3))
        notas_a.append(float(julg["nota_a"]))
        notas_b.append(float(julg["nota_b"]))
        placar[str(julg["vencedor"])] += 1
        vieses_eval += int(bool(julg["vies_posicao"]))
        resultados_casos.append({
            "id": caso["id"],
            "resposta_a": resp_a,
            "resposta_b": resp_b,
            **julg,
        })

    boot = bootstrap_pareado(notas_a, notas_b, n_amostras=n_bootstrap, seed=seed)
    return {
        "calibracao": {
            "pares": len(pares_cal),
            "kappa": kappa,
            "limiar_kappa": limiar_kappa,
            "juiz_calibrado": juiz_calibrado,
            "vieses_posicao": vieses_cal,
            "kappa_ic95_bootstrap": kappa_bootstrap(rotulos_humanos, rotulos_juiz, seed=seed) if pares_cal else None,
            "concordancia": round(concordantes / max(len(pares_cal), 1), 4),
            "wilson95_concordancia": est.wilson(concordantes, len(pares_cal)),
            "por_origem": por_origem,
        },
        "avaliacao": {
            "casos": len(casos),
            "placar": placar,
            "vieses_posicao": vieses_eval,
            "bootstrap": boot,
            "wilson95_vitorias_b": est.wilson(placar["B"], len(casos)),
            "teste_sinal_vitorias": {"vitorias_b": placar["B"], "vitorias_a": placar["A"],
                                     "p_valor_binomial_exato": est.mcnemar_exato(placar["B"], placar["A"])},
            "latencia_ms": {
                "gerador": mb.resumir_latencias_ms(latencias_gerador_ms),
                "juiz": mb.resumir_latencias_ms(latencias_juiz_ms),
            },
        },
        "promover_b": bool(juiz_calibrado and boot["significativo"]),
        "casos": resultados_casos,
    }
