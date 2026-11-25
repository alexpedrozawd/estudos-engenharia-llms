"""Detecção e mascaramento centralizados de dados pessoais (PII) na Camada 3."""
from __future__ import annotations

import re
from typing import List, Tuple

RE_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
RE_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
RE_TELEFONE = re.compile(r"(?:\(?\b\d{2}\)?\s?)?\b9?\d{4}-?\d{4}\b")


def cpf_valido(valor: str) -> bool:
    """Valida os 11 dígitos e os dois dígitos verificadores (módulo 11) de um CPF."""
    digitos = [int(c) for c in valor if c.isdigit()]
    if len(digitos) != 11 or len(set(digitos)) == 1:
        return False
    for tamanho in (9, 10):
        soma = sum(digitos[i] * (tamanho + 1 - i) for i in range(tamanho))
        resto = (soma * 10) % 11
        esperado = 0 if resto == 10 else resto
        if digitos[tamanho] != esperado:
            return False
    return True


def mascarar_pii(texto: str) -> Tuple[str, List[str]]:
    """Mascara CPF válido, e-mail e telefone; devolve (texto_mascarado, tipos_detectados).

    CPFs são verificados e substituídos antes de telefones para evitar colisão parcial em
    sequências de 11 dígitos sem pontuação.
    """
    detectados: List[str] = []

    def _subst_cpf(match: re.Match[str]) -> str:
        candidato = match.group(0)
        if not cpf_valido(candidato):
            return candidato
        if "cpf" not in detectados:
            detectados.append("cpf")
        return "[CPF]"

    mascarado = RE_CPF.sub(_subst_cpf, texto)
    for nome, rx, rotulo in (
        ("email", RE_EMAIL, "[EMAIL]"),
        ("telefone", RE_TELEFONE, "[TELEFONE]"),
    ):
        if rx.search(mascarado):
            detectados.append(nome)
            mascarado = rx.sub(rotulo, mascarado)
    return mascarado, detectados


def detectar_pii(texto: str) -> List[str]:
    """Devolve a lista ordenada de tipos de PII detectados no texto."""
    return mascarar_pii(texto)[1]
