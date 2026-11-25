"""Exercita a API do projeto 05 em execução: resposta completa, streaming SSE, cancelamento e métricas.

    .venv-mercado/bin/python -I laboratorios-mercado/05_api_llmops/cliente_api_real.py --url http://127.0.0.1:8000 --registrar
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402

import httpx  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--url", default="http://127.0.0.1:8000")
    ap.add_argument("--registrar", action="store_true")
    args = ap.parse_args(argv)
    out = {}
    with httpx.Client(base_url=args.url, timeout=180.0) as c:
        t0 = time.perf_counter()
        r = c.post("/v1/respostas", json={"prompt": "Em uma frase: o que é rematrícula?", "max_tokens": 60,
                                          "id_requisicao": "real-completa-1"})
        out["completa"] = {"status": r.status_code, "ms": round((time.perf_counter() - t0) * 1000, 1), **r.json()}

        t0, primeiro, deltas, fim = time.perf_counter(), None, 0, None
        with c.stream("POST", "/v1/respostas/stream", json={"prompt": "Liste três documentos pedidos na matrícula.",
                                                            "max_tokens": 80, "id_requisicao": "real-stream-1"}) as s:
            evento = ""
            for linha in s.iter_lines():
                if linha.startswith("event: "):
                    evento = linha[7:]
                elif linha.startswith("data: "):
                    if evento == "delta":
                        deltas += 1
                        primeiro = primeiro or round((time.perf_counter() - t0) * 1000, 1)
                    elif evento in ("fim", "erro"):
                        fim = {"evento": evento, **json.loads(linha[6:])}
        out["stream"] = {"deltas": deltas, "ttft_ms_cliente": primeiro,
                         "total_ms": round((time.perf_counter() - t0) * 1000, 1), "final": fim}

        recebidos = 0
        with c.stream("POST", "/v1/respostas/stream", json={"prompt": "Escreva um texto longo sobre bibliotecas.",
                                                            "max_tokens": 400, "id_requisicao": "real-cancelada-1"}) as s:
            for linha in s.iter_lines():
                if linha.startswith("event: delta"):
                    recebidos += 1
                    if recebidos == 3:
                        break  # cliente desiste: a conexão é fechada ao sair do bloco
        time.sleep(2.0)  # tempo para o servidor notar a desconexão
        out["cancelamento"] = {"deltas_antes_de_desistir": recebidos}
        out["metricas"] = c.get("/v1/metricas").json()
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p05-api-llmops", out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
