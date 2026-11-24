"""Cliente resiliente com SSE, backoff+jitter, fila limitada e idempotência."""
from dataclasses import dataclass
import hashlib
import json
import random
from typing import Callable, Dict, Iterable, List, Optional


class ErroTransitorio(RuntimeError):
    """Erro temporário (429 ou 503) elegível a nova tentativa."""


class ErroPermanente(RuntimeError):
    """Erro de pedido inválido (400/401) que não deve ser repetido."""


@dataclass(frozen=True)
class ResultadoChamada:
    """Resultado consolidado de uma chamada ao modelo."""

    id_pedido: str
    impressao_digital: str
    texto: str
    motivo_parada: str
    tentativas: int
    de_cache_idempotencia: bool = False


def calcular_espera_s(tentativa: int, base_s: float = 0.25, teto_s: float = 4.0, rng: Optional[random.Random] = None) -> float:
    """Calcula espera exponencial com jitter completo determinístico."""
    gerador = rng or random.Random(7)
    limite = min(teto_s, base_s * (2 ** tentativa))
    return round(gerador.uniform(0.0, limite), 4)


def analisar_eventos_sse(linhas: Iterable[str]) -> Dict[str, object]:
    """Lê eventos SSE simulados e detecta se o fim foi natural ou cortado."""
    pedacos: List[str] = []
    motivo_parada = "incompleto"
    for bruta in linhas:
        linha = bruta.strip()
        if not linha.startswith("data:"):
            continue
        carga = linha[5:].strip()
        if carga == "[DONE]":
            if motivo_parada == "incompleto":
                motivo_parada = "end_turn"
            break
        evento = json.loads(carga)
        if "delta" in evento:
            pedacos.append(str(evento["delta"]))
        if "stop_reason" in evento:
            motivo_parada = str(evento["stop_reason"])
    return {"texto": "".join(pedacos), "motivo_parada": motivo_parada}


class ClienteResiliente:
    """Coordena fila máxima, registro de idempotência e novas tentativas limitadas."""

    def __init__(self, max_em_fila: int = 4, max_tentativas: int = 3, semente_jitter: int = 7):
        self.max_em_fila = max_em_fila
        self.max_tentativas = max_tentativas
        self._rng = random.Random(semente_jitter)
        self._registros: Dict[str, ResultadoChamada] = {}
        self.esperas_registradas: List[float] = []
        self.em_andamento = 0

    @staticmethod
    def gerar_impressao(payload: Dict[str, object]) -> str:
        canonico = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canonico.encode("utf-8")).hexdigest()[:16]

    def executar(
        self,
        id_pedido: str,
        payload: Dict[str, object],
        transporte: Callable[[Dict[str, object]], Dict[str, str]],
    ) -> ResultadoChamada:
        impressao = self.gerar_impressao(payload)
        if id_pedido in self._registros:
            previo = self._registros[id_pedido]
            if previo.impressao_digital != impressao:
                raise ValueError("id_pedido reutilizado com payload diferente")
            return ResultadoChamada(
                id_pedido=previo.id_pedido,
                impressao_digital=previo.impressao_digital,
                texto=previo.texto,
                motivo_parada=previo.motivo_parada,
                tentativas=previo.tentativas,
                de_cache_idempotencia=True,
            )
        if self.em_andamento >= self.max_em_fila:
            raise ErroTransitorio("recusa controlada: fila de simultaneidade cheia (503)")

        self.em_andamento += 1
        try:
            ultimo_erro: Optional[Exception] = None
            for tentativa in range(1, self.max_tentativas + 1):
                try:
                    resp = transporte(payload)
                    res = ResultadoChamada(
                        id_pedido=id_pedido,
                        impressao_digital=impressao,
                        texto=resp["texto"],
                        motivo_parada=resp.get("stop_reason", "end_turn"),
                        tentativas=tentativa,
                    )
                    self._registros[id_pedido] = res
                    return res
                except ErroTransitorio as exc:
                    ultimo_erro = exc
                    if tentativa < self.max_tentativas:
                        self.esperas_registradas.append(calcular_espera_s(tentativa - 1, rng=self._rng))
            raise ErroTransitorio(f"esgotadas {self.max_tentativas} tentativas: {ultimo_erro}")
        finally:
            self.em_andamento -= 1
