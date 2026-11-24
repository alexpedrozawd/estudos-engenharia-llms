# Changelog: Ajustes pontuais nos laboratórios/docs e plano rumo à nota 10 — 24/11/2026

Registra a auditoria/revisão crítica de mercado do guia (`7,2 / 10`), a correção dos defeitos pontuais comprovados nos laboratórios e na higiene documental, e o plano estruturado rumo à nota 10 em [plano-evolucao-mercado-e-nota-10-2026-11-24.md](plano-evolucao-mercado-e-nota-10-2026-11-24.md). O HTML e o PDF principais permaneceram inalterados.

## Autoria

- **24/11/2026, `agy - ap`:** auditoria/revisão, correções pontuais de código/documentação, criação do plano em 5 fases (`5A`–`5E`), validações e fechamento Git.

## O que mudou

- **Correção de `logprob_medio` no Lab 01 ([tokens_e_amostragem.py](laboratorios/lab_01_fundamentos/tokens_e_amostragem.py)):**
  - `inspecionar_logprobs_remoto()` deixou de retornar `-0.12` fixo no modo HTTP e passou a calcular a média real a partir de `choices[0].logprobs.content` (retornando `None` quando ausente).
  - Cobertura adicionada em [test_lab_01.py](laboratorios/lab_01_fundamentos/test_lab_01.py).
- **Adaptadores HTTP reais opcionais ([cliente_llm.py](laboratorios/comum/cliente_llm.py)):**
  - Adicionados `ClienteHTTPOpenAICompativel`, `ClienteHTTPAnthropic`, `ClienteHTTPGemini` (chave enviada apenas em `x-goog-api-key`), `ClienteHTTPOllama` e fábrica `criar_cliente_por_ambiente()`, mantendo 100% de retrocompatibilidade com `ClienteMockDeterministico`.
  - Cobertura determinística sem rede via `opener` fake em [test_cliente_llm.py](laboratorios/comum/test_cliente_llm.py) e alinhamento de [laboratorios/README.md](laboratorios/README.md).
- **Higiene documental (3 itens baixos):**
  - Substituídos 6 links absolutos `file:///D:/...` por links relativos em [fabricas-de-agentes-e-o-papel-do-operador-de-llms.md](fabricas-de-agentes-e-o-papel-do-operador-de-llms.md).
  - Removido link quebrado para arquivo movido a `arquivo/` em [planejamento-capitulo-5-avaliacao-e-experimentacao.md](planejamento-capitulo-5-avaliacao-e-experimentacao.md).
  - Marcada como histórica a nota de preflight de 10/11/2026 em [CLAUDE.md](CLAUDE.md).
- **Planejamento (somente plano, sem implementação):**
  - Criado [plano-evolucao-mercado-e-nota-10-2026-11-24.md](plano-evolucao-mercado-e-nota-10-2026-11-24.md) com as Fases `5A` (lacunas 2026), `5B` (questões e estudos de caso), `5C` (diagramas SVG e decisão `18` vs. `73` aquarelas), `5D` (Camada 3 prática de mercado com 6 projetos reais) e `5E` (`L1`/`L2` humanos + `L8` + PDF definitivo).
  - Atualizados [CLAUDE.md](CLAUDE.md), [README.md](README.md) e [roadmap.md](roadmap.md).

## Hashes (SHA-256, 16 primeiros dígitos)

- `guia-engenharia-llms.html`: `eff7ad47d12bf57a` (inalterado)
- `guia-engenharia-llms.pdf`: `53129052eebf7800` (inalterado)
- `laboratorios/lab_01_fundamentos/tokens_e_amostragem.py`: `5eeb1ff42cf3d118`
- `laboratorios/lab_01_fundamentos/test_lab_01.py`: `aea580e6e1bb1b16`
- `laboratorios/comum/cliente_llm.py`: `6ee8e232728ed5d9`
- `laboratorios/comum/test_cliente_llm.py`: `105cd918a0dc39cb`
- `laboratorios/README.md`: `1dd6e478163a52f2`
- `fabricas-de-agentes-e-o-papel-do-operador-de-llms.md`: `4d47413c63c52243`
- `planejamento-capitulo-5-avaliacao-e-experimentacao.md`: `a634aa2700f98aed`
- `plano-evolucao-mercado-e-nota-10-2026-11-24.md`: `201e10158aaed8d0`

## Validações executadas

- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: `Ran 84 tests in 0.201s -> OK` (sem `ResourceWarning`).
- `python3 -I ferramentas/guia.py fechar`: `0` falhas (`16 OK, 0 FALHA` em `validar-guia.py`; `26 OK, 0 FALHA` em `executar-trechos-de-codigo.py`).
- `python3 -I ferramentas/testar-ferramentas.py`: `Ran 15 tests in 34.448s -> OK`.
- `python3 -I -W error::ResourceWarning ferramentas/testar-fontes.py`: `Ran 14 tests in 0.544s -> OK`.
- `python3 -I ferramentas/testar-livros.py`: `Ran 2 tests in 0.100s -> OK`.
- `audit-surface.py --lenses docs,qa`: zero links locais quebrados nos arquivos versionados.

Assinatura: agy - ap (24/11/2026).