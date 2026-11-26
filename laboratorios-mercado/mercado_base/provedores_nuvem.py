"""Provedores de nuvem gerenciados sem SDK: Azure OpenAI no Foundry, Amazon Bedrock e Vertex AI.

Caminho principal (usado pelo P06): o endpoint compatível com OpenAI de cada nuvem, com o mesmo
`ClienteChatOpenAI` do projeto, de modo que *tool calling* e `json_schema` continuam iguais.
Muda só a URL e a autenticação:

- Azure: `https://<recurso>.openai.azure.com/openai/v1` com `api-key` ou token do Microsoft Entra ID.
- Bedrock: `https://bedrock-runtime.<região>.amazonaws.com/openai/v1` com chave de API do Bedrock
  (Bearer). SigV4 com credenciais IAM fica fora daqui, porque exigiria `botocore`.
- Vertex AI: `.../v1/projects/<projeto>/locations/<local>/endpoints/openapi` com token OAuth (Bearer).

Formatos nativos (Bedrock Converse e Vertex `generateContent`): funções puras que montam o pedido
e leem a resposta, testadas offline, para mostrar o que o endpoint compatível esconde.

Credenciais só por variável de ambiente. Mensagens de erro citam o nome da variável, nunca o valor.
Não há chamada de rede neste módulo além da que o cliente fizer quando usado de verdade.
"""
from __future__ import annotations

import email.utils
import os
import time
from typing import Dict, List, Mapping, Optional, Sequence, Tuple
from urllib.parse import quote

import httpx

from mercado_base.cliente_openai import ClienteChatOpenAI, RespostaChat

PROVEDORES_NUVEM = ("azure", "bedrock", "vertex")


def _ler(env: Mapping[str, str], nome: str) -> str:
    return str(env.get(nome, "") or "").strip()


def _exigir(env: Mapping[str, str], nome: str) -> str:
    valor = _ler(env, nome)
    if not valor:
        raise ValueError(f"variável de ambiente ausente: {nome}")
    return valor


# --- URLs -----------------------------------------------------------------------------------

def url_azure_openai_v1(endpoint: str) -> str:
    """`https://<recurso>.openai.azure.com` -> `.../openai/v1` (aceita o endpoint já com o sufixo)."""
    base = endpoint.strip().rstrip("/")
    if not base.startswith("https://"):
        raise ValueError("o endpoint do Azure OpenAI deve usar https")
    return base if base.endswith("/openai/v1") else base + "/openai/v1"


def url_bedrock_openai(regiao: str) -> str:
    return f"https://bedrock-runtime.{_validar_rotulo(regiao)}.amazonaws.com/openai/v1"


def url_bedrock_converse(regiao: str, modelo_id: str) -> str:
    # O ID pode ser ARN ou ter ':' (ex.: versão); vai codificado no caminho.
    return f"https://bedrock-runtime.{_validar_rotulo(regiao)}.amazonaws.com/model/{quote(modelo_id, safe='')}/converse"


def _host_vertex(local: str) -> str:
    # Endpoint global sem prefixo; regionais com o local antes do host (página "Deployments and endpoints").
    local = _validar_rotulo(local)
    return "https://aiplatform.googleapis.com" if local == "global" else f"https://{local}-aiplatform.googleapis.com"


def url_vertex_openai(projeto: str, local: str) -> str:
    return f"{_host_vertex(local)}/v1/projects/{_validar_rotulo(projeto)}/locations/{local}/endpoints/openapi"


def url_vertex_generate_content(projeto: str, local: str, modelo: str) -> str:
    return (f"{_host_vertex(local)}/v1/projects/{_validar_rotulo(projeto)}/locations/{local}"
            f"/publishers/google/models/{quote(modelo, safe='.-_')}:generateContent")


