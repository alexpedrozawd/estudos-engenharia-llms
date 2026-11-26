"""Amplia `dados/casos_eval.json` (Etapa 3) de forma determinística, sem LLM, a partir do corpus do P02.

- Casos de avaliação: os 16 manuais + 1 por pergunta de `consultas_ampliadas.json` (contexto = página que
  responde, rotulada [T1]) + recusas por construção (pergunta de um documento, contexto de outro de outro
  departamento; referência = frase de recusa do PROMPT_B), até `--total-casos`.
- Pares de calibração: os 12 pré-rotulados pelo autor do lab na Fase 6 (`origem: pre_rotulado`; não houve
  revisão humana independente) + pares com **defeito conhecido**
  (`origem: construcao`): uma resposta correta (referência) contra uma cópia com número trocado, sem
  citação, com afirmação inventada ou com recusa indevida; metade dos pares tem a boa em A, escolhida por hash. O rótulo vem da
  construção, não de julgamento humano: mede se o juiz pega defeitos claros e é mais fácil que o par pré-rotulado.

    .venv-mercado/bin/python -I laboratorios-mercado/07_evals_e_multimodal/montar_casos_ampliados.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
P02 = os.path.join(os.path.dirname(AQUI), "02_rag_producao", "dados")
CASOS = os.path.join(AQUI, "dados", "casos_eval.json")
RECUSA = "Não encontrei essa informação nos documentos."
INVENTADA = " Além disso, o pedido pode ser feito a qualquer momento, sem custo e sem documentos."
DEFEITOS = ("numero_trocado", "sem_citacao", "afirmacao_inventada", "recusa_indevida")


def _h(semente: str, texto: str) -> str:
    return hashlib.sha256((semente + texto).encode()).hexdigest()


def trocar_numero(texto: str) -> str | None:
    m = re.search(r"\d+", texto)
    if not m:
        return None
    n = int(m.group())
    novo = n * 2 if n > 1 else n + 1
    return texto[:m.start()] + str(novo) + texto[m.end():]


def aplicar_defeito(referencia: str, defeito: str) -> str:
    if defeito == "numero_trocado":
        return trocar_numero(referencia) or referencia.rstrip(".") + "." + INVENTADA
    if defeito == "sem_citacao":
        return re.sub(r"\s*\[T1\]", "", referencia)
    if defeito == "afirmacao_inventada":
        return referencia + INVENTADA
    return RECUSA


def contexto_da_pagina(corpus: dict, doc: str, pagina: int) -> str:
    linhas = corpus[doc]["paginas"][pagina - 1]
    texto = " ".join(" | ".join(l) if isinstance(l, list) else l for l in linhas)
    return f"[T1] ({doc}) {texto}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--total-casos", type=int, default=150)
    ap.add_argument("--pares-construcao", type=int, default=28)
    ap.add_argument("--semente", default="aurora-p07-v1")
    args = ap.parse_args(argv)

    with open(CASOS, encoding="utf-8") as f:
        dados = json.load(f)
    manuais = [c for c in dados["casos_avaliacao"] if c.get("origem", "manual") == "manual"]
    humanos = [p for p in dados["pares_calibracao"] if p.get("origem", "pre_rotulado") == "pre_rotulado"]
    with open(os.path.join(P02, "corpus_ampliado.json"), encoding="utf-8") as f:
        corpus = json.load(f)["documentos"]
    with open(os.path.join(P02, "consultas_ampliadas.json"), encoding="utf-8") as f:
        consultas = json.load(f)

    casos = [dict(c, origem="manual") for c in manuais]
    for q in consultas:
        crit = q["relevantes"][0]
        casos.append({"id": f"ev-{q['id']}", "origem": "corpus_p02", "consulta_p02": q["id"],
                      "contexto": contexto_da_pagina(corpus, crit["doc"], int(crit["pagina"])),
                      "pergunta": q["pergunta"], "referencia": q["resposta_referencia"]})
    faltam = args.total_casos - len(casos)
    if faltam < 0:
        raise SystemExit(f"FALHA {len(casos)} casos já passam de --total-casos")
    ordem = sorted(consultas, key=lambda q: _h(args.semente + "|recusa|", q["id"]))
    for q in ordem[:faltam]:
        doc_q = q["relevantes"][0]["doc"]
        depto = corpus[doc_q]["metadados"]["departamento"]
        outros = sorted((d for d in corpus if corpus[d]["metadados"]["departamento"] != depto),
                        key=lambda d: _h(args.semente + q["id"], d))
        casos.append({"id": f"ev-recusa-{q['id']}", "origem": "recusa_construcao", "consulta_p02": q["id"],
                      "contexto": contexto_da_pagina(corpus, outros[0], 1), "pergunta": q["pergunta"],
                      "referencia": RECUSA})

    pares = [dict(p, origem="pre_rotulado") for p in humanos]
    escolhidas = sorted(consultas, key=lambda q: _h(args.semente + "|cal|", q["id"]))[:args.pares_construcao]
    # Metade dos pares com a resposta boa em A, escolhida por hash (sem viés de posição no rótulo).
    boa_em_a_ids = {q["id"] for q in sorted(escolhidas, key=lambda q: _h(args.semente + "|lado|", q["id"]))
                    [:len(escolhidas) // 2]}
    for i, q in enumerate(escolhidas):
        defeito = DEFEITOS[i % len(DEFEITOS)]
        boa, ruim = q["resposta_referencia"], aplicar_defeito(q["resposta_referencia"], defeito)
        boa_em_a = q["id"] in boa_em_a_ids
        pares.append({"id": f"cal-{q['id']}", "origem": "construcao", "defeito": defeito,
                      "pergunta": q["pergunta"], "referencia": q["resposta_referencia"],
                      "resposta_a": boa if boa_em_a else ruim, "resposta_b": ruim if boa_em_a else boa,
                      "julgamento_humano": "A" if boa_em_a else "B"})

    with open(CASOS, "w", encoding="utf-8") as f:
        json.dump({"pares_calibracao": pares, "casos_avaliacao": casos}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps({"casos": len(casos), "pares": len(pares),
                      "casos_por_origem": {o: sum(1 for c in casos if c["origem"] == o)
                                           for o in ("manual", "corpus_p02", "recusa_construcao")},
                      "pares_por_origem": {o: sum(1 for p in pares if p["origem"] == o)
                                           for o in ("pre_rotulado", "construcao")}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
