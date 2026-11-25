"""Resiliência para chamadas a LLM (projeto 05): erros classificados, retry com backoff e disjuntor."""
from __future__ import annotations

import asyncio
import random
import time
from typing import Awaitable, Callable, Optional, TypeVar

T = TypeVar("T")


class ErroTransitorio(Exception):
    """Vale nova tentativa: 429, 5xx, timeout, conexão recusada."""

    def __init__(self, mensagem: str, retry_after_s: Optional[float] = None):
        super().__init__(mensagem)
        self.retry_after_s = retry_after_s


class ErroPermanente(Exception):
    """Não vale nova tentativa: 4xx de contrato (exceto 408/429), validação, autenticação."""


class CircuitoAberto(Exception):
    def __init__(self, retry_after_s: float):
        super().__init__("disjuntor aberto")
        self.retry_after_s = retry_after_s


def classificar_status(status: int, retry_after: Optional[str] = None) -> Exception:
    if status in (408, 429) or status >= 500:
        espera = None
        if retry_after:
            try:
                espera = max(0.0, float(retry_after))
            except ValueError:
                espera = None
        return ErroTransitorio(f"HTTP {status}", espera)
    return ErroPermanente(f"HTTP {status}")


def atraso_backoff(tentativa: int, *, base_s: float = 0.25, teto_s: float = 8.0,
                   rng: Optional[random.Random] = None) -> float:
    """Backoff exponencial com *full jitter*: uniforme em [0, min(teto, base * 2^tentativa)]."""
    limite = min(teto_s, base_s * (2 ** tentativa))
    return (rng or random).uniform(0.0, limite)


async def com_retry(fn: Callable[[], Awaitable[T]], *, tentativas: int = 3, base_s: float = 0.25,
                    teto_s: float = 8.0, rng: Optional[random.Random] = None,
                    dormir: Callable[[float], Awaitable[None]] = asyncio.sleep,
                    ao_tentar: Optional[Callable[[int, Exception], None]] = None) -> T:
    """Repete só erros transitórios; respeita `Retry-After` quando o servidor informa."""
    if tentativas < 1:
        raise ValueError("tentativas deve ser >= 1")
    for i in range(tentativas):
        try:
            return await fn()
        except ErroTransitorio as exc:
            if ao_tentar:
                ao_tentar(i + 1, exc)
            if i == tentativas - 1:
                raise
            espera = exc.retry_after_s if exc.retry_after_s is not None else atraso_backoff(
                i, base_s=base_s, teto_s=teto_s, rng=rng)
            await dormir(min(espera, teto_s))
    raise AssertionError("inalcançável")


class Disjuntor:
    """Disjuntor (*circuit breaker*) fechado → aberto → meio-aberto, com relógio injetável."""

    def __init__(self, limite_falhas: int = 3, tempo_aberto_s: float = 30.0,
                 relogio: Callable[[], float] = time.monotonic):
        self.limite_falhas = limite_falhas
        self.tempo_aberto_s = tempo_aberto_s
        self._relogio = relogio
        self.falhas = 0
        self.aberto_desde: Optional[float] = None
        self._sonda_em_andamento = False

    @property
    def estado(self) -> str:
        if self.aberto_desde is None:
            return "fechado"
        if self._relogio() - self.aberto_desde >= self.tempo_aberto_s:
            return "meio_aberto"
        return "aberto"

    def permitir(self) -> None:
        """Levanta `CircuitoAberto` se a chamada não deve sair. No meio-aberto, deixa passar 1 sonda."""
        estado = self.estado
        if estado == "aberto":
            raise CircuitoAberto(self.tempo_aberto_s - (self._relogio() - self.aberto_desde))
        if estado == "meio_aberto":
            if self._sonda_em_andamento:
                raise CircuitoAberto(1.0)
            self._sonda_em_andamento = True

    def registrar_sucesso(self) -> None:
        self.falhas = 0
        self.aberto_desde = None
        self._sonda_em_andamento = False

    def registrar_falha(self) -> None:
        self._sonda_em_andamento = False
        self.falhas += 1
        if self.falhas >= self.limite_falhas or self.aberto_desde is not None:
            self.aberto_desde = self._relogio()
