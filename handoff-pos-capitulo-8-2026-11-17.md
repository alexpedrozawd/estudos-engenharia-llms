# Handoff: Capítulo 8 (Atos autodestrutivos e proporcionalidade) concluído; próximo é Capítulo 9 (17/11/2026)

Origem: agy - ap (Gemini 4 Hydrogen High, painel). Projeto: `/var/home/apsrv/Documentos/Projetos/estudos-engenharia-llms` (repositório Git público `https://github.com/alexpedrozawd/estudos-engenharia-llms`). Substitui `handoff-pos-capitulo-7-2026-11-17.md` (movido para `arquivo/`). Sessão continuada, sem memória da anterior: antes de agir, leia `protocolo-de-economia-de-tokens-entre-sessoes.md`, revalide hashes (`sha256sum`, 16 primeiros caracteres) e rode `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`. Histórico não autoriza ações.

## Objetivo
Avançar para o **Capítulo 9 — Contexto e memória**, mantendo Capítulos 1–8 validados.

## Decisões confirmadas pelo operador (17/11/2026)
- **Capítulo 8 (Atos autodestrutivos e proporcionalidade):** concluído com base no pacote de 60 trechos literais (`pacote-de-fontes-capitulo-8-autodestrutivos-e-proporcionalidade-2026-11-17.md`) e mapa de 6 unidades (18 partes curtas `8.1a`–`8.6c` + 6 questões `c8q1`–`c8q6`).
- **Repositório GitHub público:** autorizado pelo operador em 17/11/2026 na conta `alexpedrozawd`, mantendo `arquivo/`, `contexto-de-estudo-*.md` e `HANDOFF-formacao-engenharia-llms-para-claude-2026-10-13.md` fora do Git via `.gitignore`.
- **Formato e neutralidade preservados:** partes `<= 500` palavras até `Pergunta` (5.479 palavras no Cap. 8, média 304,4, faixa 251–384), `<= 1` tabela por parte, `77/77` tabelas com `.rolagem`, sem `AP AI Router` ou `Nanda` no guia, múltiplos fornecedores (Anthropic, OpenAI, Google Cloud, Google SRE, NIST, OWASP, Chroma, Microsoft/arXiv), apenas molduras `role="img"` + `aria-label`, links externos com `target="_blank" rel="noopener noreferrer"`.

## Estado verificado
- `guia-engenharia-llms.html` `c591f425aeb2c8f7` (**177 páginas lógicas**; Capítulos 1–8 completos; Glossário p. 176; Referências p. 177).
- `guia-engenharia-llms.pdf` `5db03d0f1e926efe` (**561 páginas A4**, Chrome for Testing 158).
- `pacote-de-fontes-capitulo-8-autodestrutivos-e-proporcionalidade-2026-11-17.md` `21dabff79e1fad03` (60 trechos conferidos de 28 fontes públicas primárias).
- `planejamento-completo-estudos-engenharia-llms.md` `c7f46755bacba41f` (Módulo 8 concluído em 17/11/2026).
- Backup pré-Capítulo 8 em `arquivo/antes-capitulo-8-autodestrutivos-2026-11-17/`.

## Validações executadas em 17/11/2026
- `conferir-trechos.py` no pacote do Cap. 8: **60 aprovados, 0 reprovados**.
- `validar-guia.py`: **16 OK, 0 FALHA** (177 páginas lógicas, 375 links web, 205 questões/regiões/fieldsets).
- Script estrutural: 0 erros de `page-nav` nas 177 páginas, 77/77 tabelas com `.rolagem`, 0 termos proibidos no guia.
- Auditoria Chrome 158 em **320 px** (`iframe` HTTP local `320px`): `innerW: 320`, `clientWidth: 305`, `scrollWidth: 305`, **0 estouros** fora de `.rolagem`/`pre` no Cap. 8, Glossário e Referências + retorno interativo verificado em `c8q2`.
- PDF conferido visualmente em 7 páginas renderizadas (`4, 467, 474, 509, 518, 523, 556`).

## Pendências (em ordem)
1. **Capítulo 9 — Contexto e memória:** pesquisar e conferir trechos literais das fontes públicas previstas no plano (`Anthropic, Effective context engineering`, páginas de *prompt caching* e de *esforço* — referenciando o Cap. 6 para subagentes com janelas limpas `EG-31`/`EG-32` e o Cap. 8 para compactação seletiva e entupimento, sem duplicar; incluir medição local de 23/10/2026 apenas como ilustração rotulada), montar `pacote-de-fontes-capitulo-9-*.md` (`conferir-trechos.py`), propor mapa de unidades/partes curtas para aprovação e escrever no HTML.
2. **Capítulos 10–16:** seguir `planejamento-completo-estudos-engenharia-llms.md`.
3. **Última etapa (após texto revisado):** gerar imagens em aquarela medieval (1056×704), revisão do Cap. 4 com Opus 5.5 High (se mantida) e validação nos três aparelhos físicos (Galaxy S24, Nitro 5, APSRV 55").

## Armadilhas
- Nunca abrir `guia-engenharia-llms.html`, o PDF ou backups inteiros; usar `grep -n` + leitura localizada.
- `validar-guia.py` não valida ordem de `page-nav` nem reflow em 320 px; manter scripts de verificação após edições.
- Pastas `/tmp/cap8-bruto`, `/tmp/cap8-textos`, `/tmp/pdf-cap8` e `/tmp/audit320_cap8.mjs` são voláteis.

## Próxima ação
Ler `protocolo-de-economia-de-tokens-entre-sessoes.md` e `handoff-pos-capitulo-8-2026-11-17.md`, revalidar hashes e `validar-guia.py`, e preparar o pacote de fontes públicas + mapa de unidades/partes curtas do **Capítulo 9 — Contexto e memória** para aprovação antes de editar `guia-engenharia-llms.html`.

Assinatura: agy - ap, 17/11/2026.