def _validar_rotulo(valor: str) -> str:
    """Região, local ou projeto: só letras minúsculas, dígitos e hífen (evita injeção no host/caminho)."""
    v = valor.strip()
    if not v or any(not (c.islower() or c.isdigit() or c == "-") for c in v):
        raise ValueError("região, local ou projeto inválido")
    return v


# --- Autenticação ---------------------------------------------------------------------------

def cabecalhos_autenticacao(provedor: str, env: Mapping[str, str]) -> Dict[str, str]:
    """Cabeçalhos de autenticação por provedor, lidos do ambiente."""
    if provedor == "azure":
        chave = _ler(env, "AZURE_OPENAI_API_KEY")
        if chave:
            return {"api-key": chave}
        token = _ler(env, "AZURE_OPENAI_AD_TOKEN")  # token do Entra ID (ex.: identidade gerenciada)
        if token:
            return {"Authorization": f"Bearer {token}"}
        raise ValueError("variável de ambiente ausente: AZURE_OPENAI_API_KEY ou AZURE_OPENAI_AD_TOKEN")
    if provedor == "bedrock":
        return {"Authorization": f"Bearer {_exigir(env, 'AWS_BEARER_TOKEN_BEDROCK')}"}
    if provedor == "vertex":
        # Token OAuth de curta duração (ex.: `gcloud auth print-access-token`), não chave fixa.
        return {"Authorization": f"Bearer {_exigir(env, 'VERTEX_ACCESS_TOKEN')}"}
    raise ValueError(f"provedor de nuvem desconhecido: {provedor}")


def criar_cliente_nuvem(
    provedor: str,
    *,
    modelo: Optional[str] = None,
    env: Optional[Mapping[str, str]] = None,
    transport: Optional[httpx.BaseTransport] = None,
    timeout_s: float = 120.0,
) -> ClienteChatOpenAI:
    """Cliente do endpoint compatível com OpenAI da nuvem escolhida.

    Variáveis: Azure `AZURE_OPENAI_ENDPOINT` e `AZURE_OPENAI_DEPLOYMENT` (nome da implantação vai em
    `model`); Bedrock `AWS_REGION` e `BEDROCK_MODELO`; Vertex `VERTEX_PROJETO`, `VERTEX_LOCAL`
    (padrão `global`) e `VERTEX_MODELO` (ex.: `google/<modelo>`). `modelo` sobrepõe a variável.
    """
    vars_env = os.environ if env is None else env
    alvo = provedor.strip().lower()
    cabecalhos = cabecalhos_autenticacao(alvo, vars_env)
    if alvo == "azure":
        base = url_azure_openai_v1(_exigir(vars_env, "AZURE_OPENAI_ENDPOINT"))
        nome = modelo or _exigir(vars_env, "AZURE_OPENAI_DEPLOYMENT")
    elif alvo == "bedrock":
        base = url_bedrock_openai(_exigir(vars_env, "AWS_REGION"))
        nome = modelo or _exigir(vars_env, "BEDROCK_MODELO")
    else:  # vertex (cabecalhos_autenticacao já rejeitou os demais)
        base = url_vertex_openai(_exigir(vars_env, "VERTEX_PROJETO"), _ler(vars_env, "VERTEX_LOCAL") or "global")
        nome = modelo or _exigir(vars_env, "VERTEX_MODELO")
    return ClienteChatOpenAI(base, nome, provedor=alvo, timeout_s=timeout_s, transport=transport,
                             cabecalhos=cabecalhos)


# --- Cotas: quanto esperar depois de um 429 --------------------------------------------------

def segundos_para_nova_tentativa(cabecalhos: Mapping[str, str], agora: Optional[float] = None) -> Optional[float]:
    """Lê `retry-after-ms` (Azure) ou `Retry-After` (segundos ou data HTTP). `None` se ausente ou inválido."""
    h = {k.lower(): v for k, v in cabecalhos.items()}
    if "retry-after-ms" in h:
        try:
            return max(0.0, float(h["retry-after-ms"]) / 1000.0)
        except ValueError:
            return None
    bruto = h.get("retry-after")
    if bruto is None:
        return None
    try:
        return max(0.0, float(bruto))
    except ValueError:
        pass
    try:
        data = email.utils.parsedate_to_datetime(bruto)
    except (TypeError, ValueError):
        return None
    return max(0.0, data.timestamp() - (time.time() if agora is None else agora))


