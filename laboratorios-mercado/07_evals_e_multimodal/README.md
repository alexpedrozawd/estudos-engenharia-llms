# 07 — Evals automatizados e extração multimodal (VLM)

Projeto complementar da Camada 3 para avaliar prompts com rigor estatístico e extrair dados estruturados de PDFs via imagem:

- `eval_pipeline.py`: compara `PROMPT_A` (simples) vs `PROMPT_B` (estruturado com citações `[T1]` e recusa segura), aplica **LLM-as-a-judge estruturado com inversão de ordem A/B** (neutralizando viés de posição), calibra contra rótulos de referência via **kappa de Cohen** (`>= 0,60`) e decide promoção via **bootstrap pareado**.
- `extracao_multimodal.py`: converte PDF em PNG via `pdftoppm` (`poppler-utils`, sem `Pillow`), monta payload OpenAI multimodal (`image_url` base64), valida por Pydantic (`FaturaExtraida`) com reparo automático e executa auditoria aritmética determinística (*code-first*) nos subtotais e total.
- `dados/casos_eval.json` (Etapa 3): `150` casos de avaliação (`16` manuais, `123` do corpus ampliado do P02 e `11` recusas por construção: pergunta de um documento com contexto de outro) e `40` pares de calibração: os `12` pré-rotulados pelo autor do lab na Fase 6 (`origem: pre_rotulado`; sem revisão humana independente) e `28` com **defeito conhecido** (`origem: construcao`: número trocado, sem citação, afirmação inventada ou recusa indevida, `7` de cada, com a resposta boa em A em metade). O rótulo de cada par fica em `rotulo_referencia` (o pipeline ainda aceita o nome antigo `julgamento_humano`), e `origem` diz quem rotulou.
- `montar_casos_ampliados.py`: monta os casos e pares acima de forma determinística, sem LLM (rodar de novo dá o mesmo arquivo).
- `executar_evals_real.py`: roda os evals contra o servidor local (`llama.cpp:server`; `--cache-llm` retoma execuções longas) e valida renderização `pdftoppm` + payload multimodal (chamada VLM remota opcional via `--vlm-base-url` e `--vlm-modelo`).

## Execução real

```bash
LLM_BASE_URL=http://127.0.0.1:11434/v1 LLM_MODELO=qwen3:4b-instruct LLM_REASONING_EFFORT=none \
JUIZ_MODELO=qwen3.8:27b-ud-iq3_xxs JUIZ_REASONING_EFFORT=none OLLAMA_HOST=http://127.0.0.1:11434 \
.venv-mercado/bin/python -I laboratorios-mercado/07_evals_e_multimodal/executar_evals_real.py --registrar
```

Em 25/11/2026 (`qwen3:4b-instruct` em CPU, autojulgamento): calibração em `12` pares atingiu `kappa = 0,7391` (`>= 0,60`, `0` vieses de posição); avaliação em `16` casos teve placar `B = 13`, `empate = 3`, `A = 0` (`3` vieses de posição neutralizados pela inversão A/B), média `A = 3,375` vs `B = 4,9375` (`diferenca_media = +1,5625`, IC95% `[1,2812; 1,8125]`, `p = 0,0`, `promover_b = true`). Renderização multimodal `pdftoppm` gerou PNG real (`55.395` bytes) com payload `image_url` base64 validado.

Em 25/11/2026 (Etapa 2 na GPU via Ollama `/v1`, **juiz separado do gerador** em duas fases): `qwen3:4b-instruct` gerou os `16` casos em lote (p50 `237,8 ms`, p95 `434,2 ms`, `2,96 GiB` VRAM) e `qwen3.8:27b-ud-iq3_xxs` calibrou (`kappa = 0,871`, `0` vieses) e julgou (placar `B = 15`, `empate = 1`, `A = 0`, `1` viés neutralizado, média `A = 3,875` vs `B = 5,0`, `diferenca_media = +1,125`, IC95% `[0,9688; 1,3125]`, `p = 0,0`, `promover_b = true`, p50 `7,10 s`, p95 `8,08 s`, `10,01 GiB` VRAM).

**Decisão registrada (25/11/2026):** a execução opcional contra VLM remoto (`--vlm-base-url` / `--vlm-modelo`) foi **arquivada/dispensada** pelo operador; código e testes offline de `extracao_multimodal.py` seguem preservados.

**Etapa 3 — escala (26/11/2026; `execucoes/p07-evals-e-multimodal-2026-11-26T02-50-59-0300.json`):** `qwen3:4b-instruct` gerou A e B nos `150` casos e `qwen3.8:27b-ud-iq3_xxs` julgou com inversão (`680` chamadas em `3` passadas com cache; o registro final saiu do cache, e as latências são as medidas na chamada original: gerador p50/p95 `498 / 969 ms`, juiz `3.513 / 3.973 ms` por chamada).

- **Calibração (`40` pares):** `kappa = 0,955`, IC 95% por bootstrap [`0,86`; `1,0`], concordância `39/40` (Wilson [`0,87`; `0,996`]), `0` vieses de posição. Por origem: `28` pares por construção com `kappa = 1,0` e `12` pré-rotulados com `kappa = 0,871` (`11/12`, Wilson [`0,65`; `0,99`]).
- **Avaliação (`150` casos):** placar `B = 137`, `empate = 9`, `A = 4` (`7` vieses de posição viraram empate); vitórias de B `0,913` (Wilson [`0,86`; `0,95`]); teste do sinal `137` contra `4` (`p ≈ 1,2 × 10⁻³⁵`); notas `A = 3,86` e `B = 4,84`, diferença `+0,98` (bootstrap IC 95% [`0,84`; `1,11`]); `promover_b = true`.

**Limites:** os pares por construção têm defeitos claros e medem só se o juiz pega erro óbvio; não há rótulos humanos independentes. Em 26/11/2026, um modelo de fronteira rotulou às cegas os `40` pares ([registro](../execucoes/revisao-fronteira-etapa-3-2026-11-26.json)): `40/40` iguais à referência e `kappa = 0,955` contra o juiz 27B, reproduzido do cache (a única divergência é `cal-12`, que o juiz deu a A e o revisor e a referência deram como empate). Isso não substitui rótulo humano. Casos, contextos e referências vêm do corpus gerado pelo 27B, o mesmo modelo do juiz.
