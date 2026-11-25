"""Corpus sintético da Aurora Educação (instituição fictícia; proposta didática, sem dados reais).

Contém 12 documentos com tabelas, distrações lexicais, versões conflitantes (2024 vs 2026) e
metadados de controle de acesso (ACL) por perfil. Cada documento vira um PDF gerado na hora por
`mercado_base.gerar_pdf_texto`. Só caracteres Latin-1 (WinAnsi).
"""
import json
import os
from typing import Dict

METADADOS_DOCUMENTOS: Dict[str, Dict[str, object]] = {
    "regulamento-academico": {
        "perfis": ("publico", "aluno", "docente", "coordenacao", "admin"),
        "departamento": "academico",
        "versao": "2026",
        "vigente": True,
    },
    "regulamento-academico-2024": {
        "perfis": ("publico", "aluno", "docente", "coordenacao", "admin"),
        "departamento": "academico",
        "versao": "2024",
        "vigente": False,
    },
    "tabela-de-servicos": {
        "perfis": ("publico", "aluno", "docente", "coordenacao", "admin"),
        "departamento": "secretaria",
        "versao": "2026",
        "vigente": True,
    },
    "tabela-de-servicos-2024": {
        "perfis": ("publico", "aluno", "docente", "coordenacao", "admin"),
        "departamento": "secretaria",
        "versao": "2024",
        "vigente": False,
    },
    "politica-de-privacidade-academica": {
        "perfis": ("publico", "aluno", "docente", "coordenacao", "admin"),
        "departamento": "privacidade",
        "versao": "2026",
        "vigente": True,
    },
    "calendario-academico-2026": {
        "perfis": ("publico", "aluno", "docente", "coordenacao", "admin"),
        "departamento": "secretaria",
        "versao": "2026",
        "vigente": True,
    },
    "tabela-bolsas-e-descontos": {
        "perfis": ("publico", "aluno", "docente", "coordenacao", "admin"),
        "departamento": "financeiro",
        "versao": "2026",
        "vigente": True,
    },
    "manual-biblioteca": {
        "perfis": ("publico", "aluno", "docente", "coordenacao", "admin"),
        "departamento": "biblioteca",
        "versao": "2026",
        "vigente": True,
    },
    "manual-estagio-e-tcc": {
        "perfis": ("publico", "aluno", "docente", "coordenacao", "admin"),
        "departamento": "academico",
        "versao": "2026",
        "vigente": True,
    },
    "guia-docente-avaliacao": {
        "perfis": ("docente", "coordenacao", "admin"),
        "departamento": "academico",
        "versao": "2026",
        "vigente": True,
    },
    "norma-interna-coordenacao": {
        "perfis": ("coordenacao", "admin"),
        "departamento": "coordenacao",
        "versao": "2026",
        "vigente": True,
    },
    "manual-financeiro-administrativo": {
        "perfis": ("admin",),
        "departamento": "financeiro",
        "versao": "2026",
        "vigente": True,
    },
}

