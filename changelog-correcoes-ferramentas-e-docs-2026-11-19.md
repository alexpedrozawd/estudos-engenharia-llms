# Changelog: correções pós-entrega das ferramentas e atualização da documentação (19/11/2026)

Autoria: agy - ap (Gemini 4 Hydrogen High). `guia-engenharia-llms.html` (`19a020013721c5a5`) e `guia-engenharia-llms.pdf` (`10ff8c03dd8dfe83`, 534 páginas A4) não foram alterados.

## O que mudou

- `ferramentas/guia.py` (`cmd_mapa`) e `ferramentas/testar-ferramentas.py`: leitura única do HTML em `cmd_mapa` e verificação de fronteira de prefixo (`test_mapa_respeita_fronteira_de_numero`), evitando que `mapa 1` retorne os capítulos 10 a 16.
- `ferramentas/testar-fontes.py`, `ferramentas/testar-llm-local.py` e `ferramentas/benchmark-llm-local.py`: fechamento de arquivos com `with open(...)`, chamada a `server_close()` no servidor HTTP de `testar-fontes.py` e limpeza da pasta temporária de `testar-llm-local.py`, eliminando os `ResourceWarning`.
- `ferramentas/fontes.py` (`cmd_manifesto`): passou a listar explicitamente os pacotes fora do manifesto por não usarem tabela com `Hash bruto (16)` (Caps. 2–5 e arquivos de conferência/equilíbrio).
- Pacotes de fontes e `protocolo-de-economia-de-tokens-entre-sessoes.md`: removida marcação Markdown residual em `IL-06` (`pacote-de-fontes-capitulo-13-inferencia-local-2026-11-17.md`) e `SG-54` (`pacote-de-fontes-capitulo-7-seguranca-e-governanca-2026-11-17.md`) para bater literalmente com o texto HTML extraído (`581/754` trechos aprovados em `fontes.py conferir`); registrada no pacote do Capítulo 14 a atualização da página `openai-model-selection` pela OpenAI após 17/11/2026 (`8253c6508713ed99` → `300a2acd19388e71`, afetando `SR-04`–`SR-07` e `SR-24`–`SR-25`) e o motivo exato de `cormack-rrf` (`https` redireciona para `http`).
- `README.md`, `roadmap.md` e `CLAUDE.md`: alinhados ao estado real de 19/11/2026 (`316` partes, `175.906` palavras em partes, `376` questões, `141` tabelas com `.rolagem`, `402` termos `<dt>` no glossário, `395` `<dfn>`, `722` links externos / `275` URLs únicas, `67` molduras, PDF A4 de `534` páginas) e integrados ao `plano-de-lacunas-para-nota-10-2026-11-19.md` (decisões abertas do operador e ordem L1–L8).

## Validações após a última edição

- `python3 -I -W error::ResourceWarning ferramentas/testar-fontes.py`: 10/10 OK.
- `python3 -I -W error::ResourceWarning ferramentas/testar-llm-local.py`: 14/14 OK.
- `python3 -I -W error::ResourceWarning ferramentas/testar-ferramentas.py`: 15/15 OK (inclui PDF de 534 páginas e mapa com fronteira numérica).
- `python3 -I ferramentas/guia.py fechar`: 0 falhas (`16 OK, 0 FALHA` em `validar-guia.py`, HTML `19a020013721c5a5`, PDF `10ff8c03dd8dfe83` com 534 páginas).

Assinatura: agy - ap
