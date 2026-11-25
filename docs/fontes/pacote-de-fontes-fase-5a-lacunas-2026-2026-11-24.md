# Pacote de fontes: Fase 5A — Lacunas conceituais de 2026 (24/11/2026)

Data: 24/11/2026. Autoria: agy - ap. Reúne trechos literais conferidos para as 8 partes curtas da Fase 5A (`2.6f`, `4.5e`, `7.4e`, `12.5d`, `12.6e`, `14.3d`, `14.6c`, `17.4d`).

## 1. Fontes baixadas e como reconferir

Arquivos baixados para `cache-fontes/bruto/` e extraídos para `cache-fontes/textos/` via `python3 -I ferramentas/fontes.py baixar --pacote pacote-de-fontes-fase-5a-lacunas-2026-2026-11-24.md && python3 -I ferramentas/fontes.py extrair`.

| Chave | Fonte pública e endereço efetivo | Hash bruto (16) |
|---|---|---|
| `fastapi-async` | FastAPI, *Concurrency and async / await* — https://fastapi.tiangolo.com/async/ | `8dbf0e7991853241` |
| `httpx-async` | HTTPX, *Async Support* — https://www.python-httpx.org/async/ | `bf8c86824c36c21b` |
| `python-asyncio` | Python 3, *Coroutines and Tasks (asyncio)* — https://docs.python.org/3/library/asyncio-task.html | `dcfd774dc0fc608a` |
| `podman-rootless` | Podman, *Basic Setup and Use of Podman in a Rootless environment* — https://raw.githubusercontent.com/containers/podman/main/docs/tutorials/rootless_tutorial.md | `debfa9e4e5aa829a` |
| `arxiv-xgrammar-2411.15100` | Dong et al., *XGrammar* (`arXiv:2411.15100`) — https://arxiv.org/abs/2411.15100 | `78af98df7777901e` |
| `outlines-readme` | Outlines, *Structured Text Generation* — https://raw.githubusercontent.com/dottxt-ai/outlines/main/README.md | `2200c02b392cf368` |
| `llamacpp-grammars` | llama.cpp, *GBNF Grammars* — https://raw.githubusercontent.com/ggml-org/llama.cpp/master/grammars/README.md | `ba3eb61f75f6a5c5` |
| `vllm-structured` | vLLM, *Structured Outputs* — https://raw.githubusercontent.com/vllm-project/vllm/main/docs/features/structured_outputs.md | `19956c98977f4391` |
| `arxiv-colpali-2407.01449` | Faysse et al., *ColPali* (`arXiv:2407.01449`) — https://arxiv.org/abs/2407.01449 | `e7454c1d3548b904` |
 |
