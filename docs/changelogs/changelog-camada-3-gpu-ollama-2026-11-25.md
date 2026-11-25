# Changelog — Camada 3 na GPU com 4B vs 27B e juiz separado (25/11/2026)

Autoria: agy - ap. Etapa 2 do [plano de prontidão para vaga pleno](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md).

## Smoke no Ollama (`/v1`) e achado de `thinking`

- Ollama `0.40.18` em `127.0.0.1:11434/v1` validado com `qwen3:4b-instruct`, `qwen3.8:27b-ud-iq3_xxs` e `qwen3-embedding:0.6b` (`dim = 1024`).
- `qwen3:4b-instruct` respondeu `tools`, `response_format: json_schema` e saídas curtas (`max_tokens=4`) sem consumo em raciocínio.
- `qwen3.8:27b-ud-iq3_xxs` possui capacidade `thinking`: sem `reasoning_effort: "none"`, esgotou `max_tokens=4` e `max_tokens=256` (em `json_schema`) na faixa de raciocínio com `content=""`. Com `reasoning_effort: "none"`, `tools`, `json_schema` estrito (Pydantic) e respostas curtas responderam normalmente (`10,01 GiB` em VRAM, 100% na GPU). A contingência `llama.cpp` Vulkan não foi necessária.

## Adaptações de código e testes offline

- `laboratorios-mercado/mercado_base/__init__.py`: `resumir_latencias_ms()` (`p50`/`p95`).
- `laboratorios-mercado/mercado_base/cliente_openai.py`: suporte a `reasoning_effort` em `ClienteChatOpenAI` (`__init__` e `completar_chat`), propriedade `RespostaChat.texto`, método `completar()` compatível com `ReordenadorLLM`/`responder` (sem alterar `laboratorios/`), e helpers centralizados `medir_memoria_ollama()` e `descarregar_modelo_ollama()`.
- `laboratorios-mercado/01_serving_local/serving_bench.py`: reuso de `medir_memoria_ollama()` de `mercado_base.cliente_openai` e defaults por ambiente `SERVING_SEM_RACIOCINIO` e `OLLAMA_HOST`.
- `laboratorios-mercado/02_rag_producao/executar_rag_real.py`: migrado para `ClienteChatOpenAI` com `--llm-reasoning-effort` (`LLM_REASONING_EFFORT`), `--ollama-host` (`OLLAMA_HOST`), memória em `/api/ps` e `latencia_ms` (`p50`/`p95`) no resumo.
- `laboratorios-mercado/06_integrador_producao/integrador_app.py` e `cliente_integrador_real.py`: suporte a `LLM_LOCAL_REASONING_EFFORT`, `--modelo-local`, `--base-url-local`, `--ollama-host` e registro de `configuracao` e `memoria`.
- `laboratorios-mercado/07_evals_e_multimodal/eval_pipeline.py` e `executar_evals_real.py`: separação entre gerador e juiz (`--juiz-modelo`/`JUIZ_MODELO`, `--juiz-base-url`/`JUIZ_BASE_URL`, `--juiz-reasoning-effort`), execução em duas fases em `avaliar_prompts` (gera todo o lote no 4B antes de calibrar e julgar no 27B, evitando alternância na VRAM) com `latencia_ms` (`p50`/`p95`) para gerador e juiz, e captura de VRAM de ambos com descarregamento do gerador na transição.
- Novos smoke-tests offline: `test_p02_rag.py` (+1), `test_p06_integrador.py` (+1) e `test_p07_evals_multimodal.py` (+2), elevando a suíte de `83` para `87` testes.

## Comparativo real na RX 9070 XT (4B vs 27B)

Registros em `laboratorios-mercado/execucoes/*-2026-11-25T10-*.json`:

