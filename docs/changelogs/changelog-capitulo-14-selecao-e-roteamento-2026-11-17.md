# Changelog: Capítulo 14 — Seleção e roteamento (17/11/2026)

Autoria: deepseek - painel, continuando a sessão iniciada por claude - pessoal (Sonnet 5.5 High), que montou o pacote de fontes antes da pausa pedida pelo operador. Terceiro capítulo da Parte III.

## O que mudou
- `guia-engenharia-llms.html`: Capítulo 14 (abertura, 18 partes `14.1a`–`14.6c`, 6 questões `c14q1`–`c14q6`, 4 molduras de imagem sem geração), 14 termos novos no Glossário (350 no total), bloco *Fontes do capítulo 14* nas Referências, Sumário com as seis unidades e listas de `@media print` com `#capitulo-14` e `#questoes-capitulo-14`. Glossário passou para a p. 296 e Referências para a 297.
- `pacote-de-fontes-capitulo-14-selecao-e-roteamento-2026-11-17.md`: 17 fontes, 59 trechos literais, 0 reprovados (conferência feita nesta sessão).
- `planejamento-completo-estudos-engenharia-llms.md` e `CLAUDE.md`: Módulo 14 marcado como concluído, contagens atualizadas e ponteiro de leitura inicial corrigido (o estado mais recente passa a estar no `CLAUDE.md`, porque não há handoff posterior ao da Parte II).
- `README.md`: estado atual atualizado de "Capítulos 1 a 8" para "1 a 14", com a Parte III e o próximo capítulo; a defasagem vinha de cinco commits atrás.

## Decisões e ressalvas
- O guia não reproduz nomes de modelo no texto corrido: o capítulo trabalha com faixas (rápido, intermediário, fronteira) e registra a data da consulta. Os trechos literais preservam o texto original nas notas de fonte.
- A hipótese de que trocar de modelo invalida o cache de prefixo na Anthropic e no Google segue sem fonte literal. O capítulo a trata como regra prudente e declara a lacuna na parte 14.6c; a base é a frase da OpenAI de que modelo diferente pode ter pesos e comportamento de cache diferentes.
- Matriz por finalidade, níveis de supervisão humana, gatilhos de reavaliação e o registro de decisão de rota são *proposta didática*. Os benchmarks citados (IFEval, LiveCodeBench, SWE-bench, Verified e Pro) aparecem com o limite de leitura de cada um.
- A página *Introducing SWE-bench Verified* da OpenAI respondeu 403 ao acesso automatizado; o guia usa a página do próprio SWE-bench, que descreve o subconjunto.

## Validação (17/11/2026)
- `conferir-trechos.py`: 59 aprovados, 0 reprovados. `validar-guia.py`: 16 OK, 0 FALHA.
- Verificação estrutural: 20 seções, nenhuma parte acima de 500 palavras (maior: 394), 120/120 tabelas com `.rolagem`, `page-nav` sequencial, níveis 2/3/1, zero termos proibidos, Glossário sem duplicatas e em ordem, todo termo novo com `<dfn>` no texto.
- Chrome em 320 px: `clientWidth` 305 = `scrollWidth` 305, 0 estouros em 23 seções; retorno interativo conferido.

## Hashes (16)
`guia-engenharia-llms.html` `64d6908e6cf2aeec`; pacote do Cap. 14 `7f694fcc45a71034`; `planejamento-completo-estudos-engenharia-llms.md` `697577de1376aec2`; `CLAUDE.md` `4c624470a6e8a0dc`; `README.md` `daa636c8907ad7c3`.

Assinatura: deepseek - painel, 17/11/2026.
