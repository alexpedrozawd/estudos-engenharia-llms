"""Receita reproduzível de ajuste fino QLoRA/LoRA (projeto 04), sem dependências pesadas.

Tudo o que decide o resultado fica explícito e com hash no manifesto: dados, divisão
estratificada por (fatia, categoria), formato de conversa, hiperparâmetros de LoRA,
quantização 4 bits (NF4), sementes e versões. A avaliação antes/depois é por fatia, e o
portão reprova o adaptador se alguma fatia piorar além da tolerância, mesmo que a média suba.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Tuple

CATEGORIAS = ("financeiro", "academico", "acesso", "secretaria")
SISTEMA = (
    "Classifique o chamado de um aluno da Aurora Educação (instituição fictícia) em uma categoria: "
    + ", ".join(CATEGORIAS) + '. Responda só com JSON no formato {"categoria": "<categoria>"}.'
)


@dataclass
class ConfigQLoRA:
    modelo_base: str = "Qwen/Qwen3-1.7B"
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    modulos_alvo: Tuple[str, ...] = ("q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj")
    quant_4bit: bool = True
    quant_tipo: str = "nf4"
    quant_dupla: bool = True
    dtype_computo: str = "bfloat16"
    taxa_aprendizado: float = 2e-4
    epocas: int = 3
    lote_por_dispositivo: int = 4
    acumulacao_gradiente: int = 4
    comprimento_max: int = 512
    semente: int = 42
    semente_divisao: str = "aurora-v1"
    fracao_teste: float = 0.34
    extras: Dict[str, object] = field(default_factory=dict)

    def validar(self) -> None:
        if self.lora_r < 1 or self.lora_alpha < 1:
            raise ValueError("lora_r e lora_alpha devem ser >= 1")
        if not 0.0 <= self.lora_dropout < 1.0:
            raise ValueError("lora_dropout fora de [0, 1)")
        if not 0.0 < self.fracao_teste < 1.0:
            raise ValueError("fracao_teste fora de (0, 1)")
        if self.quant_tipo not in ("nf4", "fp4"):
            raise ValueError("quant_tipo deve ser nf4 ou fp4")


def carregar_jsonl(caminho: str) -> List[Dict[str, str]]:
    exemplos = []
    with open(caminho, encoding="utf-8") as f:
        for n, linha in enumerate(f, start=1):
            if not linha.strip():
                continue
            ex = json.loads(linha)
            faltando = {"id", "fatia", "categoria", "texto"} - set(ex)
            if faltando:
                raise ValueError(f"linha {n}: campos ausentes {sorted(faltando)}")
            if ex["categoria"] not in CATEGORIAS:
                raise ValueError(f"linha {n}: categoria inválida {ex['categoria']!r}")
            exemplos.append(ex)
    ids = [e["id"] for e in exemplos]
    if len(ids) != len(set(ids)):
        raise ValueError("ids duplicados")
    return exemplos


def dividir(exemplos: Sequence[Dict[str, str]], fracao_teste: float, semente: str) -> Tuple[List[dict], List[dict]]:
    """Divisão estratificada por (fatia, categoria) e ordenada por hash: estável entre máquinas."""
    grupos: Dict[Tuple[str, str], List[dict]] = {}
    for e in exemplos:
        grupos.setdefault((e["fatia"], e["categoria"]), []).append(e)
    treino, teste = [], []
    for chave in sorted(grupos):
        ordem = sorted(grupos[chave], key=lambda e: hashlib.sha256((semente + e["id"]).encode()).hexdigest())
        n_teste = max(1, round(len(ordem) * fracao_teste)) if len(ordem) > 1 else 0
        teste += ordem[:n_teste]
        treino += ordem[n_teste:]
    return sorted(treino, key=lambda e: e["id"]), sorted(teste, key=lambda e: e["id"])


def para_conversa(ex: Dict[str, str]) -> Dict[str, List[Dict[str, str]]]:
    """Formato conversacional aceito pelo SFT do `trl` (`{"messages": [...]}`)."""
    return {"messages": [
        {"role": "system", "content": SISTEMA},
        {"role": "user", "content": ex["texto"]},
        {"role": "assistant", "content": json.dumps({"categoria": ex["categoria"]}, ensure_ascii=False)},
    ]}


def extrair_categoria(texto: str) -> Tuple[Optional[str], bool]:
    """Devolve (categoria, formato_valido). Formato válido = JSON com chave `categoria` conhecida."""
    m = re.search(r"\{.*?\}", texto or "", re.S)
    if m:
        try:
            cat = json.loads(m.group()).get("categoria")
            if cat in CATEGORIAS:
                return cat, True
        except (json.JSONDecodeError, AttributeError):
            pass
    achadas = [c for c in CATEGORIAS if c in (texto or "").lower()]
    return (achadas[0] if len(achadas) == 1 else None), False


def avaliar(teste: Sequence[Dict[str, str]], prever: Callable[[str], str]) -> Dict[str, object]:
    por_fatia: Dict[str, Dict[str, float]] = {}
    detalhes = []
    for ex in teste:
        bruto = prever(ex["texto"])
        cat, ok_formato = extrair_categoria(bruto)
        acerto = cat == ex["categoria"]
        f = por_fatia.setdefault(ex["fatia"], {"n": 0, "acertos": 0, "formato_valido": 0})
        f["n"] += 1
        f["acertos"] += int(acerto)
        f["formato_valido"] += int(ok_formato)
        detalhes.append({"id": ex["id"], "esperado": ex["categoria"], "previsto": cat, "formato_valido": ok_formato})
    for f in por_fatia.values():
        f["acuracia"] = round(f["acertos"] / f["n"], 4)
        f["taxa_formato"] = round(f["formato_valido"] / f["n"], 4)
    n = max(len(teste), 1)
    return {
        "n": len(teste),
        "acuracia": round(sum(f["acertos"] for f in por_fatia.values()) / n, 4),
        "taxa_formato": round(sum(f["formato_valido"] for f in por_fatia.values()) / n, 4),
        "por_fatia": dict(sorted(por_fatia.items())),
        "detalhes": detalhes,
    }


def comparar(antes: Dict[str, object], depois: Dict[str, object], tolerancia: float = 0.05) -> Dict[str, object]:
    """Portão de promoção: média melhora e nenhuma fatia cai mais que `tolerancia`."""
    deltas, regressoes = {}, []
    for fatia, a in antes["por_fatia"].items():
        d = depois["por_fatia"].get(fatia)
        if d is None:
            regressoes.append(f"{fatia}: ausente na avaliação posterior")
            continue
        delta = round(d["acuracia"] - a["acuracia"], 4)
        deltas[fatia] = delta
        if delta < -tolerancia:
            regressoes.append(f"{fatia}: {a['acuracia']:.2f} -> {d['acuracia']:.2f}")
    melhora = round(depois["acuracia"] - antes["acuracia"], 4)
    return {"delta_global": melhora, "delta_por_fatia": deltas, "regressoes": regressoes,
            "aprovado": melhora > 0 and not regressoes, "tolerancia": tolerancia}


def sha_json(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def manifesto(cfg: ConfigQLoRA, caminho_dados: str, treino: Sequence[dict], teste: Sequence[dict],
              versoes: Optional[Dict[str, str]] = None) -> Dict[str, object]:
    cfg.validar()
    with open(caminho_dados, "rb") as f:
        sha_dados = hashlib.sha256(f.read()).hexdigest()
    conf = asdict(cfg)
    conf["modulos_alvo"] = list(cfg.modulos_alvo)
    return {
        "configuracao": conf,
        "sha256_configuracao": sha_json(conf),
        "sha256_dados": sha_dados,
        "ids_treino": [e["id"] for e in treino],
        "ids_teste": [e["id"] for e in teste],
        "sha256_divisao": sha_json({"treino": [e["id"] for e in treino], "teste": [e["id"] for e in teste]}),
        "sha256_formato_conversa": sha_json(para_conversa({"texto": "<x>", "categoria": CATEGORIAS[0]})),
        "versoes": dict(sorted((versoes or {}).items())),
    }


def versoes_instaladas(pacotes: Sequence[str] = ("torch", "transformers", "peft", "trl", "datasets",
                                                  "bitsandbytes", "accelerate")) -> Dict[str, str]:
    from importlib import metadata

    saida = {}
    for p in pacotes:
        try:
            saida[p] = metadata.version(p)
        except metadata.PackageNotFoundError:
            saida[p] = "ausente"
    return saida
