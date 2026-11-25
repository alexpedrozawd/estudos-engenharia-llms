"""Corpus sintético da Aurora Educação (instituição fictícia; proposta didática, sem dados reais).

Cada documento vira um PDF gerado na hora por `mercado_base.gerar_pdf_texto`; linhas em lista
são células de tabela. Só caracteres Latin-1 (o gerador usa WinAnsi).
"""
import json
import os

DOCUMENTOS = {
    "regulamento-academico": [
        [
            "Regulamento acadêmico da Aurora Educação (documento fictício de laboratório).",
            "A rematrícula é obrigatória a cada semestre e deve ser feita pelo portal do aluno",
            "até o décimo dia útil do início das aulas. Quem perde o prazo entra em lista de espera",
            "e só pode cursar disciplinas com vagas remanescentes.",
            "O trancamento de matrícula pode ser pedido até a metade do semestre letivo e vale",
            "por no máximo dois semestres consecutivos.",
        ],
        [
            "Avaliação e aprovação.",
            "A média final é ponderada: a prova vale 60 por cento, os trabalhos 30 por cento e a",
            "participação 10 por cento. É aprovado quem obtém média final igual ou maior que 6,0",
            "e frequência mínima de 75 por cento das aulas.",
            "Quem fica com média entre 4,0 e 5,9 pode fazer exame final; abaixo de 4,0 há reprovação direta.",
        ],
    ],
    "tabela-de-servicos": [
        [
            "Serviços da secretaria acadêmica e prazos de atendimento.",
            ["Serviço", "Prazo (dias úteis)", "Taxa (R$)"],
            ["Declaração de matrícula", "2", "0,00"],
            ["Segunda via do diploma", "30", "120,00"],
            ["Histórico escolar", "5", "25,00"],
            ["Revisão de prova", "7", "0,00"],
            ["Aproveitamento de disciplina", "15", "60,00"],
            "Os pedidos são feitos pelo portal do aluno; prazos contam a partir do pagamento da taxa.",
        ],
    ],
    "politica-de-privacidade-academica": [
        [
            "Política de privacidade acadêmica (texto didático, não jurídico).",
            "A Aurora Educação usa dados pessoais de alunos apenas para fins acadêmicos e",
            "administrativos. Notas e frequência só são exibidas ao próprio aluno e aos docentes",
            "da disciplina. Pedidos de correção de dados são atendidos em até 15 dias.",
            "O atendimento automatizado não deve pedir nem repetir CPF, senha ou dados de cartão.",
        ],
    ],
}


def gerar_pdfs(pasta: str) -> dict:
    """Grava um PDF por documento em `pasta` e devolve {doc: caminho}."""
    import mercado_base as mb

    os.makedirs(pasta, exist_ok=True)
    caminhos = {}
    for doc, paginas in DOCUMENTOS.items():
        caminho = os.path.join(pasta, f"{doc}.pdf")
        with open(caminho, "wb") as f:
            f.write(mb.gerar_pdf_texto(paginas))
        caminhos[doc] = caminho
    return caminhos


def carregar_consultas() -> list:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados", "consultas_ouro.json"),
              encoding="utf-8") as f:
        return json.load(f)
