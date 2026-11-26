"""Amplia `dados/chamados_aurora.jsonl` com chamados sintéticos gerados por um LLM local (Etapa 3).

Fluxo (parte 6.2 do guia): gerar por estrato (fatia × categoria) → descartar PII, tamanho fora da faixa
e quase duplicatas lexicais → conferir o rótulo com o mesmo LLM às cegas (descarta o que ele classifica
diferente, ou seja, chamados ambíguos) → agrupar variações semânticas por cosseno de embeddings → escolher
por hash até `--por-estrato` exemplos → gravar o JSONL e o manifesto da geração em `execucoes/`.

Chamadas ao LLM ficam em cache (`--cache`, fora do Git): rodar de novo continua de onde parou.
Os dados gerados são congelados no Git; o CI só confere a integridade (test_p04_qlora.py).

    .venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/gerar_chamados_sinteticos.py \
        --base-url http://127.0.0.1:11434/v1 --modelo qwen3.8:27b-ud-iq3_xxs --embed-modelo qwen3-embedding:0.6b
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402
from mercado_base import dados_sinteticos as ds  # noqa: E402
from mercado_base.cliente_openai import ClienteChatOpenAI  # noqa: E402
from mercado_base.pii import detectar_pii  # noqa: E402

import qlora_receita as qr  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados", "chamados_aurora.jsonl")
FATIAS = ("formal", "informal", "com_ruido")

ESTILOS = {
    "formal": "português formal e completo, cordial, com frases inteiras, acentos e pontuação corretos, sem gírias",
    "informal": "mensagem de aplicativo de conversa, em minúsculas, com abreviações comuns (pra, tá, vc, q) e "
                "tom coloquial, mas sem erros graves de grafia",
    "com_ruido": "mensagem telegráfica digitada com pressa no celular: erros de digitação, letras trocadas ou "
                 "faltando, sem acentos, quase sem pontuação e sem artigos",
}
CATEGORIAS = {
    "financeiro": ("pagamentos e dinheiro", ["boleto e segunda via", "cobrança indevida ou duplicada",
                   "parcelamento de dívida", "reembolso ou estorno", "bolsa ou desconto na mensalidade",
                   "multa e juros por atraso", "nota fiscal ou comprovante de pagamento", "reajuste da mensalidade",
                   "pagamento por cartão ou Pix", "débito de rematrícula"]),
    "academico": ("vida acadêmica: aulas, notas e disciplinas", ["revisão de nota", "data de prova ou prova substitutiva",
                  "faltas e frequência", "horário ou sala de aula", "trancamento ou inclusão de uma disciplina",
                  "aproveitamento de disciplina cursada fora", "orientação e prazos do TCC", "atividades complementares",
                  "plano de ensino ou ementa", "dúvida sobre professor ou monitoria"]),
    "acesso": ("acesso a sistemas digitais", ["login no portal do aluno", "senha do ambiente virtual (AVA)",
               "e-mail institucional bloqueado", "Wi-Fi do campus", "aplicativo da instituição travando",
               "autenticação em duas etapas", "acesso à biblioteca digital", "página fora do ar ou com erro",
               "conta duplicada ou usuário inexistente", "acesso negado a uma sala virtual"]),
    "secretaria": ("documentos e cadastro na secretaria", ["declaração de matrícula", "histórico escolar",
                   "emissão ou prazo do diploma", "certificado de conclusão", "atualização de dados cadastrais",
                   "carteirinha estudantil", "transferência para outra instituição", "trancamento do curso inteiro",
                   "colação de grau", "autenticação de documentos"]),
}
ESQUEMA = {
    "type": "json_schema",
    "json_schema": {"name": "chamados", "strict": True, "schema": {
        "type": "object", "additionalProperties": False, "required": ["chamados"],
        "properties": {"chamados": {"type": "array", "items": {"type": "string"}}}}},
}
ESQUEMA_CLASSE = {
    "type": "json_schema",
    "json_schema": {"name": "classe", "strict": True, "schema": {
        "type": "object", "additionalProperties": False, "required": ["categoria"],
        "properties": {"categoria": {"type": "string", "enum": list(qr.CATEGORIAS)}}}},
}


def prompt_geracao(fatia: str, categoria: str, subtemas: list, quantidade: int, exemplos: list) -> str:
    tema, _ = CATEGORIAS[categoria]
    outras = ", ".join(f"{c} ({CATEGORIAS[c][0]})" for c in CATEGORIAS if c != categoria)
    return (
        f"Escreva {quantidade} chamados diferentes que alunos de uma faculdade fictícia, a Aurora Educação, "
        f"enviariam ao atendimento. Todos são da categoria '{categoria}' ({tema}) e não podem ser confundidos "
        f"com as outras categorias: {outras}.\n"
        f"Estilo obrigatório: {ESTILOS[fatia]}.\n"
        f"Distribua os chamados entre estes assuntos: {'; '.join(subtemas)}.\n"
        "Regras: cada chamado tem de 4 a 30 palavras; não use nomes de pessoas, CPF, e-mail, telefone, "
        "número de matrícula nem valores exatos de documentos; não repita a mesma ideia com outras palavras; "
        "não copie os exemplos.\n"
        f"Exemplos do estilo (não repita): {json.dumps(exemplos, ensure_ascii=False)}\n"
        'Responda só com JSON: {"chamados": ["...", "..."]}.'
    )


class Cache:
    def __init__(self, caminho: str):
        self.caminho = caminho
        self.dados = json.load(open(caminho, encoding="utf-8")) if os.path.exists(caminho) else {}

    def obter(self, chave: str, calcular):
        if chave not in self.dados:
            self.dados[chave] = calcular()
            os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
            tmp = self.caminho + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, ensure_ascii=False)
            os.replace(tmp, self.caminho)
        return self.dados[chave]


def _embeddings(base_url: str, modelo: str, textos: list) -> list:
    import httpx

    vetores = []
    with httpx.Client(timeout=120.0) as c:
        for i in range(0, len(textos), 64):
            r = c.post(f"{base_url.rstrip('/')}/embeddings", json={"model": modelo, "input": textos[i:i + 64]})
            r.raise_for_status()
            vetores += [d["embedding"] for d in sorted(r.json()["data"], key=lambda d: d["index"])]
    return vetores


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", default=os.environ.get("LLM_BASE_URL", "http://127.0.0.1:11434/v1"))
    ap.add_argument("--modelo", default="qwen3.8:27b-ud-iq3_xxs")
    ap.add_argument("--embed-modelo", default="qwen3-embedding:0.6b")
    ap.add_argument("--por-estrato", type=int, default=30)
    ap.add_argument("--rodadas", type=int, default=2, help="pedidos de geração por estrato")
    ap.add_argument("--quantidade", type=int, default=24, help="chamados por pedido")
    ap.add_argument("--limiar-jaccard", type=float, default=0.6)
    ap.add_argument("--limiar-cosseno", type=float, default=0.85)
    ap.add_argument("--temperatura", type=float, default=0.9)
    ap.add_argument("--semente", default="aurora-sintetico-v1")
    ap.add_argument("--cache", default=os.path.join(mb.RAIZ_REPO, "rascunho-local", "p04-geracao", "cache.json"))
    ap.add_argument("--fase", choices=("gerar", "classificar", "montar", "tudo"), default="tudo")
    args = ap.parse_args(argv)

    originais = [e for e in qr.carregar_jsonl(DADOS) if e.get("origem", "manual") == "manual"]
    cache = Cache(args.cache)
    cliente = ClienteChatOpenAI(args.base_url, args.modelo, reasoning_effort="none", timeout_s=300.0)

    candidatos = []  # (fatia, categoria, texto)
    for fatia in FATIAS:
        for categoria, (_, subtemas) in CATEGORIAS.items():
            exemplos = [e["texto"] for e in originais if (e["fatia"], e["categoria"]) == (fatia, categoria)]
            for r in range(args.rodadas):
                metade = subtemas[r::args.rodadas]
                chave = f"gerar|{args.modelo}|{fatia}|{categoria}|{r}|{args.quantidade}"
                if args.fase in ("classificar", "montar") and chave not in cache.dados:
                    print("FALHA geração incompleta; rode --fase gerar")
                    return 2

                def gerar(f=fatia, c=categoria, m=metade, x=exemplos):
                    resp = cliente.completar_chat(
                        [{"role": "user", "content": prompt_geracao(f, c, m, args.quantidade, x)}],
                        response_format=ESQUEMA, temperatura=args.temperatura, max_tokens=2500)
                    return json.loads(resp.conteudo).get("chamados", [])
                for t in cache.obter(chave, gerar):
                    candidatos.append((fatia, categoria, " ".join(str(t).split())))
            print(f"gerado {fatia}/{categoria}", flush=True)
    if args.fase == "gerar":
        return 0

    descartes = Counter()
    filtrados = []
    for fatia, categoria, texto in candidatos:
        palavras = len(texto.split())
        if not 3 <= palavras <= 40:
            descartes["tamanho"] += 1
        elif detectar_pii(texto):
            descartes["pii"] += 1
        else:
            filtrados.append((fatia, categoria, texto))
    mantidos, desc = ds.deduplicar([t for _, _, t in filtrados], args.limiar_jaccard,
                                   existentes=[e["texto"] for e in originais])
    descartes.update(d["motivo"] for d in desc)
    filtrados = [filtrados[i] for i in mantidos]

    concordancia = Counter()
    rotulados = []
    for fatia, categoria, texto in filtrados:
        chave = f"classe|{args.modelo}|{texto}"
        if args.fase == "montar" and chave not in cache.dados:
            print("FALHA classificação incompleta; rode --fase classificar")
            return 2

        def classificar(t=texto):
            resp = cliente.completar_chat([{"role": "system", "content": qr.SISTEMA}, {"role": "user", "content": t}],
                                          response_format=ESQUEMA_CLASSE, temperatura=0.0, max_tokens=32)
            return qr.extrair_categoria(resp.conteudo)[0]
        previsto = cache.obter(chave, classificar)
        concordancia[(categoria, previsto == categoria)] += 1
        if previsto == categoria:
            rotulados.append((fatia, categoria, texto))
        else:
            descartes["rotulo_divergente"] += 1
    if args.fase == "classificar":
        print(json.dumps({"filtrados": len(filtrados), "concordantes": len(rotulados)}, ensure_ascii=False))
        return 0

    escolhidos = []
    for fatia in FATIAS:
        for categoria in CATEGORIAS:
            ja = sum(1 for e in originais if (e["fatia"], e["categoria"]) == (fatia, categoria))
            pool = sorted((t for f, c, t in rotulados if (f, c) == (fatia, categoria)),
                          key=lambda t: hashlib.sha256((args.semente + t).encode()).hexdigest())
            falta = args.por_estrato - ja
            if len(pool) < falta:
                print(f"FALHA {fatia}/{categoria}: {len(pool)} candidatos para {falta} vagas; aumente --rodadas")
                return 2
            escolhidos += [(fatia, categoria, t) for t in pool[:falta]]

    exemplos = [dict(e) for e in originais]
    for e in exemplos:
        e["origem"] = "manual"
    proximo = len(exemplos) + 1
    for fatia, categoria, texto in escolhidos:
        exemplos.append({"id": f"c{proximo:03d}", "fatia": fatia, "categoria": categoria, "texto": texto,
                         "origem": "sintetico-llm"})
        proximo += 1
    vetores = _embeddings(args.base_url, args.embed_modelo, [e["texto"] for e in exemplos])
    rotulos = ds.agrupar(len(exemplos), lambda i, j: ds.cosseno(vetores[i], vetores[j]), args.limiar_cosseno)
    for e, r in zip(exemplos, rotulos):
        e["grupo"] = exemplos[r]["id"]
    tamanhos = Counter(Counter(rotulos).values())

    with open(DADOS, "w", encoding="utf-8") as f:
        for e in exemplos:
            f.write(json.dumps({k: e[k] for k in ("id", "fatia", "categoria", "texto", "origem", "grupo")},
                               ensure_ascii=False) + "\n")
    manifesto = {
        "gerador": args.modelo, "embeddings": args.embed_modelo, "temperatura": args.temperatura,
        "rodadas_por_estrato": args.rodadas, "quantidade_por_pedido": args.quantidade,
        "limiar_jaccard": args.limiar_jaccard, "limiar_cosseno": args.limiar_cosseno, "semente": args.semente,
        "sha256_prompt_exemplo": mb.sha256_texto(prompt_geracao("formal", "financeiro", ["x"], 1, [])),
        "candidatos": len(candidatos), "descartes": dict(descartes),
        "concordancia_rotulo": {f"{c}|{'sim' if ok else 'nao'}": n for (c, ok), n in sorted(concordancia.items())},
        "total": len(exemplos), "originais": len(originais), "sinteticos": len(escolhidos),
        "grupos_por_tamanho": dict(sorted(tamanhos.items())), "sha256_dados": mb.sha256_arquivo(DADOS),
    }
    print(json.dumps(manifesto, ensure_ascii=False, indent=2))
    print("registro:", mb.registrar_execucao("p04-geracao-sintetica", manifesto))
    return 0


if __name__ == "__main__":
    sys.exit(main())
