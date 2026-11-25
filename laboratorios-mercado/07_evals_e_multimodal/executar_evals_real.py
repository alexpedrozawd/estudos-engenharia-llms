"""Execução real do Projeto 07: evals A vs B contra LLM local + renderização/payload VLM com pdftoppm.

    .venv-mercado/bin/python -I laboratorios-mercado/07_evals_e_multimodal/executar_evals_real.py \
        --llm-base-url http://127.0.0.1:8081/v1 --llm-modelo qwen3-4b-instruct --registrar
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402
from mercado_base.cliente_openai import ClienteChatOpenAI  # noqa: E402

import eval_pipeline as ep  # noqa: E402
import extracao_multimodal as em  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--llm-base-url", default=os.environ.get("LLM_BASE_URL", "http://127.0.0.1:8081/v1"))
    ap.add_argument("--llm-modelo", default=os.environ.get("LLM_MODELO", "qwen3-4b-instruct"))
    ap.add_argument("--vlm-base-url", default=os.environ.get("VLM_BASE_URL", ""))
    ap.add_argument("--vlm-modelo", default=os.environ.get("VLM_MODELO", ""))
    ap.add_argument("--registrar", action="store_true")
    args = ap.parse_args(argv)

    dados = ep.carregar_casos()
    cli_llm = ClienteChatOpenAI(args.llm_base_url, args.llm_modelo, timeout_s=180.0)
    res_eval = ep.avaliar_prompts(dados, cli_llm, cli_llm, n_bootstrap=2000, seed=42)

    pdf_bytes = em.gerar_pdf_recibo_aurora()
    pngs = em.renderizar_pdf_pngs(pdf_bytes, dpi=150)
    msgs_vlm = em.montar_mensagens_vlm(pngs, "Extraia documento, data_emissao, itens e total_informado.")
    bloco_vlm: dict[str, object] = {
        "vlm_remoto_executado": False,
        "paginas_png": len(pngs),
        "bytes_png": [len(p) for p in pngs],
        "payload_multimodal_valido": (
            isinstance(msgs_vlm[1]["content"], list)
            and msgs_vlm[1]["content"][1]["image_url"]["url"].startswith("data:image/png;base64,")
        ),
    }
    if args.vlm_base_url and args.vlm_modelo:
        cli_vlm = ClienteChatOpenAI(args.vlm_base_url, args.vlm_modelo, timeout_s=180.0)
        bloco_vlm["vlm_remoto_executado"] = True
        bloco_vlm["extracao"] = em.extrair_fatura_de_pdf(pdf_bytes, cli_vlm)

    saida = {
        "configuracao": {"llm_modelo": args.llm_modelo, "vlm_modelo": args.vlm_modelo or None},
        "calibracao": res_eval["calibracao"],
        "avaliacao": res_eval["avaliacao"],
        "promover_b": res_eval["promover_b"],
        "amostra_casos": res_eval["casos"][:4],
        "multimodal": bloco_vlm,
    }
    print(json.dumps(saida, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p07-evals-e-multimodal", saida))
    return 0


if __name__ == "__main__":
    sys.exit(main())
