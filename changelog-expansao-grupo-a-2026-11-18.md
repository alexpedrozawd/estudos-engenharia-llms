# Changelog — Expansão do Grupo A (18/11/2026)

**Responsável:** `agy - ap` (em 18/11/2026), após aprovação explícita do operador para incluir os 5 blocos selecionados do Grupo A sem programação.

## Resumo da mudança

- Foram inseridas **8 partes curtas novas** distribuídas pelos 5 blocos temáticos aprovados, mantendo o padrão visual do guia, a neutralidade entre fornecedores e a conferência literal das fontes:
  - **Bloco 1 — Voz e tempo real (`Cap. 2`):**
    - `2.3d` (`#unidade-2-3d`) — *Voz direta e canais nos dois sentidos* (Speech-to-Speech, WebRTC, WebSockets e contrapressão).
  - **Bloco 2 — Controles locais, repetição e corte estatístico (`Cap. 4`):**
    - `4.5d` (`#unidade-4-5d`) — *Controles de repetição e corte local* (`frequency_penalty`, `presence_penalty`, `repeat_penalty`, `min_p`, `seed` e `logprobs`).
  - **Bloco 3 — Estatística de avaliação, pós-treinamento e rollout (`Caps. 5, 13 e 15`):**
    - `5.6e` (`#unidade-5-6e`) — *Intervalo de confiança e agrupamento* (intervalos de confiança, erro padrão agrupado quando itens compartilham contexto, e pontuação vs. execução).
    - `13.6d` (`#unidade-13-6d`) — *Quatro caminhos de pós-treinamento* (SFT, DPO, RLVR com raciocínio em DeepSeek-R1 e destilação de modelo maior para menor).
    - `15.6d` (`#unidade-15-6d`) — *Sombra (dark launch) versus canário e A/B* (comparação de estratégias de rollout e detecção de deriva).
  - **Bloco 4 — A2A e interface gráfica / uso de computador (`Cap. 10`):**
    - `10.6d` (`#unidade-10-6d`) — *MCP versus protocolo A2A* (agente-ferramenta vs. agente-agente, Agent Card, execução opaca e riscos de uso de computador/GUI).
  - **Bloco 5 — HNSW e PDFs em RAG (`Cap. 11`):**
    - `11.3d` (`#unidade-11-3d`) — *Busca aproximada com HNSW* (grafo em camadas `M`, `efConstruction`, `efSearch`, filtro pós-busca e risco OWASP LLM08 de vazamento por permissão).
    - `11.4c` (`#unidade-11-4c`) — *Por que PDFs com tabelas quebram o RAG* (ordem de leitura multi-coluna, reconstrução estrutural de tabelas e fusão por Reciprocal Rank Fusion).
- Cada parte nova recebeu 1 questão inline contextualizada (`p2-3d`, `p4-5d`, `p5-6e`, `p10-6d`, `p11-3d`, `p11-4c`, `p13-6d`, `p15-6d`), elevando o total de `385` para `393` questões (`6` por capítulo no fechamento preservadas), com distribuição equilibrada nas 8 novas questões (`2` gabaritos A, `2` B, `2` C e `2` D).
- Os blocos `Fontes da unidade` afetados foram reposicionados e consolidados na nova última parte de cada unidade (`2.3d`, `4.5d`, `5.6e`, `10.6d`, `11.3d`, `11.4c`, `13.6d`, `15.6d`), mantendo a distinção `Ler:` / `Aprofundar:` / `Assistir:`.
- `Sumário` (`#sumario`), cabeçalhos de capítulo (`21`, `21`, `21`, `17`, `18`, `19`, `19` partes curtas nos Caps. 2, 4, 5, 10, 11, 13 e 15), navegação entre páginas (`page-nav`), `#glossario` (`397` entradas `<dt>` no total) e `#referencias` foram atualizados e renumerados sequencialmente de `1` a `333` via `ferramentas/renumerar-paginas.py`.

## Pacote de fontes e backup

- Fontes públicas primárias salvas em [pacote-de-fontes-expansao-grupo-a-2026-11-18.md](pacote-de-fontes-expansao-grupo-a-2026-11-18.md) com `40` trechos literais (`GA-01` a `GA-40`).
- Backup pré-expansão preservado em `arquivo/antes-expansao-grupo-a-2026-11-18/` (`guia-engenharia-llms.html`, `guia-engenharia-llms.pdf` e `CLAUDE.md`).

## Validações executadas

- `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-expansao-grupo-a-2026-11-18.md --textos /tmp/expansao-grupo-a-textos --projeto .` → **40 aprovados, 0 reprovados (total 40)**.
- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html` → **16 OK, 0 FALHA** (`333` páginas sequenciais `1..333`, `393` questões/regiões/fieldsets, `682` links externos).
- `python3 -I ferramentas/executar-trechos-de-codigo.py --guia guia-engenharia-llms.html` → **0 OK, 0 FALHA, 21 ilustrativos (não executados), 0 blocos `<pre>` sem classe `codigo`/`saida`**.
- PDF regerado via Chromium headless (`--no-pdf-header-footer --print-to-pdf`): `989` páginas A4 (`594.96 x 841.92 pts`, `14.796.141 bytes`), com inspeção visual por renderização (`pdftoppm`) das amostras de `2.3d` e `4.5d`.
- **Pendência observada:** `playwright` não está instalado neste ambiente; o teste automatizado de `reflow` em `320 px` e `axe-core` sobre as 8 partes novas permanece pendente para validação em navegador.

## Integridade (SHA-256, 16 hex)

- `guia-engenharia-llms.html`: `85cc31a74dbf1fdc` (pós-revisão geral) → `6787437d3daeddba`
- `guia-engenharia-llms.pdf`: `86a4939d61981ee5` (pós-revisão geral) → `0688ded7c6ffb3cf`

---
Assinatura: agy - ap
