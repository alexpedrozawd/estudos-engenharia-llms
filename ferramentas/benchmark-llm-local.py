"""Teste do LLM local na triagem de trechos de fonte (gabarito = trechos já conferidos dos pacotes).

Tarefa: dada uma afirmação do guia, o script lexical (busca por palavras) separa 10 trechos candidatos da fonte;
o LLM local só ESCOLHE até 3 números (nunca escreve texto) ou diz `sem_suporte`. A fronteira passa a ler só os
trechos escolhidos. Como o modelo não escreve citação, não há citação inventada: o risco é escolher o trecho errado
ou aceitar o que a fonte não sustenta.

Limites fixados ANTES de medir (aprovados pelo operador em 19/11/2026):
  G1  acerto@3 do local >= acerto@3 do script lexical (os mesmos casos);
  G2  falso aceite <= 5% nos controles negativos (afirmação sem suporte na fonte sorteada);
  G3  bytes que a fronteira lê <= 50% dos bytes dos 10 candidatos do script.
Aprovado só se G1, G2 e G3 passarem. Reprovado: a tarefa fica no script/fronteira.

Uso (Python com -I, só biblioteca padrão; exige cache-fontes/textos e o Ollama local):
    python -I benchmark-llm-local.py rodar --modelo TAG [--tempo-total 520] [--limite N]
    python -I benchmark-llm-local.py resumir
Resultados brutos: rascunho-local/benchmark/<modelo>.jsonl (fora do Git); retoma de onde parou.
"""
import argparse
import glob
import importlib.util
import json
import math
import os
import re
import sys
import time
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
TEXTOS = os.path.join(RAIZ, "cache-fontes", "textos")
SAIDA = os.path.join(RAIZ, "rascunho-local", "benchmark")
CASOS = os.path.join(AQUI, "casos-llm-local.json")
K_CAND, K_ESC, ALVO, PASSO, MAX_CHUNK_PROMPT = 10, 3, 500, 250, 600

ESQUEMA = {"type": "object", "properties": {"selecionados": {"type": "array", "items": {"type": "integer"}, "maxItems": K_ESC},
                                             "sem_suporte": {"type": "boolean"}}, "required": ["selecionados", "sem_suporte"]}
SISTEMA = ("Você ajuda a conferir fontes públicas. Responda somente em JSON. Você NÃO escreve nem altera trechos: "
           "apenas indica os números dos trechos que sustentam diretamente a afirmação.")


def carregar(nome, arquivo):
    s = importlib.util.spec_from_file_location(nome, os.path.join(AQUI, arquivo))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def palavras(t):
    return {w for w in re.findall(r"\w+", sem_acento(t)) if len(w) > 2}


def fazer_chunks(texto, alvo=ALVO, passo=PASSO):
    """Janelas de ~alvo caracteres sobre linhas não vazias, avançando ~passo (sobreposição de 50%)."""
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    chunks, i = [], 0
    while i < len(linhas):
        acc, j = 0, i
        while j < len(linhas) and acc < alvo:
            acc += len(linhas[j]) + 1
            j += 1
        chunks.append(" ".join(linhas[i:j]))
        adv, k = 0, i
        while k < j and adv < passo:
            adv += len(linhas[k]) + 1
            k += 1
        i = max(k, i + 1)
    return chunks


def cobre(gold, chunk, limiar=0.8):
    g = palavras(gold)
    return bool(g) and len(g & palavras(chunk)) / len(g) >= limiar


