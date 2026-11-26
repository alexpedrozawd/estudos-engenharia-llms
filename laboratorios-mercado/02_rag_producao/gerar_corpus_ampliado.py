"""Gera o corpus ampliado da Aurora Educação (Etapa 3): 45 documentos e 3 perguntas por documento.

O LLM local escreve cada documento fictício (páginas curtas, sem acentos, com números concretos) e as
perguntas com o trecho literal que as responde. Uma pergunta só entra se o trecho e a resposta curta
aparecerem no texto do documento **e** o critério (`doc`, `pagina`, `contem`) resolver para pelo menos
um trecho da segmentação real (PDF → texto → trechos). Documentos restritos geram perguntas `acl`.
Chamadas ao LLM ficam em cache fora do Git; os arquivos gerados ficam congelados no Git.

    .venv-mercado/bin/python -I laboratorios-mercado/02_rag_producao/gerar_corpus_ampliado.py \
        --base-url http://127.0.0.1:11434/v1 --modelo qwen3.8:27b-ud-iq3_xxs
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402
from mercado_base import dados_sinteticos as ds  # noqa: E402
from mercado_base.cliente_openai import ClienteChatOpenAI  # noqa: E402
from mercado_base.pii import detectar_pii  # noqa: E402

import corpus_aurora  # noqa: E402
import rag_ingestao as ing  # noqa: E402
import rag_pipeline as rp  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
TODOS = ("publico", "aluno", "docente", "coordenacao", "admin")
DOCENTES = ("docente", "coordenacao", "admin")
COORD = ("coordenacao", "admin")
ADMIN = ("admin",)

TEMAS = [
    ("regulamento-laboratorios-informatica", "academico", TODOS, "uso dos laboratorios de informatica"),
    ("politica-uso-wifi-campus", "ti", TODOS, "rede Wi-Fi do campus e limites de uso"),
    ("manual-restaurante-universitario", "servicos", TODOS, "restaurante universitario: horarios e precos"),
    ("regulamento-monitoria", "academico", TODOS, "programa de monitoria e bolsa de monitor"),
    ("programa-intercambio", "internacional", TODOS, "intercambio internacional e requisitos"),
    ("manual-ouvidoria", "ouvidoria", TODOS, "ouvidoria: canais e prazos de resposta"),
    ("nucleo-acessibilidade", "acessibilidade", TODOS, "nucleo de acessibilidade e adaptacoes de prova"),
    ("regulamento-atividades-complementares", "academico", TODOS, "horas de atividades complementares"),
    ("transporte-fretado-campus", "servicos", TODOS, "onibus fretado entre campi"),
    ("regulamento-estacionamento", "servicos", TODOS, "estacionamento do campus e credenciais"),
    ("achados-e-perdidos", "servicos", TODOS, "achados e perdidos: guarda e retirada de objetos"),
    ("iniciacao-cientifica", "pesquisa", TODOS, "iniciacao cientifica: edital e bolsas"),
    ("empresa-junior", "extensao", TODOS, "empresa junior: processo seletivo e horas"),
    ("segunda-chamada-de-provas", "academico", TODOS, "pedido de segunda chamada de provas"),
    ("colacao-de-grau", "secretaria", TODOS, "colacao de grau: inscricao e cerimonia"),
    ("seguranca-laboratorios-quimica", "academico", TODOS, "seguranca nos laboratorios de quimica"),
    ("seguro-estudantil", "financeiro", TODOS, "seguro contra acidentes pessoais do aluno"),
    ("carteirinha-estudantil", "secretaria", TODOS, "carteirinha estudantil: emissao e segunda via"),
    ("programa-apoio-psicologico", "bem-estar", TODOS, "apoio psicologico ao estudante"),
    ("regulamento-esportes-e-academia", "bem-estar", TODOS, "academia e equipes esportivas"),
    ("emprestimo-de-notebooks", "ti", TODOS, "emprestimo de notebooks pela biblioteca de equipamentos"),
    ("regulamento-eventos-academicos", "extensao", TODOS, "eventos academicos e certificados"),
    ("cursos-de-extensao", "extensao", TODOS, "cursos livres de extensao"),
    ("nivelamento-matematica", "academico", TODOS, "curso de nivelamento em matematica para calouros"),
    ("disciplinas-ead", "academico", TODOS, "disciplinas a distancia e encontros presenciais"),
    ("politica-integridade-academica", "academico", TODOS, "plagio e integridade academica"),
    ("regras-provas-online", "academico", TODOS, "provas online com supervisao"),
    ("transferencia-externa", "secretaria", TODOS, "transferencia de outra instituicao para a Aurora"),
    ("reingresso-e-reabertura", "secretaria", TODOS, "reingresso apos abandono e reabertura de matricula"),
    ("dupla-diplomacao", "internacional", TODOS, "dupla diplomacao com universidade parceira"),
    ("financiamento-estudantil-privado", "financeiro", TODOS, "financiamento estudantil privado"),
    ("regras-de-reembolso", "financeiro", TODOS, "reembolso de taxas e mensalidades"),
    ("pagamento-pix-e-cartao", "financeiro", TODOS, "pagamento por Pix e cartao de credito"),
    ("servicos-de-impressao", "ti", TODOS, "cotas de impressao e copias"),
    ("uso-de-armarios", "servicos", TODOS, "aluguel de armarios"),
    ("programa-de-mentoria", "bem-estar", TODOS, "mentoria entre veteranos e calouros"),
    ("eleicoes-diretorio-academico", "extensao", TODOS, "eleicoes do diretorio academico"),
    ("guia-docente-diarios-de-classe", "academico", DOCENTES, "diarios de classe e registro de frequencia"),
    ("guia-docente-orientacao-tcc", "academico", DOCENTES, "orientacao de TCC pelos docentes"),
    ("norma-coordenacao-pre-requisitos", "coordenacao", COORD, "quebra de pre-requisito autorizada pela coordenacao"),
    ("norma-coordenacao-banca-revisao", "coordenacao", COORD, "banca de revisao de notas"),
    ("manual-ti-administracao-contas", "ti", ADMIN, "administracao de contas e bloqueios pela TI"),
    ("guia-docente-horas-complementares", "academico", DOCENTES, "horas de preparacao e reuniao dos docentes"),
    ("manual-financeiro-inadimplencia", "financeiro", ADMIN, "regua interna de cobranca de inadimplencia"),
    ("protocolo-incidentes-de-dados", "privacidade", COORD, "resposta a incidentes com dados pessoais"),
]

ESQUEMA = {
    "type": "json_schema",
    "json_schema": {"name": "documento", "strict": True, "schema": {
        "type": "object", "additionalProperties": False, "required": ["paginas", "perguntas"],
        "properties": {
            "paginas": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}},
            "perguntas": {"type": "array", "items": {
                "type": "object", "additionalProperties": False,
                "required": ["pergunta", "pagina", "trecho_exato", "resposta_curta", "resposta_referencia"],
                "properties": {"pergunta": {"type": "string"}, "pagina": {"type": "integer"},
                               "trecho_exato": {"type": "string"}, "resposta_curta": {"type": "string"},
                               "resposta_referencia": {"type": "string"}}}}}}},
}


def ascii_latin(texto: str) -> str:
    """Sem acentos, como o corpus original (PDF WinAnsi simples)."""
    t = unicodedata.normalize("NFKD", texto or "")
    t = "".join(c for c in t if not unicodedata.combining(c))
    return " ".join(t.encode("latin-1", "ignore").decode("latin-1").split())


def prompt_documento(doc: str, tema: str, restrito: bool) -> str:
    publico = "uso interno de docentes, coordenacao ou administracao" if restrito else "alunos e publico"
    return (
        f"Escreva um documento institucional ficticio da Aurora Educacao (faculdade ficticia) sobre: {tema}. "
        f"Identificador: {doc}. Publico: {publico}.\n"
        "Formato: 3 paginas; cada pagina e uma lista de 4 a 6 linhas curtas (ate 90 caracteres cada), "
        "em portugues SEM acentos nem cedilha. A primeira linha da pagina 1 e o titulo, com '(documento ficticio)'. "
        "Use regras concretas e diferentes entre si: prazos em dias ou horas, valores em R$, percentuais, horarios, "
        "limites e quantidades. Nao use nomes de pessoas, e-mails, telefones nem CPF.\n"
        "Depois escreva exatamente 3 perguntas que um usuario faria, cada uma respondida por uma pagina diferente. "
        "Para cada pergunta: 'pagina' (1, 2 ou 3), 'trecho_exato' (3 a 6 palavras copiadas literalmente da linha "
        "que responde), 'resposta_curta' (o valor que responde, 1 a 4 palavras copiadas literalmente da mesma linha, "
        "de preferencia um numero com unidade) e 'resposta_referencia' (uma frase completa que responde e termina "
        "com [T1]). A pergunta nao pode copiar o trecho palavra por palavra.\n"
        'Responda so com JSON: {"paginas": [["..."]], "perguntas": [{...}]}.'
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", default=os.environ.get("LLM_BASE_URL", "http://127.0.0.1:11434/v1"))
    ap.add_argument("--modelo", default="qwen3.8:27b-ud-iq3_xxs")
    ap.add_argument("--temperatura", type=float, default=0.7)
    ap.add_argument("--max-palavras", type=int, default=40)
    ap.add_argument("--cache", default=os.path.join(mb.RAIZ_REPO, "rascunho-local", "p02-geracao", "cache.json"))
    ap.add_argument("--so-gerar", action="store_true")
    args = ap.parse_args(argv)

    cache = json.load(open(args.cache, encoding="utf-8")) if os.path.exists(args.cache) else {}
    cliente = ClienteChatOpenAI(args.base_url, args.modelo, reasoning_effort="none", timeout_s=300.0)
    for doc, _, perfis, tema in TEMAS:
        chave = f"{args.modelo}|{doc}"
        if chave not in cache:
            r = cliente.completar_chat([{"role": "user", "content": prompt_documento(doc, tema, "aluno" not in perfis)}],
                                       response_format=ESQUEMA, temperatura=args.temperatura, max_tokens=2500)
            cache[chave] = json.loads(r.conteudo)
            os.makedirs(os.path.dirname(args.cache), exist_ok=True)
            with open(args.cache + ".tmp", "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False)
            os.replace(args.cache + ".tmp", args.cache)
            print("gerado", doc, flush=True)
    if args.so_gerar:
        return 0

    documentos, consultas, descartes = {}, [], Counter()
    for doc, depto, perfis, tema in TEMAS:
        bruto = cache[f"{args.modelo}|{doc}"]
        paginas = [[ascii_latin(l) for l in p if ascii_latin(l)] for p in bruto["paginas"]][:3]
        texto_doc = " ".join(" ".join(p) for p in paginas)
        if len(paginas) < 3 or detectar_pii(texto_doc):
            descartes["documento_invalido"] += 1
            continue
        meta = {"perfis": list(perfis), "departamento": depto, "versao": "2026", "vigente": True}
        trechos = ing.segmentar(ing.extrair_paginas_pdf(mb.gerar_pdf_texto(paginas)), doc,
                                max_palavras=args.max_palavras, sobreposicao=8, perfis=perfis,
                                departamento=depto, versao="2026", vigente=True)
        aceitas = []
        for q in bruto["perguntas"]:
            pag, contem, curta = int(q["pagina"]), ascii_latin(q["trecho_exato"]), ascii_latin(q["resposta_curta"])
            if not 1 <= pag <= len(paginas):
                descartes["pagina_invalida"] += 1
                continue
            crit = [{"doc": doc, "pagina": pag, "contem": contem}]
            ids = rp.resolver_relevantes(trechos, crit)
            if not ids:
                descartes["trecho_nao_encontrado"] += 1
                continue
            if not any(curta.lower() in t.texto.lower() for t in trechos if t.id in ids):
                descartes["resposta_fora_do_trecho"] += 1
                continue
            if ds.normalizar(contem) in ds.normalizar(q["pergunta"]):
                descartes["pergunta_copia_trecho"] += 1
                continue
            # O assunto entra na pergunta: num corpus com dezenas de documentos, "qual a multa?" é ambígua.
            pergunta = " ".join(q["pergunta"].split())
            aceitas.append({"pergunta": f"Sobre {tema}: {pergunta[:1].lower()}{pergunta[1:]}", "crit": crit,
                            "curta": curta, "pagina": pag,
                            "ref": re.sub(r"\[T\d+\]", "[T1]", " ".join(q["resposta_referencia"].split()))})
        documentos[doc] = {"metadados": meta, "paginas": paginas}
        for a in aceitas:
            c = {"id": f"qa{len(consultas) + 1:03d}", "categoria": "ampliado" if "aluno" in perfis else "acl",
                 "pergunta": a["pergunta"], "relevantes": a["crit"], "resposta_esperada_contem": [a["curta"]],
                 "resposta_referencia": a["ref"]}
            if "aluno" not in perfis:
                c["filtro"] = {"perfil": perfis[0], "apenas_vigentes": True}
                c["docs_restritos"] = [doc]
            consultas.append(c)

    with open(os.path.join(AQUI, "dados", "corpus_ampliado.json"), "w", encoding="utf-8") as f:
        json.dump({"documentos": documentos}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(AQUI, "dados", "consultas_ampliadas.json"), "w", encoding="utf-8") as f:
        json.dump(consultas, f, ensure_ascii=False, indent=1)
    base = corpus_aurora.carregar_consultas()
    manifesto = {"gerador": args.modelo, "temperatura": args.temperatura, "temas": len(TEMAS),
                 "documentos": len(documentos), "consultas_novas": len(consultas),
                 "consultas_total": len(base) + len(consultas),
                 "por_categoria": dict(Counter(c["categoria"] for c in consultas)), "descartes": dict(descartes),
                 "sha256_prompt_exemplo": mb.sha256_texto(prompt_documento("x", "y", False))}
    print(json.dumps(manifesto, ensure_ascii=False, indent=2))
    print("registro:", mb.registrar_execucao("p02-geracao-corpus", manifesto))
    return 0


if __name__ == "__main__":
    sys.exit(main())
