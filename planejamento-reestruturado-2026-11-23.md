# Planejamento reestruturado: Chip Huyen (fontes primárias) + fontes 2026 + programação

Estado: **aprovado pelo operador em 23/11/2026** (reorganização em 18 capítulos e programação em duas camadas). A execução no HTML ainda não começou: `guia-engenharia-llms.html` (`19a020013721c5a5`) e `guia-engenharia-llms.pdf` (`10ff8c03dd8dfe83`) seguem intactos.
Substitui a restrição "sem programação" de 15/10/2026 e unifica o currículo com:
- **Fontes primárias estruturantes (locais, fora do Git):**
  1. Chip Huyen, *AI Engineering: Building Applications with Foundation Models* (1ª ed., dez/2024, © 2025 — 10 capítulos, `535` pág. PDF, offset `+24`).
  2. Chip Huyen, *Designing Machine Learning Systems* (DMLS, 1ª ed., mai/2022, © 2022 — 11 capítulos, `389` pág. PDF, offset `+20`).
- **Fontes complementares atualizadas (públicas, já conferidas):** os pacotes `pacote-de-fontes-*.md` e os 16 capítulos existentes em `guia-engenharia-llms.html` (`316` partes, `376` questões), preservando protocolos e especificações vigentes de 2026 (`MCP`, `A2A`, `effort`, `Responses API`, `ZDR`, `Qwen3.8`, `Gemma 4`).
- **Evolução de qualidade:** incorpora as lacunas `L1`–`L8` de `plano-de-lacunas-para-nota-10-2026-11-19.md`.

---

## 1. Diretrizes de arquitetura, formato e direitos autorais

1. **Programação em duas camadas complementares:**
   - **No HTML (`guia-engenharia-llms.html`):** blocos curtos `<pre class="codigo" data-executavel="true">` (`10`–`35` linhas, com `<pre class="saida">`), usando apenas Python 3 padrão e `unittest.mock`, validados de forma determinística por `ferramentas/executar-trechos-de-codigo.py` (sem rede e sem leitura/escrita no projeto).
   - **Trilha prática separada (`laboratorios/`):** `18` laboratórios (um por capítulo) + `1` projeto integrador final em Python completo (chamadas HTTP/API compatíveis com OpenAI e Ollama local, avaliação em datasets fictícios da Aurora Educação, métricas e logs), com suíte de testes local usando mocks para rodar sem custo de nuvem por padrão.
2. **Preservação do formato TDAH (`requisitos-de-formato-html-do-material.md` §8–§9):**
   - Partes curtas (~`400`–`600` palavras incluindo explicação do código), com `Em 3 linhas`, analogia, texto/código enxuto, `1` pergunta inline, ponto de retomada e notas de fonte.
   - Blocos longos ou laboratórios com bibliotecas externas não entram no texto corrido do HTML; ficam em `laboratorios/`.
   - Exemplos empresariais continuam usando a empresa fictícia **Aurora Educação** e descrições genéricas (sem nomes internos do operador).
3. **Direitos autorais e repositório público:**
   - Textos extraídos, índices detalhados e fichamentos dos dois livros ficam exclusivamente em `cache-fontes/livros/` (ignorado no `.gitignore`), nunca no Git público.
   - No HTML, nos pacotes e nos documentos versionados entram apenas referências bibliográficas (livro, capítulo, seção, página), sínteses autorais e código original testado.
4. **Precedência entre fontes:**
   - Os livros fornecem a espinha dorsal conceitual, engenharia de sistemas, dados, métricas, fine-tuning e MLOps.
   - Onde houver mudança posterior à edição dos livros (ex.: `effort`, depreciação de parâmetros de amostragem, `MCP`, `A2A`, políticas atuais de cache/ZDR e modelos abertos de 2026), prevalecem as documentações primárias de 2026 com nota explicativa.