- **P01 (`serving_bench.py`, `max_tokens=64`, `reasoning_effort=none`):**
  - `qwen3:4b-instruct` (`2,96 GiB` VRAM): c=1 TTFT p50 `17,8 ms` / p95 `30,5 ms`, e2e p50 `351,1 ms` / p95 `385,6 ms`, `175,3 tok/s`, `100%` no SLO; c=4 TTFT p50 `883,3 ms` / p95 `1.030,4 ms`, e2e p50 `1.215,0 ms` / p95 `1.321,0 ms`, `185,5 tok/s`, `100%` no SLO.
  - `qwen3.8:27b-ud-iq3_xxs` (`10,01 GiB` VRAM): c=1 TTFT p50 `189,2 ms` / p95 `224,4 ms`, e2e p50 `1.579,7 ms` / p95 `1.614,9 ms`, `39,7 tok/s`, `100%` no SLO; c=4 TTFT p50 `4.309,5 ms` / p95 `4.706,1 ms`, e2e p50 `5.702,6 ms` / p95 `5.712,3 ms`, `40,1 tok/s`, `25%` no SLO.
- **P02 (`executar_rag_real.py`, `qwen3-embedding:0.6b` `1,13 GiB` + `pgvector`, 28 consultas):**
  - `4B` (`4,09 GiB` VRAM totais): `hibrida_reranker_llm` MRR `0,90`; geração (`vetorial`) `23/25` acertos, `3/3` recusas, fidelidade `0,84`, p50 `300,1 ms` / p95 `538,9 ms`.
  - `27B iq3_xxs` (`11,14 GiB` VRAM totais): `hibrida_reranker_llm` subiu para **MRR `0,98` / recall `1,0` / nDCG `0,9803`**; geração `24/25` acertos (o único item em `faltou_esperado` foi acentuação `"décimo dia útil"` vs `"decimo dia util"`), `3/3` recusas, **fidelidade `1,0`**, p50 `1.422,5 ms` / p95 `2.182,6 ms`.
- **P06 (`integrador_app.py` + `cliente_integrador_real.py`, 8 cenários):**
  - `4B` (`4,09 GiB` VRAM totais): `5` chamadas MCP, `0` reparos/falhas de esquema, `0` bloqueios de saída, `9.511` tokens em cache de `16.629` entrada, p50 `2.373,7 ms` / p95 `4.578,2 ms`.
  - `27B iq3_xxs` (`11,14 GiB` VRAM totais): `3` chamadas MCP (`consultar_prazo`, `calcular_media_ponderada`, `executar_python_isolado`), `0` reparos/falhas de esquema, `0` bloqueios de saída, `8.075` tokens em cache de `15.864` entrada, p50 `7.930,2 ms` / p95 `17.778,7 ms`.
- **P07 (`executar_evals_real.py`, 4B gera vs 27B `iq3_xxs` julga):**
  - `4B` gerador (`2,96 GiB` VRAM): p50 `237,8 ms` / p95 `434,2 ms`.
  - `27B iq3_xxs` juiz (`10,01 GiB` VRAM): calibração `kappa = 0,871` (`12` pares, `0` vieses de posição); avaliação em `16` casos `B = 15`, `empate = 1`, `A = 0` (`1` viés neutralizado), diferença média `+1,125` (IC95% `[0,9688; 1,3125]`, `p = 0,0`), `promover_b = true`, p50 `7.102,4 ms` / p95 `8.081,5 ms`.
  - Qualidade da `iq3_xxs` validada na própria suíte; alternativa `iq4_xs` não foi necessária.

## Validação

- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: `84` OK (`laboratorios/` inalterado).
- `.venv-mercado/bin/python -I -W error::ResourceWarning laboratorios-mercado/executar_smoke.py`: `87` OK.
- `python3 -I ferramentas/gerar-exercicios.py --checar`, `--verificar labs` e `--verificar mercado`: `79` trechos em `26` labs, todos cobertos.
- `python3 -I ferramentas/testar-ferramentas.py --rapido` e `python3 -I ferramentas/guia.py fechar`: OK.
- `guia-engenharia-llms.html` (`bb004776a6cdc9cb`) e `guia-engenharia-llms.pdf` (`81d2fffd7394a880`) inalterados.
