# 04 — Ajuste fino QLoRA/LoRA reproduzível

Tudo o que decide o resultado fica explícito e com hash: dados, divisão estratificada por (fatia, categoria) e por grupo, formato de conversa, LoRA (`r`, `alpha`, `dropout`, módulos), quantização 4 bits NF4 com dupla quantização, sementes e versões.

- `dados/chamados_aurora.jsonl`: `360` chamados fictícios, 4 categorias × 3 fatias (`formal`, `informal`, `com_ruido`), `30` por estrato: os `36` manuais (`c01`–`c36`, `origem: manual`) e `324` sintéticos (`origem: sintetico-llm`). O campo `grupo` junta paráfrases do mesmo pedido (cosseno de embeddings `>= 0,85`): `15` grupos com 2 ou 3 itens.
- `gerar_chamados_sinteticos.py`: gera os sintéticos com o LLM local (Etapa 3; ver abaixo), com cache fora do Git. Os dados ficam congelados no Git e o CI só confere a integridade (sem PII, sem quase duplicatas, `30` por estrato, grupos inteiros em um só conjunto).
- `executar_ciclo_qlora.py`: ciclo sem intervenção manual: treina um adaptador por época candidata, escolhe na validação, avalia o teste uma vez e aplica o portão (código `0` só se `aprovado`).
- `qlora_receita.py`: validação dos dados, divisão estável por hash e por grupo (`237` treino / `123` teste; com `--fracao-validacao 0.2`, `163` treino / `74` validação / `123` teste, e o teste não muda), conversa para SFT, avaliação por fatia (acurácia e formato JSON) e **portão** com três vereditos: `reprovado` (média não sobe ou alguma fatia cai mais que a tolerância), `inconclusivo` (ganho sem significância no teste pareado McNemar exato, `alfa = 0,05`, ou sem detalhes por caso) e `aprovado`. O relatório traz o intervalo de Wilson 95% antes e depois (parte 5.6f do guia).
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

**Escolher épocas sem vazamento (parte 6.4b do guia):** passe a mesma `--fracao-validacao` (antes do subcomando) em todos os passos, compare os candidatos com `avaliar --conjunto validacao` e avalie o teste **uma única vez**, com a configuração já escolhida. O `executar_ciclo_qlora.py` faz isso sozinho:

```bash
# No container ROCm (ou ambiente CUDA); cada passo grava JSON em rascunho-local/p04-ciclo/ e é retomável:
python -I laboratorios-mercado/04_qlora_peft/executar_ciclo_qlora.py --epocas 1,3,6
```

**Geração dos sintéticos (26/11/2026; registro em `execucoes/p04-geracao-sintetica-*.json`):** `qwen3.8:27b-ud-iq3_xxs` no Ollama `/v1` (`json_schema`, temperatura `0,9`), `2` pedidos de `24` chamados por estrato, com `5` assuntos cada e as definições das outras categorias no prompt. Dos `578` candidatos: `11` fora de `3`–`40` palavras, `4` quase duplicatas (Jaccard de trigramas `>= 0,6`, inclusive contra os manuais), `0` com PII e `60` com rótulo divergente na conferência às cegas pelo mesmo 27B (`49` de `145` em `academico`, a fronteira mais difícil). Dos `503` restantes, a ordem por hash escolheu `27` por estrato. **Limites:** o gerador e o conferente são o mesmo modelo, então chamados ambíguos saem e o conjunto fica mais fácil que o mundo real; a revisão amostral de `36` itens (`3` por estrato) foi feita por modelo de fronteira, não por pessoa (26/11/2026, [registro](../execucoes/revisao-fronteira-etapa-3-2026-11-26.json)): `36/36` categorias iguais às do conjunto, rotuladas às cegas, `0` com PII e `3` ambíguos ou pouco naturais.

Em 24/11/2026: manifestoEm 24/11/2026: manifesto registrado e linha de base do avaliador HTTP com Qwen3-4B-Instruct-2507 (acurácia `0,75` em cada fatia, formato `100%`).

Em 25/11/2026 (**AMD Radeon RX 9070 XT `gfx1201`, PyTorch `2.12.0+rocm7.14.1`, `bitsandbytes 0.50.2`, QLoRA 4-bit NF4 + `bfloat16` em `Qwen/Qwen3-1.7B`**; registro em `execucoes/p04-qlora-rocm-*.json`):
- **Linha de base (`Qwen/Qwen3-1.7B`):** acurácia global `0,6667`, formato `100%` (`com_ruido`: `0,50`, `formal`: `0,75`, `informal`: `0,75`).
- **Configuração padrão (`3` épocas, `6` passos, `8,55 s`):** acurácia `0,5833` (`com_ruido`: `0,75`, `formal`: `0,75`, `informal`: `0,25`); o portão **reprovou** (`exit code 2`, regressão em `informal: 0,75 -> 0,25`), demonstrando proteção contra promoção prematura.
- **Com `--epocas 12` (`24` passos, `22,53 s`):** acurácia `0,9167` (`+0,25` global; `com_ruido`: `0,75`, `formal`: `1,00`, `informal`: `1,00`), formato `100%`; o portão da época (só média e fatias) aprovou.
- **Reclassificação (25/11/2026, portão estatístico):** o resultado é **inconclusivo**, não aprovado. (1) 8/12 → 11/12: Wilson 95% `[0,39; 0,86]` antes e `[0,65; 0,99]` depois, faixas sobrepostas; o registro não guardou acertos por caso, mas houve pelo menos `3` casos discordantes, então McNemar exato `p ≥ 0,25`. (2) As `12` épocas foram escolhidas depois de ver a reprovação de `3` épocas **no mesmo teste**, sem validação: vazamento de seleção. O que a execução prova é que o QLoRA 4-bit roda na RX 9070 XT, não que o adaptador seja melhor. A reprovação de `3` épocas também se apoia em poucos casos (`informal`: 3 de 4 → 1 de 4).

**Ciclo completo em 26/11/2026 (RX 9070 XT, ROCm `7.14`, QLoRA 4-bit NF4 em `Qwen/Qwen3-1.7B`, `transformers 5.24.1`, `peft 0.22.0`, `trl 1.18.2`; registro em `execucoes/p04-qlora-ciclo-*.json`, cerca de `6` min):**

| Conjunto | Base | 1 época | 3 épocas | 6 épocas |
|---|---|---|---|---|
| Validação (`74`) | `0,635` [`0,52`; `0,74`] | `0,811` | `0,878` | **`0,973`** [`0,91`; `0,99`] |
| Teste (`123`, uma vez) | `0,610` [`0,52`; `0,69`] | — | — | **`0,976`** [`0,93`; `0,99`] |

Validação escolheu `6` épocas. No teste, Wilson 95% sem sobreposição, `45` ganhos e `0` perdas por caso (McNemar exato `p < 10⁻⁶`; o registro arredonda para `0.0`), nenhuma fatia cai (`formal +0,52`, `com_ruido +0,32`, `informal +0,25`) e formato `100%`: o portão **aprovou** sem intervenção (código `0`). **Leitura honesta:** `6` é o maior candidato da grade, então mais épocas talvez rendessem mais; o ganho vale para este conjunto sintético e fácil, não para chamados reais.
