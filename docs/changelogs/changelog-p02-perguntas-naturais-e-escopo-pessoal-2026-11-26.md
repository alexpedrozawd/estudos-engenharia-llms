# Changelog — P02 com perguntas naturais e escopo pessoal (26/11/2026)

Autoria: claude - pessoal; revisão, ajustes documentais e execução em GPU por agy - ap (Gemini 4 Hydrogen High). HTML, PDF e `laboratorios/` inalterados.

## Decisões do operador (26/11/2026)

- Corrigir o achado médio da revisão da Etapa 3: as `123` perguntas do corpus ampliado do P02 começam por "Sobre <tema>:".
- O deploy em nuvem (antiga Etapa 6b) e a revisão humana dos dados ficam **fora do escopo**, porque o material é de uso pessoal. Não serão propostos nem perguntados de novo. `CLAUDE.md`, `README.md`, `roadmap.md`, o plano de prontidão, o mapa de vagas, `casos-de-system-design.md`, o README de `k8s/` e o changelog da Etapa 7 foram atualizados. O roteiro de entrevista do guia de portfólio continua citando esses dois pontos como "o que faria a seguir", porque é material de entrevista, não pendência do projeto.

## P02 — perguntas sem o prefixo do tema

**Causa:** `gerar_corpus_ampliado.py` punha na frente de cada pergunta o tema usado para escrever o documento. Isso resolve a ambiguidade ("qual a multa?" num corpus de `57` documentos), mas repete o vocabulário do próprio documento, e a recuperação fica mais fácil do que com perguntas reais.

**Correção preparada:**

  - `02_rag_producao/reescrever_perguntas.py`: o 27B reescreve cada pergunta como quem usa o atendimento escreveria (aluno, professor, coordenação ou servidor, conforme o perfil da pergunta), citando o assunto com palavras próprias. A reescrita só entra se:
    - passar em `checar_reescrita`, que é determinística: de `4` a `30` palavras, termina com `?`, não contém a expressão do tema, não repete mais da metade das palavras do tema (no mínimo `1`), não contém a resposta nem o trecho que responde;
    - o mesmo LLM, às cegas e com temperatura `0`, confirmar que ela pede a mesma informação sobre o mesmo assunto.

    Se a reescrita é recusada, há até `6` tentativas com o motivo da recusa (e, a partir da 3ª tentativa, com as formulações já recusadas no prompt e nota explícita de que pode manter uma palavra-chave do assunto, evitando repetição idêntica no cache de `qa059`). Se alguma pergunta ficar sem reescrita válida, o script sai com código `2` e não grava nada. O tema sai da lista do gerador (`TEMAS`), e não de uma expressão regular, porque alguns temas têm dois-pontos. Um JSON inválido do modelo vira recusa com motivo, para não travar a retomada pelo cache. A pergunta gerada fica em `pergunta_original`, e rodar de novo dá o mesmo resultado.
- `07_evals_e_multimodal/montar_casos_ampliados.py` lê `pergunta_original` quando existe. Assim o P07 continua igual: após a reescrita de `consultas_ampliadas.json`, o arquivo `casos_eval.json` gerado continua idêntico ao do Git, conferido por `git diff`.
- Teste `test_reescrita_tira_o_tema_sem_entregar_a_resposta` em `test_p02_rag.py`: confere as travas, valida que todas as `123` perguntas reescritas passam em `checar_reescrita` e verifica que `prompt_reescrita` varia quando recebe uma formulação anterior recusada.

## Execução concluída na GPU (26/11/2026)

