# Changelog — Fase 5E: aquarelas finais (`L8`), PDF definitivo e encerramento (24/11/2026)

Data: 24/11/2026. Autoria: `claude - pessoal`.
Plano de referência: [`roteiro-central-evolucao-nota-10-por-sessao.md`](../historico/roteiro-central-evolucao-nota-10-por-sessao.md) (Sessão 5 — Fase 5E) e [`plano-evolucao-mercado-e-nota-10-2026-11-24.md`](../historico/plano-evolucao-mercado-e-nota-10-2026-11-24.md).

## 1. Resultado

| Item | Situação |
|---|---|
| `L1` — revisão técnica humana (Caps. 5, 12, 14, 15, 17 e 2 projetos de `laboratorios-mercado/`) | **Bloqueado.** O operador informou em 24/11/2026 que não há revisores. Nada foi simulado. |
| `L2` — piloto com 2–3 estudantes | **Bloqueado.** O operador informou em 24/11/2026 que não há estudantes. Nada foi simulado. |
| `L8` — 18 aquarelas de abertura | **Concluído.** Geradas localmente, inspecionadas uma a uma e embutidas no HTML. |
| PDF definitivo | **Concluído.** `664` páginas A4, `18.808.421` bytes, sha `81d2fffd7394a880`; anterior (provisório `482a150cb91f3efc`) em `arquivo/antes-fechamento-nota-10-2026-11-24/`. |

## 2. Como as aquarelas foram geradas

- **Modelo e motor:** Qwen-Image 2.1 Q8 (GGUF) no `stable-diffusion.cpp` (`sd-cli`, Vulkan, RX 9070 16 GB), o mesmo motor local do modo mídia do painel, com codificador `qwen3vl_8b_int8_convrot` e VAE `qwen_image_2.1_vae_bf16`. Execução em escopo `systemd-run --user --scope` transitório com `MemoryMax=18G` e ambiente limpo (sem credenciais). Nada foi instalado; a imagem base do Bazzite não mudou.
- **Parâmetros:** `1056×704`, `25` passos, `cfg 4`, `euler`, `--offload-to-cpu --flash-attn on --vae-tiling`; cerca de 63 s por imagem.
- **Prompt:** prefixo fixo de estilo (`Medieval fantasy watercolor painting, storybook illustration, soft translucent washes, visible cold-press paper texture, warm muted earthy palette, gentle light.`), cena abaixo e sufixo `No text, no letters, no words, no numbers, no writing, no logos, no signature, no watermark.`; prompt negativo: `text, letters, words, numbers, writing, typography, calligraphy, caption, watermark, signature, logo, photorealistic, 3d render, modern objects`.
- **Revisão visual:** 8 das 18 foram regeradas por falha objetiva — pseudoletras e coroa no mensageiro (`cap-12`), algarismos romanos num relógio (`cap-15`), marcas em X (`cap-17`), layout de quadrinhos (`cap-11`), composição vazia (`cap-18`), cena fora da descrição (`cap-16`, `cap-5` duas vezes). Versão final: sem texto legível, logotipos ou personagens reconhecíveis; o `cap-4` tem rabiscos ilegíveis nas folhas (sem letras). Os textos alternativos (`alt`) são os mesmos das molduras da Fase 5C.

