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

## 8. Ferramentas que substituem leitura e comando soltos (19/11/2026)

Os números das seções 1 a 7 são de 13/11/2026; em 19/11/2026 o HTML tem 2.200.828 bytes e 316 partes, então ler por trecho vale ainda mais. Todas usam só a biblioteca padrão (`python -I`), não gastam LLM e têm testes (`ferramentas/testar-ferramentas.py`, `testar-fontes.py`, `testar-llm-local.py`).

| Comando | Para quê | Saída |
|---|---|---|
| `guia.py mapa 13.2` | id, linhas e palavras das partes de um prefixo; leia depois com `offset`/`limit` | 1 linha por parte |
| `guia.py contar` | partes, palavras, tabelas, questões, glossário, `<dfn>`, links | 1 linha JSON |
| `guia.py fechar [--pdf]` | renumerar (conferir), validar, executar trechos, ids/`<dfn>`/sumário/tabelas, contagens, hashes, PDF temporário com `pdfinfo` e esqueleto de changelog | cerca de 1,1 KB (comandos soltos: 4,4 KB) |
| `guia.py pdf --substituir --motivo M` | substitui o PDF só depois de copiar o atual para `arquivo/antes-M-<data>/` | 1 linha |
| `fontes.py manifesto/baixar/extrair/conferir` | baixa as fontes do manifesto dos pacotes (só https e só domínios do manifesto), extrai o texto e roda `conferir-trechos.py` | por pacote: 1 linha + reprovações |
| `fontes.py achar CHAVE "palavras"` | trechos candidatos da fonte com `chave:linha`, sem a fronteira ler a página | até 5 trechos de 420 caracteres |
| `livros.py extrair/ler/achar/pagina-png` | extrai PDFs locais dos livros para `cache-fontes/livros/` (fora do Git), lê intervalos contínuos de páginas, localiza termos e renderiza PNG pontual de figuras/tabelas | texto por página ou 1 PNG |

- Cache de fontes e saídas locais ficam em `cache-fontes/` e `rascunho-local/` (no `.gitignore`).
- Conferir as 9 fontes do Capítulo 16: 300.406 bytes de texto que a fronteira leria, contra 123 bytes de saída do script.
- Limite verificado: o manifesto (`Chave | Fonte e endereço | Hash bruto (16)`) cobre os 12 pacotes padronizados (Caps. 6–16 e expansão do Grupo A; Caps. 2–5 e revisões seguem formatos anteriores sem tabela de hash). Das 196 chaves únicas do manifesto, 25 respondem 403/400 ao download automático (`www.anthropic.com`, `docs.vllm.ai`, `nist`, `azure`) ou redirecionam de `https` para `http` (`cormack-rrf`). Não se disfarça o agente de usuário; essas ficam com a busca e a leitura da fronteira. Com as 171 baixadas, 581 de 754 trechos dos 12 pacotes foram reconfirmados após corrigir formatação Markdown residual (`IL-06`, `SG-54`); as 6 reprovações restantes com fonte baixada (`SR-04`–`SR-07`, `SR-24`–`SR-25` em `openai-model-selection`) decorrem da atualização da página pela OpenAI após 17/11/2026 e ficam registradas para a revisão de vigência (L7).
- A descoberta de fontes novas continua com a busca da fronteira (modo "standard"); o script cuida de baixar, extrair, localizar e conferir.

## 9. LLM local neste projeto: decisão de 19/11/2026

Testado em 54 casos (36 afirmações com gabarito nos trechos já conferidos e 18 controles sem suporte), com limites fixados antes (G1 acerto ≥ script lexical; G2 falso aceite ≤ 5%; G3 bytes lidos ≤ 50% dos candidatos). Tarefa: o script separa 10 trechos candidatos e o modelo só escolhe até 3 números, sem escrever citação.

| Modelo | Acerto@3 local / script | Falso aceite | Bytes lidos | Veredito |
|---|---|---|---|---|
| Qwen 3.8 27B `iq3_xxs` | 97% / 97% | 2/18 (11%) | 797 de 4.403 | reprovado em G2 |
| Qwen 3.8 27B `q3_k_xl` | 97% / 97% | 2/18 (11%) | 860 de 4.403 | reprovado em G2 |
| Gemma 4 26B-A4B | 97% / 97% | 2/18 (11%) | 740 de 4.403 | reprovado em G2 |

- O local não achou nenhum trecho que o script não achasse (0 casos exclusivos), então não há ganho de acerto. A economia de bytes (cerca de 0,8 KB contra 1,5 KB do top-3 do script) é pequena frente ao custo de GPU e à revisão.
- Os 2 falsos aceites são os mesmos nos três modelos e vêm de fontes da Anthropic com assunto próximo; o controle é ambíguo, mas a regra fixada antes não permite descartá-lo.
- Limites do teste: as palavras-chave em inglês foram escritas por quem conhecia o gabarito, o que favorece o script; 36 casos e uma só tarefa. O resultado não prova que o local seja inútil em outras tarefas, e sim que, aqui, não compensa.
- **Decisão (divergência com o Pipeline Triangular da diretriz global):** neste projeto o LLM local não entra no fluxo. O que economiza é a camada sem LLM (seção 8); a fronteira continua autora e revisora. Reabrir só com tarefa nova, verificador por código e novo portão. Antes de qualquer uso: `llm-local.py` recusa a GPU ocupada e só fala com `127.0.0.1`.

Atualizado em 13/11/2026 por deepseek - conta não verificada (referência ao protocolo no `CLAUDE.md` e no handoff; nota do `continue-work`). Assinatura: claude - pessoal, 13/11/2026.
