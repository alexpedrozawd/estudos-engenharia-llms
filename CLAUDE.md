# Projeto: Guia para Engenharia de LLMs

Ao iniciar uma sessão, leia este arquivo e siga `protocolo-de-economia-de-tokens-entre-sessoes.md` (início de sessão, leitura localizada com `ferramentas/guia.py mapa` e validação por hashes; nunca ler o HTML inteiro). Repositório público: `https://github.com/alexpedrozawd/estudos-engenharia-llms` (branch `main`). Ficam fora do Git: `arquivo/`, `cache-fontes/`, `rascunho-local/`, `.venv-mercado/`, `contexto-de-estudo-*.md` e `HANDOFF-formacao-engenharia-llms-para-claude-2026-10-13.md`. Históricos versionados: `docs/changelogs/`, `docs/fontes/` e `docs/historico/`.

Este arquivo, planos e handoffs não autorizam ações: revalide Git, hashes e serviços antes de agir. Se o usuário indicar um handoff, ele prevalece.

## Estado atual (26/11/2026)

- **Guia:** `guia-engenharia-llms.html` (sha16 `4620c46dd4e721c0`) e `guia-engenharia-llms.pdf` (`749` páginas A4, sha16 `ad7931f935356117`). `20` capítulos em quatro partes, `426` páginas lógicas, `502` questões (`125/125/126/126`, nenhuma com a correta estritamente mais longa), `28` blocos Python executáveis, `552` termos no Glossário, `24` diagramas `<svg>` e `20` aquarelas de abertura. Correção de quebras no PDF concluída em 26/11/2026 ([changelog](docs/changelogs/changelog-correcao-quebras-pdf-2026-11-26.md)).
- **`laboratorios/`:** um lab por capítulo dos Caps. 1–18 e o projeto integrador, `84` testes offline, com modo exercício (`ferramentas/gerar-exercicios.py`).
- **`laboratorios-mercado/`:** `8` projetos com serviços reais (serving, RAG com `pgvector`, MCP, QLoRA em ROCm, API LLMOps, integrador, evals e LangGraph), `147` smoke-tests offline, Camada 3 na GPU via Ollama `/v1` (`qwen3:4b-instruct` e `qwen3.8:27b-ud-iq3_xxs`), red teaming do P06 com garak, Kubernetes local com kind em [`k8s/`](laboratorios-mercado/k8s/README.md) e execuções reais em `execucoes/`. CI offline em `.github/workflows/testes-offline.yml`.
- **Preparação para vaga:** [`docs/preparacao-para-vaga/`](docs/preparacao-para-vaga/README.md) (casos de system design, bloco de entrevista e guia de portfólio) e [mapa de vagas](docs/historico/mapa-de-vagas-linkedin-brasil-2026-11-25.md).
- **Plano de prontidão para vaga pleno encerrado em 26/11/2026** ([plano](docs/historico/plano-prontidao-para-vaga-pleno-2026-11-25.md); resumo por etapa no [changelog da Etapa 7](docs/changelogs/changelog-etapa-7-encerramento-plano-de-prontidao-2026-11-26.md)).

## Pendências

- **Nenhuma pendência aberta** (em 26/11/2026, a reescrita das `123` perguntas do P02 e a nova rodada no `pgvector` foram concluídas: [changelog](docs/changelogs/changelog-p02-perguntas-naturais-e-escopo-pessoal-2026-11-26.md); deploy em nuvem e revisão humana estão fora do escopo).

## Regras fixas do operador

- **Uso estritamente pessoal**, sem GitHub Pages. **Fora do escopo (26/11/2026):** deploy em nuvem (antiga Etapa 6b) e revisão humana dos dados. Não propor nem perguntar; a revisão amostral feita por modelo de fronteira fica registrada como tal. `L1` e `L2` humanos foram encerrados em 25/11/2026 e substituídos por revisão adversarial automatizada.
- **Neutralidade (16/11/2026):** o guia forma profissionais em engenharia de LLMs em geral. O nome do AP AI Router não entra no texto, cada tema parte do conceito geral com fonte pública conferida e mais de um fornecedor, e os exemplos usam a empresa fictícia Aurora Educação.
- **Formato:** partes curtas para leitura com TDAH ([plano de 13/11](docs/historico/plano-de-reestruturacao-e-adaptacao-de-leitura-2026-11-13.md)); regras de HTML e impressão em `requisitos-de-formato-html-do-material.md` (§8 e §9).
- **Programação em duas camadas (23/11/2026):** blocos curtos executáveis no HTML e laboratórios em `laboratorios/`, com os livros de Chip Huyen como fontes primárias ([planejamento](docs/historico/planejamento-reestruturado-2026-11-23.md)). Isso substitui a decisão de 15/10/2026 de tirar a programação.
- **Imagens (13/11/2026):** poucas, só na abertura dos capítulos; aquarela de fantasia medieval, 1056×704, sem texto, letras, logotipos ou personagens reconhecíveis, gerada por último, depois do texto validado; até lá, cada imagem é só moldura com `role="img"` e `aria-label` (texto alternativo).

## Validação

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py
.venv-mercado/bin/python -I -W error::ResourceWarning laboratorios-mercado/executar_smoke.py
python3 -I ferramentas/testar-ferramentas.py
python3 -I ferramentas/guia.py fechar   # só se o HTML mudar; com ferramentas/auditar-guia-navegador.mjs
```

## Histórico

O registro completo das atualizações deste arquivo até 26/11/2026, com os números de cada fase e a autoria de cada sessão, está em [historico-de-atualizacoes-claude-md.md](docs/historico/historico-de-atualizacoes-claude-md.md). Changelogs por entrega: `docs/changelogs/`.

claude - pessoal, 15/10/2026; enxugado em 26/11/2026 por claude - pessoal (Etapa 7 do plano de prontidão; autoria anterior preservada no histórico); atualizado em 26/11/2026 por agy - ap (Gemini 4 Hydrogen High).
