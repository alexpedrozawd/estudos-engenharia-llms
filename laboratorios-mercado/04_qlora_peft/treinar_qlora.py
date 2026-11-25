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
from dataclasses import replace

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mercado_base as mb  # noqa: E402

import qlora_receita as qr  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "dados", "chamados_aurora.jsonl")


def _carregar(cfg: qr.ConfigQLoRA):
    exemplos = qr.carregar_jsonl(DADOS)
    return qr.dividir(exemplos, cfg.fracao_teste, cfg.semente_divisao)


def detectar_acelerador(torch_mod) -> dict[str, object]:
    """Identifica GPU NVIDIA CUDA ou AMD ROCm/HIP sem exigir CUDA exclusiva."""
    if not torch_mod.cuda.is_available():
        return {"disponivel": False, "backend": "cpu", "dispositivo": None, "versao_runtime": None}
    versao = getattr(torch_mod, "version", None)
    hip = getattr(versao, "hip", None)
    cuda = getattr(versao, "cuda", None)
    backend = "rocm" if hip else "cuda"
    nome = torch_mod.cuda.get_device_name(0) if hasattr(torch_mod.cuda, "get_device_name") else "gpu"
    return {
        "disponivel": True,
        "backend": backend,
        "dispositivo": str(nome),
        "versao_runtime": hip or cuda,
    }


def _carregar_modelo_hf(modelo_id: str, cfg: qr.ConfigQLoRA, *, usar_quant_4bit: bool):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    acel = detectar_acelerador(torch)
    dtype = getattr(torch, cfg.dtype_computo) if acel["disponivel"] else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(modelo_id)
    if tokenizer.pad_token is None and tokenizer.eos_token is not None:
        tokenizer.pad_token = tokenizer.eos_token

    if usar_quant_4bit and acel["disponivel"]:
        from transformers import BitsAndBytesConfig

        quant = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type=cfg.quant_tipo,
            bnb_4bit_use_double_quant=cfg.quant_dupla,
            bnb_4bit_compute_dtype=dtype,
        )
        modelo = AutoModelForCausalLM.from_pretrained(modelo_id, quantization_config=quant, device_map="auto")
    else:
        sig = inspect.signature(AutoModelForCausalLM.from_pretrained).parameters
        chave_dtype = "dtype" if "dtype" in sig else "torch_dtype"
        kwargs = {chave_dtype: dtype}
        if acel["disponivel"]:
            kwargs["device_map"] = "auto"
        modelo = AutoModelForCausalLM.from_pretrained(modelo_id, **kwargs)
    return torch, tokenizer, modelo, acel


def _renderizar_prompt_hf(tokenizer, texto: str) -> str:
    msgs = [{"role": "system", "content": qr.SISTEMA}, {"role": "user", "content": texto}]
    if hasattr(tokenizer, "apply_chat_template") and getattr(tokenizer, "chat_template", None):
        try:
            return tokenizer.apply_chat_template(
                msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False
            )
        except TypeError:
            return tokenizer.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    return f"{qr.SISTEMA}\n\nUsuário: {texto}\nAssistente:"


def cmd_plano(args, cfg) -> int:
    treino, teste = _carregar(cfg)
    m = qr.manifesto(cfg, DADOS, treino, teste, qr.versoes_instaladas())
    print(json.dumps(m, ensure_ascii=False, indent=2))
    if args.registrar:
        print("registro:", mb.registrar_execucao("p04-qlora-manifesto", m))
    return 0


def cmd_avaliar(args, cfg) -> int:
    _, teste = _carregar(cfg)
    extra_meta: dict[str, object] = {"backend": args.backend}
    if args.backend == "hf":
        try:
            torch, tokenizer, modelo, acel = _carregar_modelo_hf(
                args.modelo, cfg, usar_quant_4bit=not args.sem_quant
            )
            if args.adaptador:
                from peft import PeftModel

                modelo = PeftModel.from_pretrained(modelo, args.adaptador)
        except ImportError as exc:
            print(f"FALHA dependência ausente ({exc.name}); instale o extra: pip install -e 'laboratorios-mercado[finetuning]'")
            return 3
        modelo.eval()
        dispositivo = next(modelo.parameters()).device

        def prever_hf(texto: str) -> str:
            prompt = _renderizar_prompt_hf(tokenizer, texto)
            entradas = tokenizer(prompt, return_tensors="pt").to(dispositivo)
            with torch.no_grad():
                gerados = modelo.generate(
                    **entradas,
                    max_new_tokens=48,
                    do_sample=False,
                    pad_token_id=tokenizer.pad_token_id,
                )
            novos = gerados[0][entradas["input_ids"].shape[1]:]
            return tokenizer.decode(novos, skip_special_tokens=True)

        resultado = qr.avaliar(teste, prever_hf)
        extra_meta["adaptador"] = args.adaptador
        extra_meta["acelerador"] = acel
    else:
        if not args.base_url:
            print("FALHA --base-url é obrigatório quando --backend=http")
            return 2
        from comum.cliente_llm import ClienteHTTPOpenAICompativel

        cliente = ClienteHTTPOpenAICompativel(
            modelo=args.modelo,
            base_url=args.base_url,
            api_key=os.environ.get("LLM_API_KEY", ""),
            provedor="openai-compativel",
            timeout_s=120.0,
        )
        resultado = qr.avaliar(
            teste,
            lambda t: cliente.completar(t, sistema=qr.SISTEMA, temperatura=0.0, max_tokens=32).texto,
        )

    resultado["modelo"] = args.modelo
    resultado.update(extra_meta)
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


