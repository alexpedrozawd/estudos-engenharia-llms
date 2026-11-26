"""Reescreve as perguntas do corpus ampliado sem o prefixo "Sobre <tema>:" (correção de 26/11/2026).

O `gerar_corpus_ampliado.py` punha na frente de cada pergunta o tema usado para escrever o documento.
Isso tira a ambiguidade ("qual a multa?"), mas copia o vocabulário do próprio documento e facilita a
recuperação. Aqui o LLM reescreve cada pergunta como quem usa o atendimento escreveria, citando o assunto
com palavras próprias. Uma reescrita só entra se passar em `checar_reescrita` (determinística) e se o mesmo
LLM, às cegas e com temperatura 0, confirmar que ela pede a mesma informação sobre o mesmo assunto; senão,
há nova tentativa com o motivo da recusa. A pergunta original fica em `pergunta_original` (o P07 usa essa).

Ordem: `gerar_corpus_ampliado.py` → este script. Rodar de novo é idempotente (parte de `pergunta_original`).

    .venv-mercado/bin/python -I laboratorios-mercado/02_rag_producao/reescrever_perguntas.py \
        --base-url http://127.0.0.1:11434/v1 --modelo qwen3.8:27b-ud-iq3_xxs --registrar
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from typing import Optional

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.dirname(AQUI), AQUI]

import mercado_base as mb  # noqa: E402
from mercado_base import dados_sinteticos as ds  # noqa: E402
from mercado_base.cliente_openai import ClienteChatComCache, ClienteChatOpenAI  # noqa: E402
from gerar_corpus_ampliado import TEMAS  # noqa: E402

CONSULTAS = os.path.join(AQUI, "dados", "consultas_ampliadas.json")
TEMA_POR_DOC = {doc: tema for doc, _, _, tema in TEMAS}
VAZIAS = {"para", "pelo", "pela", "pelos", "pelas", "sobre", "como", "entre", "apos", "qual", "quais",
          "quanto", "quantos", "quantas", "quando", "onde", "esta", "este", "isso", "minha", "meus", "minhas"}
QUEM = {"aluno": "um aluno", "docente": "um professor", "coordenacao": "alguem da coordenacao",
        "admin": "um servidor administrativo"}
ESQUEMA = {"type": "json_schema", "json_schema": {"name": "pergunta", "strict": True, "schema": {
    "type": "object", "additionalProperties": False, "required": ["pergunta"],
    "properties": {"pergunta": {"type": "string"}}}}}
ESQUEMA_EQUIVALENCIA = {"type": "json_schema", "json_schema": {"name": "equivalencia", "strict": True, "schema": {
    "type": "object", "additionalProperties": False, "required": ["equivalente"],
    "properties": {"equivalente": {"type": "boolean"}}}}}
MAX_TENTATIVAS = 6


def palavras_de_conteudo(texto: str) -> set:
    return {p for p in ds.normalizar(texto).split() if len(p) >= 4 and p not in VAZIAS}


def separar_prefixo(pergunta: str, tema: str) -> str:
    """Tira "Sobre <tema>: " (o tema exato do gerador; alguns têm dois-pontos) e devolve o resto."""
    prefixo = f"Sobre {tema}: "
    if not pergunta.startswith(prefixo):
        raise ValueError(f"pergunta sem o prefixo {prefixo!r}: {pergunta!r}")
    return pergunta[len(prefixo):]


def ler_json(conteudo: str, campo: str):
    try:
        return json.loads(conteudo).get(campo)
    except (ValueError, AttributeError):
        return None


def checar_reescrita(nova: str, tema: str, resposta_curta: str, trecho: str) -> Optional[str]:
    """Devolve o motivo da recusa, ou None se a reescrita serve."""
    n = ds.normalizar(nova)
    if not 4 <= len(n.split()) <= 30:
        return "tamanho fora de 4 a 30 palavras"
    if not nova.rstrip().endswith("?"):
        return "não termina com ponto de interrogação"
    if ds.normalizar(tema) in n:
        return "repete a expressão do tema"
    do_tema = palavras_de_conteudo(tema)
    limite = max(1, len(do_tema) // 2)
    if len(do_tema & palavras_de_conteudo(nova)) > limite:
        return f"repete mais de {limite} palavra(s) do tema"
    if ds.normalizar(resposta_curta) in n:
        return "contém a resposta"
    if ds.normalizar(trecho) in n:
        return "copia o trecho que responde"
    return None


def prompt_reescrita(resto: str, tema: str, quem: str, motivo: str = "", anterior: str = "") -> str:
    texto = (
        f"Voce e {quem} da Aurora Educacao (faculdade ficticia) escrevendo no chat de atendimento. "
        "Reescreva a pergunta abaixo do jeito que voce digitaria, numa frase so, terminando com '?'. "
        "Ela deve pedir exatamente a mesma informacao e deixar claro de que assunto se trata, "
        f"mas com palavras suas: nao use a expressao \"{tema}\" nem repita a maior parte das palavras dela, "
        "e nao escreva a resposta. Pode usar nomes curtos que a comunidade usa (como RU, TCC, EAD ou ouvidoria).\n"
        f"Assunto: {tema}\nPergunta: {resto}\n"
    )
    if motivo:
        texto += f"Uma tentativa anterior foi recusada porque {motivo}. Escreva de outro jeito.\n"
    if anterior:
        texto += (
            f"Nao repita formulacao ja recusada: {anterior}. "
            "(Se precisar para nao mudar o sentido, voce pode usar uma unica palavra-chave do assunto.)\n"
        )
    return texto + 'Responda so com JSON: {"pergunta": "..."}'


def prompt_equivalencia(original: str, nova: str) -> str:
    return (
        "Duas perguntas enviadas ao atendimento da Aurora Educacao (faculdade ficticia).\n"
        f"A: {original}\nB: {nova}\n"
        "B pede a mesma informacao que A, sobre o mesmo assunto, de modo que a mesma resposta serve para as duas "
        "e quem le B entende de que servico ou regra se trata? "
        'Responda so com JSON: {"equivalente": true} ou {"equivalente": false}.'
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base-url", default=os.environ.get("LLM_BASE_URL", "http://127.0.0.1:11434/v1"))
    ap.add_argument("--modelo", default="qwen3.8:27b-ud-iq3_xxs")
    ap.add_argument("--temperatura", type=float, default=0.7)
    ap.add_argument("--cache", default=os.path.join(mb.RAIZ_REPO, "rascunho-local", "p02-reescrita", "cache.json"))
    ap.add_argument("--registrar", action="store_true")
    args = ap.parse_args(argv)

    with open(CONSULTAS, encoding="utf-8") as f:
        consultas = json.load(f)
    cliente = ClienteChatComCache(
        ClienteChatOpenAI(args.base_url, args.modelo, reasoning_effort="none", timeout_s=300.0), args.cache)
    tentativas, motivos, falhas, sobreposicao = Counter(), Counter(), [], []
    for q in consultas:
        original = q.get("pergunta_original", q["pergunta"])
        crit = q["relevantes"][0]
        tema = TEMA_POR_DOC[crit["doc"]]
        resto = separar_prefixo(original, tema)
        perfil = q.get("filtro", {}).get("perfil", "aluno")
        motivo, nova, rejeitadas = "", None, []
        for i in range(1, MAX_TENTATIVAS + 1):
            anterior = "; ".join(rejeitadas) if i >= 3 else ""
            r = cliente.completar_chat(
                [{"role": "user", "content": prompt_reescrita(resto, tema, QUEM.get(perfil, "um aluno"), motivo, anterior)}],
                response_format=ESQUEMA, temperatura=args.temperatura, max_tokens=200)
            # JSON inválido vira recusa com motivo: o prompt seguinte muda, e o cache não repete o erro.
            candidata = " ".join(str(ler_json(r.conteudo, "pergunta") or "").split())
            motivo = checar_reescrita(candidata, tema, q["resposta_esperada_contem"][0], crit["contem"]) or ""
            if not motivo:
                v = cliente.completar_chat([{"role": "user", "content": prompt_equivalencia(original, candidata)}],
                                           response_format=ESQUEMA_EQUIVALENCIA, temperatura=0.0, max_tokens=50)
                if ler_json(v.conteudo, "equivalente") is not True:
                    motivo = "mudou o sentido ou deixou o assunto pouco claro"
            if not motivo:
                nova = candidata
                tentativas[i] += 1
                break
            rejeitadas.append(candidata or "(vazio)")
            motivos[motivo] += 1
        if nova is None:
            falhas.append(q["id"])
            continue
        do_tema = palavras_de_conteudo(tema)
        sobreposicao.append(len(do_tema & palavras_de_conteudo(nova)) / max(1, len(do_tema)))
        q["pergunta_original"], q["pergunta"] = original, nova
    if falhas:
        print("FALHA sem reescrita válida:", ", ".join(falhas))
        return 2
    with open(CONSULTAS + ".tmp", "w", encoding="utf-8") as f:
        json.dump(consultas, f, ensure_ascii=False, indent=1)
    os.replace(CONSULTAS + ".tmp", CONSULTAS)
    resumo = {"modelo": args.modelo, "temperatura": args.temperatura, "perguntas": len(consultas),
              "aceitas_na_tentativa": {str(k): v for k, v in sorted(tentativas.items())},
              "recusas_por_motivo": dict(motivos),
              "sobreposicao_media_com_o_tema": {"antes": 1.0,
                                                "depois": round(sum(sobreposicao) / len(sobreposicao), 4)},
              "cache_llm": {"reaproveitadas": cliente.acertos_cache, "chamadas_reais": cliente.chamadas_reais},
              "sha256_prompt_exemplo": mb.sha256_texto(prompt_reescrita("x", "y", "um aluno")),
              "sha256_prompt_equivalencia": mb.sha256_texto(prompt_equivalencia("x", "y"))}
    print(json.dumps(resumo, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p02-reescrita-perguntas", resumo))
    return 0


if __name__ == "__main__":
    sys.exit(main())
