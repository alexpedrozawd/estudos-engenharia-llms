"""Exercita a API do projeto 05 em execução: resposta completa, streaming SSE, cancelamento e métricas.

    .venv-mercado/bin/python -I laboratorios-mercado/05_api_llmops/cliente_api_real.py --url http://127.0.0.1:8000 --registrar
"""
from __future__ import annotations

import argparse
import datetime
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
    ap.add_argument("--api-key", default=os.environ.get("AURORA_API_KEY", ""))
    ap.add_argument("--jaeger-url", default="")
    ap.add_argument("--registrar", action="store_true")
    args = ap.parse_args(argv)
    out = {}
    headers = {"X-API-Key": args.api_key} if args.api_key else {}
    with httpx.Client(base_url=args.url, timeout=180.0, headers=headers) as c:
        if args.api_key:
            sem_chave = httpx.post(f"{args.url}/v1/respostas", json={"prompt": "oi"}, timeout=10.0)
            out["auth_sem_chave_status"] = sem_chave.status_code

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
        prom = c.get("/metrics")
        out["prometheus"] = {
            "status": prom.status_code,
            "amostras": [l for l in prom.text.splitlines() if l and not l.startswith("#")][:8],
        }
    if args.jaeger_url:
        time.sleep(5.5)  # BatchSpanProcessor exporta periodicamente em lotes
        base_j = args.jaeger_url.rstrip("/")
        agora = datetime.datetime.now(datetime.timezone.utc)
        t_ini = (agora - datetime.timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
        t_fim = (agora + datetime.timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        jr = httpx.get(
            f"{base_j}/api/v3/traces",
            params={
                "query.service_name": "aurora-api-llmops",
                "query.start_time_min": t_ini,
                "query.start_time_max": t_fim,
                "query.search_depth": 10,
            },
            timeout=15.0,
        )
        if jr.status_code == 200:
            res_spans = (jr.json().get("result") or {}).get("resourceSpans") or []
            spans_total = sum(
                len(ss.get("spans") or [])
                for rs_item in res_spans
                for ss in (rs_item.get("scopeSpans") or [])
            )
            out["jaeger"] = {"status": 200, "api": "v3", "resource_spans": len(res_spans), "spans": spans_total}
        else:
            jr1 = httpx.get(f"{base_j}/api/traces", params={"service": "aurora-api-llmops", "limit": 10}, timeout=15.0)
            traces = (jr1.json().get("data") or []) if jr1.status_code == 200 else []
            out["jaeger"] = {
                "status": jr1.status_code,
                "api": "v1",
                "traces": len(traces),
                "spans": sum(len(t.get("spans") or []) for t in traces),
            }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p05-api-llmops", out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
