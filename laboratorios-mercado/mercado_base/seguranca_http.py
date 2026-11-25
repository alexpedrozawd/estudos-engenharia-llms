"""Autenticação opcional (X-API-Key/Bearer) e rate limiting para APIs FastAPI da Camada 3."""
from __future__ import annotations

import hashlib
import hmac
import math
import os
import time
from collections import deque
from typing import Callable, Deque, Dict, Iterable, Optional, Sequence, Tuple

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AutenticadorOpcional:
    """Valida X-API-Key ou Authorization: Bearer quando chaves estão configuradas."""

    def __init__(self, chaves: Optional[Sequence[str]] = None):
        self._chaves = tuple(c.strip() for c in (chaves or ()) if c and c.strip())

    @property
    def ativo(self) -> bool:
        return bool(self._chaves)

    @staticmethod
    def extrair_chave(request: Request) -> Optional[str]:
        chave_api = request.headers.get("x-api-key")
        if chave_api:
            return chave_api.strip()
        auth = request.headers.get("authorization", "")
        if auth.lower().startswith("bearer "):
            return auth[7:].strip()
        return None

    def autorizar(self, request: Request) -> Optional[str]:
        """Devolve identificador seguro do cliente (hash curto) ou None se não autorizado."""
        if not self.ativo:
            return "anonimo"
        fornecida = self.extrair_chave(request)
        if not fornecida:
            return None
        for valida in self._chaves:
            if hmac.compare_digest(fornecida, valida):
                return "key:" + hashlib.sha256(valida.encode("utf-8")).hexdigest()[:12]
        return None


class LimitadorTaxa:
    """Limitador por janela deslizante em memória com evicção limitada de clientes."""

    def __init__(
        self,
        limite: int = 0,
        janela_s: float = 60.0,
        relogio: Callable[[], float] = time.monotonic,
        max_clientes: int = 4096,
    ):
        self.limite = int(limite)
        self.janela_s = float(janela_s)
        self._relogio = relogio
        self.max_clientes = max(1, int(max_clientes))
        self._janelas: Dict[str, Deque[float]] = {}

    @property
    def ativo(self) -> bool:
        return self.limite > 0

    def permitir(self, chave_cliente: str) -> Tuple[bool, int]:
        """Verifica se o cliente pode prosseguir; devolve (permitido, retry_after_s)."""
        if not self.ativo:
            return True, 0
        agora = self._relogio()
        corte = agora - self.janela_s
        if chave_cliente not in self._janelas and len(self._janelas) >= self.max_clientes:
            mais_antigo = next(iter(self._janelas))
            del self._janelas[mais_antigo]
        hist = self._janelas.setdefault(chave_cliente, deque())
        while hist and hist[0] <= corte:
            hist.popleft()
        if len(hist) >= self.limite:
            restante = max(1, math.ceil(self.janela_s - (agora - hist[0])))
            return False, restante
        hist.append(agora)
        return True, 0


def instalar_seguranca_http(
    app: FastAPI,
    *,
    api_keys: Optional[Sequence[str]] = None,
    limite_taxa: int = 0,
    janela_taxa_s: float = 60.0,
    rotas_publicas: Iterable[str] = ("/saude",),
    relogio: Callable[[], float] = time.monotonic,
    contadores: Optional[Dict[str, int]] = None,
) -> None:
    """Registra middleware de autenticação opcional e rate limiting em uma app FastAPI."""
    autenticador = AutenticadorOpcional(api_keys)
    limitador = LimitadorTaxa(limite_taxa, janela_s=janela_taxa_s, relogio=relogio)
    publicas = frozenset(rotas_publicas)
    app.state.autenticador = autenticador
    app.state.limitador = limitador

    if not autenticador.ativo and not limitador.ativo:
        return

    @app.middleware("http")
    async def _middleware_seguranca(request: Request, call_next):
        if request.url.path in publicas:
            return await call_next(request)
        identidade = autenticador.autorizar(request)
        if identidade is None:
            if contadores is not None:
                contadores["rejeitados_auth"] = contadores.get("rejeitados_auth", 0) + 1
            return JSONResponse(
                {"erro": "nao_autenticado"},
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )
        chave_rl = identidade if autenticador.ativo else (request.client.host if request.client else "local")
        permitido, retry_after = limitador.permitir(chave_rl)
        if not permitido:
            if contadores is not None:
                contadores["rejeitados_rate_limit"] = contadores.get("rejeitados_rate_limit", 0) + 1
            return JSONResponse(
                {"erro": "limite_de_taxa_excedido"},
                status_code=429,
                headers={"Retry-After": str(retry_after)},
            )
        return await call_next(request)


def carregar_seguranca_de_ambiente(prefixo: str = "") -> Dict[str, object]:
    """Lê chaves e limite por minuto das variáveis AURORA_* ou específicas do serviço."""
    bruto_chaves = os.environ.get(f"{prefixo}API_KEYS") or os.environ.get("AURORA_API_KEYS", "")
    api_keys = [c.strip() for c in bruto_chaves.split(",") if c.strip()]
    bruto_limite = os.environ.get(f"{prefixo}RATE_LIMIT_RPM") or os.environ.get("AURORA_RATE_LIMIT_RPM", "0")
    try:
        limite_taxa = max(0, int(bruto_limite))
    except ValueError:
        limite_taxa = 0
    return {"api_keys": api_keys or None, "limite_taxa": limite_taxa}
