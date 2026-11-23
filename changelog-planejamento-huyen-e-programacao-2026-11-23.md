# Changelog: planejamento reestruturado (Chip Huyen + programação) e extrator local de livros (23/11/2026)

Autoria: agy - ap (Gemini 4 Hydrogen High). `guia-engenharia-llms.html` (`19a020013721c5a5`) e `guia-engenharia-llms.pdf` (`10ff8c03dd8dfe83`, 534 páginas A4) não foram alterados.

## O que entrou

- `ferramentas/livros.py` e `ferramentas/testar-livros.py`: extrator e leitor localizado de PDFs locais (`extrair`, `ler`, `achar`, `pagina-png` via `pdftotext` e `pdftoppm`), salvando textos e índices exclusivamente em `cache-fontes/livros/` (ignorado pelo `.gitignore`).
- Extração local e mapa dos dois livros de Chip Huyen (`cache-fontes/livros/ai-engineering.txt`, `dmls.txt`, `indice.json` e `mapa-livros.md`, fora do Git): *AI Engineering* (`535` páginas, `171.606` palavras, dez/2024) e *Designing Machine Learning Systems* (`389` páginas, `133.414` palavras, mai/2022).
- `planejamento-reestruturado-2026-11-23.md`: planejamento curricular aprovado para reorganização em `18` capítulos (incluindo Cap. 6 novo de Engenharia de Dados/Datasets e Cap. 15 novo de Fine-tuning/Quantização/Destilação), com programação em duas camadas (blocos curtos executáveis no HTML + `18` laboratórios e projeto integrador em `laboratorios/`), preservação do formato TDAH e integração das lacunas `L1`–`L8`.
- `requisitos-de-formato-html-do-material.md`, `roadmap.md`, `README.md`, `CLAUDE.md` e `protocolo-de-economia-de-tokens-entre-sessoes.md`: atualizados para refletir a inclusão de programação, o novo planejamento aprovado e as ferramentas em `ferramentas/livros.py`.

## Validações após a última edição

- `python3 -I -W error::ResourceWarning ferramentas/testar-livros.py`: `2/2 OK` (inclui geração e extração de PDF sintético e verificação de `git check-ignore` em `cache-fontes/livros/`).
- `python3 -I -W error::ResourceWarning ferramentas/testar-fontes.py && python3 -I -W error::ResourceWarning ferramentas/testar-llm-local.py && python3 -I -W error::ResourceWarning ferramentas/testar-ferramentas.py --rapido`: suíte completa sem `ResourceWarning`.
- `python3 -I ferramentas/guia.py fechar`: `0` falhas (`16 OK, 0 FALHA`, HTML `19a020013721c5a5`, PDF `10ff8c03dd8dfe83` com 534 páginas).

Assinatura: agy - ap
