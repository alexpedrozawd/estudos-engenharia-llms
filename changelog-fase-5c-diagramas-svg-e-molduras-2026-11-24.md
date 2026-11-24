# Changelog — Fase 5C: Diagramas técnicos SVG, redução de molduras (73 → 18) e PDF provisório (24/11/2026)

Data: 24/11/2026. Autoria: `agy - ap`.
Plano de referência: [`roteiro-central-evolucao-nota-10-por-sessao.md`](roteiro-central-evolucao-nota-10-por-sessao.md) (Sessão 3 — Fase 5C) e [`plano-evolucao-mercado-e-nota-10-2026-11-24.md`](plano-evolucao-mercado-e-nota-10-2026-11-24.md).

## 1. Resumo das alterações

1. **Redução das molduras `data-imagem=` (`73 → 18`):**
   - Removidas todas as `73` molduras tracejadas que ficavam espalhadas dentro das unidades em [`guia-engenharia-llms.html`](guia-engenharia-llms.html) (nenhum parágrafo referenciava as molduras antigas).
   - Inseridas exatamente **18 molduras** (`data-imagem="cap-1"` .. `"cap-18"`) na abertura de cada capítulo (`#capitulo-1` .. `#capitulo-18`, logo após `<h2>`), preservando a descrição (`aria-label`) de fantasia medieval sem texto (com ajuste no Cap. 7 trocando menção a código numérico por selo metálico entalhado). A geração das 18 aquarelas finais permanece na Fase 5E (`L8`).
2. **22 diagramas técnicos `<svg>` inline acessíveis (`figure.diagrama`):**
   - Adicionado CSS responsivo (`width: 100%; height: auto; max-width: 100%`) e regras de impressão A4 (`break-inside: avoid`, fundo `#fff`, `max-width: 168mm`, `svg { max-height: 115mm }`) em [`guia-engenharia-llms.html`](guia-engenharia-llms.html).
   - Inseridos `22` diagramas `<svg>` inline sem fontes, `<script>` ou URLs externas (exceto `xmlns`), com `role="img"`, `viewBox`, `<title id="...">`, `<desc id="...">`, `aria-labelledby`, `aria-describedby`, IDs únicos (`svg-<slug>-*`) e `<figcaption>`:
     - Cap. 1: `1-4a-prefill-decode` (`#unidade-1-4a`), `1-5c-transformer-qk` (`#unidade-1-5c`)
     - Cap. 2: `2-1d-arquitetura-5-camadas` (`#unidade-2-1d`), `2-6b-fila-disjuntor` (`#unidade-2-6b`)
     - Cap. 4: `4-5e-decodificacao-restrita` (`#unidade-4-5e`)
     - Cap. 5: `5-4a-tres-avaliadores` (`#unidade-5-4a`)
     - Cap. 6: `6-2b-fluxo-dados-etl` (`#unidade-6-2b`)
     - Cap. 7: `7-4a-rag-hibrido-rrf` (`#unidade-7-4a`)
     - Cap. 8: `8-1a-graphrag-vs-estado` (`#unidade-8-1a`)
     - Cap. 9: `9-2b-orcamento-contexto` (`#unidade-9-2b`), `9-5a-compactacao-contexto` (`#unidade-9-5a`)
     - Cap. 10: `10-6a-mcp-sandbox` (`#unidade-10-6a`)
     - Cap. 11: `11-1b-laco-harness` (`#unidade-11-1b`)
     - Cap. 12: `12-4b-defesa-profundidade` (`#unidade-12-4b`)
     - Cap. 13: `13-3a-preservacao-rollback` (`#unidade-13-3a`)
     - Cap. 14: `14-2b-memoria-gpu-kv` (`#unidade-14-2b`), `14-3b-gqa-pagedattention` (`#unidade-14-3b`), `14-6c-desagregacao-radix` (`#unidade-14-6c`)
     - Cap. 15: `15-2b-memoria-lora-qlora` (`#unidade-15-2b`)
     - Cap. 16: `16-4a-gateway-roteamento` (`#unidade-16-4a`)
     - Cap. 17: `17-6a-pipeline-llmops-canario` (`#unidade-17-6a`)
     - Cap. 18: `18-5a-cache-prefixo` (`#unidade-18-5a`)
