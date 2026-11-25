# Mapa de vagas — engenharia de LLMs no Brasil (LinkedIn, 25/11/2026)

Insumo da etapa 5 do [plano de prontidão](plano-prontidao-para-vaga-pleno-2026-11-25.md), antecipado por pedido do operador (prioridade para vagas no Brasil).

## Método e limites

- **Coleta:** busca pública de vagas do LinkedIn (rota sem login, por navegador sem interface), filtro geográfico Brasil, termos `LLM Engineer`, `Generative AI Engineer`, `GenAI Engineer`, `IA Generativa` e `Engenheiro de IA LLM`; leitura só de vagas, com pausas entre pedidos; a conta do operador não foi usada.
- **Amostra:** 33 anúncios, **29 vagas únicas** após remover repetições (mesmo texto em outra cidade).
- **Contagem:** expressões regulares sobre o texto de cada vaga; amostras conferidas à mão (Kubernetes, frameworks de agentes, bancos vetoriais, fine-tuning). Não separa requisito obrigatório de desejável; pode haver falso positivo em categorias amplas (APIs, comunicação, custo).
- **Senioridade:** pelo título, 17 sênior ou lead, 1 pleno e 2 júnior; 9 sem nível no título (no LinkedIn: 2 "Mid-Senior", 1 "Associate", 6 sem informação). O mercado amostrado pede mais senioridade do que "pleno"; o plano mira os requisitos dessas vagas.
- **Dados brutos:** `rascunho-local/vagas-linkedin-2026-11-25/` (fora do Git).

## Frequência dos requisitos (29 vagas)

| Requisito | Vagas | % | Cobertura atual no projeto |
|---|---:|---:|---|
| RAG | 26 | 90 | Forte (Cap. 7, Lab 07, P02) |
| Agentes | 24 | 83 | Forte (Caps. 10–11, Labs 10–11, P03, P06) |
| APIs / integração | 24 | 83 | Forte (P05, P06) |
| Python | 22 | 76 | Forte (todos os labs) |
| Arquitetura / system design | 19 | 66 | Conceitual forte; falta treino de entrevista (etapa 5) |
| Avaliação (evals) | 18 | 62 | Forte (Cap. 5, Lab 05, P07) |
| Observabilidade | 18 | 62 | Boa (OTLP, Jaeger, Prometheus); ferramentas de rastreamento de LLM (Langfuse, LangSmith, Phoenix/Arize) em 6 vagas (21%); no guia, Langfuse só citado |
| Custo e latência | 18 | 62 | Forte (Caps. 14, 16 e 18) |
| Comunicação com negócio | 17 | 59 | Parcial (Cap. 3); falta preparo de entrevista (etapa 5) |
| **Framework de LLM/agentes** | **16** | **55** | **Lacuna prática:** LangChain 13 (45%), LangGraph 11 (38%), CrewAI 5, Semantic Kernel 4, AutoGen 3, LlamaIndex 2; no guia só como fonte |
| **Nuvem (AWS, Azure ou GCP)** | **15** | **52** | **Lacuna:** AWS 13 (45%), Azure 12 (41%), GCP 10 (34%); Azure OpenAI/AI Foundry 6 (21%), Bedrock 2, Vertex AI 2; guia sem serviços gerenciados |
| Banco vetorial | 14 | 48 | Boa (pgvector); Pinecone, Weaviate e FAISS em 3 vagas cada (10%) |
| Inglês | 12 | 41 | Fora do escopo do guia |
| Multiagentes | 12 | 41 | Conceitual (Caps. 8 e 11); sem prática |
| Guardrails / segurança | 10 | 34 | Forte (Caps. 12–13, Lab 12, P06) |
| SQL, CI/CD | 10 cada | 34 | Pré-requisito de engenharia; CI no projeto |
| Docker ou Kubernetes | 10 | 34 | Docker/Podman forte; Kubernetes em 4 vagas (14%) |
| Fine-tuning (LoRA/PEFT) | 8 | 28 | Forte (Cap. 15, P04) |
| LGPD / compliance | 8 | 28 | Boa (Cap. 12) |
| MCP ou A2A | 7 | 24 | Boa (Cap. 10, P03) |
| Assistentes de código (Copilot, Cursor, Claude Code) | 7 | 24 | Parcial (Cap. 11, harnesses) |

## Conclusões para o plano

1. Acima do corte de um terço e sem prática no projeto: **frameworks de orquestração e agentes** (55%) e **nuvem com serviços gerenciados de LLM** (52%). Viram capítulos novos com laboratório (etapa 5B do plano).
2. Multiagentes (41%) entra no capítulo de frameworks, com padrão supervisor/especialistas.
3. Langfuse/LangSmith (21%), bancos vetoriais gerenciados (≤ 10% cada) e Kubernetes (14%) ficam abaixo do corte: Langfuse entra como item prático curto via OTLP; bancos vetoriais como trade-off nos casos de system design; Kubernetes segue opcional (etapa 6a).
4. Comunicação com negócio (59%) e arquitetura (66%) reforçam a etapa 5 (casos de system design e bloco de comunicação); inglês (41%) é preparo pessoal, fora do guia.

