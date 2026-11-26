# 02 — RAG de produção com pgvector

Fluxo completo: PDF com tabela → trechos → embeddings → PostgreSQL + `pgvector` (índice HNSW por cosseno) e busca lexical (`tsvector` em português) → fusão RRF → reranker → resposta com citações `[T1]` → métricas.

- `rag_ingestao.py`: lê o PDF em modo `layout` (pypdf), transforma blocos alinhados em tabela Markdown e repete o cabeçalho em cada pedaço; texto corrido em janelas com sobreposição.
- `rag_store.py`: `EmbedderOpenAICompativel` (`/v1/embeddings`), `ArmazemPgvector` (SQL parametrizado, sem sintaxe de busca vinda do usuário) e `ArmazemMemoria`/`EmbedderHash` para testes.
- `rag_pipeline.py`: RRF, `ReordenadorLexico`, `ReordenadorLLM` (nota 0–3, falha segura), recall@k, MRR, nDCG@k e fidelidade lexical (frases apoiadas no trecho citado).
- `corpus_aurora.py` e `dados/consultas_ouro.json`: corpus fictício (`12` PDFs, `41` trechos com `4` tabelas Markdown, versões conflitantes 2024 vs 2026, distrações lexicais e documentos restritos por perfil) e `28` consultas ouro (incluindo versões conflitantes, ACL e `3` sem resposta).
- `rag_store.py` e `rag_pipeline.py`: `FiltroBusca` com pré-filtragem SQL parametrizada (ACL por `perfis` e `vigente`) antes do `ORDER BY ... LIMIT`, modos `vetorial`, `lexical` e `hibrida` (RRF), `ReordenadorLexico`, `ReordenadorLLM` e `auditar_acl`.
- `gerar_corpus_ampliado.py`, `dados/corpus_ampliado.json` e `dados/consultas_ampliadas.json` (Etapa 3): mais `45` documentos fictícios (`8` restritos a docente, coordenação ou admin) e `123` perguntas gerados pelo `qwen3.8:27b-ud-iq3_xxs`. Uma pergunta só entrou se o trecho literal e a resposta curta estivessem no documento e o critério resolvesse para um trecho da segmentação real (`12` descartadas). O assunto do documento abre cada pergunta, porque num corpus de `57` documentos "qual a multa?" é ambígua. `corpus_aurora.documentos(ampliado=True)` e `carregar_consultas(ampliado=True)` ligam a ampliação; o P06 segue no corpus base.
- `reescrever_perguntas.py` (26/11/2026): tira o prefixo "Sobre <tema>:" das `123` perguntas novas. O 27B reescreve cada uma como quem usa o atendimento escreveria; travas determinísticas recusam a reescrita que repete o tema, a resposta ou o trecho, e o mesmo LLM confere às cegas se o sentido se manteve. A pergunta gerada fica em `pergunta_original` (o P07 usa essa). **Execução pendente.**
- `executar_rag_real.py`: ingestão, comparação de `5` variantes (`vetorial`, `lexical`, `hibrida_rrf`, `hibrida_reranker_lexico`, `hibrida_reranker_llm`), auditoria de vazamentos ACL e geração. `--corpus base|ampliado` (padrão `ampliado`), `--cache-llm` para retomar execuções longas, `--fracao-selecao` (padrão `0.5`: metade das perguntas escolhe a variante, a outra metade testa) e `estatistica_recuperacao` no registro, só nas perguntas de teste: acerto@k por pergunta com Wilson 95% por variante e a variante escolhida contra cada outra (McNemar exato no acerto@k e bootstrap pareado no MRR).

## Execução real

```bash
podman compose -f laboratorios-mercado/compose.yaml --profile serving --profile rag up -d
PGVECTOR_DSN=postgresql://aurora:senha-local-de-laboratorio@127.0.0.1:5433/rag \
.venv-mercado/bin/python -I laboratorios-mercado/02_rag_producao/executar_rag_real.py \
  --embed-base-url http://127.0.0.1:8082/v1 --embed-modelo embed-local \
  --llm-base-url http://127.0.0.1:8081/v1 --llm-modelo modelo-local --registrar
```

Resultado da Fase 6 (`25/11/2026`, `qwen3-embedding:0.6b` + `qwen3:4b-instruct`, `12` PDFs, `41` trechos, `28` consultas): `auditoria_acl` com `0` vazamentos em `4` consultas restritas; `recall@4` `1,0` (`vetorial`), `0,92` (`lexical`), `0,98` (`híbrida RRF`), `0,94` (*reranker* léxico) e `0,98` (*reranker* LLM); MRR `0,9333` (`vetorial`), `0,92` (`híbrida RRF`), `0,88` (*reranker* LLM); geração com `23/25` conteúdos esperados, `3/3` recusas corretas e fidelidade lexical média `0,84`.

