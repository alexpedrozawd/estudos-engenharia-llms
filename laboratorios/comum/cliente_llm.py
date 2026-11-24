"""Cliente neutro para provedores de LLM com modo mock determinístico offline.

Separa claramente o contrato de chamada (provedor, modelo, esforço de raciocínio,
mensagens e metadados de custo/latência) da camada de transporte HTTP opcional.
"""
from dataclasses import dataclass, field
import json
import os
import time
from typing import Callable, Dict, List, Mapping, Optional
import urllib.request


@dataclass(frozen=True)
class RespostaLLM:
    """Resposta padronizada independente do provedor."""

    texto: str
    provedor: str
    modelo: str
    tokens_entrada: int
    tokens_saida: int
    latencia_ms: float
    tokens_cache: int = 0
    metadados: Dict[str, str] = field(default_factory=dict)

    @property
    def custo_relativo_tokens(self) -> float:
        """Estimativa neutra de custo relativo (saída ~3x entrada; cache ~0.25x)."""
        entrada_nao_cache = max(0, self.tokens_entrada - self.tokens_cache)
        return entrada_nao_cache + 0.25 * self.tokens_cache + 3.0 * self.tokens_saida


class ClienteMockDeterministico:
    """Simulador determinístico para testes unitários offline sem rede."""

    def __init__(
        self,
        respostas: Optional[Dict[str, str]] = None,
        fallback: str = "Resposta sintética padrão (modo offline).",
        provedor: str = "mock-aurora",
        modelo: str = "modelo-didatico-v1",
    ):
        self.respostas = dict(respostas or {})
        self.fallback = fallback
        self.provedor = provedor
        self.modelo = modelo
        self.chamadas: List[Dict[str, object]] = []

    def completar(
        self,
        prompt: str,
        *,
        sistema: str = "",
        esforco: str = "medium",
        temperatura: float = 0.0,
        max_tokens: int = 256,
    ) -> RespostaLLM:
        self.chamadas.append(
            {
                "prompt": prompt,
                "sistema": sistema,
                "esforco": esforco,
                "temperatura": temperatura,
                "max_tokens": max_tokens,
            }
        )
        texto = self.fallback
        for chave, valor in self.respostas.items():
            if chave in prompt:
                texto = valor
                break
        tokens_in = max(1, len((sistema + " " + prompt).split()))
        tokens_out = max(1, len(texto.split()))
        return RespostaLLM(
            texto=texto,
            provedor=self.provedor,
            modelo=self.modelo,
            tokens_entrada=tokens_in,
            tokens_saida=tokens_out,
            latencia_ms=18.5 if esforco == "low" else 42.0,
            tokens_cache=max(0, len(sistema.split()) - 1) if sistema else 0,
            metadados={"esforco": esforco},
        )


def chamar_http_json(
    url: str,
    payload: Dict[str, object],
    cabecalhos: Optional[Dict[str, str]] = None,
    timeout_s: float = 15.0,
    opener: Optional[Callable[..., object]] = None,
) -> Dict[str, object]:
    """Envia requisição POST JSON sem acoplar bibliotecas externas.

    Permite injeção de `opener` para validação unitária via unittest.mock.
    """
    corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if cabecalhos:
        headers.update(cabecalhos)
    req = urllib.request.Request(url, data=corpo, headers=headers, method="POST")
    fn = opener or urllib.request.urlopen
    with fn(req, timeout=timeout_s) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _mensagens_padrao(prompt: str, sistema: str) -> List[Dict[str, str]]:
    msgs: List[Dict[str, str]] = []
    if sistema:
        msgs.append({"role": "system", "content": sistema})
    msgs.append({"role": "user", "content": prompt})
    return msgs


