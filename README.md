# Guia para Engenharia de LLMs

Material de estudo em HTML semântico (`guia-engenharia-llms.html`) e PDF A4 (`guia-engenharia-llms.pdf`) sobre especificação, arquitetura, integração, avaliação e operação de sistemas com modelos de linguagem (LLMs), locais ou de fronteira (em transição para incluir programação em duas camadas conforme o novo planejamento de 23/11/2026).

## Estado atual (23/11/2026)

- **Edição vigente (Capítulos 1 a 16 concluídos, revisados e fechados):** `316` partes (`175.906` palavras em partes; HTML `sha256` `19a020013721c5a5`), `376` questões (`94/94/94/94`), `141` tabelas (`141` com `.rolagem`), `402` termos `<dt>` no Glossário (`395` `<dfn>`), `67` molduras `data-imagem=` e `722` links externos (`275` URLs únicas); o PDF, de `534` páginas A4 (`sha256` `10ff8c03dd8dfe83`), foi regerado em 18/11/2026.
  - **Parte I — Fundamentos e controle:** Cap. 1 (`19` partes), Cap. 2 (`18`), Cap. 3 (`17`), Cap. 4 (`18`), Cap. 5 (`17`).
  - **Parte II — Contexto, grafos, segurança e proporcionalidade:** Cap. 6 (Engenharia de grafos aplicada a LLMs), Cap. 7 (Segurança e governança), Cap. 8 (Atos autodestrutivos e proporcionalidade), Cap. 9 (Contexto e memória), Cap. 10 (Ferramentas e integrações), Cap. 11 (Busca, indexação e RAG).
  - **Parte III — Operação, desempenho e economia:** Cap. 12 (Harnesses, workflows e agentes), Cap. 13 (Inferência local), Cap. 14 (Seleção e roteamento), Cap. 15 (Integração empresarial e LLMOps), Cap. 16 (Eficiência e economia).
- **Novo planejamento aprovado (23/11/2026):** ver [planejamento-reestruturado-2026-11-23.md](planejamento-reestruturado-2026-11-23.md) e [roadmap.md](roadmap.md) — reorganização para `18` capítulos integrando os dois livros de Chip Huyen (*AI Engineering* e *Designing Machine Learning Systems*) como fontes primárias, as fontes públicas de 2026 como complementares e programação executável em duas camadas (blocos curtos no HTML + `18` laboratórios em `laboratorios/`), preservando o formato para TDAH. Ferramenta local de leitura dos PDFs criada em `ferramentas/livros.py` (textos mantidos fora do Git em `cache-fontes/livros/`). Ver `changelog-planejamento-huyen-e-programacao-2026-11-23.md`.

## Estrutura principal

- `guia-engenharia-llms.html` — livro completo interativo (questões com retorno imediato em `aria-live`, glossário e referências).
- `guia-engenharia-llms.pdf` — versão A4 gerada via Chromium headless (`534` páginas).
- `planejamento-reestruturado-2026-11-23.md` — novo plano curricular aprovado (`18` capítulos + programação).
- `planejamento-completo-estudos-engenharia-llms.md` — plano curricular anterior (`16` módulos).
- `plano-de-lacunas-para-nota-10-2026-11-19.md` — plano de lacunas de qualidade (`L1`–`L8`).
- `pacote-de-fontes-*.md` — trechos literais conferidos de fontes públicas primárias.
- `ferramentas/` — `guia.py`, `fontes.py`, `livros.py`, `validar-guia.py`, `renumerar-paginas.py`, `executar-trechos-de-codigo.py`, `conferir-trechos.py`, `extrair-texto-web.py`, `auditar-guia-navegador.mjs` e testes (`testar-ferramentas.py`, `testar-fontes.py`, `testar-livros.py`, `testar-llm-local.py`).
- `CLAUDE.md` — estado atual, instruções de retomada e protocolo de economia de tokens (`protocolo-de-economia-de-tokens-entre-sessoes.md`).

## Validação rápida

```bash
python3 -I ferramentas/guia.py fechar
```
