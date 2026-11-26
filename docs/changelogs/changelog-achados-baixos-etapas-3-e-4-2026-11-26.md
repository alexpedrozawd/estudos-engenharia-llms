# Changelog — achados baixos das Etapas 3 e 4 (26/11/2026)

Autoria: claude - pessoal. Os três achados baixos das auditorias das Etapas 3 e 4 foram corrigidos a pedido do operador. HTML, PDF e `laboratorios/` inalterados.

1. **P02 — escolha e teste nas mesmas perguntas (p-valores otimistas).** `executar_rag_real.py` ganhou `--fracao-selecao` (padrão `0.5`) e `dividir_selecao_teste()`: metade das `148` perguntas escolhe a variante pelo MRR, e a estatística (`Wilson`, McNemar e bootstrap) usa só a outra metade. Na reexecução, todas as chamadas ao LLM saíram do cache e a memória do Ollama ficou fora do registro (`execucoes/p02-rag-pgvector-2026-11-26T06-21-09-0300.json`).
   - O *reranker* LLM segue escolhido e melhora o MRR em `+0,16` a `+0,18` contra todas as variantes (IC acima de zero).
   - No acerto@4 (`63/74`), não é significativo contra as híbridas (`p = 0,125` e `0,22`). Antes, com seleção e teste juntos, todos os `p` eram menores que `0,02`.
2. **P07 — o campo `julgamento_humano` sugeria rótulo humano.** Passou a `rotulo_referencia`. `eval_pipeline.rotulo_de_referencia()` aceita o nome antigo e recusa rótulo ausente. `montar_casos_ampliados.py` migra os dados, e o arquivo novo é equivalente ao anterior (conferido campo a campo). O registro do P07 não muda, porque o campo não entra nas chamadas ao juiz.
3. **Container do garak — `--network host` e `label=disable`.** `executar_garak.sh` agora usa a rede própria do Podman (`pasta`) com só a porta do P06 encaminhada (`-T,${P06_PORTA:-8001}`) e montagens com rótulo SELinux (`:ro,z` e `:z`). Conferido contra o P06 real com `web_injection.StringAssemblyDataExfil` (`2/2` aprovadas).

## Validação

- `executar_smoke.py`: `136` OK (`2` testes novos e asserções a mais no P02 e no P07).
- `gerar-exercicios.py`: `--checar` com `82` trechos; `--verificar mercado` OK.
- Hashes de HTML e PDF sem mudança. As demais suítes estão no fechamento do commit.
