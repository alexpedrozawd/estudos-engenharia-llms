"""Projeto 01 — benchmark assíncrono de serving local (Ollama, llama-server ou vLLM).

Mede, por requisição em streaming no endpoint OpenAI-compatível `/v1/chat/completions`:
- TTFT (tempo até o primeiro token, contando raciocínio visível ou conteúdo);
- TPOT (tempo médio por token de saída após o primeiro);
- latência ponta a ponta, p50/p95, vazão de tokens e goodput (requisições/s que cumprem o SLO);
- memória real do runtime (Ollama `/api/ps` ou `VmRSS` de um PID em `/proc`).

Uso real (exemplo com o Ollama do host):
    .venv-mercado/bin/python -I laboratorios-mercado/01_serving_local/serving_bench.py \
        --base-url http://127.0.0.1:11434/v1 --modelo qwen3:4b --requisicoes 8 --concorrencia 2 --registrar
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional, Sequence

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402

import httpx  # noqa: E402

PROMPTS_PADRAO = (
    "Explique em duas frases o que é rematrícula em uma faculdade.",
    "Liste três cuidados ao enviar documentos pessoais por e-mail.",
    "Resuma em uma frase a diferença entre média simples e média ponderada.",
    "Dê dois exemplos de perguntas frequentes de alunos sobre calendário acadêmico.",
)


@dataclass
class SLO:
    """Objetivo de nível de serviço usado no goodput."""

    ttft_ms: float = 2000.0
    tpot_ms: float = 150.0


@dataclass
class Amostra:
    """Tempos absolutos (relógio monotônico, s) e contagens de uma requisição."""

    inicio: float
    fim: float
    primeiro_token: Optional[float] = None
    tokens_saida: int = 0
    tokens_fonte: str = "contagem_de_eventos"
    ok: bool = True
    erro: str = ""
    texto: str = ""

    @property
    def ttft_ms(self) -> Optional[float]:
        # EXERCICIO-INICIO: (primeiro_token − inicio) em ms; None se não chegou token.
        if self.primeiro_token is None:
            return None
        return (self.primeiro_token - self.inicio) * 1000.0
        # EXERCICIO-FIM

    @property
    def tpot_ms(self) -> Optional[float]:
        # EXERCICIO-INICIO: (fim − primeiro_token) em ms dividido por (tokens_saida − 1); None com menos de 2 tokens.
        if self.primeiro_token is None or self.tokens_saida < 2:
            return None
        return (self.fim - self.primeiro_token) * 1000.0 / (self.tokens_saida - 1)
        # EXERCICIO-FIM

    @property
    def e2e_ms(self) -> float:
        return (self.fim - self.inicio) * 1000.0

    def cumpre(self, slo: SLO) -> bool:
        if not self.ok or self.ttft_ms is None:
            return False
        tpot = self.tpot_ms
        return self.ttft_ms <= slo.ttft_ms and (tpot is None or tpot <= slo.tpot_ms)


def resumir(amostras: Sequence[Amostra], duracao_s: float, slo: SLO) -> Dict[str, object]:
    """Agrega métricas de serving; só requisições bem-sucedidas entram nos percentis."""
    # EXERCICIO-INICIO: só amostras ok: p50/p95 de TTFT, TPOT e ponta a ponta, vazão em tokens/s e fração que cumpre o SLO (veja as chaves no teste).
    oks = [a for a in amostras if a.ok]
    ttft = [a.ttft_ms for a in oks if a.ttft_ms is not None]
    tpot = [a.tpot_ms for a in oks if a.tpot_ms is not None]
    e2e = [a.e2e_ms for a in oks]
    tokens = sum(a.tokens_saida for a in oks)
    cumprem = sum(1 for a in amostras if a.cumpre(slo))
    duracao = max(duracao_s, 1e-9)

    def r(x: float) -> float:
        return round(x, 3)

    return {
        "requisicoes": len(amostras),
        "falhas": len(amostras) - len(oks),
        "ttft_ms_p50": r(mb.percentil(ttft, 50)) if ttft else None,
        "ttft_ms_p95": r(mb.percentil(ttft, 95)) if ttft else None,
        "tpot_ms_p50": r(mb.percentil(tpot, 50)) if tpot else None,
        "tpot_ms_p95": r(mb.percentil(tpot, 95)) if tpot else None,
        "e2e_ms_p50": r(mb.percentil(e2e, 50)) if e2e else None,
        "e2e_ms_p95": r(mb.percentil(e2e, 95)) if e2e else None,
        "tokens_saida_total": tokens,
        "vazao_tokens_s": r(tokens / duracao),
        "requisicoes_s": r(len(oks) / duracao),
        "goodput_req_s": r(cumprem / duracao),
        "fracao_dentro_do_slo": r(cumprem / len(amostras)) if amostras else 0.0,
        "slo": asdict(slo),
        "duracao_s": r(duracao_s),
    }
    # EXERCICIO-FIM


async def requisitar_stream(
    cliente: httpx.AsyncClient,
    base_url: str,
    modelo: str,
    prompt: str,
    *,
    max_tokens: int = 64,
    extra: Optional[Dict[str, object]] = None,
    relogio: Callable[[], float] = time.perf_counter,
) -> Amostra:
    """Faz uma requisição em streaming e registra os tempos de cada evento."""
    payload: Dict[str, object] = {
        "model": modelo,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.0,
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    if extra:
        payload.update(extra)
    inicio = relogio()
    amostra = Amostra(inicio=inicio, fim=inicio)
    eventos_com_token = 0
    partes: List[str] = []
    try:
        async with cliente.stream("POST", f"{base_url.rstrip('/')}/chat/completions", json=payload) as resp:
            if resp.status_code != 200:
                corpo = (await resp.aread()).decode("utf-8", "replace")[:200]
                amostra.ok = False
                amostra.erro = f"HTTP {resp.status_code}: {corpo}"
                amostra.fim = relogio()
                return amostra
            async for linha in resp.aiter_lines():
                for evento in mb.iterar_eventos_sse([linha]):
                    delta = mb.extrair_delta(evento)
                    if delta["conteudo"] or delta["raciocinio"]:
                        agora = relogio()
                        if amostra.primeiro_token is None:
                            amostra.primeiro_token = agora
                        eventos_com_token += 1
                        partes.append(delta["conteudo"])
                    uso = evento.get("usage") or {}
                    if uso.get("completion_tokens"):
                        amostra.tokens_saida = int(uso["completion_tokens"])
                        amostra.tokens_fonte = "usage"
    except httpx.HTTPError as exc:
        amostra.ok = False
        amostra.erro = f"{type(exc).__name__}: {exc}"
    amostra.fim = relogio()
    if amostra.tokens_fonte != "usage":
        amostra.tokens_saida = eventos_com_token
    amostra.texto = "".join(partes)
    if amostra.ok and amostra.primeiro_token is None:
        amostra.ok = False
        amostra.erro = "stream sem tokens"
    return amostra


async def executar_benchmark(
    base_url: str,
    modelo: str,
    prompts: Sequence[str],
    *,
    requisicoes: int,
    concorrencia: int,
    max_tokens: int = 64,
    extra: Optional[Dict[str, object]] = None,
    transport: Optional[httpx.AsyncBaseTransport] = None,
    relogio: Callable[[], float] = time.perf_counter,
    timeout_s: float = 120.0,
) -> tuple[List[Amostra], float]:
    """Dispara `requisicoes` com no máximo `concorrencia` simultâneas."""
    if concorrencia < 1 or requisicoes < 1:
        raise ValueError("requisicoes e concorrencia devem ser >= 1")
    semaforo = asyncio.Semaphore(concorrencia)
    async with httpx.AsyncClient(transport=transport, timeout=timeout_s) as cliente:

        async def uma(i: int) -> Amostra:
            async with semaforo:
                return await requisitar_stream(
                    cliente, base_url, modelo, prompts[i % len(prompts)],
                    max_tokens=max_tokens, extra=extra, relogio=relogio,
                )

        t0 = relogio()
        amostras = await asyncio.gather(*(uma(i) for i in range(requisicoes)))
        return list(amostras), relogio() - t0


def medir_memoria_ollama(host: str, transport: Optional[httpx.BaseTransport] = None) -> Dict[str, object]:
    """Lê `/api/ps` do Ollama: bytes totais e em VRAM de cada modelo carregado."""
    with httpx.Client(transport=transport, timeout=10.0) as c:
        dados = c.get(f"{host.rstrip('/')}/api/ps").json()
    modelos = [
        {"modelo": m.get("name") or m.get("model"), "bytes": int(m.get("size") or 0), "bytes_vram": int(m.get("size_vram") or 0)}
        for m in dados.get("models") or []
    ]
    return {"fonte": "ollama /api/ps", "modelos": modelos}


def medir_memoria_pid(pid: int, raiz_proc: str = "/proc") -> Dict[str, object]:
    """Lê `VmRSS` e `VmHWM` (pico) de um processo do runtime (llama-server, vLLM)."""
    valores: Dict[str, object] = {"fonte": f"{raiz_proc}/{pid}/status", "pid": pid}
    with open(os.path.join(raiz_proc, str(pid), "status"), encoding="utf-8") as f:
        for linha in f:
            if linha.startswith(("VmRSS:", "VmHWM:")):
                chave, resto = linha.split(":", 1)
                valores[chave.lower() + "_kib"] = int(resto.split()[0])
    return valores


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", default=os.environ.get("SERVING_BASE_URL", "http://127.0.0.1:11434/v1"))
    ap.add_argument("--modelo", default=os.environ.get("SERVING_MODELO", "qwen3:4b"))
    ap.add_argument("--requisicoes", type=int, default=8)
    ap.add_argument("--concorrencia", type=int, default=2)
    ap.add_argument("--max-tokens", type=int, default=64)
    ap.add_argument("--slo-ttft-ms", type=float, default=2000.0)
    ap.add_argument("--slo-tpot-ms", type=float, default=150.0)
    ap.add_argument("--sem-raciocinio", action="store_true", help="envia reasoning_effort=none (modelos com raciocínio)")
    ap.add_argument("--aquecer", action="store_true", help="faz 1 requisição fora da medição para carregar o modelo")
    ap.add_argument("--memoria-ollama", default="", help="host do Ollama para ler /api/ps (ex.: http://127.0.0.1:11434)")
    ap.add_argument("--memoria-pid", type=int, default=0)
    ap.add_argument("--registrar", action="store_true", help="grava JSON em laboratorios-mercado/execucoes/")
    args = ap.parse_args(argv)

    extra = {"reasoning_effort": "none"} if args.sem_raciocinio else None
    slo = SLO(args.slo_ttft_ms, args.slo_tpot_ms)
    if args.aquecer:
        asyncio.run(executar_benchmark(args.base_url, args.modelo, PROMPTS_PADRAO[:1], requisicoes=1,
                                       concorrencia=1, max_tokens=8, extra=extra))
    amostras, duracao = asyncio.run(
        executar_benchmark(args.base_url, args.modelo, PROMPTS_PADRAO, requisicoes=args.requisicoes,
                           concorrencia=args.concorrencia, max_tokens=args.max_tokens, extra=extra)
    )
    resumo = resumir(amostras, duracao, slo)
    memoria: Dict[str, object] = {}
    if args.memoria_ollama:
        memoria = medir_memoria_ollama(args.memoria_ollama)
    elif args.memoria_pid:
        memoria = medir_memoria_pid(args.memoria_pid)
    resultado = {
        "configuracao": {
            "base_url": args.base_url, "modelo": args.modelo, "requisicoes": args.requisicoes,
            "concorrencia": args.concorrencia, "max_tokens": args.max_tokens, "extra": extra or {},
        },
        "resumo": resumo,
        "memoria": memoria,
        "erros": sorted({a.erro for a in amostras if a.erro}),
        "fontes_de_tokens": sorted({a.tokens_fonte for a in amostras}),
    }
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p01-serving-local", resultado))
    return 0 if resumo["falhas"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
