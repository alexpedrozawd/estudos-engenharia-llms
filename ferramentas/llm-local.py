"""Cliente mínimo do Ollama local para tarefas estreitas e verificáveis (uma chamada, sem ferramentas).

Uso (Python com -I, só biblioteca padrão):
    python -I llm-local.py ping [--modelo M]       # lista modelos carregados e VRAM, sem inferência
    python -I llm-local.py descarregar --modelo M  # keep_alive 0: libera a GPU deste modelo

Regras fixas (não configuráveis por variável de ambiente):
- fala só com http://127.0.0.1:11434; OLLAMA_HOST é ignorado;
- uma chamada = uma resposta JSON validada por esquema; sem acesso a arquivos, shell ou rede pelo modelo;
- recusa rodar se a VRAM usada por OUTROS processos passar do limite (GPU compartilhada com o desktop);
- registra tag, tokens, tempos e tarefa em rascunho-local/chamadas.jsonl (fora do Git); não grava o texto dos prompts;
- temperatura 0 e semente fixa; `think` desligado (Qwen) e `format` com esquema (Gemma responde vazio sem formato).
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
BASE = "http://127.0.0.1:11434"
LOG = os.path.join(RAIZ, "rascunho-local", "chamadas.jsonl")
LIMITE_OUTROS_MB = 4096


class GpuOcupada(RuntimeError):
    pass


def _get(caminho, tempo=10):
    with urllib.request.urlopen(BASE + caminho, timeout=tempo) as r:
        return json.loads(r.read())


def vram_usada_mb():
    r = subprocess.run(["rocm-smi", "--showmeminfo", "vram"], capture_output=True, text=True, timeout=15)
    m = re.search(r"Total Used Memory \(B\):\s*(\d+)", r.stdout)
    return int(m.group(1)) // (1024 * 1024) if m else None


def modelos_carregados():
    return _get("/api/ps").get("models", [])


def outros_mb():
    """VRAM usada por processos que não são modelos do próprio Ollama (desktop, Transcritor etc.)."""
    usada = vram_usada_mb()
    if usada is None:
        raise GpuOcupada("não consegui ler a VRAM (rocm-smi); recusando por segurança")
    nossos = sum(m.get("size_vram", 0) for m in modelos_carregados()) // (1024 * 1024)
    return max(0, usada - nossos)


def verificar_gpu(limite=LIMITE_OUTROS_MB):
    o = outros_mb()
    if o > limite:
        raise GpuOcupada(f"outros processos usam {o} MB de VRAM (limite {limite} MB); não vou competir pela GPU")
    return o


def registrar(tarefa, modelo, resp, segundos, extra=None):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    linha = {"quando": datetime.now(timezone.utc).isoformat(timespec="seconds"), "tarefa": tarefa, "modelo": modelo,
             "prompt_tokens": resp.get("prompt_eval_count"), "saida_tokens": resp.get("eval_count"),
             "carga_s": round(resp.get("load_duration", 0) / 1e9, 2), "total_s": round(segundos, 2)}
    linha.update(extra or {})
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")


def chat(modelo, sistema, usuario, esquema, tarefa="sem-nome", num_ctx=8192, num_predict=200, tempo=300,
         manter="10m", checar_gpu=True):
    """Uma chamada. Retorna (objeto_json, info). Levanta GpuOcupada, urllib.error.URLError ou ValueError."""
    if checar_gpu:
        verificar_gpu()
    corpo = {"model": modelo, "stream": False, "think": False, "keep_alive": manter, "format": esquema,
             "options": {"temperature": 0, "seed": 7, "num_ctx": num_ctx, "num_predict": num_predict},
             "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": usuario}]}
    req = urllib.request.Request(BASE + "/api/chat", data=json.dumps(corpo).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=tempo) as r:
        resp = json.loads(r.read())
    seg = time.time() - t0
    texto = (resp.get("message") or {}).get("content", "")
    try:
        obj = json.loads(texto)
    except json.JSONDecodeError as e:
        registrar(tarefa, modelo, resp, seg, {"erro": "json_invalido"})
        raise ValueError(f"resposta não é JSON válido: {texto[:80]!r}") from e
    registrar(tarefa, modelo, resp, seg)
    return obj, {"prompt_tokens": resp.get("prompt_eval_count"), "saida_tokens": resp.get("eval_count"), "segundos": round(seg, 2)}


def descarregar(modelo):
    corpo = {"model": modelo, "keep_alive": 0, "stream": False, "messages": []}
    req = urllib.request.Request(BASE + "/api/chat", data=json.dumps(corpo).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        r.read()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("comando", choices=["ping", "descarregar"])
    p.add_argument("--modelo")
    a = p.parse_args()
    if a.comando == "descarregar":
        if not a.modelo:
            p.error("--modelo é obrigatório")
        descarregar(a.modelo)
        print(f"OK    {a.modelo} descarregado")
        return 0
    try:
        carregados = [m["name"] for m in modelos_carregados()]
        print(f"OK    Ollama em {BASE}; carregados: {carregados or 'nenhum'}; VRAM usada: {vram_usada_mb()} MB; de outros: {outros_mb()} MB")
        return 0
    except (urllib.error.URLError, GpuOcupada) as e:
        print(f"FALHA {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
