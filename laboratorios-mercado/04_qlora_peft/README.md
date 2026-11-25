# 04 — Ajuste fino QLoRA/LoRA reproduzível

Tudo o que decide o resultado fica explícito e com hash: dados, divisão estratificada por (fatia, categoria), formato de conversa, LoRA (`r`, `alpha`, `dropout`, módulos), quantização 4 bits NF4 com dupla quantização, sementes e versões.

- `dados/chamados_aurora.jsonl`: 36 chamados fictícios, 4 categorias × 3 fatias (`formal`, `informal`, `com_ruido`).
- `qlora_receita.py`: validação dos dados, divisão estável (24 treino / 12 teste), conversa para SFT, avaliação por fatia (acurácia e formato JSON) e **portão**: reprova se alguma fatia cair mais que a tolerância, mesmo com média maior.
- `treinar_qlora.py`: `plano` (manifesto), `avaliar` (`--backend http` para endpoints OpenAI-compatíveis ou `--backend hf` com `--adaptador` para avaliação direta em `transformers`/`peft`), `comparar` (código 2 se reprovar) e `treinar` (`transformers` + `peft` + `trl`, compatível com **GPU NVIDIA CUDA e AMD ROCm/HIP**, com `--sem-quant` opcional para LoRA em `bfloat16` e `--epocas`).

## Execução

```bash
.venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py plano --registrar
# Avaliação via endpoint HTTP (llama.cpp, vLLM, Ollama):
.venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py avaliar \
  --base-url http://127.0.0.1:8081/v1 --modelo modelo-local --saida antes.json

# Treino e avaliação direta do mesmo modelo base + adaptador (container ROCm ou ambiente CUDA):
# No host AMD (RX 9070 XT / gfx1201), use o serviço `qlora-rocm` (--profile finetuning no compose.yaml).
python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py avaliar \
  --backend hf --modelo Qwen/Qwen3-1.7B --saida antes.json
python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py treinar \
  --epocas 12 --saida-adaptador adaptador/
python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py avaliar \
  --backend hf --modelo Qwen/Qwen3-1.7B --adaptador adaptador/ --saida depois.json
python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py comparar antes.json depois.json
```

Em 24/11/2026: manifesto registrado e linha de base do avaliador HTTP com Qwen3-4B-Instruct-2507 (acurácia `0,75` em cada fatia, formato `100%`).

Em 25/11/2026 (**AMD Radeon RX 9070 XT `gfx1201`, PyTorch `2.12.0+rocm7.14.1`, `bitsandbytes 0.50.2`, QLoRA 4-bit NF4 + `bfloat16` em `Qwen/Qwen3-1.7B`**; registro em `execucoes/p04-qlora-rocm-*.json`):
- **Linha de base (`Qwen/Qwen3-1.7B`):** acurácia global `0,6667`, formato `100%` (`com_ruido`: `0,50`, `formal`: `0,75`, `informal`: `0,75`).
- **Configuração padrão (`3` épocas, `6` passos, `8,55 s`):** acurácia `0,5833` (`com_ruido`: `0,75`, `formal`: `0,75`, `informal`: `0,25`); o portão **reprovou** (`exit code 2`, regressão em `informal: 0,75 -> 0,25`), demonstrando proteção contra promoção prematura.
- **Com `--epocas 12` (`24` passos, `22,53 s`):** acurácia `0,9167` (`+0,25` global; `com_ruido`: `0,75`, `formal`: `1,00`, `informal`: `1,00`), formato `100%`, **aprovado** pelo portão sem regressões.
