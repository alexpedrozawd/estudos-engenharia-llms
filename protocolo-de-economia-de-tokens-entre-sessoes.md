# Protocolo de economia de tokens entre sessões

Data: 13/11/2026. Autoria: claude - pessoal (painel, conta DeepSeek). Vale para toda sessão que escreva, revise, valide ou entregue o guia. Números conferidos no projeto em 13/11/2026.

## 1. Regra central

O custo não está no formato do arquivo; está em quanto dele entra no contexto por turno. O guia tem 408.620 caracteres (estimativa de 102–117 mil tokens). Uma parte mediana tem 6.772 caracteres (≈ 1,9 mil tokens). A diferença entre ler o guia inteiro e ler uma parte é de cerca de 98%.

Consequência: nenhuma sessão abre o guia inteiro, o PDF inteiro ou um backup inteiro. Todo trabalho começa localizado.

## 2. Início de sessão (meta: até 3 mil tokens)

1. `CLAUDE.md` já chega no contexto; não reler.
2. Handoff vigente, o único citado no `CLAUDE.md`: ≈ 1,9 mil tokens.
3. Changelog só para o que o handoff não responde.
4. `requisitos-de-formato-html-do-material.md`, `planejamento-*` e `pacote-de-fontes-*` só quando a tarefa toca o assunto — sempre por seção (`rg -n '^## '`).
5. Revalidar o estado com hashes de 16 caracteres, não com leitura.

## 3. Localizar, ler e editar

- Localizar: `rg -n 'id="unidade-2-4a"' guia-engenharia-llms.html`, depois `Read` com `offset` e `limit` (≈ 120 linhas de folga).
- Editar: `Edit` com âncora única. Nunca `Write` sobre o guia inteiro.
- Reescrita de uma parte custa o tamanho dela (≈ 1,9 mil tokens). Prefira edições pequenas e cirúrgicas a reescrever a seção.
- Varredura de muitos documentos (3 ou mais, grandes): delegar a subagente e receber só a conclusão. Varredura pequena sai mais barato inline.
- Chamadas independentes no mesmo turno.

## 4. Validar sem ler

| O que | Como | Custo |
|---|---|---|
| Estrutura, links, questões, numeração | `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html` | ~1,2 KB de saída (≈ 350 tokens) |
| "Não mudou" | `sha256sum` e comparar os 16 primeiros caracteres | ≈ 20 tokens |
| PDF | gerar com Chrome headless e conferir 5 ou 6 páginas renderizadas | ≈ 6–9 mil tokens |

Não conferir as 178 páginas do PDF como imagem. Não diffar o HTML atual contra o backup para provar "não mudou": custa ≈ 210 mil tokens e o hash responde a mesma pergunta.

## 5. Handoff e limpeza entre sessões

- Um handoff vigente; os superados ficam em `arquivo/` e não são relidos.
- O teto de 12.000 caracteres do bloco copiável, já na skill `handoff` (≈ 3,3 mil tokens), vale como meta de tamanho.
- Divisão de papéis: handoff = estado, decisões, pendências, próxima ação. Changelog = o que mudou, por quê, com hashes. Não repetir o mesmo conteúdo nos dois: repetição custa duas leituras e cria divergência.
- Hashes de 16 caracteres, nunca conteúdo colado.
- Fim de sessão: handoff novo, changelog da rodada, backup em `arquivo/antes-<motivo>-<data>/`. Nada é apagado.

## 6. Avaliado e descartado

- **Fragmentar o HTML em 51 arquivos com script de montagem.** A economia de leitura é zero (o `offset`/`limit` já limita o custo) e a de escrita também (uma parte custa o mesmo tamanho nos dois modelos). Em troca: 51 arquivos, um script, risco de o HTML entregue ficar defasado dos fragmentos e um segundo lugar onde procurar. Reavaliar só diante de motivo novo, como geração automática de capítulos.
- **Escrever em markdown e converter.** O material é HTML por requisito (`requisitos-de-formato-html-do-material.md`, §1). A marcação é 37% do arquivo; markdown economizaria no máximo isso, menos na prática, porque questões, tabelas e figuras voltariam como HTML. O formato não é o custo.
- **`continue-work`.** Não existe como skill nem comando instalado (conferido em 13/11/2026). O `CLAUDE.md` e o handoff vigente mandavam aplicá-lo; em 13/11/2026 a frase foi trocada por esta instrução: ler o handoff vigente, seguir este protocolo e revalidar hashes.

## 7. Como comprovar

Número sem prova não vale. Meça com `wc -c`, `sha256sum` e o `validar-guia.py`; converta para tokens apenas como estimativa (caracteres ÷ 3,5 em HTML, ÷ 3,6 em prosa). Não há tokenizador instalado no ambiente (13/11/2026), então nenhum número deste documento é medida exata de tokens.

Atualizado em 13/11/2026 por deepseek - conta não verificada (referência ao protocolo no `CLAUDE.md` e no handoff; nota do `continue-work`). Assinatura: claude - pessoal, 13/11/2026.