## Vagas consideradas

| Vaga | Empresa | Local | Nível |
|---|---|---|---|
| [Sênior AI Engineer / LLM Engineer](https://www.linkedin.com/jobs/view/4388229754) | Leaf Consulting | Vitória, Espírito Santo | Sênior/lead |
| [Lead, AI Engineer](https://www.linkedin.com/jobs/view/4453312275) | Bain & Company | São Paulo, São Paulo | Sênior/lead |
| [Especialista IA](https://www.linkedin.com/jobs/view/4454152617) | Opportunity Gestora | São Paulo, São Paulo | Sênior/lead |
| [AI Engineer - COM INGLÊS](https://www.linkedin.com/jobs/view/4463611411) | Capco | São Paulo, São Paulo | Não informado |
| [Senior, AI Engineer](https://www.linkedin.com/jobs/view/4464922441) | Bain & Company | São Paulo, São Paulo | Sênior/lead |
| [Senior Deployed AI Engineer](https://www.linkedin.com/jobs/view/4467388931) | Artefact | Grande São Paulo | Sênior/lead |
| [Senior Deployed AI Engineer – OpenAI](https://www.linkedin.com/jobs/view/4467390986) | Artefact | Grande São Paulo | Sênior/lead |
| [Desenvolvedor Especialista IA](https://www.linkedin.com/jobs/view/4469391780) | Mais Contabilidade | Santo André, São Paulo | Sênior/lead |
| [AI Machine Learning Engineer - Remote - Latin America](https://www.linkedin.com/jobs/view/4475041492) | FullStack | Recife, Pernambuco | Associado |
| [Senior Application AI Engineer and Data Scientist - Globalization E-Invoicing Unit](https://www.linkedin.com/jobs/view/4475261580) | SAP | Grande São Paulo | Sênior/lead |
| [Senior Application AI Engineer - Globalization E-Invoicing Unit](https://www.linkedin.com/jobs/view/4475262498) | SAP | Grande São Paulo | Sênior/lead |
| [Generative AI Engineer](https://www.linkedin.com/jobs/view/4481478812) | Claro Brasil | São Paulo, São Paulo | Pleno/sênior |
| [AI Engineer Senior](https://www.linkedin.com/jobs/view/4482541880) | Hotmart | Belo Horizonte, Minas Gerais | Sênior/lead |
| [ENGENHEIRO(A) DE IA JUNIOR](https://www.linkedin.com/jobs/view/4483916028) | Agricopel | Jaraguá do Sul, Santa Catarina | Júnior |
| [Especialista em IA Generativa e Automação](https://www.linkedin.com/jobs/view/4485124293) | LUZA Group | Curitiba, Paraná | Sênior/lead |
| [Engenheiro(a) de Inteligência Artificial Sênior/Especialista](https://www.linkedin.com/jobs/view/4485214775) | FOURSYS | Osasco, São Paulo | Sênior/lead |
| [Desenvolvedor de IA Júnior](https://www.linkedin.com/jobs/view/4486251079) | Fundação CERTI | Florianópolis, Santa Catarina | Júnior |
| [Desenvolvedor de IA Pleno](https://www.linkedin.com/jobs/view/4486251087) | Fundação CERTI | Florianópolis, Santa Catarina | Pleno |
| [Senior AI Engineer (Python, LLMs) - Remote Work](https://www.linkedin.com/jobs/view/4487030019) | REF#308881 | BairesDev | Sênior/lead |
| [AI Engineer](https://www.linkedin.com/jobs/view/4487253658) | AMP | Alvarez & Marsal | Não informado |
| [Engenheiro(a) de Inteligência Artificial Sênior](https://www.linkedin.com/jobs/view/4488896301) | Petlove | Brazil | Sênior/lead |
| [Desenvolvedor de Inteligência Artificial](https://www.linkedin.com/jobs/view/4489904938) | Mais Contabilidade | Santo André, São Paulo | Não informado |
| [Machine Learning Engineer](https://www.linkedin.com/jobs/view/4489918821) | Bull | Monções, São Paulo | Não informado |
| [AI Engineer (Amazon Bedrock & LangChain) - Remote Work](https://www.linkedin.com/jobs/view/4491709575) | REF#311040 | BairesDev | Não informado |
| [NLP Engineer - Remote Work](https://www.linkedin.com/jobs/view/4491712688) | REF#310145 | BairesDev | Não informado |
| [AI Engineer](https://www.linkedin.com/jobs/view/4492090716) | BEES Brasil | Campinas, São Paulo | Pleno/sênior |
| [Engenheiro(a) de IA Sênior](https://www.linkedin.com/jobs/view/4492526662) | Clínica Experts | Lajeado, Rio Grande do Sul | Sênior/lead |
| [Senior AI Engineer](https://www.linkedin.com/jobs/view/4494397562) | Keyrus | São Paulo, São Paulo | Sênior/lead |
| [Analista Sênior de Engenharia de IA](https://www.linkedin.com/jobs/view/4494743737) | Accenture Brasil | São Paulo, São Paulo | Sênior/lead |

claude - pessoal, 25/11/2026.
