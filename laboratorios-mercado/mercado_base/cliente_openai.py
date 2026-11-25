"""Cliente OpenAI-compatível com tool calling nativo, structured outputs e medição de cache."""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple, Type

import httpx
from pydantic import BaseModel, ValidationError


@dataclass(frozen=True)
class ChamadaFerramenta:
    id: str
    nome: str
    argumentos: Dict[str, Any]
    argumentos_brutos: str = ""
    erro_json: str = ""


@dataclass(frozen=True)
class RespostaChat:
    conteudo: str
    chamadas_ferramentas: Tuple[ChamadaFerramenta, ...] = ()
    modelo: str = ""
    tokens_entrada: int = 0
    tokens_saida: int = 0
    tokens_cache: int = 0
    latencia_ms: float = 0.0
    finish_reason: str = "stop"

    @property
    def texto(self) -> str:
        return self.conteudo


def _adicionar_additional_properties_false(no: Any) -> Any:
    if isinstance(no, dict):
        copia = {k: _adicionar_additional_properties_false(v) for k, v in no.items()}
        if copia.get("type") == "object" or "properties" in copia:
            copia.setdefault("additionalProperties", False)
        return copia
    if isinstance(no, list):
        return [_adicionar_additional_properties_false(item) for item in no]
    return no


def esquema_json_estrito(modelo_pydantic: Type[BaseModel]) -> Dict[str, object]:
    """Gera payload `response_format` (`json_schema` estrito) a partir de um modelo Pydantic."""
    schema = _adicionar_additional_properties_false(modelo_pydantic.model_json_schema())
    return {
        "type": "json_schema",
        "json_schema": {
            "name": modelo_pydantic.__name__,
            "strict": True,
            "schema": schema,
        },
    }


def _extrair_json_limpo(texto: str) -> str:
    limpo = texto.strip()
    m = re.match(r"^```(?:json)?\s*(.*?)\s*```$", limpo, flags=re.S | re.I)
    if m:
        return m.group(1).strip()
    return limpo


def _extrair_tokens_cache(dados: Dict[str, Any]) -> int:
    uso = dados.get("usage") or {}
    detalhes = uso.get("prompt_tokens_details") or {}
    timings = dados.get("timings") or {}
    return int(detalhes.get("cached_tokens") or timings.get("cache_n") or 0)


