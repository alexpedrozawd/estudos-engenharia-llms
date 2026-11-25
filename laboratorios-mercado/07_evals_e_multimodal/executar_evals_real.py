"""Execução real do Projeto 07: evals A vs B (gerador e juiz separáveis) + payload VLM via pdftoppm.

    LLM_BASE_URL=http://127.0.0.1:11434/v1 LLM_MODELO=qwen3:4b-instruct \
    JUIZ_MODELO=qwen3.8:27b-ud-iq3_xxs JUIZ_REASONING_EFFORT=none OLLAMA_HOST=http://127.0.0.1:11434 \
    .venv-mercado/bin/python -I laboratorios-mercado/07_evals_e_multimodal/executar_evals_real.py --registrar
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402
from mercado_base.cliente_openai import (  # noqa: E402
    ClienteChatOpenAI,
    descarregar_modelo_ollama,
    medir_memoria_ollama,
)

import eval_pipeline as ep  # noqa: E402
import extracao_multimodal as em  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--llm-base-url", default=os.environ.get("LLM_BASE_URL", "http://127.0.0.1:8081/v1"))
    ap.add_argument("--llm-modelo", default=os.environ.get("LLM_MODELO", "qwen3-4b-instruct"))
    ap.add_argument("--llm-reasoning-effort", default=os.environ.get("LLM_REASONING_EFFORT", ""))
    ap.add_argument("--juiz-base-url", default=os.environ.get("JUIZ_BASE_URL", ""))
    ap.add_argument("--juiz-modelo", default=os.environ.get("JUIZ_MODELO", ""))
    ap.add_argument("--juiz-reasoning-effort", default=os.environ.get("JUIZ_REASONING_EFFORT", ""))
    ap.add_argument("--ollama-host", default=os.environ.get("OLLAMA_HOST", ""))
    ap.add_argument("--vlm-base-url", default=os.environ.get("VLM_BASE_URL", ""))
    ap.add_argument("--vlm-modelo", default=os.environ.get("VLM_MODELO", ""))
    ap.add_argument("--registrar", action="store_true")
    args = ap.parse_args(argv)

    juiz_base_url = args.juiz_base_url or args.llm_base_url
    juiz_modelo = args.juiz_modelo or args.llm_modelo
    juiz_esforco = args.juiz_reasoning_effort or (args.llm_reasoning_effort if juiz_modelo == args.llm_modelo else "")

    dados = ep.carregar_casos()
    cli_gerador = ClienteChatOpenAI(
        args.llm_base_url,
        args.llm_modelo,
        timeout_s=180.0,
        reasoning_effort=args.llm_reasoning_effort or None,
    )
    cli_juiz = (
        cli_gerador
        if (juiz_base_url == args.llm_base_url and juiz_modelo == args.llm_modelo and juiz_esforco == args.llm_reasoning_effort)
        else ClienteChatOpenAI(
            juiz_base_url,
            juiz_modelo,
            timeout_s=180.0,
            reasoning_effort=juiz_esforco or None,
        )
    )

    memoria: dict[str, object] = {}

    def _ao_concluir_geracao() -> None:
        if not args.ollama_host:
            return
        memoria["gerador"] = medir_memoria_ollama(args.ollama_host)
        if juiz_modelo != args.llm_modelo:
            descarregar_modelo_ollama(args.ollama_host, args.llm_modelo)

    res_eval = ep.avaliar_prompts(
        dados,
        cli_gerador,
        cli_juiz,
        n_bootstrap=2000,
        seed=42,
        ao_concluir_geracao=_ao_concluir_geracao,
    )
    if args.ollama_host:
        memoria["juiz"] = medir_memoria_ollama(args.ollama_host)

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
        "configuracao": {
            "llm_base_url": args.llm_base_url,
            "llm_modelo": args.llm_modelo,
            "llm_reasoning_effort": args.llm_reasoning_effort or None,
            "juiz_base_url": juiz_base_url,
            "juiz_modelo": juiz_modelo,
            "juiz_reasoning_effort": juiz_esforco or None,
            "vlm_modelo": args.vlm_modelo or None,
        },
        "calibracao": res_eval["calibracao"],
        "avaliacao": res_eval["avaliacao"],
        "promover_b": res_eval["promover_b"],
        "amostra_casos": res_eval["casos"][:4],
        "multimodal": bloco_vlm,
    }
    if memoria:
        saida["memoria"] = memoria
    print(json.dumps(saida, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p07-evals-e-multimodal", saida))
    return 0


if __name__ == "__main__":
    sys.exit(main())