def ranking_lexico(chunks, kw, k):
    termos = palavras(kw)
    pont = sorted(((len(termos & palavras(c)), -i, i) for i, c in enumerate(chunks)), reverse=True)
    escolhidos = []
    for score, _, i in pont:
        if score == 0:
            break
        if all(abs(i - j) >= 2 for j in escolhidos):
            escolhidos.append(i)
        if len(escolhidos) == k:
            break
    return escolhidos


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def prompt(afirmacao, trechos):
    corpo = "\n".join(f"[{i}] {t[:MAX_CHUNK_PROMPT]}" for i, t in enumerate(trechos))
    return (f"Afirmação (português): {afirmacao}\n\nTrechos da fonte (inglês), numerados:\n{corpo}\n\n"
            f"Escolha até {K_ESC} trechos que SUSTENTAM DIRETAMENTE a afirmação, do mais ao menos relevante. "
            "Se nenhum sustentar, responda sem_suporte=true e selecionados vazio.")


def montar_casos():
    ct = carregar("ct", "conferir-trechos.py")
    fo = carregar("fo", "fontes.py")
    ouro = {}
    for p in fo.pacotes_padrao():
        if fo.manifesto([p]):
            for _, _, c in ct.ler_pacote(p):
                ouro[c[0]] = {"fonte": c[3], "trecho": c[7]}
    base = json.load(open(CASOS, encoding="utf-8"))
    casos = []
    for b in base:
        g = ouro[b["id"]]
        casos.append({"id": b["id"], "tipo": "pos", "afirmacao": b["afirmacao"], "palavras": b["palavras"],
                      "fonte": g["fonte"], "gold": g["trecho"]})
    for i in range(0, len(base), 2):  # 18 controles negativos: afirmação de uma família, fonte de outra
        b, outro = base[i], base[(i + 18) % len(base)]
        casos.append({"id": b["id"] + "~" + outro["id"], "tipo": "neg", "afirmacao": b["afirmacao"], "palavras": b["palavras"],
                      "fonte": ouro[outro["id"]]["fonte"], "gold": None})
    return casos


def rodar_caso(llm, modelo, caso):
    texto = open(os.path.join(TEXTOS, caso["fonte"] + ".txt"), encoding="utf-8", errors="replace").read()
    chunks = fazer_chunks(texto)
    cand = ranking_lexico(chunks, caso["palavras"], K_CAND)
    trechos = [chunks[i] for i in cand]
    r = {"id": caso["id"], "tipo": caso["tipo"], "fonte": caso["fonte"], "n_cand": len(cand), "bytes_fonte": len(texto.encode()),
         "bytes_cand": sum(len(t.encode()) for t in trechos), "bytes_lex3": sum(len(t.encode()) for t in trechos[:K_ESC])}
    if caso["tipo"] == "pos":
        r["teto"] = any(cobre(caso["gold"], t) for t in trechos)
        r["acerto_lex3"] = any(cobre(caso["gold"], t) for t in trechos[:K_ESC])
    if not trechos:
        r.update({"selecionados": [], "sem_suporte": True, "tokens": 0, "segundos": 0, "bytes_local": 0, "acerto_local": False, "falso_aceite": False})
        return r
    obj, info = llm.chat(modelo, SISTEMA, prompt(caso["afirmacao"], trechos), ESQUEMA, tarefa="triagem-trechos")
    sel = [i for i in obj.get("selecionados", []) if isinstance(i, int) and 0 <= i < len(trechos)][:K_ESC]
    r.update({"selecionados": sel, "sem_suporte": bool(obj.get("sem_suporte")), "tokens": (info["prompt_tokens"] or 0) + (info["saida_tokens"] or 0),
              "segundos": info["segundos"], "bytes_local": sum(len(trechos[i].encode()) for i in sel)})
    if caso["tipo"] == "pos":
        r["acerto_local"] = any(cobre(caso["gold"], trechos[i]) for i in sel)
    else:
        r["falso_aceite"] = bool(sel) and not r["sem_suporte"]
    return r


def arquivo_modelo(modelo):
    return os.path.join(SAIDA, re.sub(r"[^A-Za-z0-9._-]", "_", modelo) + ".jsonl")


