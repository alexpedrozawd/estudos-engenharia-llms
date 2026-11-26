# Mapa de vagas — engenharia de LLMs no Brasil (LinkedIn, 25/11/2026)

Insumo da etapa 5 do [plano de prontidão](plano-prontidao-para-vaga-pleno-2026-11-25.md), antecipado por pedido do operador (prioridade para vagas no Brasil).

**Reconferido em 26/11/2026** (seção [Reconferência](#reconferência-em-26112026-55-vagas)): amostra ampliada para `55` vagas abertas, regra de 1/3 reaplicada sem nova lacuna prática.

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

## Reconferência em 26/11/2026 (55 vagas)

- **Coleta:** mesma rota pública e os mesmos `5` termos, mais `Engenheiro de IA Pleno` e `AI Engineer Pleno` (a amostra de 25/11 tinha só `1` vaga pleno), duas páginas por termo, `71` anúncios. Descrições das vagas já vistas reaproveitadas do cache de 25/11.
- **Seleção:** remoção de `8` repetições (mesmo texto de descrição em outro anúncio), da vaga encerrada e das vagas sem foco explícito em LLM ou IA generativa na descrição (`10`, quase todas de ML clássico; `2` delas estavam na amostra de 25/11).
- **Situação das 29 vagas de 25/11:** `28` seguem abertas; a da Claro Brasil (`4481478812`) não aceita mais candidaturas. Com o filtro de foco, `26` continuam na amostra. Entram `29` novas (tabela no fim).
- **Senioridade pelo título:** `26` sênior, lead ou especialista, `2` pleno, `5` júnior e `22` sem nível (no LinkedIn: `8` "Mid-Senior", `2` "Associate", `12` sem informação). O mercado segue pedindo mais senioridade do que "pleno".
- **Limites:** os mesmos de 25/11 (expressões regulares, sem separar obrigatório de desejável). As categorias agregadas abaixo usam expressões novas, então a comparação com 25/11 é aproximada. Scripts, descrições e matriz em `rascunho-local/vagas-linkedin-2026-11-26/` (fora do Git).

| Requisito | Vagas (55) | % | Sem nível sênior no título (29) | Cobertura no projeto em 26/11 |
|---|---:|---:|---:|---|
| Agentes | 46 | 84 | 76% | Forte (Caps. 11 e 19, P03, P06, P08) |
| APIs / integração | 44 | 80 | 72% | Forte (P05, P06) |
| RAG | 43 | 78 | 69% | Forte (Cap. 7, P02) |
| Python | 42 | 76 | 83% | Forte |
| Arquitetura / system design | 40 | 73 | 69% | Conceitual forte; treino em [casos de system design](../preparacao-para-vaga/casos-de-system-design.md) |
| Comunicação com negócio | 38 | 69 | 69% | Cap. 3; treino em [entrevista](../preparacao-para-vaga/entrevista-comunicacao-e-diagnostico.md) |
| Custo e latência | 36 | 65 | 62% | Forte (Caps. 14, 16 e 18) |
| Avaliação (evals) | 33 | 60 | 52% | Forte (Cap. 5, P07) |
| Observabilidade | 32 | 58 | 48% | Boa (OTLP, Prometheus, Jaeger, Langfuse) |
| Prompt | 31 | 56 | 55% | Forte (Cap. 4) |
| Nuvem (AWS, Azure ou GCP) | 29 | 53 | 55% | Cap. 20 e P06 com provedores testados offline; deploy real descartado pelo operador (uso pessoal) |
| Framework de LLM/agentes | 25 | 45 | 41% | Cap. 19 e P08 (LangGraph + `ChatOpenAI` do LangChain) |
| Inglês | 24 | 44 | 41% | Fora do escopo do guia |
| Multiagentes | 20 | 36 | 34% | P08 (supervisor) |
| Guardrails / segurança | 20 | 36 | 31% | Forte (Cap. 12, P06 com red teaming) |
| API da OpenAI | 20 | 36 | — | P06 (fronteira opcional, testada offline) |
| Banco vetorial (qualquer) | 20 | 36 | 34% | `pgvector` (P02); Pinecone `7`, Weaviate `5`, FAISS `3` vagas: trade-off no caso 1 |
| LGPD / compliance | 19 | 35 | 34% | Boa (Cap. 12, P06) |
| LangChain / LangGraph | 19 / 17 | 35 / 31 | 24% / 28% | P08 |
| Docker / CI/CD | 16 cada | 29 | 24% (Docker) | Podman, `Containerfile` e CI |
| MCP | 16 | 29 | 21% | Cap. 10, P03 |
| Fine-tuning | 13 | 24 | 24% | Cap. 15, P04 |
| Rastreamento de LLM (Langfuse, LangSmith, Phoenix/Arize) | 9 | 16 | — | Langfuse auto-hospedado (17.4e) |
| Kubernetes | 8 | 15 | 21% | Etapa 6a (opcional) |

**Regra de 1/3 reaplicada:** nenhum requisito sem prática passou do corte. Nuvem (`53%`) tem prática sem custo, e o deploy real foi descartado pelo operador em 26/11/2026 (uso pessoal). Bancos vetoriais gerenciados continuam abaixo do corte cada um (`≤ 13%`) e ficam como trade-off. Nas vagas sem nível sênior no título, o perfil é o mesmo: agentes, RAG, Python, APIs, arquitetura e comunicação a partir de `69%`.

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
| [Generative AI Engineer](https://www.linkedin.com/jobs/view/4481478812) | Claro Brasil | São Paulo, São Paulo | Pleno/sênior (encerrada em 26/11) |
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

## Vagas novas na reconferência de 26/11/2026

| Vaga | Empresa | Local | Nível |
|---|---|---|---|
| [AI/ML Engineer](https://www.linkedin.com/jobs/view/4415690659) | Perform | São Paulo, São Paulo | Não informado (Mid-Senior) |
| [Pipeline - Engenheiro de IA - Pleno](https://www.linkedin.com/jobs/view/4415726843) | EY | Fortaleza, Ceará | Pleno |
| [Engenheiro de IA (Senior)](https://www.linkedin.com/jobs/view/4454140268) | EY | São Paulo, São Paulo | Sênior/lead |
| [Engenheiro(a) de IA Generativa](https://www.linkedin.com/jobs/view/4455974806) | 4DF Connect | São Paulo, São Paulo | Não informado (Mid-Senior) |
| [Gestor(a) de Inteligência Artificial](https://www.linkedin.com/jobs/view/4461462345) | Engeform | São Paulo, São Paulo | Não informado |
| [Software Dev Engineer - AI Agents, IES LATech](https://www.linkedin.com/jobs/view/4466010041) | Amazon | Grande São Paulo | Não informado |
| [Staff AI Engineer (Agentic Systems)](https://www.linkedin.com/jobs/view/4468777459) | Livelo Brasil | Barueri, São Paulo | Sênior/lead |
| [Pessoa Engenheira de IA](https://www.linkedin.com/jobs/view/4472641584) | Volkswagen do Brasil | São Bernardo do Campo, São Paulo | Não informado |
| [Engenheiro de IA](https://www.linkedin.com/jobs/view/4473372497) | Jump | São Paulo, São Paulo | Não informado |
| [AI Engineer - GenAI, LLMs & AI Agents](https://www.linkedin.com/jobs/view/4474355836) | 4DF Connect | Joinville, Santa Catarina | Não informado (Mid-Senior) |
| [Especialista em Engenharia de IA - Holding](https://www.linkedin.com/jobs/view/4474630588) | JHSF | São Paulo, São Paulo | Sênior/lead |
| [AI Engineer (Developer) - Autonomous Compliance Foundation](https://www.linkedin.com/jobs/view/4477017254) | SAP | Grande São Paulo | Não informado (Mid-Senior) |
| [Senior AI Engineer (Developer) - Autonomous Compliance Foundation](https://www.linkedin.com/jobs/view/4477018184) | SAP | Grande São Paulo | Sênior/lead |
| [Engenheiro de IA Sênior](https://www.linkedin.com/jobs/view/4479116355) | Selbetti Tecnologia | São Paulo, São Paulo | Sênior/lead |
| [Senior AI Engineer](https://www.linkedin.com/jobs/view/4479839763) | Artefact | Grande São Paulo | Sênior/lead |
| [Analista de Inteligência Artificial](https://www.linkedin.com/jobs/view/4480063337) | Grupo Alves da Cunha | Salvador, Bahia | Não informado |
| [Pessoa Desenvolvedora (.Net + IA Generativa)](https://www.linkedin.com/jobs/view/4480269105) | MJV Technology & Innovation | São Paulo, São Paulo | Não informado |
| [Engenheiro de Machine Learning / IA - presencial em São Paulo](https://www.linkedin.com/jobs/view/4483166734) | 4DF Connect | São Paulo, São Paulo | Não informado (Mid-Senior) |
| [Machine Learning Engineer](https://www.linkedin.com/jobs/view/4485366988) | 4flow | Campinas, São Paulo | Não informado (Associate) |
| [(1609) Senior AI Engineer (Full Stack)](https://www.linkedin.com/jobs/view/4487023121) | Nortal | Grande Rio de Janeiro | Sênior/lead |
| [Desenvolvedor(a) de Agentes de IA](https://www.linkedin.com/jobs/view/4487096360) | Loovi | Grande Belo Horizonte | Não informado (Mid-Senior) |
| [Senior Software Engineer, AI Assistant (Bella)](https://www.linkedin.com/jobs/view/4490820903) | ejobs Finland | Brasília, Distrito Federal | Sênior/lead |
| [Engenheiro(a) de Inteligência Artificial - AI Engineer](https://www.linkedin.com/jobs/view/4492110536) | nommad | São Paulo, São Paulo | Não informado (Mid-Senior) |
| [Senior AI Engineer (Internal Tools & Agents)](https://www.linkedin.com/jobs/view/4492581494) | Jobgether | Brasil | Sênior/lead |
| [Software Engineer I - GenAI (CLT) - Remoto](https://www.linkedin.com/jobs/view/4492655776) | GRAN | Brasil | Júnior |
| [Junior Forward Deployed AI Engineer - AI/ML & Data Track](https://www.linkedin.com/jobs/view/4493217970) | FullStack | Manaus, Amazonas | Júnior |
| [Junior Forward Deployed AI Engineer - Application Engineering](https://www.linkedin.com/jobs/view/4493225271) | FullStack | Manaus, Amazonas | Júnior |
| [AI Applied Engineer](https://www.linkedin.com/jobs/view/4493391930) | Artefact | Grande São Paulo | Não informado |
| [Engenheiro de Inteligência Artificial](https://www.linkedin.com/jobs/view/4493472261) | LICAV | Limeira, São Paulo | Não informado |

claude - pessoal, 25/11/2026; reconferido em 26/11/2026 por claude - pessoal.
