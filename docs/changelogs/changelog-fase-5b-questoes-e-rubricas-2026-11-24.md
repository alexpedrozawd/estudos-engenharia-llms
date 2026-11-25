# Changelog: Fase 5B — Endurecimento pedagógico das 108 questões e 18 rubricas (24/11/2026)

Registra a conclusão da **Sessão 2 (Fase 5B)** em [guia-engenharia-llms.html](../../guia-engenharia-llms.html), focada exclusivamente nas `18` seções de fechamento (`#questoes-capitulo-1` a `#questoes-capitulo-18`): endurecimento dos distratores das `108` questões de múltipla escolha (`91` modificadas, priorizando médias e difíceis e removendo caricaturas em fáceis) e inclusão de critérios quantitativos e bloqueios explícitos nas rubricas de todos os `18` estudos de caso. Conforme política definida para o ciclo, o PDF provisório ([guia-engenharia-llms.pdf](../../guia-engenharia-llms.pdf), `657` páginas) permaneceu inalterado nesta fase e será regerado ao final da **Fase 5C**.

## Autoria

- **24/11/2026, `agy - ap`:** auditoria e reescrita localizada de distratores/explicações nas `18` seções `#questoes-capitulo-*`, endurecimento quantitativo das `18` rubricas de estudo de caso, validações completas sem regerar PDF, atualização documental e fechamento Git da Fase 5B.

## O que mudou

- **Questões de fechamento (`91 / 108` endurecidas; `0 / 345` inline alteradas):**
  - Substituídos distratores caricatos ou com pistas estilísticas por *trade-offs* reais de arquitetura e produção (ex.: `temperature: 0` sem checar `stop_reason`, cache de prefixo vs. *context rot*, vazamento de estatísticas de *features*, *position bias*, `token passthrough`, erro composto de etapas, cálculo de KV cache sem fator 2 ou sem corte GQA, ajuste prematuro, troca de modelo/esforço no meio da conversa e retenção de PII em logs).
  - Nas questões difíceis de múltiplos eixos (`q5`, `c2q5`, `c10q6`, `c11q6`, `c13q6`, `c14q6`, `c15q6`, `c16q6`, `c17q6`, `c18q6`), os distratores passaram a combinar 2–3 acertos reais com 1–2 falhas sutis plausíveis.
  - Reescritas as `data-explicacao` correspondentes (`0` falhas em `Correta.`/`Incorreta.`), preservando a distribuição exata dos gabaritos (`A=113, B=113, C=114, D=113`), `LONGEST_TRUE = 0` e `SHORTEST_TRUE = 0` (gap `> 20` caracteres nas 108 questões de fechamento).