| Imagem | Semente | Cena (prompt) |
|---|---|---|
| `cap-1` | `5001` | a cheerful bard with a lute standing on a wooden bench in the middle of a cozy tavern, surrounded by villagers listening by candlelight |
| `cap-2` | `5002` | a cutaway view of a medieval inn showing three rooms side by side connected by wooden doors: a hall with tables, a kitchen with a cauldron over a fire, and a front counter with a closed ledger book |
| `cap-3` | `5003` | a scribe seated at a table covered with maps receives a wax-sealed rolled scroll from a messenger, while keeping one hand flat on the open map in front of him, studying the terrain |
| `cap-4` | `5004` | a scribe handing a messenger two loose sheets of parchment and pointing with his finger at the gap that separates them, the sheets covered only in faint illegible scribbles |
| `cap-5` | `7005` | at a rustic tavern table, three villagers of different trades (a baker in a white apron, a smith in a leather apron, a weaver in a shawl) judge the same loaf of bread; nobody is eating: the baker points at the golden crust, the smith points at the soft white crumb of a torn piece, and the weaver calmly sets her untouched slice back down on the plate with a doubtful expression |
| `cap-6` | `5006` | a scriptorium workshop where a master sorts parchments into three wicker baskets on a long table, while apprentices clean and stack loose sheets under the light of a tall window |
| `cap-7` | `5007` | in front of an endless towering bookshelf, a researcher holds a brass magnifying glass, searching for one small engraved metal seal on the spine of an ancient tome |
| `cap-8` | `5008` | a cartographer's table with two open maps: the left one connects villages and rivers with trade lines, the right one shows crossroads with arrows going back and forth between travel stations, all drawn without any writing |
| `cap-9` | `5009` | a candlelit cartography workshop where an archivist picks only three essential scrolls from dozens of closed wooden boxes and places them on a small work table |
| `cap-10` | `5010` | at a wrought iron counter, a counselor hands over a single wax-sealed note, while a clerk behind an iron grille inspects the seal before opening a cabinet of files |
| `cap-11` | `6011` | a single unified scene, not a comic strip, no panels: a messenger in light armor walks out of a stone tower along a path that circles to several small craft workshops (a potter, a smith, a carpenter), handing a rolled scroll to one craftsman and carrying replies back, while at the tower door a clerk sits writing in an open ledger with blank pages |
| `cap-12` | `6012` | a humble messenger without crown, in a simple tunic, standing in a village square reading aloud from one long unrolled parchment held facing himself, so only the plain blank back of the parchment is visible to the viewer; a stern royal herald on one side and chatty gossiping villagers on the other side listen, both groups equally close, no seal on the parchment |
| `cap-13` | `5013` | a brass automaton holding an enchanted broom, sweeping rare scrolls from a records room into a fireplace, while a worried scribe tries to close the door |
| `cap-14` | `5014` | three stone workshops on a green hillside: a small one with a thin chimney, a medium one full of organized shelves, and a large one with many workbenches in a row, all linked by dirt paths to the same road |
| `cap-15` | `6015` | a clockmaker's workshop lit by colorful stained-glass windows, an artisan pausing at his bench between adjusting a fine brass gear with brass tweezers and turning toward a large open book with blank pages on the shelf beside him; brass gears, springs and tools around, no clock faces, no dials |
| `cap-16` | `6016` | a cartographer in a robe standing at a wooden table indoors, looking down at a large hand-drawn map divided into four colored regions, each region crossed by a small road marked by a differently shaped little waymarker stone (round, square, pointed, flat), map drawn only with shapes and lines |
| `cap-17` | `6017` | an ancient weathered stone city wall with a new dark iron gate fitted into the original arched opening; beyond the gate two paths bordered by small wooden stakes split apart, one leading to a small tidy vegetable test garden and the other to a busy colorful market fair with plain cloth awnings |
| `cap-18` | `6018` | a well-balanced composition filling the frame: a merchant standing beside a two-pan balance scale on a wooden table, weighing small sacks of grain, his half-loaded wooden cart behind him on a village road, and a small open account book with blank pages lying on the table |

## 3. Inserção no HTML

- Cada `figure.imagem[data-imagem="cap-N"]` trocou a moldura por `<img src="data:image/jpeg;base64,…" alt="…" width="1056" height="704" decoding="async">`. O HTML continua um arquivo único, sem recurso externo.
- **Por que JPEG embutido:** com WebP, o Chrome recodificava as imagens sem perda no PDF (`40,4 MB`); com JPEG (`q80`, `4:2:0`, progressivo; `2,45 MB` no total), o Chrome repassa o arquivo ao PDF (`18,8 MB`). Custo: HTML `6.156.758` bytes (antes `2.885.919`).
- CSS: saem `.moldura` e `.moldura-texto` (tela e impressão); entra `figure.imagem img { display: block; width: 100%; height: auto; border-radius: 4px; }`. A largura de impressão (`92 mm`) e a proporção `3:2` foram mantidas, então a paginação não mudou (`664` páginas).
- [`requisitos-de-formato-html-do-material.md`](../../requisitos-de-formato-html-do-material.md) §8 atualizado.
- Originais PNG, WebP descartados, prompts e script de geração ficam em `arquivo/aquarelas-fase-5e/` (fora do Git); HTML e PDF anteriores em `arquivo/antes-fase-5e-aquarelas-2026-11-24/`.

## 4. Validações (HTML final, sha `bb004776a6cdc9cb`)

- `guia.py fechar`: `0` falhas (`validar-guia.py` `18 OK`; `26` blocos executáveis OK; `453` questões e gabaritos; `18` figuras com texto alternativo).
- `auditar-guia-navegador.mjs` (`--guia`, `--playwright`, `--axe`, `--chrome`): `385` seções sem estouro em `320 px`, `453/453` questões, `axe-core` com `48 passes` e `0` violações em `1280×800` e `320×640`, `0` erros de página.
- Inspeção visual: abertura do Cap. 5 em `320 px` (imagem `280×187`, carregada) e página `378` do PDF (abertura do Cap. 12); `pdfimages` lista `18` imagens `1056×704 jpeg`.
- `testar-ferramentas.py` completo `19` OK; `testar-fontes.py` `14` OK; `testar-livros.py` OK; `executar_labs.py` `84` OK; `laboratorios-mercado/executar_smoke.py` `56` OK.

## 5. Riscos e pendências

- **Licença do modelo:** segundo um plano interno de mídia do operador (fora deste repositório), o Qwen-Image 2.1 usa a licença *Qwen Research*, descrita como restritiva. Não foi conferida online nesta sessão. Antes de qualquer uso comercial do guia, conferir os termos sobre as imagens geradas.
- `L1` e `L2` bloqueados: a nota final continua limitada pela falta de validação humana fora da bolha de IA. Para retomar, o operador fornece revisores/estudantes e as evidências nominais.
- Herdadas da 5D (não bloqueiam): treino QLoRA real (precisa de GPU CUDA), vLLM só configurado, corpus RAG pequeno.

Assinatura: claude - pessoal.
