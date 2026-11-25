"""CLI do projeto 04: plano/manifesto, avaliação por fatia (antes/depois), comparação e treino QLoRA.

    # 1) plano + manifesto (sem dependências pesadas)
    .venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py plano --registrar
    # 2) linha de base "antes" em qualquer endpoint OpenAI-compatível (llama-server, vLLM, Ollama)
    .venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py avaliar \
        --base-url http://127.0.0.1:8081/v1 --modelo modelo-local --saida antes.json
    # 3) treino (exige GPU CUDA + extra `finetuning`: torch, transformers, peft, trl, datasets, bitsandbytes)
    .venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py treinar --saida-adaptador adaptador/
    # 4) servir modelo base + adaptador, avaliar de novo ("depois") e aplicar o portão
    .venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py comparar antes.json depois.json
"""
from __future__ import annotations

import argparse
import inspect
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402

import qlora_receita as qr  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados", "chamados_aurora.jsonl")


def _carregar(cfg: qr.ConfigQLoRA):
    exemplos = qr.carregar_jsonl(DADOS)
    return qr.dividir(exemplos, cfg.fracao_teste, cfg.semente_divisao)


def cmd_plano(args, cfg) -> int:
    treino, teste = _carregar(cfg)
    m = qr.manifesto(cfg, DADOS, treino, teste, qr.versoes_instaladas())
    print(json.dumps(m, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p04-qlora-manifesto", m))
    return 0


def cmd_avaliar(args, cfg) -> int:
    from comum.cliente_llm import ClienteHTTPOpenAICompativel

    _, teste = _carregar(cfg)
    cliente = ClienteHTTPOpenAICompativel(modelo=args.modelo, base_url=args.base_url, api_key=os.environ.get("LLM_API_KEY", ""),
                                          provedor="openai-compativel", timeout_s=120.0)
    resultado = qr.avaliar(teste, lambda t: cliente.completar(t, sistema=qr.SISTEMA, temperatura=0.0, max_tokens=32).texto)
    resultado["modelo"] = args.modelo
    with open(args.saida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in resultado.items() if k != "detalhes"}, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p04-qlora-avaliacao", resultado))
    return 0


def cmd_comparar(args, cfg) -> int:
    with open(args.antes, encoding="utf-8") as f:
        antes = json.load(f)
    with open(args.depois, encoding="utf-8") as f:
        depois = json.load(f)
    r = qr.comparar(antes, depois, args.tolerancia)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r["aprovado"] else 2


def _filtrar_kwargs(classe, kwargs):
    """Mantém só parâmetros aceitos pela versão instalada (nomes mudam entre versões do trl)."""
    aceitos = set(inspect.signature(classe).parameters)
    return {k: v for k, v in kwargs.items() if k in aceitos}


def cmd_treinar(args, cfg) -> int:  # pragma: no cover - exige GPU CUDA e dependências pesadas
    try:
        import torch
        from datasets import Dataset
        from peft import LoraConfig
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        from trl import SFTConfig, SFTTrainer
    except ImportError as exc:
        print(f"FALHA dependência ausente ({exc.name}); instale o extra: pip install -e 'laboratorios-mercado[finetuning]'")
        return 3
    if not torch.cuda.is_available():
        print("FALHA QLoRA com bitsandbytes exige GPU CUDA; nada foi treinado.")
        return 3
    treino, teste = _carregar(cfg)
    torch.manual_seed(cfg.semente)
    quant = BitsAndBytesConfig(load_in_4bit=cfg.quant_4bit, bnb_4bit_quant_type=cfg.quant_tipo,
                               bnb_4bit_use_double_quant=cfg.quant_dupla,
                               bnb_4bit_compute_dtype=getattr(torch, cfg.dtype_computo))
    tokenizer = AutoTokenizer.from_pretrained(cfg.modelo_base)
    modelo = AutoModelForCausalLM.from_pretrained(cfg.modelo_base, quantization_config=quant, device_map="auto")
    lora = LoraConfig(r=cfg.lora_r, lora_alpha=cfg.lora_alpha, lora_dropout=cfg.lora_dropout,
                      target_modules=list(cfg.modulos_alvo), task_type="CAUSAL_LM")
    sft_kwargs = _filtrar_kwargs(SFTConfig, {
        "output_dir": args.saida_adaptador, "num_train_epochs": cfg.epocas,
        "per_device_train_batch_size": cfg.lote_por_dispositivo,
        "gradient_accumulation_steps": cfg.acumulacao_gradiente, "learning_rate": cfg.taxa_aprendizado,
        "max_length": cfg.comprimento_max, "max_seq_length": cfg.comprimento_max, "seed": cfg.semente,
        "bf16": cfg.dtype_computo == "bfloat16", "logging_steps": 1, "save_strategy": "no", "report_to": [],
    })
    dados = Dataset.from_list([qr.para_conversa(e) for e in treino])
    treinador = SFTTrainer(**_filtrar_kwargs(SFTTrainer, {
        "model": modelo, "args": SFTConfig(**sft_kwargs), "train_dataset": dados,
        "peft_config": lora, "processing_class": tokenizer, "tokenizer": tokenizer,
    }))
    treinador.train()
    treinador.save_model(args.saida_adaptador)
    m = qr.manifesto(cfg, DADOS, treino, teste, qr.versoes_instaladas())
    with open(os.path.join(args.saida_adaptador, "manifesto.json"), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    print("adaptador salvo em", args.saida_adaptador)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plano")
    p.add_argument("--registrar", action="store_true")
    p = sub.add_parser("avaliar")
    p.add_argument("--base-url", required=True)
    p.add_argument("--modelo", required=True)
    p.add_argument("--saida", required=True)
    p.add_argument("--registrar", action="store_true")
    p = sub.add_parser("comparar")
    p.add_argument("antes")
    p.add_argument("depois")
    p.add_argument("--tolerancia", type=float, default=0.05)
    p = sub.add_parser("treinar")
    p.add_argument("--saida-adaptador", required=True)
    args = ap.parse_args(argv)
    cfg = qr.ConfigQLoRA()
    return {"plano": cmd_plano, "avaliar": cmd_avaliar, "comparar": cmd_comparar, "treinar": cmd_treinar}[args.cmd](args, cfg)


if __name__ == "__main__":
    sys.exit(main())
