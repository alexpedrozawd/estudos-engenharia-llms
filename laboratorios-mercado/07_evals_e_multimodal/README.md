# 07 — Evals automatizados e extração multimodal (VLM)

Projeto complementar da Camada 3 para avaliar prompts com rigor estatístico e extrair dados estruturados de PDFs via imagem:

- `eval_pipeline.py`: compara `PROMPT_A` (simples) vs `PROMPT_B` (estruturado com citações `[T1]` e recusa segura), aplica **LLM-as-a-judge estruturado com inversão de ordem A/B** (neutralizando viés de posição), calibra contra rótulos humanos via **kappa de Cohen** (`>= 0,60`) e decide promoção via **bootstrap pareado**.
- `extracao_multimodal.py`: converte PDF em PNG via `pdftoppm` (`poppler-utils`, sem `Pillow`), monta payload OpenAI multimodal (`image_url` base64), valida por Pydantic (`FaturaExtraida`) com reparo automático e executa auditoria aritmética determinística (*code-first*) nos subtotais e total.
- `dados/casos_eval.json`: `12` pares pré-rotulados de calibração e `16` casos de avaliação na Aurora Educação (proposta didática).
- `executar_evals_real.py`: roda os evals contra o servidor local (`llama.cpp:server`) e valida renderização `pdftoppm` + payload multimodal (chamada VLM remota opcional via `--vlm-base-url` e `--vlm-modelo`).

## Execução real

```bash
LLM_BASE_URL=http://127.0.0.1:11434/v1 LLM_MODELO=qwen3:4b-instruct LLM_REASONING_EFFORT=none \
JUIZ_MODELO=qwen3.8:27b-ud-iq3_xxs JUIZ_REASONING_EFFORT=none OLLAMA_HOST=http://127.0.0.1:11434 \
.venv-mercado/bin/python -I laboratorios-mercado/07_evals_e_multimodal/executar_evals_real.py --registrar
```

Em 25/11/2026 (`qwen3:4b-instruct` em CPU, autojulgamento): calibração em `12` pares atingiu `kappa = 0,7391` (`>= 0,60`, `0` vieses de posição); avaliação em `16` casos teve placar `B = 13`, `empate = 3`, `A = 0` (`3` vieses de posição neutralizados pela inversão A/B), média `A = 3,375` vs `B = 4,9375` (`diferenca_media = +1,5625`, IC95% `[1,2812; 1,8125]`, `p = 0,0`, `promover_b = true`). Renderização multimodal `pdftoppm` gerou PNG real (`55.395` bytes) com payload `image_url` base64 validado.

Em 25/11/2026 (Etapa 2 na GPU via Ollama `/v1`, **juiz separado do gerador** em duas fases): `qwen3:4b-instruct` gerou os `16` casos em lote (p50 `237,8 ms`, p95 `434,2 ms`, `2,96 GiB` VRAM) e `qwen3.8:27b-ud-iq3_xxs` calibrou (`kappa = 0,871`, `0` vieses) e julgou (placar `B = 15`, `empate = 1`, `A = 0`, `1` viés neutralizado, média `A = 3,875` vs `B = 5,0`, `diferenca_media = +1,125`, IC95% `[0,9688; 1,3125]`, `p = 0,0`, `promover_b = true`, p50 `7,10 s`, p95 `8,08 s`, `10,01 GiB` VRAM).

**Decisão registrada (25/11/2026):** a execução opcional contra VLM remoto (`--vlm-base-url` / `--vlm-modelo`) foi **arquivada/dispensada** pelo operador; código e testes offline de `extracao_multimodal.py` seguem preservados.
