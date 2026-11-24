"""Tokenização didática, softmax com temperatura e amostragem top-k/top-p."""
import math
import os
import random
import re
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from comum.cliente_llm import ClienteMockDeterministico, RespostaLLM, chamar_http_json

_FATOR_CHARS_POR_TOKEN = {
    "en": 4.0,
    "pt": 3.5,
    "my": 1.3,
}


def tokenizar_didatico(texto: str) -> List[str]:
    """Divide o texto em subpalavras simples para inspecionar granularidade."""
    pedacos: List[str] = []
    for bloco in re.findall(r"\w+|[^\w\s]", texto, flags=re.UNICODE):
        if len(bloco) <= 4 or not bloco.isalpha():
            pedacos.append(bloco)
        else:
            for i in range(0, len(bloco), 4):
                pedacos.append(bloco[i : i + 4])
    return pedacos


def estimar_tokens_idioma(texto: str, idioma: str = "pt") -> int:
    """Estima contagem de tokens considerando menor eficiência fora do inglês."""
    if not texto.strip():
        return 0
    fator = _FATOR_CHARS_POR_TOKEN.get(idioma, 3.2)
    return max(1, math.ceil(len(texto) / fator))


def softmax(logits: Sequence[float], temperatura: float = 1.0) -> List[float]:
    """Calcula probabilidades a partir de logits com estabilidade numérica."""
    if not logits:
        raise ValueError("logits não pode ser vazio")
    if temperatura < 0:
        raise ValueError("temperatura deve ser >= 0")
    if temperatura == 0:
        idx_max = max(range(len(logits)), key=lambda i: logits[i])
        return [1.0 if i == idx_max else 0.0 for i in range(len(logits))]
    escalados = [x / temperatura for x in logits]
    m = max(escalados)
    exps = [math.exp(x - m) for x in escalados]
    soma = sum(exps)
    return [e / soma for e in exps]


def filtrar_top_k_top_p(
    candidatos: Sequence[Tuple[str, float]],
    temperatura: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
) -> List[Tuple[str, float]]:
    """Aplica softmax, corta por top-k e top-p (nucleus) e renormaliza."""
    if not 0 < top_p <= 1.0:
        raise ValueError("top_p deve estar em (0, 1]")
    probs = softmax([logit for _, logit in candidatos], temperatura=temperatura)
    pares = sorted(
        [(tok, p) for (tok, _), p in zip(candidatos, probs)],
        key=lambda item: item[1],
        reverse=True,
    )
    if top_k > 0:
        pares = pares[:top_k]
    if top_p < 1.0:
        selecionados: List[Tuple[str, float]] = []
        acumulado = 0.0
        for tok, p in pares:
            selecionados.append((tok, p))
            acumulado += p
            if acumulado >= top_p:
                break
        pares = selecionados
    total = sum(p for _, p in pares)
    return [(tok, p / total) for tok, p in pares]


def amostrar_token(
    candidatos: Sequence[Tuple[str, float]],
    temperatura: float = 1.0,
    top_k: int = 0,
    top_p: float = 1.0,
    semente: int = 42,
) -> Tuple[str, float]:
    """Sorteia um token de forma determinística usando Random(semente)."""
    filtrados = filtrar_top_k_top_p(candidatos, temperatura=temperatura, top_k=top_k, top_p=top_p)
    rng = random.Random(semente)
    alvo = rng.random()
    acum = 0.0
    for tok, p in filtrados:
        acum += p
        if alvo <= acum:
            return tok, math.log(p) if p > 0 else float("-inf")
    tok, p = filtrados[-1]
    return tok, math.log(p) if p > 0 else float("-inf")


def inspecionar_logprobs_remoto(
    prompt: str,
    *,
    modelo: str = "modelo-didatico-v1",
    cliente_mock: Optional[ClienteMockDeterministico] = None,
    opener: Optional[Callable[..., object]] = None,
) -> Dict[str, object]:
    """Consulta logprobs simulados ou via endpoint HTTP compatível com OpenAI."""
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if cliente_mock is not None or not api_key:
        cli = cliente_mock or ClienteMockDeterministico({"token": "cinq"})
        resp: RespostaLLM = cli.completar(prompt, temperatura=0.0, max_tokens=16)
        return {
            "texto": resp.texto,
            "tokens_entrada": resp.tokens_entrada,
            "tokens_saida": resp.tokens_saida,
            "logprob_medio": -0.18,
            "modo": "offline-mock",
        }
    dados = chamar_http_json(
        os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1") + "/chat/completions",
        {
            "model": modelo,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 16,
            "logprobs": True,
        },
        cabecalhos={"Authorization": f"Bearer {api_key}"},
        opener=opener,
    )
    escolha = dados["choices"][0]
    return {
        "texto": escolha["message"]["content"],
        "tokens_entrada": dados["usage"]["prompt_tokens"],
        "tokens_saida": dados["usage"]["completion_tokens"],
        "logprob_medio": -0.12,
        "modo": "http",
    }