| `anthropic-vision` | Anthropic, *Vision* — https://platform.claude.com/docs/en/build-with-claude/vision | `d1e250209077db0c` |
| `openai-vision` | OpenAI, *Images and vision* — https://developers.openai.com/api/docs/guides/images-vision | `0488c390b97f6a36` |
| `gvisor-arch` | gVisor, *Introduction to gVisor* — https://gvisor.dev/docs/architecture_guide/intro/ | `ff89548eab1a048b` |
| `firecracker-design` | Firecracker, *Design* — https://raw.githubusercontent.com/firecracker-microvm/firecracker/main/docs/design.md | `58cde9cfa1e9cf7a` |
| `docker-security` | Docker, *Security* — https://docs.docker.com/engine/security/ | `b2bd544837bca00e` |
| `eu-ai-act-eurlex` | União Europeia, *Regulation (EU) 2024/1689 (AI Act)* — https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401689 | `6c5c9abe5696965b` |
| `iso-42001` | Google Cloud, *ISO/IEC 42001* — https://cloud.google.com/security/compliance/iso-42001 | `0d5867f8bddf347c` |
| `aicpa-soc2` | AICPA, *SOC 2 Trust Services Criteria* — https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2 | `09a7fc120d4aff20` |
| `arxiv-flashattn2-2307.08691` | Dao, *FlashAttention-2* (`arXiv:2307.08691`) — https://arxiv.org/abs/2307.08691 | `cad73fde8f8c2b09` |
| `arxiv-deepseekv2-2405.04434` | DeepSeek-AI, *DeepSeek-V2* (`arXiv:2405.04434`) — https://arxiv.org/abs/2405.04434 | `89f22ceefcb05b59` |
| `arxiv-yarn-2309.00071` | Peng et al., *YaRN* (`arXiv:2309.00071`) — https://arxiv.org/abs/2309.00071 | `4c742d09250178a4` |
| `arxiv-sglang-2312.07104` | Zheng et al., *SGLang / RadixAttention* (`arXiv:2312.07104`) — https://arxiv.org/abs/2312.07104 | `d7bd2c78de970ccc` |
| `arxiv-distserve-2401.09670` | Zhong et al., *DistServe* (`arXiv:2401.09670`) — https://arxiv.org/abs/2401.09670 | `2a7bb0d40e7eedf7` |
| `arxiv-mx-2310.10537` | Rouhani et al., *Microscaling Data Formats (MX)* (`arXiv:2310.10537`) — https://arxiv.org/abs/2310.10537 | `74877e636e143a47` |
| `vllm-disagg` | vLLM, *Disaggregated Prefilling* — https://raw.githubusercontent.com/vllm-project/vllm/main/docs/features/disagg_prefill.md | `1b16cfc47bcb1265` |
| `prometheus-metrics` | Prometheus, *Metric types* — https://prometheus.io/docs/concepts/metric_types/ | `6a9701809f5d1ff8` |
| `grafana-alerting` | Grafana, *Alerting* — https://grafana.com/docs/grafana/latest/alerting/ | `cfa7712427606627` |
| `github-actions-docs` | GitHub, *Understanding GitHub Actions* — https://docs.github.com/en/actions/about-github-actions/understanding-github-actions | `b6018492e62357f1` |

Comando de conferência: `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-fase-5a-lacunas-2026-2026-11-24.md --textos cache-fontes/textos --projeto .`

## 2. Fontes e trechos

