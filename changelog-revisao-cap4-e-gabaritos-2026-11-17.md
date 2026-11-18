# Changelog — Redistribuição de gabaritos e revisão do Capítulo 4

- **Data:** 17/11/2026
- **Responsável:** Gemini 4 Hydrogen (`agy - ap`)
- **Escopo:** redistribuição equilibrada das alternativas corretas em todo o guia (`guia-engenharia-llms.html`), revisão integral do Capítulo 4 (*Prompts, parâmetros e respostas*) com Gemini 4 Hydrogen contra os pacotes já salvos (`pacote-de-fontes-capitulo-4-2026-11-13.md` e `pacote-de-fontes-equilibrio-de-fornecedores-2026-11-16.md`) e `requisitos-de-formato-html-do-material.md` (§8 e §9), e regeração do PDF.
- **Backup pré-edição:** `arquivo/antes-revisao-cap4-gabaritos-2026-11-17/` (`guia-engenharia-llms.html`, `guia-engenharia-llms.pdf`, `CLAUDE.md`).

---

## 1. Redistribuição dos gabaritos (`385` questões)

Todas as `385` questões (`20–23` de parte + `6` de fechamento em cada capítulo) foram analisadas quanto à letra correta, sequência consecutiva e eventuais referências posicionais ("alternativa A", "todas as anteriores" etc.): **0 referências posicionais** encontradas.

- **Capítulos 1, 2 e 4:** mantidos com as distribuições originais por já estarem equilibrados (`7/7/7/8`, `7/6/6/7` e `6/7/6/7`, sem sequência maior que 2).
- **Capítulos 3, 5 e 6–16:** alternativas embaralhadas de modo determinístico (`seed 20261117`), preservando na íntegra o texto de cada alternativa, `data-correta` e `data-explicacao`, atualizando apenas a ordem dos blocos `<label>`, o atributo `value="a..d"` e `<strong>A..D.</strong>`. Nenhuma letra se repete em questões consecutivas (`max_streak = 1`) nesses capítulos, e as `6` questões de fechamento por capítulo cobrem todas as 4 letras (`{1, 1, 2, 2}`).

| Escopo | Antes (`A / B / C / D`) | Depois (`A / B / C / D`) | Total |
|---|---|---|---|
| Capítulo 1 | `7 / 7 / 7 / 8` | `7 / 7 / 7 / 8` | 29 |
| Capítulo 2 | `7 / 6 / 6 / 7` | `7 / 6 / 6 / 7` | 26 |
| Capítulo 3 | `3 / 6 / 11 / 6` | `6 / 7 / 7 / 6` | 26 |
| Capítulo 4 | `6 / 7 / 6 / 7` | `6 / 7 / 6 / 7` | 26 |
| Capítulo 5 | `7 / 7 / 5 / 7` | `7 / 6 / 7 / 6` | 26 |
| Capítulos 6–11 (Parte II, 22 cada) | `2 / 117 / 13 / 0` | `33 / 33 / 33 / 33` (`{5,5,6,6}` rotacionado) | 132 |
| Capítulos 12–16 (Parte III, 24 cada) | `118 / 2 / 0 / 0` | `30 / 30 / 30 / 30` (`6/6/6/6` por capítulo) | 120 |
| **Total do guia** | **`150 / 152 / 48 / 35`** | **`96 / 96 / 96 / 97`** | **385** |

---

## 2. Revisão do Capítulo 4 (`p. 72–93`)

Leitura integral das 22 páginas lógicas do Capítulo 4 (`capitulo-4`, `unidade-4-1a` a `unidade-4-6d`, `questoes-capitulo-4`) sem baixar URLs da web.

### 2.1 [ANALISADO / NÃO ALTERADO] — Estrutura, citações e referências
- **Estrutura de parte curta (§8):** todas as 20 partes trazem resumo em 3 linhas, analogia, no máximo 1 tabela por parte, 1 questão interativa com `Notas de fonte` e navegação encadeada (`p=72..93`).
- **Citações literais:** todos os trechos literais citados no texto e em `Notas de fonte` batem com os registros `C4-01` a `C4-33` de `pacote-de-fontes-capitulo-4-2026-11-13.md` e com `pacote-de-fontes-equilibrio-de-fornecedores-2026-11-16.md` (Google, OpenAI, Qwen3.8-27B e Gemma 4).
- **Links, Glossário e Referências:** `0` âncoras quebradas no capítulo; todos os `28` termos em `<dfn>` constam do `#glossario`; todas as `14` fontes do capítulo constam em `#referencias`.

### 2.2 [CORRIGIDO / AJUSTADO] — Clareza na 1ª ocorrência e viés de tamanho nas questões
- **`4.3b` (`unidade-4-3b`):** explicação breve de `base64` na primeira ocorrência (`em base64 (texto codificado)`).
- **`4.6a` (`unidade-4-6a`):** tradução explícita das chaves de tipo usadas no JSON Schema ilustrativo (`string` como texto, `integer` como número inteiro, `null` como vazio e `enum` como lista fechada).
- **`questoes-capitulo-4` (`c4q1`–`c4q6`):** enxugamento das alternativas corretas nas 6 questões de fechamento para reduzir a disparidade visual de comprimento frente aos distratores, sem alterar sentido nem explicações.

---

## 3. `[Não verificado]` nesta etapa (sem novo download da web)

Trechos do Capítulo 4 apresentados como paráfrase na criação inicial do pacote (13–14/11/2026) que não constam literalmente na tabela reduzida de `pacote-de-fontes-capitulo-4-2026-11-13.md` (os arquivos temporários em `/tmp/cap4-fontes/txt` não existem mais e nenhuma URL foi baixada nesta revisão):
- **`4.2a` (Min et al., 2022):** paráfrase de "12 modelos" e "classificação e múltipla escolha" no resumo do artigo (`C4-05`, `C4-06` e `C4-11` trazem só os três trechos literais da tabela).
- **`4.3b` e `4.4a` (Anthropic, *Token counting*):** menção à lista de entradas incluir "ferramentas e servidores de ferramentas" além de imagens e PDFs (`C4-31` traz apenas o trecho de imagens e PDFs em base64).
- **Permanecem pendentes de conferência/execução global:** itens `[Não verificado]` dos pacotes anteriores, geração das imagens em aquarela e inspeção em tela de 320 px / três aparelhos reais.

---

## 4. Validação final e hashes

- **Integridade de alternativas:** script de conferência confirmou os `379` conjuntos de alternativas não editados com texto, `data-correta` e `data-explicacao` idênticos ao backup, mais os `6` enunciados `c4q1`–`c4q6` atualizados.
- **`python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`:** `16 OK, 0 FALHA` (`325` páginas lógicas, `385` questões/regiões/fieldsets, `651` links web).
- **PDF (`chromium-1254 --headless=new --print-to-pdf`):** `966` páginas A4 (`594.96 x 841.92 pts`).
- **Amostras visuais inspecionadas (`pdftoppm -png -r 110`):** páginas PDF `263` (`4.3b`), `285` (`4.6a`), `298` (`Questões do capítulo 4`), `557` (`Questões do capítulo 9`) e `908` (`Questões do capítulo 16`) sem sobreposição, cortes de bloco ou divergência entre `Resposta: <letra>` impresso e alternativa correta.
- **Hashes SHA-256 (16 hex):**
  - `guia-engenharia-llms.html`: `1e0d640f4c0e8802`
  - `guia-engenharia-llms.pdf`: `186709cd285a03bd`

Assinatura: agy - ap (Gemini 4 Hydrogen High), 17/11/2026.
