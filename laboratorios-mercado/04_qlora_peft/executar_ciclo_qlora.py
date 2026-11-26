"""Ciclo completo e sem intervenção manual do projeto 04 (Etapa 3): épocas escolhidas na validação,
teste avaliado uma vez e portão estatístico (Wilson 95% + McNemar exato com acertos por caso).

1. treina um adaptador por candidato de `--epocas` e avalia cada um no conjunto de validação;
2. escolhe a maior acurácia de validação (empate: menos épocas, o modelo mais simples);
3. avalia no teste só o modelo base e o adaptador escolhido, aplica `comparar` e registra tudo.

Cada passo grava seu JSON em `--pasta` (fora do Git); rodar de novo pula o que já existe.
Exige GPU (container `qlora-rocm` ou ambiente CUDA):

    python -I laboratorios-mercado/04_qlora_peft/executar_ciclo_qlora.py --epocas 1,3,6
Código de saída: 0 se o portão aprovar; 2 se reprovar ou ficar inconclusivo; 3 se a pasta for de outros dados.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.dirname(AQUI))
import mercado_base as mb  # noqa: E402

import qlora_receita as qr  # noqa: E402
import treinar_qlora as tq  # noqa: E402


def _ler(caminho: str) -> dict:
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


def escolher_epocas(validacoes: dict) -> int:
    """Maior acurácia de validação; empate fica com menos épocas."""
    return min(validacoes, key=lambda e: (-float(validacoes[e]["acuracia"]), e))


def _resumo(r: dict) -> dict:
    n = int(r["n"])
    return {"n": n, "acuracia": r["acuracia"], "taxa_formato": r["taxa_formato"],
            "wilson95": qr.wilson(round(float(r["acuracia"]) * n), n),
            "por_fatia": {f: v["acuracia"] for f, v in r["por_fatia"].items()}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--epocas", default="1,3,6")
    ap.add_argument("--fracao-validacao", default="0.2")
    ap.add_argument("--modelo", default=qr.ConfigQLoRA().modelo_base)
    ap.add_argument("--pasta", default=os.path.join(mb.RAIZ_REPO, "rascunho-local", "p04-ciclo"))
    ap.add_argument("--sem-registro", action="store_true")
    args = ap.parse_args(argv)
    candidatos = sorted({int(x) for x in args.epocas.split(",") if x.strip()})
    os.makedirs(args.pasta, exist_ok=True)
    base = ["--fracao-validacao", args.fracao_validacao]
    # Retomar só com os mesmos dados, modelo e fração; senão os JSON antigos se misturariam ao registro novo.
    impressao = json.dumps({"sha256_dados": mb.sha256_arquivo(tq.DADOS), "modelo": args.modelo,
                            "fracao_validacao": args.fracao_validacao}, sort_keys=True)
    marca = os.path.join(args.pasta, "impressao.json")
    if os.path.exists(marca):
        with open(marca, encoding="utf-8") as f:
            if f.read() != impressao:
                print(f"FALHA {args.pasta} tem passos de outros dados ou configuração; use outra --pasta ou apague-a")
                return 3
    else:
        with open(marca, "w", encoding="utf-8") as f:
            f.write(impressao)

    def passo(saida: str, argv_passo: list) -> dict:
        if not os.path.exists(saida):
            codigo = tq.main(base + argv_passo)
            if codigo != 0 or not os.path.exists(saida):
                raise SystemExit(f"FALHA passo {argv_passo[0]} terminou com código {codigo}")
        return _ler(saida)

    def adaptador(e: int) -> str:
        pasta = os.path.join(args.pasta, f"adaptador-ep{e}")
        passo(os.path.join(pasta, "manifesto.json"), ["treinar", "--epocas", str(e), "--saida-adaptador", pasta])
        return pasta

    val_base = passo(os.path.join(args.pasta, "val-base.json"),
                     ["avaliar", "--backend", "hf", "--modelo", args.modelo, "--conjunto", "validacao",
                      "--saida", os.path.join(args.pasta, "val-base.json")])
    validacoes = {}
    for e in candidatos:
        saida = os.path.join(args.pasta, f"val-ep{e}.json")
        validacoes[e] = passo(saida, ["avaliar", "--backend", "hf", "--modelo", args.modelo, "--adaptador",
                                      adaptador(e), "--conjunto", "validacao", "--saida", saida])
    escolha = escolher_epocas(validacoes)
    teste_base = passo(os.path.join(args.pasta, "teste-base.json"),
                       ["avaliar", "--backend", "hf", "--modelo", args.modelo, "--conjunto", "teste",
                        "--saida", os.path.join(args.pasta, "teste-base.json")])
    saida_teste = os.path.join(args.pasta, f"teste-ep{escolha}.json")
    teste_escolhido = passo(saida_teste, ["avaliar", "--backend", "hf", "--modelo", args.modelo, "--adaptador",
                                          adaptador(escolha), "--conjunto", "teste", "--saida", saida_teste])
    portao = qr.comparar(teste_base, teste_escolhido)
    manifesto = _ler(os.path.join(args.pasta, f"adaptador-ep{escolha}", "manifesto.json"))
    registro = {
        "modelo_base": args.modelo, "fracao_validacao": float(args.fracao_validacao),
        "epocas_candidatas": candidatos, "epocas_escolhidas": escolha,
        "criterio": "maior acurácia de validação; empate fica com menos épocas; teste avaliado uma vez",
        "validacao": {"base": _resumo(val_base), **{f"ep{e}": _resumo(v) for e, v in validacoes.items()}},
        "teste": {"base": _resumo(teste_base), f"ep{escolha}": _resumo(teste_escolhido)},
        "portao": portao,
        "acertos_por_caso": {
            "base": {d["id"]: d["previsto"] == d["esperado"] for d in teste_base["detalhes"]},
            f"ep{escolha}": {d["id"]: d["previsto"] == d["esperado"] for d in teste_escolhido["detalhes"]},
        },
        "acelerador": teste_escolhido.get("acelerador"),
        "sha256_dados": manifesto["sha256_dados"], "sha256_divisao": manifesto["sha256_divisao"],
        "versoes": manifesto["versoes"],
    }
    print(json.dumps({k: v for k, v in registro.items() if k != "acertos_por_caso"}, ensure_ascii=False, indent=2))
    if not args.sem_registro:
        print("registro:", mb.registrar_execucao("p04-qlora-ciclo", registro))
    return 0 if portao["aprovado"] else 2


if __name__ == "__main__":
    sys.exit(main())
