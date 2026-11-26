# Changelog — Capítulo 20 (LLMs em nuvem e serviços gerenciados), P06 com provedor de nuvem e Langfuse (25/11/2026)

Autoria: claude - pessoal. Etapa 5B, segunda entrega, do [plano de prontidão para vaga pleno](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md). Lacunas fechadas: nuvem (52% das vagas do [mapa de vagas](../historico/mapa-de-vagas-linkedin-brasil-2026-11-25.md); AWS 45%, Azure 41%, GCP 34%) e rastreamento de LLM (21%). Plano aprovado pelo operador; um único commit no fim.

## Decisões do operador (25/11/2026)

- **Parte IV confirmada:** os Caps. 19 e 20 ficam na "Parte IV — Frameworks e plataformas de mercado"; a introdução passa a dizer "20 capítulos em quatro partes".
- **P06:** as três nuvens pelo endpoint compatível com OpenAI, reaproveitando `ClienteChatOpenAI`; formatos nativos (Bedrock Converse e Vertex `generateContent`) só como funções puras testadas offline. SigV4 e chamada real à nuvem ficam fora (etapa opcional 6b, com autorização).
- **Achado baixo do P08 corrigido** nesta entrega (ver abaixo).

## Fontes

[pacote-de-fontes-capitulo-20-llms-em-nuvem-e-servicos-gerenciados-2026-11-25.md](../fontes/pacote-de-fontes-capitulo-20-llms-em-nuvem-e-servicos-gerenciados-2026-11-25.md): `38` fontes (Microsoft Learn, AWS, Google Cloud, LGPD e Langfuse) e `79` trechos literais aprovados em `conferir-trechos.py`. As páginas do Microsoft Learn responderam HTTP 400 ao `urllib` do `fontes.py` e 200 ao `curl`; foram baixadas por `curl` e registradas com `fontes.py importar`. A LGPD reaproveita a cópia `lgpd-13709-atualizada` já conferida (o Planalto recusou a conexão). A documentação do Google chama hoje a plataforma de *Gemini Enterprise Agent Platform*; o capítulo usa "Vertex AI", com a nota.

## Guia (HTML e PDF)

- **Cap. 20:** abertura com aquarela, `18` partes `20.1a`–`20.6c` (nuvem gerenciada e quando usar; APIs e formatos; identidade e chaves; cotas e capacidade; residência, LGPD e rede; custo, cache e mapa para o guia), `24` questões (`18` de parte + `6` de fechamento), estudo de caso com rubrica, diagrama 20.1 (P06 com as três nuvens), bloco executável `cod-20-6a-py` (teto na aplicação contra orçamento que só alerta), sumário na Parte IV, `12` termos no Glossário e Referências.
- **Parte 17.4e — Langfuse auto-hospedado:** unidade 17.4 passa a ter 5 partes (Cap. 17 com 21 partes); o bloco "Fontes da unidade" da 17.4 foi para a 17.4e, com as fontes do Langfuse.
- **Aquarela `cap-20`:** Qwen-Image local, semente `7020` (a `6020` foi descartada por ter só dois castelos), prompt na linha `cap-20` de `arquivo/aquarelas-fase-5e/prompts.tsv`; JPEG de `84 KB` embutido.

## Código (`laboratorios-mercado/`)