class ClienteHTTPOpenAICompativel:
    """Adaptador HTTP para endpoints OpenAI e servidores compatíveis (ex.: vLLM, llama.cpp)."""

    def __init__(
        self,
        modelo: str = "gpt-5-mini",
        api_key: str = "",
        base_url: str = "https://api.openai.com/v1",
        provedor: str = "openai",
        timeout_s: float = 30.0,
        opener: Optional[Callable[..., object]] = None,
    ):
        self.modelo = modelo
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.provedor = provedor
        self.timeout_s = timeout_s
        self.opener = opener

    def completar(
        self,
        prompt: str,
        *,
        sistema: str = "",
        esforco: str = "medium",
        temperatura: float = 0.0,
        max_tokens: int = 256,
    ) -> RespostaLLM:
        cabecalhos = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None
        payload: Dict[str, object] = {
            "model": self.modelo,
            "messages": _mensagens_padrao(prompt, sistema),
            "temperature": temperatura,
            "max_tokens": max_tokens,
        }
        t0 = time.perf_counter()
        dados = chamar_http_json(
            f"{self.base_url}/chat/completions",
            payload,
            cabecalhos=cabecalhos,
            timeout_s=self.timeout_s,
            opener=self.opener,
        )
        latencia_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        escolha = (dados.get("choices") or [{}])[0]
        texto = ((escolha.get("message") or {}).get("content")) or ""
        uso = dados.get("usage") or {}
        detalhes = uso.get("prompt_tokens_details") or {}
        return RespostaLLM(
            texto=str(texto),
            provedor=self.provedor,
            modelo=str(dados.get("model") or self.modelo),
            tokens_entrada=int(uso.get("prompt_tokens") or 0),
            tokens_saida=int(uso.get("completion_tokens") or 0),
            latencia_ms=latencia_ms,
            tokens_cache=int(detalhes.get("cached_tokens") or 0),
            metadados={"esforco": esforco, "transporte": "http"},
        )


class ClienteHTTPAnthropic:
    """Adaptador HTTP para a API Messages da Anthropic."""

    def __init__(
        self,
        api_key: str,
        modelo: str = "claude-sonnet-5-5",
        base_url: str = "https://api.anthropic.com/v1",
        api_version: str = "2023-06-01",
        timeout_s: float = 30.0,
        opener: Optional[Callable[..., object]] = None,
    ):
        self.api_key = api_key
        self.modelo = modelo
        self.base_url = base_url.rstrip("/")
        self.api_version = api_version
        self.timeout_s = timeout_s
        self.opener = opener

    def completar(
        self,
        prompt: str,
        *,
        sistema: str = "",
        esforco: str = "medium",
        temperatura: float = 0.0,
        max_tokens: int = 256,
    ) -> RespostaLLM:
        payload: Dict[str, object] = {
            "model": self.modelo,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if sistema:
            payload["system"] = sistema
        t0 = time.perf_counter()
        dados = chamar_http_json(
            f"{self.base_url}/messages",
            payload,
            cabecalhos={
                "x-api-key": self.api_key,
                "anthropic-version": self.api_version,
            },
            timeout_s=self.timeout_s,
            opener=self.opener,
        )
        latencia_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        blocos = dados.get("content") or []
        texto = "".join(
            str(b.get("text", ""))
            for b in blocos
            if isinstance(b, dict) and b.get("type") == "text"
        )
        uso = dados.get("usage") or {}
        return RespostaLLM(
            texto=texto,
            provedor="anthropic",
            modelo=str(dados.get("model") or self.modelo),
            tokens_entrada=int(uso.get("input_tokens") or 0),
            tokens_saida=int(uso.get("output_tokens") or 0),
            latencia_ms=latencia_ms,
            tokens_cache=int(uso.get("cache_read_input_tokens") or 0),
            metadados={"esforco": esforco, "transporte": "http"},
        )


class ClienteHTTPGemini:
    """Adaptador HTTP para a API Gemini (chave enviada apenas por cabeçalho)."""

    def __init__(
        self,
        api_key: str,
        modelo: str = "gemini-2.5-flash",
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        timeout_s: float = 30.0,
        opener: Optional[Callable[..., object]] = None,
    ):
        self.api_key = api_key
        self.modelo = modelo
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.opener = opener

    def completar(
        self,
        prompt: str,
        *,
        sistema: str = "",
        esforco: str = "medium",
        temperatura: float = 0.0,
        max_tokens: int = 256,
    ) -> RespostaLLM:
        payload: Dict[str, object] = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperatura,
                "maxOutputTokens": max_tokens,
            },
        }
        if sistema:
            payload["systemInstruction"] = {"parts": [{"text": sistema}]}
        t0 = time.perf_counter()
        dados = chamar_http_json(
            f"{self.base_url}/models/{self.modelo}:generateContent",
            payload,
            cabecalhos={"x-goog-api-key": self.api_key},
            timeout_s=self.timeout_s,
            opener=self.opener,
        )
        latencia_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        cand = (dados.get("candidates") or [{}])[0]
        partes = ((cand.get("content") or {}).get("parts")) or []
        texto = "".join(
            str(p.get("text", ""))
            for p in partes
            if isinstance(p, dict) and "text" in p
        )
        uso = dados.get("usageMetadata") or {}
        return RespostaLLM(
            texto=texto,
            provedor="gemini",
            modelo=str(dados.get("modelVersion") or self.modelo),
            tokens_entrada=int(uso.get("promptTokenCount") or 0),
            tokens_saida=int(uso.get("candidatesTokenCount") or 0),
            latencia_ms=latencia_ms,
            tokens_cache=int(uso.get("cachedContentTokenCount") or 0),
            metadados={"esforco": esforco, "transporte": "http"},
        )


