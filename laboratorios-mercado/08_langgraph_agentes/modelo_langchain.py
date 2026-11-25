"""Adaptador: um chat model do LangChain (ex.: `ChatOpenAI` do `langchain-openai`) com a interface `completar_chat`.

Os nós do grafo falam com qualquer objeto que tenha `completar_chat` (o LangGraph não exige LangChain). Este
adaptador permite trocar o cliente próprio (`mercado_base.cliente_openai.ClienteChatOpenAI`) pelo modelo
padronizado do LangChain sem mexer no grafo. `temperature` e `max_tokens` ficam na construção do modelo.
"""
from __future__ import annotations

import json
import time
from typing import Dict, Optional, Sequence

from langchain_core.messages import convert_to_messages

from mercado_base.cliente_openai import ChamadaFerramenta, RespostaChat


class ModeloLangChain:
    def __init__(self, chat_model, nome: str = ""):
        self.chat_model = chat_model
        self.modelo = nome or str(getattr(chat_model, "model_name", "") or type(chat_model).__name__)
        self.provedor = "langchain"

    def completar_chat(self, mensagens: Sequence[Dict[str, object]], *, tools=None, tool_choice=None,
                       response_format: Optional[Dict[str, object]] = None, **_ignorados) -> RespostaChat:
        extras: Dict[str, object] = {}
        if tools:
            extras["tools"] = list(tools)
            if tool_choice is not None:
                extras["tool_choice"] = tool_choice
        if response_format is not None:
            extras["response_format"] = response_format
        t0 = time.perf_counter()
        msg = self.chat_model.invoke(convert_to_messages(list(mensagens)), **extras)
        chamadas = [ChamadaFerramenta(str(tc.get("id") or f"call_{i + 1}"), str(tc["name"]), dict(tc.get("args") or {}),
                                      json.dumps(tc.get("args") or {}, ensure_ascii=False))
                    for i, tc in enumerate(msg.tool_calls)]
        chamadas += [ChamadaFerramenta(str(tc.get("id") or "call_invalida"), str(tc.get("name") or ""), {},
                                       str(tc.get("args") or ""), f"JSON invalido nos argumentos: {tc.get('error')}")
                     for tc in getattr(msg, "invalid_tool_calls", None) or ()]
        uso = msg.usage_metadata or {}
        return RespostaChat(
            conteudo=msg.text if isinstance(msg.text, str) else str(msg.content or ""),
            chamadas_ferramentas=tuple(chamadas),
            modelo=self.modelo,
            tokens_entrada=int(uso.get("input_tokens") or 0),
            tokens_saida=int(uso.get("output_tokens") or 0),
            tokens_cache=int((uso.get("input_token_details") or {}).get("cache_read") or 0),
            latencia_ms=round((time.perf_counter() - t0) * 1000.0, 3),
        )
