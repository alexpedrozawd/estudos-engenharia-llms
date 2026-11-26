# Changelog — Etapa 3: escala estatística em P02, P04 e P07 (26/11/2026)

Autoria: claude - pessoal. Etapa 3 do [plano de prontidão para vaga pleno](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md). HTML, PDF e `laboratorios/` inalterados.

## Decisões do operador (25 e 26/11/2026)

- Dados sintéticos gerados pelo `qwen3.8:27b-ud-iq3_xxs`, com deduplicação, divisão por grupo e revisão humana amostral (recomendação do plano).
- Execução autônoma até o fim, sem handoff no meio. Por isso, a rotulagem humana do P07 e a revisão amostral **ficaram pendentes**: nenhum rótulo humano foi inventado. Os 28 pares novos de calibração têm rótulo **por construção** (defeito conhecido).
- Um commit para a Etapa 3 inteira, em vez de dois: a divisão existia para a rotulagem humana não travar o P04, e esse bloqueio deixou de existir.

## Base comum (`laboratorios-mercado/mercado_base/`)

- `dados_sinteticos.py`: normalização, quase duplicatas por Jaccard de trigramas e agrupamento por união-busca, aceitando qualquer similaridade (no P04, o cosseno de embeddings).
- `estatistica.py`: Wilson 95%, McNemar exato, bootstrap da diferença pareada e `comparar_binario`.
- `cliente_openai.py`: `ClienteChatComCache`, cache em disco por hash do pedido, para execuções longas e retomáveis; guarda a latência medida na chamada original.

## P04 — QLoRA

- `dados/chamados_aurora.jsonl`: de `36` para `360` chamados (`30` por estrato; `36` manuais e `324` sintéticos), com os campos `origem` e `grupo`. Geração em `gerar_chamados_sinteticos.py`: `578` candidatos; descartados `11` por tamanho, `4` quase duplicatas e `60` com rótulo divergente na conferência às cegas pelo 27B; `0` com PII. Paráfrases com cosseno `>= 0,85` formam `15` grupos.
- `qlora_receita.py`: a divisão por hash passa a respeitar grupos. Um grupo nunca se divide entre treino, validação e teste; sem o campo `grupo`, o resultado é o mesmo de antes.
- `executar_ciclo_qlora.py`: treina por época candidata, escolhe na validação, avalia o teste uma vez e aplica o portão. É retomável e recusa a pasta de passos feitos com outros dados (código `3`).
- Execução real na RX 9070 XT (ROCm): validação `0,635` (base) → `0,811` / `0,878` / `0,973` (1 / 3 / 6 épocas). No teste (`123`), a base marcou `0,610` [`0,52`; `0,69`] e o adaptador de 6 épocas `0,976` [`0,93`; `0,99`], com `45` ganhos e `0` perdas, McNemar `p < 10⁻⁶`. O portão **aprovou** sem intervenção.

## P02 — RAG

- Corpus ampliado e opcional (`ampliado=True`; o P06 segue no corpus base): mais `45` documentos (`8` restritos) e `123` perguntas, chegando a `57` documentos, `275` trechos e `151` perguntas. Uma pergunta só entra se o trecho literal resolver na segmentação real.
- `executar_rag_real.py`: `--corpus`, `--cache-llm` e `estatistica_recuperacao` (Wilson por variante, McNemar no acerto@4 e bootstrap no MRR). A conferência do conteúdo esperado agora ignora acentos.
- Execução real: o *reranker* LLM chegou a `134/148` [`0,85`; `0,94`] e venceu as outras `4` variantes (McNemar de `p = 0,0003` a `p = 0,02`). ACL com `0` vazamentos em `26` consultas restritas. Geração: `127/148` com o conteúdo esperado e `3/3` recusas corretas.

## P07 — Evals

- `montar_casos_ampliados.py` (determinístico): `150` casos (`16` manuais, `123` do corpus do P02 e `11` recusas por construção) e `40` pares de calibração (`12` pré-rotulados e `28` por construção, com `4` tipos de defeito e a resposta boa em A em metade).
- `eval_pipeline.py`: kappa com IC por bootstrap, concordância por origem com Wilson, Wilson das vitórias de B e teste do sinal. `executar_evals_real.py`: `--cache-llm`, latência lida do cache e memória omitida quando nenhuma chamada foi real.
- Execução real (4B gera, 27B julga): `kappa = 0,955` [`0,86`; `1,0`] (`1,0` nos pares por construção e `0,871` nos pré-rotulados). Placar `B = 137`, `empate = 9`, `A = 4`; diferença de nota `+0,98` [`0,84`; `1,11`].

## Auditoria (`/auditorias`, 2 rodadas)

- **Médio, corrigido:** os `12` pares antigos estavam marcados como `humano`, mas foram pré-rotulados pelo autor do lab na Fase 6, sem revisão humana independente. Passaram a `pre_rotulado`, e o registro foi regerado.
- **Médio, corrigido:** o ciclo do P04 reaproveitaria JSON de outra versão dos dados e misturaria resultados no registro. Agora uma impressão (dados, modelo e fração) é conferida e há teste.
- **Baixos registrados, sem correção:**
  - no P02, a variante vencedora é escolhida nas mesmas perguntas do teste, o que deixa os p-valores otimistas (documentado no README);
  - o campo `julgamento_humano` mantém o nome por compatibilidade.

## Limites honestos

- O gerador e o conferente ou juiz são o mesmo 27B: os conjuntos ficam mais fáceis que o mundo real, e os ganhos valem para eles.
- **Pendências com o operador:** revisar `36` chamados do P04 e cerca de `12` perguntas do P02, e rotular pares do P07 de forma independente.
- No P04, `6` épocas é o maior candidato da grade.

## Validação

- `executar_smoke.py`: `131` OK (era `113`).
- `gerar-exercicios.py --checar`: `82` trechos em `27` labs. `--verificar mercado`: OK.
- `laboratorios/executar_labs.py`: `84` OK. `testar-ferramentas.py`: `24` OK. `testar-fontes.py` e `testar-livros.py`: OK.
- HTML (`da073a1210e36792`) e PDF (`8431be316ec3b881`) conferidos por hash, sem mudança.
- Varredura de segredos no diff: ver o fechamento do commit.