# --- Formatos nativos -----------------------------------------------------------------------

def _separar_sistema(mensagens: Sequence[Dict[str, object]]) -> Tuple[List[str], List[Dict[str, object]]]:
    sistema, conversa = [], []
    for m in mensagens:
        if m.get("role") == "system":
            sistema.append(str(m.get("content") or ""))
        elif m.get("role") in ("user", "assistant"):
            conversa.append(m)
        else:
            raise ValueError("papel não suportado no formato nativo (use o endpoint compatível para ferramentas)")
    return sistema, conversa


def pedido_converse(mensagens: Sequence[Dict[str, object]], *, max_tokens: int = 512,
                    temperatura: float = 0.0) -> Dict[str, object]:
    """Corpo do Bedrock Converse: `system` separado e `content` como lista de blocos `{text}`."""
    sistema, conversa = _separar_sistema(mensagens)
    corpo: Dict[str, object] = {
        "messages": [{"role": m["role"], "content": [{"text": str(m.get("content") or "")}]} for m in conversa],
        "inferenceConfig": {"maxTokens": max_tokens, "temperature": temperatura},
    }
    if sistema:
        corpo["system"] = [{"text": s} for s in sistema]
    return corpo


def ler_resposta_converse(dados: Dict[str, object], modelo: str = "") -> RespostaChat:
    msg = ((dados.get("output") or {}).get("message") or {})
    texto = "".join(str(b.get("text") or "") for b in (msg.get("content") or ()) if isinstance(b, dict))
    uso = dados.get("usage") or {}
    return RespostaChat(
        conteudo=texto,
        modelo=modelo,
        tokens_entrada=int(uso.get("inputTokens") or 0),
        tokens_saida=int(uso.get("outputTokens") or 0),
        tokens_cache=int(uso.get("cacheReadInputTokens") or 0),
        latencia_ms=float((dados.get("metrics") or {}).get("latencyMs") or 0.0),
        finish_reason=str(dados.get("stopReason") or "end_turn"),
    )


def pedido_generate_content(mensagens: Sequence[Dict[str, object]], *, max_tokens: int = 512,
                            temperatura: float = 0.0) -> Dict[str, object]:
    """Corpo do Vertex `generateContent`: `contents` com `parts`, papel `model` e `systemInstruction`."""
    sistema, conversa = _separar_sistema(mensagens)
    corpo: Dict[str, object] = {
        "contents": [{"role": "model" if m["role"] == "assistant" else "user",
                      "parts": [{"text": str(m.get("content") or "")}]} for m in conversa],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": temperatura},
    }
    if sistema:
        corpo["systemInstruction"] = {"parts": [{"text": s} for s in sistema]}
    return corpo


def ler_resposta_generate_content(dados: Dict[str, object], modelo: str = "") -> RespostaChat:
    candidato = (dados.get("candidates") or [{}])[0]
    partes = ((candidato.get("content") or {}).get("parts") or ())
    texto = "".join(str(p.get("text") or "") for p in partes if isinstance(p, dict))
    uso = dados.get("usageMetadata") or {}
    return RespostaChat(
        conteudo=texto,
        modelo=str(dados.get("modelVersion") or modelo),
        tokens_entrada=int(uso.get("promptTokenCount") or 0),
        tokens_saida=int(uso.get("candidatesTokenCount") or 0),
        tokens_cache=int(uso.get("cachedContentTokenCount") or 0),
        finish_reason=str(candidato.get("finishReason") or "STOP"),
    )