class ClienteHTTPOllama:
    """Adaptador HTTP para a API local /api/chat do Ollama."""

    def __init__(
        self,
        modelo: str = "qwen3:8b",
        host: str = "http://127.0.0.1:11434",
        timeout_s: float = 30.0,
        opener: Optional[Callable[..., object]] = None,
    ):
        self.modelo = modelo
        self.host = host.rstrip("/")
        self.timeout_s = timeout_s
        self.opener = opener

    def completar(
        self,
        prompt: str,
        *,
        sistema: str = "",
        esforco: str = "medium",
        temperatura: float = 0.0,
        max_tokens: int = 256,
    ) -> RespostaLLM:
        payload: Dict[str, object] = {
            "model": self.modelo,
            "stream": False,
            "messages": _mensagens_padrao(prompt, sistema),
            "options": {"temperature": temperatura, "num_predict": max_tokens},
        }
        t0 = time.perf_counter()
        dados = chamar_http_json(
            f"{self.host}/api/chat",
            payload,
            timeout_s=self.timeout_s,
            opener=self.opener,
        )
        latencia_ms = round((time.perf_counter() - t0) * 1000.0, 3)
        texto = ((dados.get("message") or {}).get("content")) or ""
        return RespostaLLM(
            texto=str(texto),
            provedor="ollama",
            modelo=str(dados.get("model") or self.modelo),
            tokens_entrada=int(dados.get("prompt_eval_count") or 0),
            tokens_saida=int(dados.get("eval_count") or 0),
            latencia_ms=latencia_ms,
            tokens_cache=0,
            metadados={"esforco": esforco, "transporte": "http"},
        )


def criar_cliente_por_ambiente(
    provedor: Optional[str] = None,
    *,
    modelo: Optional[str] = None,
    opener: Optional[Callable[..., object]] = None,
    env: Optional[Mapping[str, str]] = None,
):
    """Seleciona um adaptador HTTP por provedor/variável de ambiente ou retorna o mock offline."""
    vars_env = os.environ if env is None else env

    def _ler(nome: str) -> str:
        return str(vars_env.get(nome, "")).strip()

    alvo = provedor.strip().lower() if provedor else None
    if alvo is None:
        if _ler("OPENAI_API_KEY"):
            alvo = "openai"
        elif _ler("ANTHROPIC_API_KEY"):
            alvo = "anthropic"
        elif _ler("GEMINI_API_KEY"):
            alvo = "gemini"
        elif _ler("OLLAMA_HOST"):
            alvo = "ollama"
        else:
            alvo = "mock"

    if alvo == "mock":
        return ClienteMockDeterministico(modelo=modelo or "modelo-didatico-v1")
    if alvo == "openai":
        chave = _ler("OPENAI_API_KEY")
        if not chave:
            raise ValueError("OPENAI_API_KEY ausente para provedor 'openai'")
        base_url = _ler("OPENAI_BASE_URL") or "https://api.openai.com/v1"
        return ClienteHTTPOpenAICompativel(
            modelo=modelo or "gpt-5-mini",
            api_key=chave,
            base_url=base_url,
            opener=opener,
        )
    if alvo == "anthropic":
        chave = _ler("ANTHROPIC_API_KEY")
        if not chave:
            raise ValueError("ANTHROPIC_API_KEY ausente para provedor 'anthropic'")
        base_url = _ler("ANTHROPIC_BASE_URL") or "https://api.anthropic.com/v1"
        return ClienteHTTPAnthropic(
            api_key=chave,
            modelo=modelo or "claude-sonnet-5-5",
            base_url=base_url,
            opener=opener,
        )
    if alvo == "gemini":
        chave = _ler("GEMINI_API_KEY")
        if not chave:
            raise ValueError("GEMINI_API_KEY ausente para provedor 'gemini'")
        base_url = _ler("GEMINI_BASE_URL") or "https://generativelanguage.googleapis.com/v1beta"
        return ClienteHTTPGemini(
            api_key=chave,
            modelo=modelo or "gemini-2.5-flash",
            base_url=base_url,
            opener=opener,
        )
    if alvo == "ollama":
        host = _ler("OLLAMA_HOST") or "http://127.0.0.1:11434"
        return ClienteHTTPOllama(
            modelo=modelo or "qwen3:8b",
            host=host,
            opener=opener,
        )
    raise ValueError(f"provedor desconhecido: {provedor}")