class ClienteChatOpenAI:
    """Adaptador HTTP `/v1/chat/completions` com suporte a `tools` e `response_format`."""

    def __init__(
        self,
        base_url: str,
        modelo: str,
        *,
        api_key: str = "",
        provedor: str = "openai-compativel",
        timeout_s: float = 180.0,
        reasoning_effort: Optional[str] = None,
        transport: Optional[httpx.BaseTransport] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.modelo = modelo
        self.provedor = provedor
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.reasoning_effort = reasoning_effort
        self._transport = transport

    def completar_chat(
        self,
        mensagens: Sequence[Dict[str, object]],
        *,
        tools: Optional[Sequence[Dict[str, object]]] = None,
        tool_choice: Optional[object] = None,
        response_format: Optional[Dict[str, object]] = None,
        temperatura: float = 0.0,
        max_tokens: int = 512,
        reasoning_effort: Optional[str] = None,
    ) -> RespostaChat:
        cabecalhos = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        payload: Dict[str, object] = {
            "model": self.modelo,
            "messages": list(mensagens),
            "temperature": temperatura,
            "max_tokens": max_tokens,
        }
        esforco = reasoning_effort if reasoning_effort is not None else self.reasoning_effort
        if esforco:
            payload["reasoning_effort"] = esforco
        if tools:
            payload["tools"] = list(tools)
            if tool_choice is not None:
                payload["tool_choice"] = tool_choice
        if response_format is not None:
            payload["response_format"] = response_format

        t0 = time.perf_counter()
        with httpx.Client(transport=self._transport, timeout=self.timeout_s, headers=cabecalhos) as c:
            resp = c.post(f"{self.base_url}/chat/completions", json=payload)
            resp.raise_for_status()
            dados = resp.json()
        latencia_ms = round((time.perf_counter() - t0) * 1000.0, 3)

        escolha = (dados.get("choices") or [{}])[0]
        msg = escolha.get("message") or {}
        chamadas: List[ChamadaFerramenta] = []
        for idx, tc in enumerate(msg.get("tool_calls") or ()):
            fn = tc.get("function") or {}
            bruto = fn.get("arguments")
            if isinstance(bruto, dict):
                args, bruto_txt, err = bruto, json.dumps(bruto, ensure_ascii=False), ""
            else:
                bruto_txt = str(bruto or "{}")
                try:
                    decodificado = json.loads(bruto_txt)
                    if not isinstance(decodificado, dict):
                        raise ValueError("argumentos devem ser um objeto JSON")
                    args, err = decodificado, ""
                except Exception as exc:
                    args, err = {}, f"JSON invalido nos argumentos: {exc}"
            chamadas.append(
                ChamadaFerramenta(
                    id=str(tc.get("id") or f"call_{idx + 1}"),
                    nome=str(fn.get("name") or ""),
                    argumentos=args,
                    argumentos_brutos=bruto_txt,
                    erro_json=err,
                )
            )
        uso = dados.get("usage") or {}
        return RespostaChat(
            conteudo=str(msg.get("content") or ""),
            chamadas_ferramentas=tuple(chamadas),
            modelo=str(dados.get("model") or self.modelo),
            tokens_entrada=int(uso.get("prompt_tokens") or 0),
            tokens_saida=int(uso.get("completion_tokens") or 0),
            tokens_cache=_extrair_tokens_cache(dados),
            latencia_ms=latencia_ms,
            finish_reason=str(escolha.get("finish_reason") or "stop"),
        )

    def completar(
        self,
        prompt: str,
        *,
        sistema: str = "",
        esforco: Optional[str] = None,
        temperatura: float = 0.0,
        max_tokens: int = 256,
    ) -> RespostaChat:
        """Interface compatível com `ClienteHTTPOpenAICompativel.completar` para reuso em RAG/evals."""
        mensagens: List[Dict[str, object]] = []
        if sistema:
            mensagens.append({"role": "system", "content": sistema})
        mensagens.append({"role": "user", "content": prompt})
        return self.completar_chat(
            mensagens,
            temperatura=temperatura,
            max_tokens=max_tokens,
            reasoning_effort=esforco,
        )


def medir_memoria_ollama(host: str, transport: Optional[httpx.BaseTransport] = None) -> Dict[str, object]:
    """Lê `/api/ps` do Ollama: bytes totais e em VRAM de cada modelo carregado."""
    with httpx.Client(transport=transport, timeout=10.0) as c:
        dados = c.get(f"{host.rstrip('/')}/api/ps").json()
    modelos = [
        {
            "modelo": m.get("name") or m.get("model"),
            "bytes": int(m.get("size") or 0),
            "bytes_vram": int(m.get("size_vram") or 0),
        }
        for m in dados.get("models") or []
    ]
    return {"fonte": "ollama /api/ps", "modelos": modelos}


def descarregar_modelo_ollama(
    host: str,
    modelo: str,
    transport: Optional[httpx.BaseTransport] = None,
) -> bool:
    """Solicita ao Ollama o descarregamento imediato (`keep_alive: 0`) de um modelo da VRAM."""
    with httpx.Client(transport=transport, timeout=30.0) as c:
        resp = c.post(f"{host.rstrip('/')}/api/chat", json={"model": modelo, "messages": [], "keep_alive": 0})
        return resp.status_code == 200


class ClienteChatFalso:
    """Simulador determinístico de `completar_chat` para smoke-tests offline."""

    def __init__(self, respostas: Sequence[RespostaChat], modelo: str = "chat-mock", provedor: str = "mock"):
        self._respostas = list(respostas)
        self.modelo = modelo
        self.provedor = provedor
        self.chamadas: List[Dict[str, object]] = []

    def completar_chat(
        self,
        mensagens: Sequence[Dict[str, object]],
        *,
        tools: Optional[Sequence[Dict[str, object]]] = None,
        tool_choice: Optional[object] = None,
        response_format: Optional[Dict[str, object]] = None,
        temperatura: float = 0.0,
        max_tokens: int = 512,
    ) -> RespostaChat:
        self.chamadas.append({
            "mensagens": [dict(m) for m in mensagens],
            "tools": list(tools) if tools else None,
            "tool_choice": tool_choice,
            "response_format": response_format,
            "temperatura": temperatura,
            "max_tokens": max_tokens,
        })
        if not self._respostas:
            raise AssertionError("ClienteChatFalso sem respostas suficientes")
        return self._respostas.pop(0)


def gerar_estruturado(
    cliente,
    mensagens: Sequence[Dict[str, object]],
    modelo_pydantic: Type[BaseModel],
    *,
    max_reparos: int = 2,
    temperatura: float = 0.0,
    max_tokens: int = 512,
) -> Tuple[BaseModel, Dict[str, object]]:
    """Chama `completar_chat` com `response_format` json_schema e repara falhas via Pydantic."""
    rf = esquema_json_estrito(modelo_pydantic)
    historico = [dict(m) for m in mensagens]
    tokens_in = tokens_out = tokens_cache = 0
    latencia = 0.0
    ultimo_erro = ""

    for tentativa in range(1, max_reparos + 2):
        resp = cliente.completar_chat(
            historico,
            response_format=rf,
            temperatura=temperatura,
            max_tokens=max_tokens,
        )
        tokens_in += resp.tokens_entrada
        tokens_out += resp.tokens_saida
        tokens_cache += resp.tokens_cache
        latencia += resp.latencia_ms
        bruto = _extrair_json_limpo(resp.conteudo)
        try:
            instancia = modelo_pydantic.model_validate_json(bruto)
            return instancia, {
                "tentativas": tentativa,
                "reparos": tentativa - 1,
                "tokens_entrada": tokens_in,
                "tokens_saida": tokens_out,
                "tokens_cache": tokens_cache,
                "latencia_ms": round(latencia, 3),
            }
        except (ValidationError, ValueError) as exc:
            ultimo_erro = str(exc)
            if tentativa > max_reparos:
                break
            historico.append({"role": "assistant", "content": resp.conteudo})
            historico.append({
                "role": "user",
                "content": (
                    "Sua resposta anterior não validou no esquema JSON obrigatório. "
                    f"Corrija devolvendo apenas JSON válido. Erro de validação: {ultimo_erro[:500]}"
                ),
            })

    raise ValueError(f"Falha ao validar {modelo_pydantic.__name__} após {max_reparos} reparo(s): {ultimo_erro}")
