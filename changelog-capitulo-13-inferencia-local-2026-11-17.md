# Changelog: Capítulo 13 — Inferência local (17/11/2026)

Autoria: claude - pessoal (Sonnet 5.5 High, painel). Segundo capítulo da Parte III.

## O que mudou
- `guia-engenharia-llms.html`: Capítulo 13 (abertura, 18 partes `13.1a`–`13.6c`, 6 questões `c13q1`–`c13q6`, 5 molduras de imagem sem geração), 12 termos novos no Glossário (336 no total), bloco *Fontes do capítulo 13* nas Referências, Sumário com as seis unidades e listas de `@media print` com `#capitulo-13` e `#questoes-capitulo-13`.
- `pacote-de-fontes-capitulo-13-inferencia-local-2026-11-17.md`: 20 fontes, 77 trechos literais, 0 reprovados. Trechos já citados nos Capítulos 1 e 2 (Mixtral 47B/13B, decodificação especulativa 2X-3X, `--parallel`) foram trocados por outros; esses temas aparecem por remissão a 1.2d, 1.5c e 2.6a.
- `planejamento-completo-estudos-engenharia-llms.md` e `CLAUDE.md`: Módulo 13 concluído e contagens atualizadas.

## Decisões e ressalvas
- Valores numéricos de tabelas (bits por peso e GiB do Llama 3.1 8B, parâmetros do Gemma 4) entram como trecho de uma célula, porque o conferidor rejeita o caractere `|`. As velocidades (tokens por segundo) da tabela do llama.cpp foram deixadas de fora: são de uma máquina específica.
- A fórmula de memória do KV cache só tem como fonte literal o exemplo do OPT-13B (PagedAttention); o modelo ilustrativo (40 camadas, 8 cabeças KV, dimensão 128) é proposta didática. O guia não calcula a memória de contexto do Qwen3.8 nem do Gemma 4, porque as fichas não detalham o armazenamento por tipo de camada (atenção linear e janela deslizante).
- As duas páginas do Ollama divergem sobre o contexto padrão (FAQ: 4096 tokens; *Context length*: por VRAM). O guia usa a segunda e registra a divergência na parte 13.2c.
- Documentação de runtimes muda sem aviso; valores e opções valem como estado de 17/11/2026.

## Validação (17/11/2026)
- `conferir-trechos.py`: 77 aprovados, 0 reprovados. `validar-guia.py`: 16 OK, 0 FALHA.
- Verificação estrutural: 20 seções, nenhuma parte acima de 500 palavras (maior: 388), 107/107 tabelas com `.rolagem`, `page-nav` sequencial, níveis 2/3/1, zero termos proibidos, Glossário sem duplicatas e em ordem, todo termo novo com `<dfn>` no texto.
- Chrome em 320 px: `clientWidth` 305 = `scrollWidth` 305, 0 estouros em 23 seções; retorno interativo conferido.

## Hashes (16)
`guia-engenharia-llms.html` `10a6591c20d7b740`; pacote do Cap. 13 `42becc9b9c01c227`; `planejamento-completo-estudos-engenharia-llms.md` `c9f05e3278ad56ff`.

Assinatura: claude - pessoal, 17/11/2026.
