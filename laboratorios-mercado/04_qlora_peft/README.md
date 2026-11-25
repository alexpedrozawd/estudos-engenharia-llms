# 04 — Ajuste fino QLoRA/LoRA reproduzível

Tudo o que decide o resultado fica explícito e com hash: dados, divisão estratificada por (fatia, categoria), formato de conversa, LoRA (`r`, `alpha`, `dropout`, módulos), quantização 4 bits NF4 com dupla quantização, sementes e versões.

- `dados/chamados_aurora.jsonl`: 36 chamados fictícios, 4 categorias × 3 fatias (`formal`, `informal`, `com_ruido`).
- `qlora_receita.py`: validação dos dados, divisão estável (24 treino / 12 teste; com `--fracao-validacao`, parte do treino vira validação e o teste não muda), conversa para SFT, avaliação por fatia (acurácia e formato JSON) e **portão** com três vereditos: `reprovado` (média não sobe ou alguma fatia cai mais que a tolerância), `inconclusivo` (ganho sem significância no teste pareado McNemar exato, `alfa = 0,05`, ou sem detalhes por caso) e `aprovado`. O relatório traz o intervalo de Wilson 95% antes e depois (parte 5.6f do guia).
- `treinar_qlora.py`: `plano` (manifesto), `avaliar` (`--backend http` para endpoints OpenAI-compatíveis ou `--backend hf` com `--adaptador` para avaliação direta em `transformers`/`peft`), `comparar` (código `0` só se `aprovado`; `2` se `reprovado`, `inconclusivo` ou conjuntos diferentes) e `treinar` (`transformers` + `peft` + `trl`, compatível com **GPU NVIDIA CUDA e AMD ROCm/HIP**, com `--sem-quant` opcional para LoRA em `bfloat16` e `--epocas`).

## Execução

```bash
.venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py plano --registrar
# Avaliação via endpoint HTTP (llama.cpp, vLLM, Ollama):
.venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py avaliar \
  --base-url http://127.0.0.1:8081/v1 --modelo modelo-local --saida antes.json

# Treino e avaliação direta do mesmo modelo base + adaptador (container ROCm ou ambiente CUDA):
# No host AMD (RX 9070 XT / gfx1201), prepare o volume `/opt/venv` do serviço `qlora-rocm`
# travando a versão ROCm do PyTorch para o pip não baixar wheel CUDA por cima:
#   podman compose -f laboratorios-mercado/compose.yaml --profile finetuning run --rm qlora-rocm bash -lc '
#     printf "torch==2.12.0+rocm7.14.1\ntorchaudio==2.11.0+rocm7.14.1\ntorchvision==0.27.0+rocm7.14.1\n" > /tmp/c.txt &&
#     python -m pip install --no-cache-dir -c /tmp/c.txt \
#       "transformers>=4.50" "peft>=0.15" "trl>=0.19" "datasets>=3.0" "bitsandbytes>=0.50" "accelerate>=1.3" "pydantic>=2.11" "httpx>=0.28"
#   '
# Em seguida, execute dentro do mesmo container `qlora-rocm`:
python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py avaliar \
  --backend hf --modelo Qwen/Qwen3-1.7B --saida antes.json
python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py treinar \
  --epocas 12 --saida-adaptador adaptador/
python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py avaliar \
  --backend hf --modelo Qwen/Qwen3-1.7B --adaptador adaptador/ --saida depois.json
python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py comparar antes.json depois.json
```

**Escolher épocas sem vazamento (parte 6.4b do guia):** passe a mesma `--fracao-validacao` (antes do subcomando) em todos os passos, compare os candidatos com `avaliar --conjunto validacao` e avalie o teste **uma única vez**, com a configuração já escolhida. Exemplo: `treinar_qlora.py --fracao-validacao 0.2 avaliar --backend hf --modelo Qwen/Qwen3-1.7B --conjunto validacao --saida val-antes.json`. Limite atual: com `36` exemplos, `0.2` deixa `12` treino / `12` validação / `12` teste. Com `12` casos de teste, o portão só aprova com pelo menos `6` casos que mudaram de resultado, quase todos para acerto (ex.: `6` ganhos e `0` perdas dá `p = 0,03125`); conjuntos maiores são pré-requisito para conclusões.

Em 24/11/2026: manifesto registrado e linha de base do avaliador HTTP com Qwen3-4B-Instruct-2507 (acurácia `0,75` em cada fatia, formato `100%`).

Em 25/11/2026 (**AMD Radeon RX 9070 XT `gfx1201`, PyTorch `2.12.0+rocm7.14.1`, `bitsandbytes 0.50.2`, QLoRA 4-bit NF4 + `bfloat16` em `Qwen/Qwen3-1.7B`**; registro em `execucoes/p04-qlora-rocm-*.json`):
- **Linha de base (`Qwen/Qwen3-1.7B`):** acurácia global `0,6667`, formato `100%` (`com_ruido`: `0,50`, `formal`: `0,75`, `informal`: `0,75`).
- **Configuração padrão (`3` épocas, `6` passos, `8,55 s`):** acurácia `0,5833` (`com_ruido`: `0,75`, `formal`: `0,75`, `informal`: `0,25`); o portão **reprovou** (`exit code 2`, regressão em `informal: 0,75 -> 0,25`), demonstrando proteção contra promoção prematura.
- **Com `--epocas 12` (`24` passos, `22,53 s`):** acurácia `0,9167` (`+0,25` global; `com_ruido`: `0,75`, `formal`: `1,00`, `informal`: `1,00`), formato `100%`; o portão da época (só média e fatias) aprovou.
- **Reclassificação (25/11/2026, portão estatístico):** o resultado é **inconclusivo**, não aprovado. (1) 8/12 → 11/12: Wilson 95% `[0,39; 0,86]` antes e `[0,65; 0,99]` depois, faixas sobrepostas; o registro não guardou acertos por caso, mas houve pelo menos `3` casos discordantes, então McNemar exato `p ≥ 0,25`. (2) As `12` épocas foram escolhidas depois de ver a reprovação de `3` épocas **no mesmo teste**, sem validação: vazamento de seleção. O que a execução prova é que o QLoRA 4-bit roda na RX 9070 XT, não que o adaptador seja melhor. A reprovação de `3` épocas também se apoia em poucos casos (`informal`: 3 de 4 → 1 de 4).
