# Changelog: revisão do capítulo 4 (14/11/2026)

Autoria: claude - pessoal (Sonnet 5.5 High, painel). O handoff previa Opus 5.5 High; o operador escolheu seguir em Sonnet. Limitação: quem escreveu também revisou, então uma segunda leitura por Opus continua útil.

## Escopo revisado
Capítulo 4 inteiro (intro, 4.1a a 4.6d, questões, glossário do capítulo por amostragem de termos) contra o pacote de fontes e as páginas originais. Referências cruzadas às unidades 1.2, 1.6 e 2.2 conferidas no HTML; módulos 5 a 15 conferidos em `planejamento-completo-estudos-engenharia-llms.md`.

## Conferido nas fontes (baixadas em 14/11/2026, fora do pacote)
- Contagem de tokens: “might differ by a small amount” confere com a paráfrase da 4.4b.
- Saída estruturada: `output_config.format` confere (4.6a).
- Motivos de parada: `end_turn`, `max_tokens`, `stop_sequence`, `refusal` e a sugestão “Raise `max_tokens` or continue the response” conferem (4.5b).
- Migração 2026-10-21: a rejeição de `temperature`, `top_p` e `top_k` é por versão da API, não por modelo (confirma o gabarito da questão 4).

## Corrigido
1. 4.2a: link “anterior” levava às questões do capítulo; agora leva à 4.1c.
2. 4.2b: “o artigo não mediu” (afirmação sobre o artigo inteiro, lido só no resumo) virou “o resumo do artigo não traz”; nota de fonte idem.
3. 4.4b: razão caracteres ÷ 3,6 não foi “calibrada” (não há tokenizador); agora é “convenção deste projeto, sem medição com tokenizador”. Nota de fonte ajustada; paráfrase “erro pequeno” registrada.
4. 4.6a: o exemplo da 4.2a usa “não informada” e o schema pede `null`; frase nova explica a diferença.
5. 4.2d, alternativa D: removida a afirmação “como a documentação recomenda” (sem trecho no pacote).
6. Questão 1: “Correta. Correta…” duplicado.
7. Intro: “consultado em 13/11/2026” → “13 e 14/11/2026” (nove trechos novos).
8. “capítulo 5” → “módulo 5” (9 ocorrências), igual ao uso dos capítulos 1 a 3 e das demais remissões do capítulo 4.
9. 4.4c: “custo total” → “custo” (custo total é do módulo 7; eficiência, do 15). 4.6d: “módulos 5 a 8” → “módulos seguintes” (o texto também remete aos módulos 9 e 15).

## Não alterado (decisão do operador)
Partes acima de 500 palavras (4.6d, 557); imagens (só molduras); reflow em 320 px e aparelhos reais.

## Estado
- Validador: 16 OK, 0 FALHA. PDF: 320 páginas A4; posições das partes iguais às anteriores (4.4c na 269, 4.5a na 271, 4.6d na 288).
- Hashes: HTML `bdb34977877270ed`; PDF `1d1dfb567fb3e5db`; pacote de fontes `f169d2f2629c8bd1` (inalterado).
- Backup (antes das edições): `arquivo/antes-revisao-capitulo-4-2026-11-14/` (HTML `fffe13bd5c4b0109`; PDF `0cfe42f8ab886203`).
- Armadilha: aumentar uma linha na nota de fonte da 4.4b empurra uma página extra no PDF; recompare as posições das partes após editar.

Assinatura: claude - pessoal, 14/11/2026.
