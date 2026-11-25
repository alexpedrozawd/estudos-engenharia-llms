# Changelog: Fase 3 da reestruturação (18 capítulos, Chip Huyen e programação em duas camadas) — 23 e 24/11/2026

Fecha a Fase 3 de [planejamento-reestruturado-2026-11-23.md](../historico/planejamento-reestruturado-2026-11-23.md). As Fases 2 e 3 rodaram sem commit intermediário, por decisão registrada no handoff; este é o primeiro registro versionado delas.

## Autoria

- **23/11/2026, sessão anterior** (origem declarada no handoff: `agy (Orchestrator Neon) - ap`; sem changelog próprio, interrompida pelo desligamento do servidor): backup em `arquivo/antes-reestruturacao-huyen-2026-11-23/`; reescrita do HTML para 18 capítulos; `laboratorios/` com `comum/`, `dados/`, runner e labs `01`–`11`; subcomando `fontes.py vigencia` (`L7`); atualização de `openai-model-selection` no pacote do Cap. 14. Registrado aqui a partir do diff, não de relato da sessão.
- **24/11/2026, `claude - pessoal`:** estado revalidado; labs `12`–`18` e projeto integrador; PDF regerado; validações de fechamento e esta documentação.

## O que mudou

- **`guia-engenharia-llms.html`** (`19a020013721c5a5` → `6351f700e6b8644d`): 16 → 18 capítulos, na ordem do plano. Os capítulos novos são o 6 (Engenharia de Dados e Datasets para IA) e o 15 (Fine-tuning, Quantização e Destilação). Os antigos foram renumerados (RAG 11→7, grafos 6→8, segurança 7→12, autodestrutivos 8→13, agentes 12→11, inferência 13→14, roteamento 14→16, LLMOps 15→17, economia 16→18). O guia tem `360` páginas lógicas (`320` partes de conteúdo), `209.641` palavras em partes, `427` questões (gabaritos `106/107/108/106`, nenhuma com a correta estritamente mais longa), `149` tabelas (todas com `.rolagem`), `479` termos no Glossário, `452` `<dfn>` e `68` molduras `data-imagem=`. Cada capítulo tem citações a Chip Huyen (*AI Engineering* e *DMLS*, só referência e síntese autoral), pelo menos um bloco Python executável (`22` no total) e um estudo de caso aberto com rubrica (`L5`).
- **`laboratorios/`** (novo, `L6`): runner `executar_labs.py`, cliente neutro com mock determinístico em `comum/`, dados fictícios da Aurora em `dados/`, os `18` laboratórios e o `projeto_integrador/`, cada um com `README.md`, código e testes (`82` testes, sem rede). Os labs `12`–`18` reproduzem os números dos blocos executáveis dos capítulos:
  - `12` guardrails: máscara de dados pessoais, entrada e saída, bateria adversarial com violação e recusa indevida;
  - `13` autodestrutivos: trava, disjuntor, transação com reversão e proporcionalidade;
  - `14` inferência: memória com KV cache, descarga para CPU, TTFT/TPOT/percentis e goodput;
  - `15` ajuste fino: memória de treino, LoRA em miniatura com parada antecipada, quantização por bloco, fatias e manifesto;
  - `16` roteamento: gateway com contingência, conversa estável e registro;
  - `17` LLMOps: rastros GenAI, PSI, canário, MTTD/MTTR/CFR;
  - `18` economia: custo por sessão, equilíbrio do cache, lote e orçamento.
- **`projeto_integrador/`:** junta os labs 05, 07, 10, 12, 16, 17 e 18 no assistente acadêmico do estudo de caso final.
- **`ferramentas/fontes.py`** e **`testar-fontes.py`:** subcomando `vigencia` (idade e divergência de hash, sem rede). **`testar-ferramentas.py`:** o teste de `mapa` passou de `13.2` para `14.2`, acompanhando a renumeração.
- **`pacote-de-fontes-capitulo-14-...md`:** `openai-model-selection` reconsultada em 19/11/2026 (hash `300a2acd19388e71`), com SR-04 a SR-07, SR-24 e SR-25 trocados pelos trechos atuais.
- **`guia-engenharia-llms.pdf`:** regerado com `628` páginas A4. O anterior (534 páginas) ficou em `arquivo/antes-reestruturacao-huyen-fase-3-2026-11-24/`. O PDF final continua previsto para a Fase 4, depois das imagens.

## Validações após a última edição (24/11/2026)

- `python3 -I ferramentas/guia.py fechar`: `0` falhas (`validar-guia.py` com `16 OK, 0 FALHA`; `executar-trechos-de-codigo.py` com `22 OK, 0 FALHA` e `21` ilustrativos; ids, `<dfn>`, sumário, `.rolagem` e gabaritos OK).
- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: `82` testes OK.
- `testar-ferramentas.py`: `15` OK, inclusive a comparação do PDF gerado com o versionado. `testar-fontes.py`: `12` OK. `testar-livros.py`: OK.
- `auditar-guia-navegador.mjs` (Chromium `1254`, `playwright-core` e `axe-core` instalados em `/tmp`, fora do projeto): reflow em `320 px` sem estouro nas `360` seções; `427/427` questões sem falha; `axe-core` com `45` passes e `0` violações em `1280×800` e `320×640`. O único item `incomplete` é `color-contrast`, o mesmo das rodadas anteriores.
- PDF: páginas `476` (bloco do Cap. 15) e `579` (projeto integrador) renderizadas e inspecionadas.

## Observações e pendências

- O Cap. 15 (novo) tem `7` partes e o Cap. 6 (novo) tem `12`; os demais têm de `17` a `22`. A profundidade ficou como a sessão anterior deixou; ampliar exige decisão do operador.
- `fontes.py vigencia` mostra `97` chaves com hash divergente e `25` fora do cache local. Na conferência do pacote do Cap. 14, SR-35 a SR-37 reprovam porque a fonte `bea` não está no cache; essas linhas não mudaram nesta fase. A reconferência das fontes web fica para a Fase 4.
- **Fase 4:** revisão técnica humana (`L1`), piloto e teste nos três aparelhos (`L2`), imagens em aquarela (`L8`) e PDF final.

Assinatura: claude - pessoal (24/11/2026); trabalho de 23/11/2026 atribuído conforme o handoff.