1. **Reescrita (`reescrever_perguntas.py --registrar`):** `123/123` perguntas aceitas (`113` na 1ª tentativa, `9` na 2ª, `1` na 4ª — justamente `qa059`, após corrigir o laço de cache em tentativas repetidas), `12` recusas intermediárias (`11` por mudança de sentido/assunto pouco claro e `1` por repetição do tema). A sobreposição lexical média com o tema caiu de `1,0` para `0,108`. Registro: [`execucoes/p02-reescrita-perguntas-2026-11-26T12-16-39-0300.json`](../../laboratorios-mercado/execucoes/p02-reescrita-perguntas-2026-11-26T12-16-39-0300.json).
2. **Conferência amostral por modelo de fronteira:** amostra determinística de `15` perguntas (`sha256("rev-reescrita|" + id)`) mais `qa015` e `qa016`, em [`execucoes/revisao-fronteira-reescrita-p02-2026-11-26.json`](../../laboratorios-mercado/execucoes/revisao-fronteira-reescrita-p02-2026-11-26.json): `15/15` naturais sem o prefixo e `0` vazamentos; `12/15` preservaram o sentido exato (inclusive `qa059`, `qa015` e `qa016`), e `3/15` (`qa007`, `qa109`, `qa054`) tiveram desvio leve ou ambiguidade sem o cabeçalho de tema.
3. **Nova rodada no `pgvector` (`executar_rag_real.py --registrar`):** `57` documentos, `275` trechos, `151` perguntas (`148` com resposta, `3` sem resposta), `qwen3-embedding:0.6b` + `qwen3.8:27b-ud-iq3_xxs` 100% em VRAM (`11,14 GiB`), `1.436` chamadas do cache + `1.107` reais. Registro: [`execucoes/p02-rag-pgvector-2026-11-26T12-28-44-0300.json`](../../laboratorios-mercado/execucoes/p02-rag-pgvector-2026-11-26T12-28-44-0300.json).

**Efeito da remoção do prefixo (comparado a `p02-rag-pgvector-2026-11-26T06-21-09-0300.json`):**

| Métrica | Com `"Sobre <tema>:"` | Sem prefixo (natural) |
|---|---|---|
| `recall@4` vetorial (`n = 148`) | `0,801` | `0,503` |
| `recall@4` lexical (`n = 148`) | `0,794` | `0,399` |
| `recall@4` híbrida RRF (`n = 148`) | `0,824` | `0,497` |
| `recall@4` *reranker* LLM (`n = 148`) | `0,902` | `0,571` |
| MRR *reranker* LLM (`n = 148`) | `0,846` | `0,539` |
| Acerto@4 teste *reranker* LLM (`n = 74`) | `63/74` [`0,75`; `0,91`] | **`45/74`** [`0,49`; `0,71`] |
| Geração com conteúdo esperado (`n = 148`) | `127/148` [`0,79`; `0,91`] | **`63/148`** [`0,35`; `0,51`] (`25/25` base, `38/123` ampliadas) |
| Fidelidade lexical / Recusas | `0,881` / `3/3` | `0,862` / `3/3` |
| Vazamentos ACL (`26` consultas) | `0` | `0` |

Sem o vocabulário copiado do tema, a busca lexical despencou e arrastou o RRF sem peso para baixo da vetorial pura (`39/74` contra `41/74`). O *reranker* LLM seguiu em primeiro na seleção (MRR `0,521`) e, no teste (`n = 74`), manteve ganho de MRR de `+0,12` a `+0,20` sobre todas as demais variantes (IC 95% acima de zero), vencendo a lexical (`p = 0,0018`), a RRF (`p = 0,031`) e o *reranker* léxico (`p = 0,031`), mas sem diferença significativa no acerto@4 contra a vetorial (`7` ganhos, `3` perdas, `p = 0,344`).

**Aceite:** `123/123` reescritas válidas, registro novo do P02 em `execucoes/`, P07 inalterado e documentos atualizados com os números novos (`02_rag_producao/README.md`, `laboratorios-mercado/README.md`, `CLAUDE.md`, `README.md`, `roadmap.md` e `docs/preparacao-para-vaga/`).

## Validação

- `executar_smoke.py`: `147` OK. `laboratorios/executar_labs.py`: `84` OK. `testar-ferramentas.py --rapido`: `22` OK (`2` pulados de PDF).
- `gerar-exercicios.py --checar` (`82` trechos em `27` labs) e `--verificar mercado`: OK.
- `montar_casos_ampliados.py` reproduz `casos_eval.json` sem diferença.
- Hashes de HTML (`da073a1210e36792`) e PDF (`8431be316ec3b881`) sem mudança.