Na comparação em GPU via Ollama `/v1` (`25/11/2026`, `LLM_REASONING_EFFORT=none`): `qwen3:4b-instruct` teve `reranker` LLM com MRR `0,90`, `23/25` acertos, fidelidade `0,84` e latência p50/p95 `300,1 / 538,9 ms`; `qwen3.8:27b-ud-iq3_xxs` elevou o `reranker` LLM para **MRR `0,98` / recall `1,0`**, `24/25` acertos (o caso restante usou `"décimo dia útil"` com acento), `3/3` recusas, **fidelidade `1,0`** e latência p50/p95 `1.422,5 / 2.182,6 ms` (`11,14 GiB` em VRAM com o *embedder*).

Limites: cada operação abre uma conexão (simples para estudo; em produção use `psycopg_pool`); a fidelidade lexical não reconhece paráfrase (ex.: `q01` citou a data do calendário em vez do texto do regulamento) e serve só de portão barato antes de avaliador por LLM ou humano; PDFs escaneados ou tabelas sem alinhamento de texto exigem OCR ou extrator de layout (ou extração VLM no Projeto 07).

**Etapa 3 — escala (26/11/2026; `execucoes/p02-rag-pgvector-2026-11-26T02-21-48-0300.json`):** `57` documentos, `275` trechos (`60` restritos, `4` revogados, `4` tabelas), `151` perguntas (`148` com resposta, `3` sem resposta), `qwen3-embedding:0.6b` + `qwen3.8:27b-ud-iq3_xxs` no Ollama `/v1`, `k = 4`.

| Variante | recall@4 | MRR | Acerto@4 (n = `148`) | Wilson 95% |
|---|---|---|---|---|
| vetorial | `0,801` | `0,665` | `119` | [`0,73`; `0,86`] |
| lexical | `0,794` | `0,677` | `119` | [`0,73`; `0,86`] |
| híbrida RRF | `0,824` | `0,684` | `123` | [`0,76`; `0,88`] |
| híbrida + *reranker* léxico | `0,835` | `0,680` | `125` | [`0,78`; `0,89`] |
| **híbrida + *reranker* LLM** | **`0,902`** | **`0,846`** | **`134`** | [`0,85`; `0,94`] |

**Seleção separada do teste (26/11/2026; `execucoes/p02-rag-pgvector-2026-11-26T06-21-09-0300.json`):** `--fracao-selecao 0.5` separa as `148` perguntas por hash. `74` escolhem a variante pelo MRR, e o *reranker* LLM vence (`0,891` contra `0,738` do segundo). As outras `74` medem, sem ter influído na escolha:

| Variante (teste, n = `74`) | Acerto@4 | Wilson 95% |
|---|---|---|
| vetorial / lexical | `56` | [`0,65`; `0,84`] |
| híbrida RRF / + *reranker* léxico | `59` | [`0,69`; `0,87`] |
| **híbrida + *reranker* LLM** | **`63`** | [`0,75`; `0,91`] |

No MRR, o *reranker* LLM ganha de `+0,16` a `+0,18` contra todas as outras, com IC 95% por bootstrap acima de zero: ele põe o trecho certo mais no alto. No acerto@4, vence a vetorial (`8` ganhos e `1` perda, McNemar `p = 0,04`) e a lexical (`7` e `0`, `p = 0,016`), mas **não** as híbridas (`4` e `0`, `p = 0,125`; `5` e `1`, `p = 0,22`). Com `74` perguntas, essa diferença ainda pode ser acaso. Na tabela acima, a escolha e a medida usaram as mesmas `148` perguntas, então os p-valores daquela versão (de `0,0003` a `0,02`) eram otimistas. ACL: `0` vazamentos em `26` consultas restritas. Geração: conteúdo esperado em `127/148` (Wilson [`0,79`; `0,91`]), fidelidade lexical `0,881`, `3/3` recusas e latência p50/p95 `1.337 / 1.643 ms`. Na amostra de `28` perguntas (Etapa 2), o recall@4 era `1,0`: a escala mostrou que a busca sem *reranker* erra quase `1` em cada `5` perguntas.

**Limites:** documentos e perguntas vêm do mesmo LLM. A revisão amostral foi feita por modelo de fronteira, não por pessoa (26/11/2026, [registro](../execucoes/revisao-fronteira-etapa-3-2026-11-26.json)): `12/12` perguntas respondíveis pelo trecho esperado, `2` referências imprecisas (unidade trocada e condição omitida), e todas as `123` perguntas começam por "Sobre <tema do documento>:". Esse prefixo repete o vocabulário usado para gerar o documento e facilita a recuperação; os números abaixo tendem a ser otimistas até a execução de `reescrever_perguntas.py` e uma nova rodada do P02. A execução levou `3` passadas com cache (`--cache-llm`): `2.543` chamadas ao LLM (o *reranker* faz `8` por pergunta), as latências registradas são as medidas na chamada original.
