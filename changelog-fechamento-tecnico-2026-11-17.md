# Changelog — Fechamento técnico e ajustes finais (17/11/2026)

- **Data:** 17/11/2026
- **Responsável:** Gemini 4 Hydrogen (`agy - ap`)
- **Escopo:** conferência online dos itens `[Não verificado]` e atualização dos pacotes de fontes (`pacote-de-fontes-*.md`), correção de `@media print` do Capítulo 5 e `3.2b`/`4.3b`, redução de viés de tamanho e repetição em questões, inclusão de `Assistir:` nos Capítulos 2–16, auditoria de `reflow` em `320 px` e `axe-core` com correções de acessibilidade, e regeração do PDF. (Criação das 67 imagens em aquarela mantida fora desta etapa.)
- **Backup pré-edição:** `arquivo/antes-finalizacao-100-2026-11-17/` (`guia-engenharia-llms.html`, `guia-engenharia-llms.pdf`, `CLAUDE.md`).

---

## 1. Conferência online e pacotes de fontes

- **OpenAI Evals (`5.5c`, `pacote-de-fontes-equilibrio-de-fornecedores-2026-11-16.md`):** reconferida em `17/11/2026`; salva literalmente `"OpenAI is deprecating the Evals platform"` junto ao aviso de desligamento previsto para `30/11/2026`.
- **45 novos trechos literais salvos e validados (`ferramentas/conferir-trechos.py` -> `APROVADO`):** distribuídos em 11 pacotes (`pacote-de-fontes-capitulo-3-2026-11-13.md`, `capitulo-4`, `engenharia-de-grafos`, `capitulo-7` a `capitulo-11`, `capitulo-13`, `capitulo-15` e `capitulo-16`).
- **Correção factual em `4.3b` (`guia-engenharia-llms.html`):** ajustado o texto sobre *Token counting* da Anthropic para refletir a documentação vigente (aceita instrução de sistema, ferramentas, imagens e PDFs, mas devolve `invalid_request_error` para quase todas as ferramentas de servidor e para o conector MCP).
- **Lacuna preservada:** `14.6c` mantém explicitamente declarada a ausência de trecho confirmando invalidação de cache entre modelos na Anthropic/Google; os demais pontos didáticos permanecem marcados como `proposta didática`.

---

## 2. Ajustes no HTML (`guia-engenharia-llms.html`)

- **`@media print` (linhas 203–207):** incluídos `#capitulo-5` e `#questoes-capitulo-5` nas regras `break-before: page` e `> h2 { margin-block-start: 0; }`.
- **Remissão em `3.2b`:** ajustada a nota para explicitar que o Capítulo 16 trata de medir e reduzir custo de chamadas, e não do levantamento inicial da linha de base.
- **Questões:**
  - Zerado o viés de alternativa correta estritamente mais longa nos conjuntos visados (`0/29` no Cap. 1, `0/20` em `p4-*` do Cap. 4, `0/22` no Cap. 9 e `0/22` no Cap. 10), mantendo intacta a distribuição equilibrada dos gabaritos (`96 A, 96 B, 96 C, 97 D`, 385 questões).
  - Reformuladas `c2q1`, `c2q2`, `c2q3` e `c2q6` (Capítulo 2) com cenários novos, eliminando repetição quase literal das perguntas de parte.
- **Linha `Assistir:` (`Fontes da unidade`):** incluída nos **90** blocos dos Capítulos 2–16 (total de 96 no guia): 6 vídeos verificados via `youtube.com/oembed` (`2.1c`, `4.1c`, `6.2c`, `10.6c`, `12.1c`, `13.3c`) e `nenhum vídeo conferido para esta unidade` nos demais 84 blocos.
- **Acessibilidade (`axe-core`):** corrigidas as 3 ocorrências menores detectadas — `<th scope="col">Aspecto</th>` na tabela `Pronto e aceito` (`empty-table-header`) e remoção do `role="region"` redundante nos dois `<figure class="bloco-codigo">` (`7.1b` e `8.6a`, mantendo `role="region"` nos `<pre>` internos).

---

## 3. Validações e hashes finais

- **`python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`:** `16 OK, 0 FALHA` (`325` páginas lógicas, `385` questões/regiões/fieldsets, `657` links web).
- **Reflow em `320 px` (`chromium-1254` headless, 326 seções):** `innerW: 320`, `docClient: 320`, `docScroll: 320`, `overflows: []` fora de `.rolagem`/`pre`; capturas PNG inspecionadas na Parte I e teste interativo em `c5q1`.
- **Auditoria `axe-core` (WCAG 2.0 A/AA, 2.1 AA, best-practice):** `45 passes`, `0` violações após correções.
- **PDF (`chromium-1254 --headless=new --print-to-pdf`):** `968` páginas A4 (`14.440.076` bytes); amostras inspecionadas com `pdftoppm -png -r 110` (`160`, `302` abertura Cap. 5, `357` questões Cap. 5, `559`).
- **Hashes SHA-256 (16 hex):**
  - `guia-engenharia-llms.html`: `1e0d640f4c0e8802` → `832697d9fe8b76e5`
  - `guia-engenharia-llms.pdf`: `186709cd285a03bd` → `86af42d2c3920429`
- **Pendentes por natureza / fora do recorte:** criação das 67 imagens em aquarela; leitura nos três aparelhos reais (Galaxy S24, Acer Nitro 5, tela APSRV 55"), teste com leitor de tela real e impressão física.

Assinatura: agy - ap (Gemini 4 Hydrogen High), 17/11/2026.