- **`mercado_base/provedores_nuvem.py` (novo):** URLs e autenticação de Azure OpenAI (`/openai/v1`, `api-key` ou token do Entra ID), Bedrock (`bedrock-runtime…/openai/v1`, chave do Bedrock como Bearer) e Vertex AI (`…/endpoints/openapi`, token OAuth); validação de região, local e projeto antes de montar o host; erros que citam a variável sem o valor; leitura de `retry-after-ms` e `Retry-After`; montagem e leitura do Converse e do `generateContent`.
- **`mercado_base/cliente_openai.py`:** parâmetro opcional `cabecalhos` em `ClienteChatOpenAI` (padrão inalterado: `Authorization: Bearer`).
- **P06:** `criar_fronteira_de_ambiente` aceita `FRONTEIRA_PROVEDOR=azure|bedrock|vertex` além dos provedores anteriores; `Assistente.tracer` opcional emite um span `gen_ai.*` por pergunta, sem texto de prompt, resposta ou PII; `OTEL_EXPORTADOR` padrão `nenhum`. Contrato e testes anteriores preservados.
- **`test_p06_nuvem.py` (novo):** `13` testes offline com `httpx.MockTransport` e credenciais falsas.
- **P08:** no ramo `GraphRecursionError`, `ferramentas_chamadas` passa a vir do checkpoint (antes, lista vazia); teste reforçado.
- **`compose.yaml`:** perfil `langfuse` (Langfuse `4.86.0` web e worker, PostgreSQL, ClickHouse, Redis e MinIO), só `127.0.0.1:3000` no host, telemetria e cadastro desligados, projeto e chaves criados na inicialização. A imagem de `docker.langfuse.com` não baixou em 8 minutos; a mesma versão (mesmo digest da tag `4`) vem de `docker.io/langfuse`. CI valida o perfil (`config -q`).
- **`executar_traces_langfuse.py` (novo):** P05 (em processo) e P06 (RAG em memória) exportam por OTLP ao Langfuse e conferem a chegada em `/api/public/v2/observations` (`/api/public/traces` responde 404 no modo `events_only` da versão 4).

## Execução real (Ollama `/v1`, `qwen3:4b-instruct`)

`execucoes/p05-p06-langfuse-2026-11-25T20-11-20-0300.json`: `5/5` observações recebidas (`2` do P05 e `3` do P06, uma bloqueada pela guarda de entrada), todas do tipo `GENERATION`, com tokens de entrada, saída e cache, sem texto de entrada ou saída e sem PII. Cadastro desligado conferido: `POST /api/auth/signup` respondeu "Sign up is disabled.".

## Auditoria (`/auditorias`)

- **Médio, corrigido — contagem errada no texto:** a 20.2c dizia "14 testes" novos; são `13`.
- **Médio, corrigido — fidelidade:** frase da 20.5b sobre registro de prompts pelo Google sem trecho no pacote; acrescentado `NV-79`.
- **Médio, corrigido — atribuição:** "cadastro desligado" na 17.4e estava como documentação; passou a execução conferida.
- **Corrigidos na validação:** legenda do trecho `cod-20-4b` (convenção de ilustrativo), caixa "fábrica" do diagrama 20.1 (texto encostava na borda) e `8` questões com a correta mais longa.
- **Baixos em aberto (decisão do operador):** tokens do Entra ID e OAuth do Vertex lidos do ambiente não são renovados (um P06 de longa duração perde a rota de fronteira quando o token expira; documentado no README do P06); no Azure, se `AZURE_OPENAI_API_KEY` e `AZURE_OPENAI_AD_TOKEN` existirem, a chave tem precedência.

## Contagens e validação

- Guia: `20` capítulos, `426` páginas lógicas, `502` questões (`125/125/126/126`, nenhuma com a correta estritamente mais longa), `168/168` tabelas com `.rolagem`, `552` termos, `525` `<dfn>`, `28` blocos executáveis, `24` SVG, `20` aquarelas. HTML sha `da073a1210e36792`; PDF com `736` páginas A4 (antes `698`), sha `8431be316ec3b881`, anterior em `arquivo/antes-capitulo-20-2026-11-25/`; páginas 562 (17.4e), 645 (abertura e aquarela) e 651 (diagrama 20.1) conferidas renderizadas.
- `guia.py fechar` `0` falhas (`validar-guia` `18 OK`); `laboratorios/executar_labs.py` `84` OK; `executar_smoke.py` `113` OK (P06 `29`, P08 `13`); `testar-ferramentas.py` `24` OK; `testar-fontes.py` e `testar-livros.py` OK; `conferir-trechos.py` Cap. 20 `79/79`; `gerar-exercicios.py --checar` `82` trechos em `27` labs e `--verificar labs|mercado` OK; `auditar-guia-navegador.mjs`: `0` estouros a `320 px` em `426` seções, `502/502` questões, `0` violações axe em `1280×800` e `320×640` (`color-contrast` como incompleto).

## Próximo

Etapa 5B concluída. Seguem, no plano de prontidão, as etapas 3 e 4; a etapa 6b (deploy real em nuvem) continua opcional e depende de autorização.