def cmd_rodar(modelo, tempo_total, limite):
    llm = carregar("llm", "llm-local.py")
    os.makedirs(SAIDA, exist_ok=True)
    caminho = arquivo_modelo(modelo)
    feitos = {json.loads(l)["id"] for l in open(caminho, encoding="utf-8")} if os.path.exists(caminho) else set()
    casos = [c for c in montar_casos() if c["id"] not in feitos]
    if limite:
        casos = casos[:limite]
    t0, n = time.time(), 0
    for c in casos:
        if time.time() - t0 > tempo_total:
            print(f"tempo-total atingido; rode de novo para retomar ({len(casos) - n} casos restantes)")
            return 2
        try:
            r = rodar_caso(llm, modelo, c)
        except Exception as e:
            print(f"FALHA {c['id']}: {str(e)[:120]}")
            return 1
        with open(caminho, "a", encoding="utf-8") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        n += 1
    print(f"OK    {n} casos rodados em {time.time() - t0:.0f}s ({modelo})")
    return 0


def resumo_modelo(caminho):
    linhas = [json.loads(l) for l in open(caminho, encoding="utf-8")]
    pos = [r for r in linhas if r["tipo"] == "pos"]
    neg = [r for r in linhas if r["tipo"] == "neg"]
    n = len(pos)
    loc = sum(r["acerto_local"] for r in pos)
    lex = sum(r["acerto_lex3"] for r in pos)
    teto = sum(r["teto"] for r in pos)
    so_loc = sum(r["acerto_local"] and not r["acerto_lex3"] for r in pos)
    so_lex = sum(r["acerto_lex3"] and not r["acerto_local"] for r in pos)
    fa = sum(r.get("falso_aceite", False) for r in neg)
    rej = sum(r["sem_suporte"] or not r["selecionados"] for r in pos)
    bl = sum(r["bytes_local"] for r in pos + neg) / max(1, len(pos + neg))
    bc = sum(r["bytes_cand"] for r in pos + neg) / max(1, len(pos + neg))
    bf = sum(r["bytes_fonte"] for r in pos + neg) / max(1, len(pos + neg))
    seg = sorted(r["segundos"] for r in linhas)
    mediana = seg[len(seg) // 2] if seg else 0
    w = lambda k, m: "%.0f%% (IC95 %.0f–%.0f%%)" % ((100 * k / m if m else 0), *[100 * x for x in wilson(k, m)])
    g1, g2, g3 = loc >= lex, (fa / len(neg) <= 0.05 if neg else False), bl <= 0.5 * bc
    return {"modelo": os.path.basename(caminho)[:-6], "pos": n, "neg": len(neg), "teto": w(teto, n), "lexical@3": w(lex, n), "local@3": w(loc, n),
            "so_local/so_lexical": f"{so_loc}/{so_lex}", "falso_aceite": f"{fa}/{len(neg)} = " + w(fa, len(neg)), "recusa_indevida_em_pos": w(rej, n),
            "bytes_lidos_local/candidatos/fonte": f"{bl:.0f}/{bc:.0f}/{bf:.0f}", "mediana_s": mediana,
            "G1": g1, "G2": g2, "G3": g3, "veredito": "APROVADO" if (g1 and g2 and g3) else "REPROVADO"}


def cmd_resumir():
    arqs = sorted(glob.glob(os.path.join(SAIDA, "*.jsonl")))
    if not arqs:
        print("nenhum resultado em rascunho-local/benchmark")
        return 1
    for a in arqs:
        print(json.dumps(resumo_modelo(a), ensure_ascii=False, indent=1))
    return 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("comando", choices=["rodar", "resumir"])
    p.add_argument("--modelo")
    p.add_argument("--tempo-total", type=int, default=520)
    p.add_argument("--limite", type=int)
    a = p.parse_args()
    if a.comando == "resumir":
        return cmd_resumir()
    if not a.modelo:
        p.error("--modelo é obrigatório")
    return cmd_rodar(a.modelo, a.tempo_total, a.limite)


if __name__ == "__main__":
    sys.exit(main())
