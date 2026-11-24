"""Fontes públicas sem gastar LLM: manifesto dos pacotes, download controlado, extração, busca e conferência.

Uso (Python com -I, só biblioteca padrão):
    python -I fontes.py manifesto [--pacote P]
    python -I fontes.py baixar   [--pacote P] [--chave K] [--atraso 1.0]    # rede: só https e só domínios do manifesto
    python -I fontes.py importar [--pasta cache-fontes/manuais] [--chave K]  # registra cópias locais autorizadas + extrai
    python -I fontes.py extrair                                              # bruto -> texto (HTML, RFC, MD e PDF via pdftotext)
    python -I fontes.py achar CHAVE "palavras da consulta" [-n 5]            # trechos candidatos com chave:linha
    python -I fontes.py conferir [--pacote P]                                # conferir-trechos.py em cada pacote, saída curta
    python -I fontes.py vigencia [--pacote P] [--dias 30] [--estrito]        # idade e divergência de hash sem tocar na rede

Manifesto = tabelas `Chave | Fonte e endereço | Hash bruto (16)` dos pacotes de fontes do projeto.
Dados baixados e extraídos ficam em cache-fontes/ (fora do Git, ver .gitignore). Nada é enviado ao servidor
além da requisição GET da URL pública: sem cookies, agente de usuário genérico, sem dados do projeto.
Código de saída 1 se houver falha.
"""
import argparse
import glob
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CACHE = os.path.join(RAIZ, "cache-fontes")
BRUTO = os.path.join(CACHE, "bruto")
TEXTOS = os.path.join(CACHE, "textos")
MANUAIS = os.path.join(CACHE, "manuais")
EXTS_MANUAIS = {".html", ".htm", ".pdf", ".md", ".txt"}
AGENTE = "guia-fontes/1.0 (leitura de documentação pública)"
LIMITE_BYTES = 25 * 1024 * 1024
TEMPO = 30

LINHA_MANIFESTO = re.compile(r"^\|\s*`([^`]+)`\s*\|(.*)\|\s*`([0-9a-f]{16})`\s*\|\s*$")
URL = re.compile(r"https?://[^\s|)>\]`]+")


def pacotes_padrao():
    return sorted(glob.glob(os.path.join(RAIZ, "pacote-de-fontes-*.md")))


def manifesto(pacotes=None):
    """Lista de dicts: pacote, chave, url, hash_bruto. Chaves repetidas entre pacotes ficam, uma por pacote."""
    itens = []
    for p in pacotes or pacotes_padrao():
        with open(p, encoding="utf-8") as f:
            for linha in f:
                m = LINHA_MANIFESTO.match(linha.rstrip("\n"))
                if not m:
                    continue
                u = URL.search(m.group(2))
                if u:
                    itens.append({"pacote": os.path.basename(p), "chave": m.group(1), "url": u.group(0).rstrip(".,;"),
                                  "hash_bruto": m.group(3)})
    return itens


def hosts_permitidos(itens):
    return {urllib.parse.urlsplit(i["url"]).hostname for i in itens}