3. **Documentação de formato e validadores:**
   - Atualizados §8 e §9 de [`requisitos-de-formato-html-do-material.md`](requisitos-de-formato-html-do-material.md).
   - Atualizado [`ferramentas/validar-guia.py`](ferramentas/validar-guia.py) com 2 novas verificações (`diagramas SVG acessíveis e sem dependências externas` e `molduras ou imagens com texto alternativo válido`, totalizando 18 checagens) e checagem de `<image>`/`<use>` externos.
   - Atualizado [`ferramentas/guia.py`](ferramentas/guia.py) para ignorar `<svg>` na contagem de palavras de prosa e expor `diagramas_svg` e `molduras_imagem` em `contar` e `fechar`.
   - Atualizado [`ferramentas/testar-ferramentas.py`](ferramentas/testar-ferramentas.py) com conferência Golden de `diagramas_svg`/`molduras_imagem` e 4 testes de mutação para `<svg>` (`role="img"`, `<desc>`, `viewBox`, `<script>`).
4. **PDF provisório regerado:**
   - Backup automático do PDF anterior (`657` páginas, sha `53129052eebf7800`) gravado em `arquivo/antes-fase-5c-diagramas-svg-2026-11-24/guia-engenharia-llms.pdf` (fora do Git).
   - Novo PDF provisório [`guia-engenharia-llms.pdf`](guia-engenharia-llms.pdf) gerado com `664` páginas A4 (sha `482a150cb91f3efc`).

## 2. Estado e validações executadas após a última edição

- `guia-engenharia-llms.html`: `385` partes, `229.063` palavras nas partes, `453` questões (`113/113/114/113`), `157/157` tabelas com `.rolagem`, `528` termos no Glossário (`502` `<dfn>` únicos), `26` blocos Python executáveis, `22` `diagramas_svg`, `18` `molduras_imagem`, sha256 `45e11a0cd880451a`.
- `guia-engenharia-llms.pdf`: `664` páginas A4, `16.465.078` bytes, sha256 `482a150cb91f3efc`.
- `python3 -I ferramentas/guia.py fechar --guia guia-engenharia-llms.html`: `0 falhas` (`validar-guia.py` `18 OK, 0 FALHA`; `executar-trechos-de-codigo.py` `26 OK + 21 ilustrativos`).
- Auditoria geométrica de SVGs no Chromium (`1280×800` e `320×640`): `22/22` SVGs com `0` sobreposições de texto, `0` transbordos de caixa e `0` overflows; inspeção visual de amostras HTML (`320 px` e `1280 px`) e páginas do PDF (`p7`, `p33`, `p236`, `p455`, `p596`) via `pdftoppm` aprovada sem cortes ou quebras no meio dos diagramas.
- `node ferramentas/auditar-guia-navegador.mjs` (Chromium 1254, Playwright e axe-core): `docClient=320`, `docScroll=320`, `bodyScroll=320`, `385` seções, `totalEstouros=0`, `453/453` questões OK (`140` acertos, `313` erradas), `axe-core` `46 passes` e `0 violations` em `1280x800` e `320x640`, `errosDePagina=[]`, `falhas=0`.
- `python3 -I ferramentas/testar-ferramentas.py` (completo, sem `--rapido`): `Ran 19 tests -> OK`.
- `python3 -I -W error::ResourceWarning ferramentas/testar-fontes.py`: `Ran 14 tests -> OK`.
- `python3 -I ferramentas/testar-livros.py`: `Ran 2 tests -> OK`.
- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: `Ran 84 tests -> OK`.

Assinatura: agy - ap.