5. **Preservação contra perda de qualidade na leitura dos PDFs:**
   - Nunca usar fragmentos isolados de busca na hora de redigir: usar `ferramentas/livros.py achar` só para localizar e `livros.py ler --de P1 --ate P2` para ler capítulos/seções contínuas (~`15`–`30` pág. por turno), registrando um fichamento local em `cache-fontes/livros/fichamentos/`.
   - Páginas com diagramas, tabelas ou fórmulas quebradas no texto são conferidas pontualmente via `livros.py pagina-png` ou `--layout`.

---

## 2. Nova matriz curricular (18 capítulos em 3 partes)

> Esta proposta reorganiza os 16 capítulos atuais em **18 capítulos** na ordem pedagógica completa (incluindo dois capítulos novos para *Engenharia de Dados/Datasets* e *Fine-tuning/Destilação*, além de incorporar *DMLS Caps. 8–11* em Segurança e LLMOps). Todos os 10 capítulos de *AI Engineering* (AIE) e os 11 de *DMLS* ficam cobertos.

### Parte I — Fundamentos, arquitetura, especificação e avaliação (Caps. 1–5)

| Cap. | Título proposto | Base Chip Huyen | Base atual + docs 2026 + lacunas | Programação no HTML (`python -I`) e Laboratório |
|---|---|---|---|---|
| **1** | **Fundamentos de IA e Modelos de Fundação** | AIE Cap. 1 (Rise of AI Eng., Stack 3 camadas, AI vs ML vs Full-Stack) · AIE Cap. 2 (Training Data, Arquitetura, Tamanho, SFT/Preferência, Sampling, Test-Time Compute) · DMLS Cap. 1 (pesquisa vs produção) | Cap. 1 atual + **L3** (atenção `Q·K`, `softmax`, custo quadrático, RLHF/DPO) + `Qwen3.8` / `Gemma 4` | HTML: cálculo de `softmax` com temperatura e amostragem top-k/top-p em Python puro. Lab 01: tokenização, contagem de tokens e inspeção de probabilidades/logprobs via API/Ollama. |
| **2** | **Arquitetura e Fluxo de Sistemas com LLM** | AIE Cap. 10 (arquitetura em 5 camadas) · DMLS Cap. 2 (confiabilidade, escalabilidade, manutenibilidade, adaptabilidade) · DMLS Cap. 7 (predição batch vs online) | Cap. 2 atual (HTTP, SSE, streaming, backoff+jitter, idempotência, concorrência) | HTML: cliente HTTP simulado com `unittest.mock`, backoff exponencial com jitter e chave de idempotência. Lab 02: cliente real com streaming SSE, timeouts, fila e retry contra Ollama/API. |
| **3** | **Problemas, Especificações e UX para IA** | AIE Cap. 1 (Use Case Evaluation, expectativas, marcos, manutenção) · DMLS Cap. 2 (objetivos de negócio e ML, enquadramento) · DMLS Cap. 11 (UX: consistência, "quase certo", falha suave) | Cap. 3 atual (RFC 2119, DoD, matriz de decisão de uso de IA) | HTML: validador determinístico de contrato de entrada/saída e fallback seguro. Lab 03: especificação executável + testes de aceite de um caso da Aurora Educação. |
| **4** | **Prompts, Parâmetros e Saídas Estruturadas** | AIE Cap. 5 (in-context learning, system/user, boas práticas, versionamento de prompts) · AIE Cap. 2 (structured outputs) | Cap. 4 atual + docs 2026 (`effort`, XML tags, JSON Schema, migração de parâmetros) | HTML: construtor de prompts versionados e validador de schema/recusa em JSON. Lab 04: extração estruturada estrita comparando versões de prompt e níveis de esforço. |
| **5** | **Avaliação, Métricas e Experimentação** | AIE Cap. 3 (entropia, cross-entropy, BPC/BPB, perplexidade, correção funcional, embeddings, AI as a Judge, avaliação comparativa) · AIE Cap. 4 (build vs buy, benchmarks, pipeline em 3 passos) · DMLS Cap. 6 (offline eval, baselines, experiment tracking) | Cap. 5 atual + **L4** (Wilson, bootstrap, comparação pareada reproduzível) | HTML: entropia/perplexidade simples, intervalo de Wilson, bootstrap e teste pareado da Aurora. Lab 05: pipeline completo de avaliação (determinística + LLM juiz com mitigação de viés). |