class RedirecionamentoControlado(urllib.request.HTTPRedirectHandler):
    def __init__(self, permitidos, permitir_http_local):
        self.permitidos, self.http_local = permitidos, permitir_http_local

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        ok, motivo = url_permitida(newurl, self.permitidos, self.http_local)
        if not ok:
            raise urllib.error.URLError(f"redirecionamento bloqueado: {motivo}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def url_permitida(url, permitidos, permitir_http_local=False):
    p = urllib.parse.urlsplit(url)
    if p.scheme != "https" and not (permitir_http_local and p.scheme == "http" and p.hostname in ("127.0.0.1", "localhost")):
        return False, f"esquema não permitido ({p.scheme})"
    if p.hostname not in permitidos:
        return False, f"domínio fora da lista do manifesto ({p.hostname})"
    return True, ""


def baixar_url(url, permitidos, permitir_http_local=False, limite=LIMITE_BYTES, tempo=TEMPO):
    """Retorna (bytes, content_type). Levanta ValueError/URLError em qualquer violação."""
    ok, motivo = url_permitida(url, permitidos, permitir_http_local)
    if not ok:
        raise ValueError(motivo)
    abridor = urllib.request.build_opener(RedirecionamentoControlado(permitidos, permitir_http_local))
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE, "Accept": "text/html,text/plain,application/pdf,*/*;q=0.5"})
    with abridor.open(req, timeout=tempo) as r:
        corpo = r.read(limite + 1)
        if len(corpo) > limite:
            raise ValueError(f"resposta acima de {limite} bytes")
        return corpo, (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()


def extensao(url, tipo, corpo):
    caminho = urllib.parse.urlsplit(url).path.lower()
    if corpo[:5] == b"%PDF-" or tipo == "application/pdf" or caminho.endswith(".pdf"):
        return ".pdf"
    if caminho.endswith((".md", ".markdown")) or tipo in ("text/markdown",):
        return ".md"
    if tipo == "text/plain" or caminho.endswith(".txt"):
        return ".txt"
    return ".html"


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def cmd_manifesto(pacote):
    todos = [p for p in pacotes_padrao() if not pacote or os.path.basename(p) == pacote]
    itens = manifesto(todos)
    por_pacote = {}
    for i in itens:
        por_pacote[i["pacote"]] = por_pacote.get(i["pacote"], 0) + 1
    for p, n in por_pacote.items():
        print(f"{n:3} chaves  {p}")
    fora = [os.path.basename(p) for p in todos if os.path.basename(p) not in por_pacote]
    print(f"{len(itens)} entradas, {len({i['chave'] for i in itens})} chaves únicas, {len(hosts_permitidos(itens))} domínios")
    if fora:
        print(f"fora do manifesto (sem tabela com Hash bruto (16)): {', '.join(fora)}")
    return 0 if itens else 1


def carregar_indice(indice_path):
    if not os.path.exists(indice_path):
        return {}
    with open(indice_path, encoding="utf-8") as f:
        return json.load(f)


def salvar_indice(indice_path, indice):
    os.makedirs(os.path.dirname(indice_path), exist_ok=True)
    with open(indice_path, "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=1)


def salvar_bruto(indice, item, ext, corpo, bruto=BRUTO, origem=None):
    """Salva bytes brutos da chave no cache e atualiza o registro no índice."""
    os.makedirs(bruto, exist_ok=True)
    chave = item["chave"]
    for antigo in glob.glob(os.path.join(bruto, chave + ".*")):
        os.remove(antigo)
    with open(os.path.join(bruto, chave + ext), "wb") as f:
        f.write(corpo)
    h = sha16(corpo)
    reg = {
        "url": item["url"],
        "hash": h,
        "bytes": len(corpo),
        "ext": ext,
        "data": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "hash_do_manifesto": item["hash_bruto"],
        "igual_ao_manifesto": h == item["hash_bruto"],
    }
    if origem:
        reg["origem"] = origem
    indice[chave] = reg
    return h, h == item["hash_bruto"]


def cmd_baixar(pacote, chave, atraso, retomar=False):
    itens = manifesto([p for p in pacotes_padrao() if not pacote or os.path.basename(p) == pacote])
    permitidos = hosts_permitidos(itens)
    indice_path = os.path.join(CACHE, "indice.json")
    indice = carregar_indice(indice_path)
    vistos, falhas = set(), 0
    for i in itens:
        if chave and i["chave"] != chave:
            continue
        if i["chave"] in vistos or (retomar and i["chave"] in indice):
            continue
        vistos.add(i["chave"])
        try:
            corpo, tipo = baixar_url(i["url"], permitidos)
        except Exception as e:  # rede, domínio, tamanho: registra e segue
            print(f"FALHA {i['chave']}: {str(e)[:120]}")
            falhas += 1
            continue
        ext = extensao(i["url"], tipo, corpo)
        h, igual = salvar_bruto(indice, i, ext, corpo)
        print(f"OK    {i['chave']} {ext} {len(corpo)} bytes {'(hash igual ao manifesto)' if igual else f'(hash difere do manifesto: {h})'}")
        time.sleep(atraso)
    salvar_indice(indice_path, indice)
    print(f"{len(vistos) - falhas} baixadas, {falhas} falhas")
    return 1 if falhas else 0


def cmd_importar(pasta=None, pacote=None, chave=None, bruto=BRUTO, textos=TEXTOS, indice_path=None, itens=None):
    """Importa cópias locais autorizadas (ex.: salvas pelo navegador) para o cache e extrai textos."""
    origem_dir = pasta or MANUAIS
    if not os.path.isdir(origem_dir):
        print(f"FALHA pasta de importação não encontrada: {origem_dir}")
        return 1
    if itens is None:
        itens = manifesto([p for p in pacotes_padrao() if not pacote or os.path.basename(p) == pacote])
    por_chave, por_url = {}, {}
    for it in itens:
        por_chave.setdefault(it["chave"], it)
        por_url.setdefault(it["url"], []).append(it)
    arquivos = [n for n in sorted(os.listdir(origem_dir))
                if not n.startswith(".") and os.path.isfile(os.path.join(origem_dir, n))]
    if not arquivos:
        print(f"FALHA nenhum arquivo encontrado em {origem_dir}")
        return 1
    chaves_presentes = {os.path.splitext(n)[0] for n in arquivos if os.path.splitext(n)[1].lower() in EXTS_MANUAIS}
    caminho_ind = indice_path or os.path.join(CACHE, "indice.json")
    indice = carregar_indice(caminho_ind)
    importadas, falhas = 0, 0
    for nome in arquivos:
        stem, ext = os.path.splitext(nome)
        ext = ".html" if ext.lower() == ".htm" else ext.lower()
        if ext not in EXTS_MANUAIS:
            print(f"IGNORADO {nome}: extensão não suportada ({ext or 'sem extensão'})")
            continue
        if stem not in por_chave:
            print(f"FALHA {nome}: chave '{stem}' ausente no manifesto")
            falhas += 1
            continue
        caminho = os.path.join(origem_dir, nome)
        if os.path.getsize(caminho) > LIMITE_BYTES:
            print(f"FALHA {nome}: arquivo acima de {LIMITE_BYTES} bytes")
            falhas += 1
            continue
        with open(caminho, "rb") as f:
            corpo = f.read()
        if not corpo:
            print(f"FALHA {nome}: arquivo vazio")
            falhas += 1
            continue
        alvos = [por_chave[stem]]
        for outro in por_url.get(por_chave[stem]["url"], []):
            if outro["chave"] != stem and outro["chave"] not in chaves_presentes and all(a["chave"] != outro["chave"] for a in alvos):
                alvos.append(outro)
        for alvo in alvos:
            if chave and alvo["chave"] != chave:
                continue
            h, igual = salvar_bruto(indice, alvo, ext, corpo, bruto=bruto, origem="manual")
            importadas += 1
            status_h = "(hash igual ao manifesto)" if igual else f"(novo hash: {h}, manifesto: {alvo['hash_bruto']})"
            print(f"OK    {alvo['chave']} <- {nome} ({len(corpo)} bytes) {status_h}")
    salvar_indice(caminho_ind, indice)
    if importadas:
        if cmd_extrair(bruto=bruto, textos=textos) != 0:
            falhas += 1
    print(f"{importadas} chave(s) importada(s), {falhas} falha(s)")
    return 1 if (falhas or not importadas) else 0


def modulo_extrator():
    spec = importlib.util.spec_from_file_location("extrair_texto_web", os.path.join(AQUI, "extrair-texto-web.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def cmd_extrair(bruto=BRUTO, textos=TEXTOS):
    ex = modulo_extrator()
    os.makedirs(textos, exist_ok=True)
    n = falhas = 0
    for caminho in sorted(glob.glob(os.path.join(bruto, "*"))):
        base, ext = os.path.splitext(os.path.basename(caminho))
        destino = os.path.join(textos, base + ".txt")
        if ext == ".pdf":
            r = subprocess.run(["pdftotext", caminho, destino], capture_output=True, text=True)
            if r.returncode != 0:
                print(f"FALHA {base}: pdftotext {r.stderr[:100]}")
                falhas += 1
                continue
        else:
            with open(caminho, encoding="utf-8", errors="replace") as f:
                bruto_txt = f.read()
            texto = ex.de_html(bruto_txt) if ext == ".html" else ex.de_rfc(bruto_txt) if ext == ".txt" else bruto_txt
            with open(destino, "w", encoding="utf-8", newline="\n") as f:
                f.write(texto)
        n += 1
    print(f"{n} textos extraídos, {falhas} falhas")
    return 1 if falhas else 0


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def achar(texto, consulta, n=5, janela=3, largura=420):
    """Candidatos por palavras em comum (busca lexical): janelas de `janela` linhas não vazias."""
    termos = {t for t in re.findall(r"\w+", sem_acento(consulta)) if len(t) > 2}
    linhas = texto.splitlines()
    pontos = []
    for i in range(len(linhas)):
        bloco = " ".join(l.strip() for l in linhas[i:i + janela])
        if not bloco.strip():
            continue
        if not termos & set(re.findall(r"\w+", sem_acento(linhas[i]))):
            continue  # a janela só começa numa linha que contém algum termo: o número de linha aponta o achado
        palavras = set(re.findall(r"\w+", sem_acento(bloco)))
        score = len(termos & palavras)
        pontos.append((score, i + 1, bloco))
    pontos.sort(key=lambda x: (-x[0], x[1]))
    escolhidos, usadas = [], []
    for score, linha, bloco in pontos:
        if any(abs(linha - u) < janela for u in usadas):
            continue
        usadas.append(linha)
        escolhidos.append((score, linha, bloco[:largura]))
        if len(escolhidos) >= n:
            break
    return escolhidos, len(termos)


def cmd_achar(chave, consulta, n):
    caminho = os.path.join(TEXTOS, chave + ".txt")
    if not os.path.exists(caminho):
        print(f"FALHA texto da chave '{chave}' não encontrado em cache-fontes/textos (rode baixar e extrair)")
        return 1
    with open(caminho, encoding="utf-8", errors="replace") as f:
        res, total = achar(f.read(), consulta, n)
    if not res:
        print("nenhum candidato")
        return 1
    for score, linha, bloco in res:
        print(f"{chave}:{linha} [{score}/{total}] {bloco}")
    return 0


def cmd_conferir(pacote):
    falhas = 0
    for p in pacotes_padrao():
        if pacote and os.path.basename(p) != pacote:
            continue
        if not manifesto([p]):
            continue
        r = subprocess.run([sys.executable, "-I", os.path.join(AQUI, "conferir-trechos.py"), "--pacote", p,
                            "--textos", TEXTOS, "--projeto", RAIZ], capture_output=True, text=True, encoding="utf-8")
        saida = r.stdout.splitlines()
        resumo = [l for l in saida if l.startswith("Trechos:")]
        print(("OK    " if r.returncode == 0 else "FALHA ") + os.path.basename(p) + " — " + (resumo[0] if resumo else "sem resumo"))
        for l in [l for l in saida if l.startswith("REPROVADO") and "->" in l][:10]:
            print("   " + l[:170])
        falhas += r.returncode != 0
    return 1 if falhas else 0


def avaliar_vigencia(itens, indice, dias=30, hoje=None):
    """Classifica chaves únicas do manifesto frente ao índice local sem tocar na rede."""
    ref = datetime.strptime(hoje, "%Y-%m-%d").date() if hoje else datetime.now(timezone.utc).date()
    por_chave = {}
    for item in itens:
        por_chave.setdefault(item["chave"], item)
    ausentes, vencidas, divergentes = [], [], []
    atuais = 0
    for chave in sorted(por_chave):
        reg = indice.get(chave)
        if not reg:
            ausentes.append(chave)
            continue
        item = por_chave[chave]
        mesmo_hash = reg.get("hash") == item["hash_bruto"]
        if not mesmo_hash:
            divergentes.append((chave, item["hash_bruto"], reg.get("hash", "-")))
        data_txt = reg.get("data") or ""
        idade = None
        if data_txt:
            try:
                idade = (ref - datetime.strptime(data_txt, "%Y-%m-%d").date()).days
            except ValueError:
                idade = None
        if idade is None or idade > dias:
            vencidas.append((chave, data_txt or "sem data", idade))
        elif mesmo_hash:
            atuais += 1
    return {
        "total": len(por_chave),
        "atuais": atuais,
        "ausentes": ausentes,
        "vencidas": vencidas,
        "divergentes": divergentes,
    }


def cmd_vigencia(pacote=None, dias=30, estrito=False, indice_path=None, hoje=None):
    todos = [p for p in pacotes_padrao() if not pacote or os.path.basename(p) == pacote]
    itens = manifesto(todos)
    if not itens:
        print("FALHA nenhuma entrada no manifesto para avaliar")
        return 1
    caminho_ind = indice_path or os.path.join(CACHE, "indice.json")
    indice = {}
    if os.path.exists(caminho_ind):
        try:
            with open(caminho_ind, encoding="utf-8") as f:
                indice = json.load(f)
        except Exception as e:
            print(f"FALHA índice inválido ({caminho_ind}): {e}")
            return 1
    res = avaliar_vigencia(itens, indice, dias=dias, hoje=hoje)
    print(f"Vigência (janela {dias}d): {res['total']} chaves únicas | {res['atuais']} atuais | "
          f"{len(res['ausentes'])} fora do cache | {len(res['vencidas'])} vencidas | {len(res['divergentes'])} hash divergente")
    if res["ausentes"]:
        print("  ausentes: " + ", ".join(res["ausentes"][:12]) + (f" (+{len(res['ausentes']) - 12})" if len(res["ausentes"]) > 12 else ""))
    if res["vencidas"]:
        amostra = [f"{k} ({d})" for k, d, _ in res["vencidas"][:12]]
        print("  vencidas: " + ", ".join(amostra) + (f" (+{len(res['vencidas']) - 12})" if len(res["vencidas"]) > 12 else ""))
    if res["divergentes"]:
        amostra = [f"{k} ({h1}->{h2})" for k, h1, h2 in res["divergentes"][:12]]
        print("  hash divergente: " + ", ".join(amostra) + (f" (+{len(res['divergentes']) - 12})" if len(res['divergentes']) > 12 else ""))
    tem_pendencia = bool(res["ausentes"] or res["vencidas"] or res["divergentes"])
    return 1 if (estrito and tem_pendencia) else 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("comando", choices=["manifesto", "baixar", "importar", "extrair", "achar", "conferir", "vigencia"])
    p.add_argument("chave_ou_nada", nargs="?")
    p.add_argument("consulta", nargs="?")
    p.add_argument("--pacote")
    p.add_argument("--chave")
    p.add_argument("--pasta", help="importar: pasta com cópias locais autorizadas (padrão: cache-fontes/manuais)")
    p.add_argument("--atraso", type=float, default=1.0)
    p.add_argument("--retomar", action="store_true", help="baixar: pula chaves já presentes no índice")
    p.add_argument("--dias", type=int, default=30, help="vigencia: prazo máximo em dias desde a última coleta")
    p.add_argument("--estrito", action="store_true", help="vigencia: sai com código 1 se houver pendência")
    p.add_argument("-n", type=int, default=5)
    a = p.parse_args()
    if a.comando == "manifesto":
        return cmd_manifesto(a.pacote)
    if a.comando == "baixar":
        return cmd_baixar(a.pacote, a.chave, a.atraso, a.retomar)
    if a.comando == "importar":
        return cmd_importar(a.pasta, a.pacote, a.chave)
    if a.comando == "extrair":
        return cmd_extrair()
    if a.comando == "achar":
        if not (a.chave_ou_nada and a.consulta):
            p.error("achar exige CHAVE e consulta")
        return cmd_achar(a.chave_ou_nada, a.consulta, a.n)
    if a.comando == "vigencia":
        return cmd_vigencia(a.pacote, a.dias, a.estrito)
    return cmd_conferir(a.pacote)


if __name__ == "__main__":
    sys.exit(main())