DOCUMENTOS = {
    "regulamento-academico": [
        [
            "Regulamento academico da Aurora Educacao (versao vigente 2026, documento ficticio).",
            "A rematricula e obrigatoria a cada semestre e deve ser feita pelo portal do aluno",
            "ate o decimo dia util do inicio das aulas. Quem perde o prazo entra em lista de espera",
            "e so pode cursar disciplinas com vagas remanescentes.",
            "O trancamento de matricula pode ser pedido ate a metade do semestre letivo e vale",
            "por no maximo dois semestres consecutivos.",
        ],
        [
            "Avaliacao e aprovacao (regulamento vigente 2026).",
            "A media final e ponderada: a prova vale 60 por cento, os trabalhos 30 por cento e a",
            "participacao 10 por cento. E aprovado quem obtem media final igual ou maior que 6,0",
            "e frequencia minima de 75 por cento das aulas.",
            "Quem fica com media entre 4,0 e 5,9 pode fazer exame final; abaixo de 4,0 ha reprovacao direta.",
        ],
    ],
    "regulamento-academico-2024": [
        [
            "Regulamento academico historico de 2024 (REVOGADO em 2026).",
            "Em 2024, a rematricula ia ate o quinto dia util e o trancamento valia por apenas um semestre.",
            "Na versao antiga de 2024, a media minima para aprovacao sem exame era 5,0 e a frequencia",
            "minima exigida era de 70 por cento das aulas.",
        ],
    ],
    "tabela-de-servicos": [
        [
            "Servicos da secretaria academica e prazos de atendimento (tabela vigente 2026).",
            ["Servico", "Prazo (dias uteis)", "Taxa (R$)"],
            ["Declaracao de matricula", "2", "0,00"],
            ["Segunda via do diploma", "30", "120,00"],
            ["Historico escolar", "5", "25,00"],
            ["Revisao de prova", "7", "0,00"],
            ["Aproveitamento de disciplina", "15", "60,00"],
            "Os pedidos sao feitos pelo portal do aluno; prazos contam a partir do pagamento da taxa.",
        ],
    ],
    "tabela-de-servicos-2024": [
        [
            "Tabela historica de servicos da secretaria de 2024 (REVOGADA em 2026).",
            ["Servico", "Prazo (dias uteis)", "Taxa (R$)"],
            ["Segunda via do diploma", "20", "90,00"],
            ["Historico escolar", "3", "15,00"],
            ["Aproveitamento de disciplina", "10", "40,00"],
        ],
    ],
    "politica-de-privacidade-academica": [
        [
            "Politica de privacidade academica (texto didatico, nao juridico).",
            "A Aurora Educacao usa dados pessoais de alunos apenas para fins academicos e",
            "administrativos. Notas e frequencia so sao exibidas ao proprio aluno e aos docentes",
            "da disciplina. Pedidos de correcao de dados sao atendidos em ate 15 dias.",
            "O atendimento automatizado nao deve pedir nem repetir CPF, senha ou dados de cartao.",
        ],
    ],
    "calendario-academico-2026": [
        [
            "Calendario academico oficial da Aurora Educacao para 2026.",
            ["Evento", "Primeiro semestre", "Segundo semestre"],
            ["Inicio das aulas", "02/02/2026", "03/08/2026"],
            ["Limite de rematricula", "13/02/2026", "14/08/2026"],
            ["Limite de trancamento", "17/04/2026", "16/10/2026"],
            ["Semana de exame final", "22/06/2026", "07/12/2026"],
            ["Colacao de grau", "18/07/2026", "19/12/2026"],
        ],
        [
            "Prazos administrativos complementares do calendario 2026.",
            "Os pedidos de aproveitamento de estudos protocolados apos o encerramento da janela",
            "de rematricula serao analisados apenas para o semestre letivo subsequente, sem efeito",
            "retroativo sobre mensalidades ja vencidas ou disciplinas em curso.",
        ],
    ],
    "tabela-bolsas-e-descontos": [
        [
            "Programa de bolsas e descontos academicos (vigente 2026).",
            ["Modalidade", "Desconto", "Requisito principal"],
            ["Bolsa merito", "30%", "Media semestral igual ou superior a 8,5"],
            ["Monitoria academica", "25%", "Dedicacao de 8 horas semanais"],
            ["Iniciacao cientifica", "40%", "Projeto aprovado pelo comite de pesquisa"],
            ["Convenio empresa", "15%", "Vinculo ativo com parceiro cadastrado"],
            "Bolsas institucionais nao sao acumulaveis entre si; prevalece o maior percentual.",
        ],
        [
            "Manutencao e cancelamento de bolsas na Aurora Educacao.",
            "A renovacao semestral exige frequencia minima de 75 por cento e ausencia de reprovacao",
            "por falta. Em caso de trancamento de matricula, o beneficio fica suspenso durante o",
            "periodo afastado e precisa de nova solicitacao no retorno regular ao curso.",
        ],
    ],
    "manual-biblioteca": [
        [
            "Manual da biblioteca central da Aurora Educacao (regulamento de acervo).",
            "O prazo de emprestimo de livros para graduacao e de 10 dias corridos, com ate duas",
            "renovacoes online se nao houver reserva. A multa por atraso e de R$ 2,50 por dia.",
            "O trancamento de armario individual dura no maximo 30 dias e exige devolucao da chave.",
            "A taxa de reposicao de cartao magnetico da biblioteca e de R$ 18,00.",
        ],
        [
            "Consulta local, obras de referencia e reserva de cabines de estudo.",
            "Obras raras, periodicos impressos e exemplares de consulta local nao podem sair da",
            "sala de leitura. A reserva de cabine em grupo tem duracao de 2 horas por turno e",
            "deve ser confirmada presencialmente ate 15 minutos apos o horario agendado.",
        ],
    ],
    "manual-estagio-e-tcc": [
        [
            "Manual de estagio supervisionado e Trabalho de Conclusao de Curso (TCC).",
            "A frequencia minima obrigatoria no estagio supervisionado e de 85 por cento da carga",
            "horaria prevista no termo de compromisso. A media da banca de TCC exige nota 7,0.",
            "O pedido de revisao de nota da banca de TCC deve ocorrer em ate 3 dias uteis apos a defesa.",
        ],
        [
            "Entrega do relatorio final e deposito digital na biblioteca.",
            "Apos a aprovacao pela banca examinadora, o estudante tem prazo de 15 dias corridos",
            "para depositar a versao definitiva em PDF no repositorio institucional, condicao",
            "indispensavel para liberacao da colacao de grau e emissao do historico escolar.",
        ],
    ],
    "guia-docente-avaliacao": [
        [
            "Guia interno do corpo docente (acesso restrito a docentes, coordenacao e admin).",
            "O prazo para lancamento de notas no sistema academico e de 10 dias uteis apos a prova.",
            "Avaliacoes substitutivas devem usar versao distinta do banco oficial de questoes.",
            "Revisoes de prova deferidas pelo docente exigem registro de justificativa no diario digital.",
        ],
        [
            "Auditoria de diarios de classe e guarda de instrumentos avaliativos.",
            "Os arquivos digitais de provas corrigidas e atas de frequencia devem permanecer no",
            "portal docente por pelo menos dois semestres apos o encerramento da turma para",
            "eventual conferencia da coordenacao de curso e comissao propria de avaliacao.",
        ],
    ],
    "norma-interna-coordenacao": [
        [
            "Norma interna de coordenacao de curso (acesso restrito a coordenacao e admin).",
            "A coordenacao pode conceder bolsa emergencial temporaria de ate 40 por cento por um",
            "semestre mediante parecer social. Quebra de pre-requisito depende de ata do colegiado.",
            "Turmas com menos de 12 matriculados exigem aprovacao da diretoria academica.",
        ],
        [
            "Fluxo de homologacao de aproveitamento e transferencia externa.",
            "Planos de ensino oriundos de outras instituicoes exigem compatibilidade minima de",
            "75 por cento da ementa e carga horaria equivalente, com despacho fundamentado do",
            "coordenador no prazo maximo de 15 dias uteis a contar da abertura do protocolo.",
        ],
    ],
    "manual-financeiro-administrativo": [
        [
            "Manual financeiro administrativo (acesso estritamente restrito ao perfil admin).",
            "O teto operacional de renegociacao de debitos vencidos e de ate 6 parcelas mensais.",
            "Estornos acima de R$ 1.500,00 exigem dupla assinatura e codigo interno AUR-FIN-2026.",
            "Relatorios de inadimplencia sao fechados todo quinto dia util de cada mes.",
        ],
        [
            "Conciliacao bancaria e repasse de bolsas de convenio.",
            "Boletos liquidados por compensacao externa sao conciliados automaticamente ate D+2.",
            "Divergencias acima de R$ 50,00 devem ser abertas na fila de auditoria contabil com",
            "comprovante anexo antes do fechamento mensal de receitas e descontos.",
        ],
    ],
}


def metadados_doc(doc: str) -> Dict[str, object]:
    """Devolve metadados declarados do documento ou padrão público vigente."""
    return dict(
        METADADOS_DOCUMENTOS.get(
            doc,
            {
                "perfis": ("publico", "aluno", "docente", "coordenacao", "admin"),
                "departamento": "geral",
                "versao": "2026",
                "vigente": True,
            },
        )
    )


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