### Parte II — Dados, conhecimento, contexto e agentes (Caps. 6–11)

| Cap. | Título proposto | Base Chip Huyen | Base atual + docs 2026 + lacunas | Programação no HTML (`python -I`) e Laboratório |
|---|---|---|---|---|
| **6** | **Engenharia de Dados e Datasets para IA *(Novo)*** | DMLS Cap. 3 (fontes, linha vs coluna, ETL, batch vs stream) · DMLS Cap. 4 (amostragem, rotulagem, desbalanceamento) · DMLS Cap. 5 (features, data leakage) · AIE Cap. 8 (curadoria, síntese, destilação, deduplicação, limpeza) | Integra noções dispersas de dados/chunking e prepara terreno para RAG e fine-tuning | HTML: amostragem estratificada, deduplicação por hash/Jaccard e detector de vazamento (*data leakage*). Lab 06: curadoria, geração sintética controlada e limpeza de dataset em JSONL. |
| **7** | **Busca, Indexação e RAG** | AIE Cap. 6 — parte RAG (arquitetura, algoritmos de recuperação, otimização, multimodal) | Cap. 11 atual (BM25, embeddings, híbrido + RRF, reranking, avaliação RAG) | HTML: chunking com sobreposição e fusão híbrida RRF em Python puro. Lab 07: mini pipeline RAG híbrido (BM25 + embeddings locais + avaliação de recuperação e fidelidade). |
| **8** | **Engenharia de Grafos Aplicada a LLMs** | AIE Cap. 6 (conexão entre recuperação estruturada e planejamento em grafo) | Cap. 6 atual (GraphRAG global/local, grafos de estado, FSMs, checkpointers, subagentes) | HTML: grafo de estados (FSM) com checkpointer persistido em `sqlite3` (em memória) e execução idempotente. Lab 08: workflow com retomada após falha e comparação de custo com/sem subagentes. |
| **9** | **Contexto, Memória e Feedback do Usuário** | AIE Cap. 5 (eficiência de contexto) · AIE Cap. 6 (Memory) · AIE Cap. 10 (User Feedback: extração conversacional, desenho e limites) | Cap. 9 atual (orçamento de contexto, notas externas, compactação vs limpeza, ciclo de sessão) | HTML: gerenciador de orçamento de tokens e extrator determinístico de sinais implícitos de feedback. Lab 09: memória persistente de sessão + coleta e análise de feedback conversacional. |
| **10** | **Ferramentas, Protocolos e Integrações** | AIE Cap. 6 — parte Tools | Cap. 10 atual (function calling, contratos, filtros de saída, MCP `2026-07-28`, A2A, computer use) | HTML: registro de ferramentas com validação estrita de argumentos e despacho seguro. Lab 10: servidor/cliente MCP local mínimo com ferramentas idempotentes e tratamento de erro. |
| **11** | **Harnesses, Workflows e Agentes** | AIE Cap. 6 — parte Agents (planning, failure modes, eval) · AIE Cap. 10 (Agent Patterns, Orchestration) | Cap. 12 atual (laços verificáveis, teto de tentativas, interrupção e retomada) | HTML: loop de agente (`ReAct` simulado) com teto de passos, registro em JSON e parada segura. Lab 11: agente multi-etapas com verificação determinística fim a fim e retomada. |

### Parte III — Segurança, adaptação, operação e economia (Caps. 12–18)