- **Rubricas quantitativas e critérios de bloqueio (`18 / 18` estudos de caso atualizados):**
  - **Caps. 1–4:** `0` erros determinísticos em cálculo de juros/descontos, `p95 ≤ 2,5 s`/`≤ 3 s`, sobrecarga de tokenização PT/ES (`~20–40%`), `Idempotency-Key` com `0` duplicatas, teto de `≤ 3` tentativas + disjuntor (`> 20%` `429/503`), estágio *Crawl* com `100%` de revisão humana, `0` injeções XML e conformidade de schema `≥ 99%` com no máximo `1` reparo.
  - **Cap. 5:** intervalo de Wilson 95% explícito (`v1 = 36/50 → [58,3%, 82,5%]` vs. `v2 = 40/50 → [67,0%, 88,8%]`), `n ≥ 100` para `+10 pp` a 95% e bloqueio por `2` regressões críticas + queda na fatia de transferidos (Paradoxo de Simpson).
  - **Caps. 6–11:** `0` vazamentos de PII no ETL, piso por estrato (`≥ 25` e `≥ 15%` recusas), `κ ≥ 0,80`, `0%` de sobreposição treino/teste, `recall@5`/`recall@10 ≥ 90%` com `0%` de editais vencidos e `p95 ≤ 400 ms`, limiar monetário na aresta condicional, orçamento de contexto (`8K–16K` com compactação em `70–80%` e cache `≥ 70%`), consolidação para `≤ 5–8` ferramentas (`≥ 95%` válidas no 1º disparo, `0` escritas sem aprovação) e conta explícita de erro composto (`0,95^5 ≈ 77,4%` vs. `0,95^10 ≈ 59,9%`).
  - **Caps. 12–13:** `100%` de mascaramento de PII antes do provedor externo, meta adversarial (`≤ 1%`/`0%` violação crítica e `≤ 5%` recusa indevida, `p95 ≤ 150 ms`), `0` exclusões irreversíveis, bloqueio em `≥ 2` repetições, `100%` de *dry-run* e bloqueio do agente sem ganho frente a script determinístico.
  - **Caps. 14–15:** conta explícita em `2 × 24 GiB = 48 GiB` (`27B Q4_K_M ≈ 15,4 GiB` de pesos; `30 × 32K` em `f16` exigiria `150 GiB`, reduzido para janela ativa `8K` em `q8_0` = `18,75 GiB`, SLOs `TTFT p95 ≤ 1,5 s`, `TPOT p95 ≤ 50 ms/tok`, `goodput ≥ 95%` e `0%` de descarga para CPU); e conta de treino `13B` em `24 GB` (pesos `26 GB` + `~78 GB` gradientes/AdamW = `≥ 104 GB` inviáveis em ajuste completo vs. QLoRA 4 bits, só liberando treino se prompt + modo estrito não baixarem erro de layout de `30%` para `< 5%`).
  - **Caps. 16–18:** roteamento de `60–80%` simples ao local, erro `429 < 1%`, fallback `≥ 90%`, `0` trocas no meio da conversa, canário `5% → 25% → 100%` com rollback se erro subir `> 1–2 pp`, `PSI` (alerta `0,10–0,20`, bloqueio `≥ 0,20`), `MTTD < 1 h`, `MTTR < 30 min`, `CFR < 10%`, orçamento mensal e peso `~100×` da saída na latência.
- **Documentação atualizada:**
  - Atualizados [roteiro-central-evolucao-nota-10-por-sessao.md](../historico/roteiro-central-evolucao-nota-10-por-sessao.md), [plano-evolucao-mercado-e-nota-10-2026-11-24.md](../historico/plano-evolucao-mercado-e-nota-10-2026-11-24.md), [CLAUDE.md](../../CLAUDE.md), [README.md](../../README.md) e [roadmap.md](../../roadmap.md).

## Hashes (SHA-256, 16 primeiros dígitos)

- `guia-engenharia-llms.html`: `81ff0e778f2ba073` (`385` partes, `453` questões, `157` tabelas, `528` termos no Glossário, `502` `<dfn>` únicos, `304` links web únicos, `22.881` linhas)
- `guia-engenharia-llms.pdf`: `53129052eebf7800` (`657` páginas A4 — mantido da rodada anterior; regeração provisória prevista ao fim da Fase 5C)

## Validações executadas

- Auditoria Python das `453` questões e `18` rubricas: `A=113, B=113, C=114, D=113`, `LONGEST_TRUE = 0`, `BAD_EXP = 0`, `SHORTEST_TRUE = 0`, `CARIC = 0`, `91/108` questões de fechamento e `18/18` rubricas atualizadas (`0/345` inline alteradas).
- `python3 -I ferramentas/guia.py fechar --guia guia-engenharia-llms.html`: `0` falhas (`16 OK, 0 FALHA` em `validar-guia.py`; `26 OK, 0 FALHA` em `executar-trechos-de-codigo.py` + `21` ilustrativos; `157/157` tabelas em `.rolagem`; `0` `<dfn>` ou IDs duplicados; sequência `1..385`).
- `node ferramentas/auditar-guia-navegador.mjs` (Chromium `1254`, Playwright e `axe-core`): `docClient=320, docScroll=320, bodyScroll=320`, `385` seções, `totalEstouros: 0`, `453/453` questões com `falhas: []`, `axe-core` com `45 passes` e `0 violations` em `1280×800` e `320×640`, `errosDePagina: []`.
- `python3 -I ferramentas/testar-ferramentas.py --rapido`: `Ran 15 tests -> OK (skipped=2)`.
- `python3 -I -W error::ResourceWarning ferramentas/testar-fontes.py`: `Ran 14 tests -> OK`.
- `python3 -I ferramentas/testar-livros.py`: `Ran 2 tests -> OK`.
- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: `Ran 84 tests -> OK`.

Assinatura: agy - ap (24/11/2026).
