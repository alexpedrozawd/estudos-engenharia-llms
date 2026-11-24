"""Catálogo de prompts versionados e validação estrita de schema JSON."""
from dataclasses import dataclass
import json
from typing import Dict, List, Optional, Tuple

from comum.cliente_llm import ClienteMockDeterministico

OFICINAS_PERMITIDAS = ("terça", "quinta", "sábado")


@dataclass(frozen=True)
class PromptVersionado:
    """Artefato versionado de prompt separado do código de chamada."""

    versao: str
    sistema: str
    esforco: str
    max_tokens: int


CATALOGO_PROMPTS: Dict[str, PromptVersionado] = {
    "inscricao-v1": PromptVersionado(
        versao="inscricao-v1",
        sistema="Extraia nome, idade (int ou null) e oficina (terça|quinta|sábado) em JSON.",
        esforco="low",
        max_tokens=160,
    ),
    "inscricao-v2": PromptVersionado(
        versao="inscricao-v2",
        sistema=(
            "Extraia estritamente em JSON: nome (string), idade (int entre 5 e 100 ou null), "
            "oficina (terça|quinta|sábado), recusa (bool) e motivo_recusa (string ou null)."
        ),
        esforco="medium",
        max_tokens=220,
    ),
}


def escapar_delimitadores_xml(texto: str) -> str:
    """Neutraliza marcas XML em entradas do usuário para evitar injeção estrutural."""
    return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def montar_prompt_inscricao(versao: str, texto_aluno: str) -> Tuple[str, PromptVersionado]:
    """Constrói o prompt final com versão explícita e bloco isolado de dados."""
    artefato = CATALOGO_PROMPTS[versao]
    seguro = escapar_delimitadores_xml(texto_aluno)
    prompt = f'<entrada versao="{artefato.versao}">\n{seguro}\n</entrada>'
    return prompt, artefato


def validar_inscricao_json(bruto: str) -> Tuple[bool, Optional[Dict[str, object]], str]:
    """Valida JSON, schema estrito e regras de negócio (idade 5..100, oficina)."""
    try:
        dados = json.loads(bruto)
    except json.JSONDecodeError as exc:
        return False, None, f"json_invalido: {exc.msg}"

    if not isinstance(dados, dict):
        return False, None, "raiz_deve_ser_objeto"
    esperadas = {"nome", "idade", "oficina", "recusa", "motivo_recusa"}
    if set(dados.keys()) != esperadas:
        return False, None, "campos_divergentes_do_schema"
    if not isinstance(dados["recusa"], bool):
        return False, None, "campo_recusa_invalido"
    if dados["recusa"]:
        if not isinstance(dados["motivo_recusa"], str) or not dados["motivo_recusa"].strip():
            return False, None, "recusa_sem_motivo"
        return True, dados, "recusa_controlada"

    if not isinstance(dados["nome"], str) or not dados["nome"].strip():
        return False, None, "nome_obrigatorio"
    idade = dados["idade"]
    if idade is not None and (isinstance(idade, bool) or not isinstance(idade, int) or not (5 <= idade <= 100)):
        return False, None, "idade_fora_da_faixa"
    if dados["oficina"] not in OFICINAS_PERMITIDAS:
        return False, None, "oficina_fora_da_lista"
    return True, dados, "ok"


def extrair_com_reparo(
    texto_aluno: str,
    versao: str,
    cliente: ClienteMockDeterministico,
    *,
    max_reparos: int = 1,
) -> Dict[str, object]:
    """Executa chamada ao modelo com limite estrito de tentativas de reparo."""
    prompt, artefato = montar_prompt_inscricao(versao, texto_aluno)
    erros: List[str] = []
    consulta = prompt
    for tentativa in range(1 + max_reparos):
        resp = cliente.completar(
            consulta,
            sistema=artefato.sistema,
            esforco=artefato.esforco,
            max_tokens=artefato.max_tokens,
        )
        ok, dados, status = validar_inscricao_json(resp.texto)
        if ok:
            return {
                "ok": True,
                "status": status,
                "dados": dados,
                "versao": artefato.versao,
                "esforco": artefato.esforco,
                "tentativas": tentativa + 1,
                "erros_previos": erros,
            }
        erros.append(status)
        consulta = f"{prompt}\n<erro_validacao>{status}</erro_validacao>"
    return {
        "ok": False,
        "status": erros[-1],
        "dados": None,
        "versao": artefato.versao,
        "esforco": artefato.esforco,
        "tentativas": 1 + max_reparos,
        "erros_previos": erros,
    }
