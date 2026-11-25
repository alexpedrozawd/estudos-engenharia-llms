# Changelog: reestruturação sem programação (15/10/2026)

Autoria: claude - pessoal (Sonnet 5.5, effort High declarado pelo operador). Plano: `planejamento-reestruturacao-sem-programacao.md`.

## Decisões do operador
- Tirar linguagens de programação do guia; foco em engenharia, arquitetura e operação de LLMs (locais ou de fronteira).
- Capítulo 2 antigo: retirar e arquivar. Critério: não ensinar nem exigir programar; texto de configuração e linhas de comando do runtime podem aparecer, só para ler.
- Manter os 15 módulos; o módulo 2 passa a "Arquitetura de sistemas com LLM" (nome provisório). Módulos 4, 5, 9, 10, 11 e 14 ficam, como arquitetura e decisão. Módulo 9 renomeado "Ferramentas e integrações".
- Chrome opcional: incluído.

## Alterações
- Arquivo `arquivo\capitulo-2-software\`: cópia do guia anterior (`guia-engenharia-llms-com-capitulo-2-2026-10-15.html`, hash `7fadf7b0cbe4cd5e`) e, movidos com hash conferido, planejamento, pacotes de fontes, changelog e dois handoffs do Capítulo 2.
- `guia-engenharia-llms.html`: removidas as páginas 11 a 18 (capítulo 2, seis unidades e cinco questões); sumário (módulo 2 como entrada futura; módulo 9 renomeado); introdução (sem pré-requisito de programação; "construí-la" e "construção" trocados); navegação da página 10 para o glossário; glossário de 91 para 45 termos; referências sem as 11 fontes exclusivas do Capítulo 2; páginas 11 e 12. Capítulo 1 sem alteração de conteúdo (diferença só no link de navegação da página 10).
- `planejamento-completo-estudos-engenharia-llms.md`: objetivo, módulo 2, módulo 9, regra "nenhum módulo ensina nem exige programar".
- `requisitos-de-formato-html-do-material.md`: questões sem "trechos de código".
- `CLAUDE.md`: aponta para o plano e o handoff da reestruturação.

## Validações executadas (15/10/2026)
- `validar-guia.py`: 15 OK, 0 FALHA (12 páginas em sequência; 5 questões).
- Resíduos (`capitulo-2`, `unidade-2-`, `cod-`, `c2q`, Python, pytest, sqlite, Pro Git, RFC) no guia: 0.
- Tags HTML equilibradas; comparação linha a linha com o arquivo: Capítulo 1 igual.
- Chrome (Playwright, `channel="chrome"`): sem rolagem horizontal em 320 e 1280 px; axe-core 4.10.2 sem violações (1 verificação incompleta, `aria-prohibited-attr`, nos números de página, já conhecida); mecânica das 5 questões do Capítulo 1: 5 de 5.

## Leitura da Fase 4 (Opus 5.5 High, effort declarado pelo operador, 15/10/2026)
- Corrigido no plano mestre: a sobreposição do módulo 2 abrange os módulos 4, 8, 11, 12, 13, 14 e 15, e não só 12, 14 e 15; "linhas de comando só para ler" vale para o texto do guia, sem contradizer os laboratórios com escopo próprio; exemplos do Router tratam a arquitetura, não o código produzido.
- Corrigido em `contexto-de-estudo-ap-ai-router.md`: nota datada no objetivo de 13/10 ("construir" passa a significar projetar, configurar e integrar).
- Apontado e resolvido no plano do módulo 2: a linha provisória do módulo 2 cita simultaneidade no texto mas não na progressão, e separa limites de novas tentativas. A linha nova entra no plano mestre e no sumário depois da aprovação do plano.
- Apontado, sem mudança agora: "busca por símbolos" (módulo 10) é orientada a código; decidir no plano do módulo 10.
- `requisitos-de-formato-html-do-material.md`: sem achado.

## Pendente
- Aprovação de `planejamento-capitulo-2-arquitetura-de-sistemas-com-llm.md` e do nome do módulo.
- Reaproveitar, com nova redação sem "Em Python", termos do glossário arquivado (idempotência, contrato, determinismo, efeito colateral, condição de corrida, espera crescente).
- Aparelhos reais; pendências 3 a 7 do handoff de 15/10 (agora no arquivo).

claude - pessoal, 15/10/2026