| ID | Unidade | Tipo | Fonte | Local | Edição/data | Qualificador | Trecho |
|---|---|---|---|---|---|---|---|
| F5A-01 | 2.6f Backend assíncrono e contêineres OCI | texto | fastapi-async | TL;DR | FastAPI, consultada em 24/11/2026 | registrado na documentação | You can mix def and async def in your path operation functions as much as you need and define each one using the best option for you. FastAPI will do the right thing with them. |
| F5A-02 | 2.6f Backend assíncrono e contêineres OCI | texto | httpx-async | Connection pooling | HTTPX, consultada em 24/11/2026 | registrado na documentação | In order to get the most benefit from connection pooling, make sure you're not instantiating multiple client instances - for example by using async with inside a "hot loop". |
| F5A-03 | 2.6f Backend assíncrono e contêineres OCI | texto | python-asyncio | asyncio.TaskGroup | Python 3, consultada em 24/11/2026 | registrado na documentação | TaskGroup provides stronger safety guarantees than gather for scheduling a nesting of subtasks |
| F5A-04 | 2.6f Backend assíncrono e contêineres OCI | texto | podman-rootless | Rootless networking e subuid | Podman, consultada em 24/11/2026 | registrado na documentação | Rootless Podman requires the user running it to have a range of UIDs listed in the files `/etc/subuid` and `/etc/subgid`. |
| F5A-05 | 4.5e Decodificação restrita | texto | arxiv-xgrammar-2411.15100 | Abstract | Dong et al., 2024 | registrado no artigo | Context-free grammar is a flexible approach to enable structured generation via constrained decoding. |
| F5A-06 | 4.5e Decodificação restrita | texto | arxiv-xgrammar-2411.15100 | Abstract | Dong et al., 2024 | registrado no artigo | XGrammar accelerates context-free grammar execution by dividing the vocabulary into context-independent tokens that can be prechecked and context-dependent tokens that need to be interpreted during runtime. |
| F5A-07 | 4.5e Decodificação restrita | texto | outlines-readme | Visão geral | Outlines, consultada em 24/11/2026 | registrado na documentação | Outlines guarantees structured outputs during generation — directly from any LLM. |
| F5A-08 | 4.5e Decodificação restrita | texto | llamacpp-grammars | Background | llama.cpp, consultada em 24/11/2026 | registrado na documentação | GBNF is an extension of BNF that primarily adds a few modern regex-like features. |
| F5A-09 | 4.5e Decodificação restrita | texto | vllm-structured | Reasoning & grammars | vLLM, consultada em 24/11/2026 | registrado na documentação | When using Qwen3 Coder models with reasoning enabled, structured outputs might become disabled if the reasoning content does not get parsed into the `reasoning` field separately (v0.11.2+). |
| F5A-10 | 4.5e Decodificação restrita | texto | vllm-structured | Custom grammars | vLLM, consultada em 24/11/2026 | registrado na documentação | A text-only grammar can emit ordinary vocabulary tokens with the same decoded spelling as a boundary token. |
| F5A-11 | 7.4e Multimodalidade prática com VLMs | texto | arxiv-colpali-2407.01449 | Abstract | Faysse et al., 2024/2025 | registrado no artigo | We release ColPali, a Vision Language Model trained to produce high-quality multi-vector embeddings from images of document pages. Combined with a late interaction matching mechanism, ColPali largely outperforms modern document retrieval pipelines while being drastically simpler, faster and end-to-end trainable. |
| F5A-12 | 7.4e Multimodalidade prática com VLMs | texto | anthropic-pdf | How it works e token costs | Anthropic, consultada em 24/11/2026 | registrado na documentação | The system converts each page of the document into an image. |
| F5A-13 | 7.4e Multimodalidade prática com VLMs | texto | anthropic-pdf | Text token costs | Anthropic, consultada em 24/11/2026 | registrado na documentação | Each page typically uses 1,500–3,000 tokens depending on content density. |
| F5A-14 | 7.4e Multimodalidade prática com VLMs | texto | anthropic-vision | Patches | Anthropic, consultada em 24/11/2026 | registrado na documentação | Claude processes images in patches instead of pixels. Each patch is a 28×28-pixel block of the image, referred to as a visual token. |
| F5A-15 | 7.4e Multimodalidade prática com VLMs | texto | openai-vision | Image detail level | OpenAI, consultada em 24/11/2026 | registrado na documentação | The detail parameter controls image preprocessing. Supported values depend on the model: low, high, original, or auto. |
| F5A-16 | 12.5d Isolamento real em produção | texto | docker-security | Docker daemon attack surface | Docker, consultada em 24/11/2026 | registrado na documentação | Running containers (and applications) with Docker implies running the Docker daemon. |
| F5A-17 | 12.5d Isolamento real em produção | texto | gvisor-arch | Visão geral | gVisor, consultada em 24/11/2026 | registrado na documentação | This kernel-like component is called the “gVisor Sentry”. |
| F5A-18 | 12.5d Isolamento real em produção | texto | gvisor-arch | Introduction | gVisor, consultada em 24/11/2026 | registrado na documentação | it is an application kernel, not a virtual machine hypervisor or a system call filter. |
| F5A-19 | 12.5d Isolamento real em produção | texto | firecracker-design | What is Firecracker | Firecracker, consultada em 24/11/2026 | registrado na documentação | Firecracker microVMs combine the security and workload isolation properties of traditional VMs with the speed, agility and resource efficiency enabled by containers. |
| F5A-20 | 12.5d Isolamento real em produção | texto | firecracker-design | Features | Firecracker, consultada em 24/11/2026 | registrado na documentação | With a microVM configured with a minimal Linux kernel, single-core CPU, and 128 MiB of RAM, Firecracker supports a steady mutation rate of 5 microVMs per host core per second |
| F5A-21 | 12.6e Marcos regulatórios e auditoria | texto | eu-ai-act-eurlex | Considerando 26 / Risk-based approach | União Europeia, 2024 | registrado na norma | In order to introduce a proportionate and effective set of binding rules for AI systems, a clearly defined risk-based approach should be followed. |
| F5A-22 | 12.6e Marcos regulatórios e auditoria | texto | eu-ai-act-eurlex | General-purpose AI models | União Europeia, 2024 | registrado na norma | This Regulation provides specific rules for general-purpose AI models and for general-purpose AI models that pose systemic risks, which should apply also when these models are integrated or form part of an AI system. |
| F5A-23 | 12.6e Marcos regulatórios e auditoria | texto | iso-42001 | ISO/IEC 42001:2023 | Google Cloud Compliance, consultada em 24/11/2026 | registrado na documentação | ISO/IEC 42001:2023 outlines and provides the requirements for an Artificial Intelligence Management System (AIMS), specifies a set of best practices, and details AI management controls that can help manage AI risks. |
| F5A-24 | 12.6e Marcos regulatórios e auditoria | texto | aicpa-soc2 | SOC 2 | AICPA, consultada em 24/11/2026 | registrado na norma | Reporting on an Examination of Controls at a Service Organization Relevant to Security, Availability, Processing Integrity, Confidentiality, or Privacy |
| F5A-25 | 14.3d Atenção moderna e contexto estendido | texto | arxiv-flashattn2-2307.08691 | Abstract | Dao, 2023 | registrado no artigo | FlashAttention exploits the asymmetric GPU memory hierarchy to bring significant memory saving (linear instead of quadratic) and runtime speedup (2-4$\times$ compared to optimized baselines), with no approximation. |
| F5A-26 | 14.3d Atenção moderna e contexto estendido | texto | arxiv-deepseekv2-2405.04434 | Abstract | DeepSeek-AI, 2024 | registrado no artigo | MLA guarantees efficient inference through significantly compressing the Key-Value (KV) cache into a latent vector |
| F5A-27 | 14.3d Atenção moderna e contexto estendido | texto | arxiv-yarn-2309.00071 | Abstract | Peng et al., 2023 | registrado no artigo | We present YaRN (Yet another RoPE extensioN method), a compute-efficient method to extend the context window of such models, requiring 10x less tokens and 2.5x less training steps than previous methods. |
| F5A-28 | 14.6c Motores e formatos modernos de serviço | texto | arxiv-sglang-2312.07104 | Abstract | Zheng et al., 2023 | registrado no artigo | The runtime accelerates execution with novel optimizations like RadixAttention for KV cache reuse and compressed finite state machines for faster structured output decoding. |
| F5A-29 | 14.6c Motores e formatos modernos de serviço | texto | arxiv-distserve-2401.09670 | Abstract | Zhong et al., 2024 | registrado no artigo | DistServe assigns prefill and decoding computation to different GPUs, hence eliminating prefill-decoding interferences. |
| F5A-30 | 14.6c Motores e formatos modernos de serviço | texto | vllm-disagg | Why disaggregated prefilling? | vLLM, consultada em 24/11/2026 | registrado na documentação | Disaggregated prefilling put prefill and decode phase of LLM inference inside different vLLM instances. |
| F5A-31 | 14.6c Motores e formatos modernos de serviço | texto | arxiv-mx-2310.10537 | Abstract | Rouhani et al., 2023 | registrado no artigo | This paper evaluates Microscaling (MX) data formats that combine a per-block scaling factor with narrow floating-point and integer types for individual elements. |
| F5A-32 | 17.4d Métricas operacionais e CI/CD de avaliações | texto | prometheus-metrics | Counter, Gauge, Histogram | Prometheus, consultada em 24/11/2026 | registrado na documentação | A histogram records observations (usually things like request durations or response sizes) by counting them in configurable buckets. |
| F5A-33 | 17.4d Métricas operacionais e CI/CD de avaliações | texto | grafana-alerting | Alert rules | Grafana, consultada em 24/11/2026 | registrado na documentação | Using Grafana Alerting, you create queries and expressions from multiple data sources, no matter where you store your data |
| F5A-34 | 17.4d Métricas operacionais e CI/CD de avaliações | texto | github-actions-docs | Overview | GitHub, consultada em 24/11/2026 | registrado na documentação | GitHub Actions is a continuous integration and continuous delivery (CI/CD) platform that allows you to automate your build, test, and deployment pipeline. |