| Cap. | Título proposto | Base Chip Huyen | Base atual + docs 2026 + lacunas | Programação no HTML (`python -I`) e Laboratório |
|---|---|---|---|---|
| **12** | **Segurança, Guardrails e IA Responsável** | AIE Cap. 5 (Defensive Prompt Engineering: jailbreak, injection, extração, defesas) · AIE Cap. 10 (Guardrails) · DMLS Cap. 11 (Responsible AI: casos e framework) | Cap. 7 atual (OWASP v2.0, NIST AI 600-1, CaMeL, LGPD, ZDR, Model Armor) | HTML: sanitizador/isolador de saída de ferramenta e verificador de política/PII com regex. Lab 12: camada de guardrails de entrada/saída + suite de testes adversariais básicos. |
| **13** | **Atos Autodestrutivos e Proporcionalidade** | DMLS Cap. 8 (causas de falha em ML vs software) · DMLS Cap. 11 (estrutura de equipe e revisão) | Cap. 8 atual (Google SRE, Denison et al., Context Rot, rollback, custo total vs ganho marginal) | HTML: travas determinísticas contra repetição/escopo (retry budget, dry-run e lista de permissão). Lab 13: simulação de incidentes de agente com rollback e circuit breaker. |
| **14** | **Inferência Local e Otimização de Serviço** | AIE Cap. 9 (métricas TTFT/TPOT/throughput, aceleradores, otimização de modelo e serviço) · DMLS Cap. 7 (cloud e edge, compilação/otimização) | Cap. 13 atual + **L3** (continuous batching, PagedAttention, tensor/pipeline parallel) + `Qwen3.8` / `Gemma 4` | HTML: calculadora executável de memória (pesos + GQA + KV cache por comprimento de contexto). Lab 14: benchmark reproduzível local no Ollama/llama.cpp medindo TTFT, ITL e uso de VRAM. |
| **15** | **Fine-tuning, Quantização e Destilação *(Novo)*** | AIE Cap. 7 (quando ajustar vs RAG, matemática de memória/backprop, precisão numérica, quantização, PEFT/LoRA, model merging, táticas) · AIE Cap. 8 (Model Distillation) · DMLS Cap. 6–7 (treino distribuído, compressão, pruning, destilação) | Absorve e aprofunda `13.5` atual (`LoRA`, `QLoRA`) | HTML: simulador de memória de treino (pesos + gradientes + estados do otimizador + LoRA) e quantização de vetor simples. Lab 15: preparação de dataset e treino/avaliação LoRA ou destilação em exemplo pequeno/simulado. |
| **16** | **Seleção, Roteamento e Gateways** | AIE Cap. 4 (workflow de seleção, build vs buy) · AIE Cap. 10 (Model Router e Gateway) | Cap. 14 atual (IFEval, LiveCodeBench, SWE-bench, RouteLLM, FrugalGPT, troca só em conversa nova) + revisão de vigência (`openai-model-selection`) | HTML: roteador baseado em regras/complexidade + fallback e cálculo de custo esperado. Lab 16: gateway de roteamento entre modelo local rápido e modelo maior com log de decisões. |
| **17** | **LLMOps, Monitoramento, Shifts e Testes em Produção** | DMLS Cap. 8 (data distribution shifts, detecção e tratamento, monitoring toolbox, observability) · DMLS Cap. 9 (continual learning, shadow, A/B, canary, interleaving, bandits) · DMLS Cap. 10 (infra, contêineres, orquestradores, model/feature store, build vs buy) · AIE Cap. 10 (Monitoring & Observability, Pipeline Orchestration) | Cap. 15 atual (OpenTelemetry GenAI, Langfuse/MLflow, SemVer, rollback) | HTML: detector simples de drift estatístico (PSI/variação de distribuição) e roteador Canary/A-B com hash determinístico. Lab 17: pipeline instrumentado com traces estruturados e análise de drift/canary. |
| **18** | **Eficiência, Cache e Economia de Escala** | AIE Cap. 9 (otimização de custo/latência) · AIE Cap. 10 (Caches) · DMLS Cap. 10 (build vs buy, custo de infra) | Cap. 16 atual (multiplicadores de cache Anthropic/OpenAI/Google, Batch API, ponto de equilíbrio) + **L5** (projeto integrador final) | HTML: simulador de custo total por sessão (com cache hit/invalidação e lote). Lab 18 + Projeto Integrador: sistema completo fim a fim (RAG + ferramentas + guardrails + roteamento + avaliação + relatório de custo). |