def cmd_treinar(args, cfg) -> int:  # pragma: no cover - exige GPU (CUDA ou AMD ROCm) e dependências pesadas
    cfg_efetiva = replace(
        cfg,
        modelo_base=args.modelo_base or cfg.modelo_base,
        quant_4bit=not args.sem_quant,
        epocas=args.epocas if args.epocas is not None else cfg.epocas,
    )
    try:
        import torch
        from datasets import Dataset
        from peft import LoraConfig
        from trl import SFTConfig, SFTTrainer
        if cfg_efetiva.quant_4bit:
            import bitsandbytes  # noqa: F401
    except ImportError as exc:
        print(f"FALHA dependência ausente ({exc.name}); instale o extra: pip install -e 'laboratorios-mercado[finetuning]'")
        return 3
    acel = detectar_acelerador(torch)
    if not acel["disponivel"]:
        print("FALHA QLoRA/LoRA exige GPU CUDA ou AMD ROCm (torch.cuda.is_available() == False); nada foi treinado.")
        return 3
    treino, teste = _carregar(cfg_efetiva)
    torch.manual_seed(cfg_efetiva.semente)
    _, tokenizer, modelo, _ = _carregar_modelo_hf(
        cfg_efetiva.modelo_base, cfg_efetiva, usar_quant_4bit=cfg_efetiva.quant_4bit
    )
    lora = LoraConfig(
        r=cfg_efetiva.lora_r,
        lora_alpha=cfg_efetiva.lora_alpha,
        lora_dropout=cfg_efetiva.lora_dropout,
        target_modules=list(cfg_efetiva.modulos_alvo),
        task_type="CAUSAL_LM",
    )
    sft_kwargs = _filtrar_kwargs(SFTConfig, {
        "output_dir": args.saida_adaptador, "num_train_epochs": cfg_efetiva.epocas,
        "per_device_train_batch_size": cfg_efetiva.lote_por_dispositivo,
        "gradient_accumulation_steps": cfg_efetiva.acumulacao_gradiente, "learning_rate": cfg_efetiva.taxa_aprendizado,
        "max_length": cfg_efetiva.comprimento_max, "max_seq_length": cfg_efetiva.comprimento_max, "seed": cfg_efetiva.semente,
        "bf16": cfg_efetiva.dtype_computo == "bfloat16", "fp16": cfg_efetiva.dtype_computo == "float16",
        "logging_steps": 1, "save_strategy": "no", "report_to": [],
    })
    dados = Dataset.from_list([qr.para_conversa(e) for e in treino])
    treinador = SFTTrainer(**_filtrar_kwargs(SFTTrainer, {
        "model": modelo, "args": SFTConfig(**sft_kwargs), "train_dataset": dados,
        "peft_config": lora, "processing_class": tokenizer, "tokenizer": tokenizer,
    }))
    treinador.train()
    os.makedirs(args.saida_adaptador, exist_ok=True)
    treinador.save_model(args.saida_adaptador)
    tokenizer.save_pretrained(args.saida_adaptador)
    m = qr.manifesto(cfg_efetiva, DADOS, treino, teste, qr.versoes_instaladas(), acelerador=acel)
    with open(os.path.join(args.saida_adaptador, "manifesto.json"), "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    print("adaptador salvo em", args.saida_adaptador, "acelerador:", json.dumps(acel, ensure_ascii=False))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plano")
    p.add_argument("--registrar", action="store_true")
    p = sub.add_parser("avaliar")
    p.add_argument("--backend", choices=("http", "hf"), default="http")
    p.add_argument("--base-url", default="")
    p.add_argument("--modelo", required=True)
    p.add_argument("--adaptador", default=None)
    p.add_argument("--sem-quant", action="store_true")
    p.add_argument("--saida", required=True)
    p.add_argument("--registrar", action="store_true")
    p = sub.add_parser("comparar")
    p.add_argument("antes")
    p.add_argument("depois")
    p.add_argument("--tolerancia", type=float, default=0.05)
    p = sub.add_parser("treinar")
    p.add_argument("--saida-adaptador", required=True)
    p.add_argument("--modelo-base", default=None)
    p.add_argument("--sem-quant", action="store_true")
    p.add_argument("--epocas", type=int, default=None)
    args = ap.parse_args(argv)
    cfg = qr.ConfigQLoRA()
    return {"plano": cmd_plano, "avaliar": cmd_avaliar, "comparar": cmd_comparar, "treinar": cmd_treinar}[args.cmd](args, cfg)


if __name__ == "__main__":
    sys.exit(main())
