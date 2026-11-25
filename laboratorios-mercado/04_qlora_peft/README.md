# 04 — Ajuste fino QLoRA/LoRA reproduzível

Tudo o que decide o resultado fica explícito e com hash: dados, divisão estratificada por (fatia, categoria), formato de conversa, LoRA (`r`, `alpha`, `dropout`, módulos), quantização 4 bits NF4 com dupla quantização, sementes e versões.

- `dados/chamados_aurora.jsonl`: 36 chamados fictícios, 4 categorias × 3 fatias (`formal`, `informal`, `com_ruido`).
- `qlora_receita.py`: validação dos dados, divisão estável (24 treino / 12 teste), conversa para SFT, avaliação por fatia (acurácia e formato JSON) e **portão**: reprova se alguma fatia cair mais que a tolerância, mesmo com média maior.
- `treinar_qlora.py`: `plano` (manifesto), `avaliar` (qualquer endpoint OpenAI-compatível), `comparar` (código 2 se reprovar) e `treinar` (`transformers` + `peft` + `trl`, com parâmetros filtrados pela assinatura da versão instalada).

## Execução

```bash
.venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py plano --registrar
.venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py avaliar \
  --base-url http://127.0.0.1:8081/v1 --modelo modelo-local --saida antes.json
# com GPU CUDA e o extra [finetuning]:
.venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py treinar --saida-adaptador adaptador/
# sirva base + adaptador (ex.: vLLM --enable-lora), avalie de novo e aplique o portão:
.venv-mercado/bin/python -I laboratorios-mercado/04_qlora_peft/treinar_qlora.py comparar antes.json depois.json
```

Em 24/11/2026: manifesto registrado e linha de base do avaliador com Qwen3-4B-Instruct-2507 (acurácia 0,75 em cada fatia, formato 100%). Esse modelo não é a base do ajuste (`Qwen/Qwen3-1.7B` na configuração padrão); o registro valida o avaliador.

**Pendente:** `treinar` não foi executado (máquina sem GPU CUDA; `bitsandbytes` 4 bits exige CUDA). O caminho de treino é `[Não verificado]` em execução.