---

## 3. Impacto em ferramentas e validações

1. **`ferramentas/livros.py` e `ferramentas/testar-livros.py`:** já implementados e aprovados (`2/2 OK`), prontos para alimentar as sessões por capítulo sem estourar contexto.
2. **`ferramentas/executar-trechos-de-codigo.py`:** permanece como validador determinístico do HTML; só ampliar `PERMITIDOS` se algum snippet de capítulo exigir módulo padrão seguro (ex.: `statistics`, `heapq`).
3. **`ferramentas/fontes.py`:** adicionar subcomando `vigencia` (`L7`) para acompanhar as URLs web complementares; manter livros fora do manifesto público de URLs.
4. **`ferramentas/validar-guia.py` e `guia.py`:** já aceitam número dinâmico de capítulos (conferindo `5` ou `6` questões de fechamento por capítulo e a convenção `<figure class="bloco-codigo">`); criar um runner/suíte dedicada para `laboratorios/` com mocks determinísticos.
5. **`requisitos-de-formato-html-do-material.md`:** atualizar §1 e §4 registrando a entrada da programação em duas camadas (snippets determinísticos no HTML + trilha em `laboratorios/`).

---

## 4. Fases de execução (após aprovação e Handoff)

- **Fase 0 — Fechamento deste planejamento e Handoff:** aprovar este mapa, atualizar `CLAUDE.md` / `roadmap.md` / `requisitos-de-formato-html-do-material.md`, commitar `ferramentas/livros.py` + `testar-livros.py` + este plano, e gerar o Handoff limpo (recomendando **Orchestrator Argon** para a execução estrutural pesada).
- **Fase 1 — Fichamento por lotes dos livros (local, fora do Git):** ler em janelas contínuas um bloco por turno (Caps. 1–5 → 6–11 → 12–18) e registrar fichamentos em `cache-fontes/livros/fichamentos/`, conferindo figuras/tabelas via `pagina-png`.
- **Fase 2 — Backup e infraestrutura:** backup integral do HTML/PDF atuais em `arquivo/antes-reestruturacao-huyen-<data>/` e criação da estrutura `laboratorios/`.
- **Fase 3 — Reescrita e expansão capítulo a capítulo (Caps. 1–18):** atualizar ou criar cada capítulo + snippets `data-executavel="true"` + estudo de caso com rubrica (`L5`) + laboratório correspondente (`L6`), validando após cada bloco com `guia.py fechar` e testes dos laboratórios.
- **Fase 4 — Validação global, revisão externa (`L1`), piloto (`L2`) e arte (`L8`):** fechar glossário/referências, rodar `auditar-guia-navegador.mjs` em `320 px` + `axe-core`, regerar PDF via `guia.py pdf --substituir`, conduzir piloto/validação nos 3 aparelhos e gerar as imagens em aquarela por último.

---

## 5. Pontos para confirmar antes do Handoff

1. Concorda com a reorganização em **18 capítulos** na sequência pedagógica acima (movendo *Engenharia de Dados/Datasets* para o Cap. 6 e *Fine-tuning/Destilação* para o Cap. 15)?
2. A estrutura do código está equilibrada assim: **snippets curtos em Python puro/`unittest.mock` no HTML** + **18 laboratórios reais em `laboratorios/`** (com testes mockados + opção local/API)?

Assinatura: agy - ap (proposta de planejamento, 23/11/2026)
