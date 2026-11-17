# Changelog — capítulo 3 escrito e integrado (13/11/2026)

Autoria: deepseek - conta não verificada (painel). Origem: pedido do operador para escrever o capítulo 3 inteiro, na estrutura dos capítulos 1 e 2, seguindo o protocolo de economia de tokens; depois `/revisar` e `/handoff`.

## O que mudou

- **Guia** (`guia-engenharia-llms.html`): 22 páginas lógicas novas — abertura do capítulo 3, 20 partes (3.1a a 3.6d) e as seis questões. Passa de 51 para 73 páginas.
- **Sumário**: capítulo 3 ganhou link, lista de sete itens (seis unidades e questões).
- **Navegação**: questões do capítulo 2 apontam para o capítulo 3; glossário e referências renumerados (72 e 73).
- **Impressão**: `#capitulo-3` e `#questoes-capitulo-3` entraram nas regras de quebra de página e de margem do título.
- **Glossário**: 32 termos novos, com a unidade de origem. Total de 146.
- **Referências**: cinco fontes normativas (RFC 2119, NASA SE Handbook, NIST AI RMF 1.0, Scrum Guide 2020, NN/g) e uma página da Anthropic; parágrafo de abertura atualizado para “capítulos 1, 2 e 3”.
- **Introdução**: a frase que descrevia o formato restrito aos capítulos 1 e 2 passou a incluir o 3.
- **Novos arquivos**: `pacote-de-fontes-capitulo-3-2026-11-13.md`, este changelog e `handoff-capitulo-3-concluido-2026-11-13.md`.
- **Backup**: `arquivo/antes-capitulo-3-2026-11-13/`, com HTML e PDF do estado anterior.
- **Arquivado**: `handoff-criacao-capitulo-3-2026-11-13.md` movido para `arquivo/`.

## Por quê

- O plano de 13/11/2026 fixou seis unidades e 20 partes (3/3/3/4/3/4), com o caso único da Aurora Educação crescendo até a 3.6d.
- Os cinco pontos que o operador aprovou entraram no texto: quatro papéis (3.1b), dados e requisitos não funcionais (3.3a), quem aceita (3.4a/3.4d), suposições e não-objetivos (3.6c/3.6d) e o aceite em três famílias (3.4d).

## Fontes

- Baixadas e conferidas em 13/11/2026: RFC 2119 (texto), NASA/SP-2016-6105 Rev2 (PDF), NIST AI 100-1 (PDF), Scrum Guide 2020 (PDF), NN/g *Personas Make Users Memorable* (03/10/2025), Anthropic *Demystifying evals for AI agents* (09/01/2026) e *Building effective agents* (19/12/2024).
- `conferir-trechos.py` no pacote: **24 trechos, 24 aprovados, 0 reprovados**. Três correções de trecho foram necessárias: hifenização do PDF do NIST (`contextspecific`), quebra de página no §4.1.1.2.3 da NASA e apóstrofo reto na citação da Anthropic.
- O guia **não afirma conformidade** com RFC 2119, NASA, NIST ou Scrum; cada nota diz isso.

## Correções feitas durante a escrita e a revisão

| Achado | Prova | Correção |
|---|---|---|
| Link da NASA apontava para página com 404 | `curl` → 404 em `nasa.gov/reference/...` | Trocado em 6 lugares pelo PDF que responde 200 |
| “A empresa de avaliação Anthropic” | A Anthropic constrói modelos; a página citada é de engenharia | Reescrito para “A Anthropic, que constrói modelos de linguagem” |
| Q3 com `name="p3-x"` | Grupo de rádio separado quebraria a correção | Trocado para `c3q3` |
| 3.5b, alternativa D sem `data-explicacao` | Atributo malformado (`data-explicacao.="x"`) | Explicação “Incorreta.” escrita |
| “três fontes de documento” contra “três páginas e duas circulares” | Contagem divergente entre 3.1c e 3.3c | 3.3c passou a “cinco fontes” |
| Glossário fora de ordem (Aprovador, Operador, Requisito/Requisição) | Conferência alfabética por script | Entradas reposicionadas |
| 3.5c classificava “identificar o assunto” como “sugerir com aprovação” | Incompatível com resposta automática da 3.6d | Passou a “automatizar com conferência” |
| “amostra de 200” na 3.4c contra 100 na 3.4d | Números divergentes | Unificado em 100 |

## Validações (13/11/2026)

- `validar-guia.py`: **16 OK, 0 FALHA**; 73 páginas numeradas em sequência.
- `conferir-trechos.py`: 24/24.
- Estrutura: 20 partes com resumo, analogia, pergunta, retomada e notas; 26 fieldsets (20 perguntas de parte e 6 de fechamento), 104 alternativas; 18 tabelas, todas com legenda e cabeçalho com `scope`; 3 molduras de imagem, nenhuma gerada.
- Equilíbrio de tags conferido por contagem; ids sem duplicata.
- PDF: **253 páginas A4**, Chrome for Testing 158.0.8127.18, `--no-pdf-header-footer`. Páginas 161 (abertura do capítulo), 193, 223 (tabela da 3.6d) e 231 (questão 6) conferidas em PNG.
- **Não executado:** reflow em 320 px, leitor de tela, axe-core, aparelhos reais, segunda leitura independente.

## Hashes (SHA-256, 16 primeiros)

- `guia-engenharia-llms.html` `78afd3998fa2c19e` (585.708 bytes)
- `guia-engenharia-llms.pdf` `a0b8f86d9f2a6df3` (253 páginas)
- `pacote-de-fontes-capitulo-3-2026-11-13.md` `3237eff413c3cb2f`
- `planejamento-capitulo-3-problemas-e-especificacoes.md` `8c7064513b4fd961` (inalterado)
- Backup `arquivo/antes-capitulo-3-2026-11-13/`: HTML `4fd56745e08b1530`, PDF `ff800aeca59ac66b`

Assinatura: deepseek - conta não verificada, 13/11/2026.
