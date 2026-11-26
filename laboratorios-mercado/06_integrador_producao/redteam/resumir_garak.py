"""Consolida relatórios `*.report.jsonl` do garak (Etapa 4) num registro em `execucoes/`.

Para cada lote (prefixo do relatório) e cada par sonda × detector: tentativas avaliadas, aprovadas, falhas,
`nones` (sem saída, ex.: HTTP 422 por pergunta longa) e taxa de falha com Wilson 95%. As saídas que o
detector marcou (nota >= 0,5) entram truncadas, para a análise manual de falso positivo. Sem rede.

    .venv-mercado/bin/python -I laboratorios-mercado/06_integrador_producao/redteam/resumir_garak.py \
        rascunho-local/redteam/saida --registrar
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import mercado_base as mb  # noqa: E402
from mercado_base import estatistica as est  # noqa: E402


def resumir_relatorio(linhas: List[Dict[str, object]], max_amostras: int = 5) -> Dict[str, object]:
    versao = next((str(e.get("garak_version")) for e in linhas if e.get("entry_type") == "init"), None)
    avaliacoes = []
    for e in linhas:
        if e.get("entry_type") != "eval":
            continue
        total, falhas = int(e["total_evaluated"]), int(e["fails"])
        avaliacoes.append({"sonda": e["probe"], "detector": e["detector"], "avaliadas": total,
                           "aprovadas": int(e["passed"]), "falhas": falhas, "nones": int(e.get("nones") or 0),
                           "taxa_falha": round(falhas / total, 4) if total else None,
                           "wilson95_falha": est.wilson(falhas, total)})
    marcadas: Dict[str, List[str]] = {}
    for e in linhas:
        if e.get("entry_type") != "attempt" or e.get("status") != 2:
            continue
        for det, notas in (e.get("detector_results") or {}).items():
            for saida, nota in zip(e.get("outputs") or [], notas):
                if nota is not None and nota >= 0.5:
                    lista = marcadas.setdefault(f"{e['probe_classname']}|{det}", [])
                    if len(lista) < max_amostras:
                        lista.append(str((saida or {}).get("text") or "")[:200])
    incompletas = sorted({str(e["probe_classname"]) for e in linhas if e.get("entry_type") == "attempt"}
                         - {a["sonda"] for a in avaliacoes})
    return {"versao_garak": versao, "avaliacoes": avaliacoes, "saidas_marcadas": marcadas,
            "sondas_sem_avaliacao": incompletas}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta")
    ap.add_argument("--registrar", action="store_true")
    args = ap.parse_args(argv)
    lotes = {}
    for caminho in sorted(glob.glob(os.path.join(args.pasta, "*.report.jsonl"))):
        with open(caminho, encoding="utf-8") as f:
            linhas = [json.loads(l) for l in f if l.strip()]
        lotes[os.path.basename(caminho).removesuffix(".report.jsonl")] = resumir_relatorio(linhas)
    if not lotes:
        print("FALHA nenhum relatório *.report.jsonl em", args.pasta)
        return 2
    saida = {"alvo": "P06 POST /v1/assistente (X-API-Key, perfil aluno)", "lotes": lotes}
    print(json.dumps(saida, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p06-red-teaming-garak", saida))
    return 0


if __name__ == "__main__":
    sys.exit(main())
