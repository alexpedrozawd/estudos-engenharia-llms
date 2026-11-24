"""Validador executável de especificação, aceite e fallback suave da Aurora."""
import json
import os
import re
from typing import Dict, List, Optional

DADOS_POLITICAS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "dados",
    "politicas_aurora.json",
)


def carregar_politicas(caminho: str = DADOS_POLITICAS) -> List[Dict[str, object]]:
    """Carrega políticas fictícias da Aurora Educação sem manter arquivo aberto."""
    with open(caminho, encoding="utf-8") as arq:
        dados = json.load(arq)
    return list(dados["politicas"])


def classificar_escopo_pedido(pergunta: str) -> str:
    """Separa pedidos dentro do escopo, fora do escopo e ações proibidas."""
    texto = pergunta.lower()
    if any(termo in texto for termo in ("confirmar matrícula", "aplicar desconto", "gabarito")):
        return "fora_escopo_proibido"
    if any(termo in texto for termo in ("cpf", "nota", "histórico escolar")):
        return "sensivel_exige_triagem"
    return "permitido"


def validar_contrato_saida(
    resposta_modelo: str,
    politicas: List[Dict[str, object]],
    *,
    max_palavras: int = 120,
    tempo_ms: Optional[float] = None,
    timeout_ms: float = 1500.0,
) -> Dict[str, object]:
    """Valida contrato I/O e aciona fallback suave (smooth failing) se violado."""
    if tempo_ms is not None and tempo_ms > timeout_ms:
        return {
            "aceito": False,
            "motivo": "fallback_latencia",
            "mensagem_usuario": "O atendimento automático demorou além do previsto. Consulte o portal oficial ou fale com a secretaria.",
        }

    ids_validos = {str(p["id"]) for p in politicas}
    citacoes = re.findall(r"\bPOL-\d+\b", resposta_modelo)
    palavras = resposta_modelo.split()

    if any(proib in resposta_modelo.lower() for proib in ("matrícula confirmada", "desconto aplicado")):
        return {
            "aceito": False,
            "motivo": "reprovacao_automatica_acao_proibida",
            "mensagem_usuario": "Não é possível confirmar matrícula ou conceder desconto por este canal; encaminhando à secretaria.",
        }
    if len(palavras) > max_palavras:
        return {
            "aceito": False,
            "motivo": "excesso_de_palavras",
            "mensagem_usuario": "Resposta resumida indisponível no momento; consulte o regulamento oficial.",
        }
    if not citacoes or not set(citacoes).issubset(ids_validos):
        return {
            "aceito": False,
            "motivo": "sem_fonte_valida",
            "mensagem_usuario": "Não encontrei referência oficial válida para responder com segurança; encaminhando à secretaria.",
        }
    return {"aceito": True, "motivo": "ok", "citacoes": citacoes, "mensagem_usuario": resposta_modelo}
