# Changelog — criação do Capítulo 6 (Engenharia de Grafos aplicada a LLMs) (17/11/2026)

Autoria: agy - ap (Gemini 4 Hydrogen High, painel). Decisões confirmadas pelo operador em 17/11/2026: (1) Opção A, abrindo a Parte II como **Capítulo 6 — Engenharia de grafos aplicada a LLMs** e deslocando os futuros módulos 6–15 para 7–16; (2) mapa de 6 unidades em 18 partes curtas + 6 questões de fechamento; (3) ampliação e reconferência literal do pacote de fontes públicas primárias.

## Mudanças
- **`pacote-de-fontes-engenharia-de-grafos-2026-11-17.md` (`ab2a45074daa6d07` → `6a6290fb7a85376c`):**
  - Baixadas novamente as 15 fontes anteriores mais `anthropic-harnesses` (Anthropic, *Effective harnesses for long-running agents*, 26/11/2025, `https://www.anthropic.com/research/effective-harnesses-for-long-running-agents`, hash `ecb2a3cded33eae9`).
  - Acrescentados os trechos literais `EG-38`–`EG-43` (paralelização, *evaluator-optimizer*, laço de agente e sessões/estado em JSON no *harness*). Conferência: **43 aprovados, 0 reprovados**.
- **`guia-engenharia-llms.html` (`fc6e9b03ec4bf587` → `69e6292f1b8569dd`):**
  - Atualizado o Sumário: inserido o Capítulo 6 abrindo a Parte II (*Parte II — Engenharia de grafos, segurança, contexto e acesso à informação*) e renumerados os módulos futuros 7–16.
  - Adicionado o Capítulo 6 por inteiro (**20 páginas lógicas**, páginas **116 a 135**): abertura (`#capitulo-6`), 18 partes curtas (`6.1a` a `6.6c`, todas entre 338 e 437 palavras até `Pergunta`, `<= 1` tabela por parte, bloco ilustrativo `cod-6-3a` de 5 linhas não executável, 5 molduras `role="img"` + `aria-label`) e 6 questões de fechamento (`c6q1`–`c6q6`: 2 fáceis, 3 médias, 1 difícil).
  - Atualizados Glossário (página **136**, 18 termos do Cap. 6 em ordem alfabética), Referências (página **137**, seção do Cap. 6 com as 16 fontes públicas primárias consultadas em 17/11/2026, sem o vídeo da Attekita Dev) e regras `@media print` para `#capitulo-6` e `#questoes-capitulo-6`.
  - Mantidos Capítulos 1–5 intactos (apenas atualizado o link `page-nav` seguinte de `#questoes-capitulo-5` para `#capitulo-6`).
- **`guia-engenharia-llms.pdf` (`fff4e10a9c2f0a74` → `c52b195af4fca244`):**
  - Regerado com Chrome for Testing 158: **447 páginas A4** (6.315.145 bytes). Conferidas visualmente 6 páginas renderizadas (`2, 3, 358, 374, 377, 411`).
- **`planejamento-completo-estudos-engenharia-llms.md` (`45ee99a31303cfed` → `9829db07603f6204`):**
  - Registrado o Módulo 6 (concluído em 17/11/2026) e renumerados os módulos 7–16; módulos 9, 11 e 12 passaram a referenciar o Capítulo 6 para evitar duplicação.
- **Backup pré-edição:** salvo em `arquivo/antes-capitulo-6-grafos-2026-11-17/`.

## Validações
- `python3 -I ferramentas/conferir-trechos.py --pacote pacote-de-fontes-engenharia-de-grafos-2026-11-17.md --textos /tmp/grafos-textos --projeto .`: **43 aprovados, 0 reprovados**.
- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: **16 OK, 0 FALHA** (137 páginas lógicas, 289 links externos, 157 questões/regiões/fieldsets).
- Ordem de `page-nav` anterior/seguinte verificada por script em todas as 137 páginas: sem falhas de sequência nem termos proibidos.
- Pendentes: reflow em 320 px e leitura em aparelhos reais (Galaxy S24, Nitro 5 e APSRV 55").

Assinatura: agy - ap, 17/11/2026.
