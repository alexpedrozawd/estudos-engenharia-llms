# Changelog — P02 com perguntas naturais e escopo pessoal (26/11/2026)

Autoria: claude - pessoal; revisão, ajustes documentais e fechamento offline por agy - ap (Gemini 4 Hydrogen High). HTML, PDF e `laboratorios/` inalterados.

## Decisões do operador (26/11/2026)

- Corrigir o achado médio da revisão da Etapa 3: as `123` perguntas do corpus ampliado do P02 começam por "Sobre <tema>:".
- O deploy em nuvem (antiga Etapa 6b) e a revisão humana dos dados ficam **fora do escopo**, porque o material é de uso pessoal. Não serão propostos nem perguntados de novo. `CLAUDE.md`, `README.md`, `roadmap.md`, o plano de prontidão, o mapa de vagas, `casos-de-system-design.md`, o README de `k8s/` e o changelog da Etapa 7 foram atualizados. O roteiro de entrevista do guia de portfólio continua citando esses dois pontos como "o que faria a seguir", porque é material de entrevista, não pendência do projeto.

## P02 — perguntas sem o prefixo do tema

**Causa:** `gerar_corpus_ampliado.py` punha na frente de cada pergunta o tema usado para escrever o documento. Isso resolve a ambiguidade ("qual a multa?" num corpus de `57` documentos), mas repete o vocabulário do próprio documento, e a recuperação fica mais fácil do que com perguntas reais.

**Correção preparada:**

- `02_rag_producao/reescrever_perguntas.py`: o 27B reescreve cada pergunta como quem usa o atendimento escreveria (aluno, professor, coordenação ou servidor, conforme o perfil da pergunta), citando o assunto com palavras próprias. A reescrita só entra se:
  - passar em `checar_reescrita`, que é determinística: de `4` a `30` palavras, termina com `?`, não contém a expressão do tema, não repete mais da metade das palavras do tema (no mínimo `1`), não contém a resposta nem o trecho que responde;
  - o mesmo LLM, às cegas e com temperatura `0`, confirmar que ela pede a mesma informação sobre o mesmo assunto.

  Se a reescrita é recusada, há até `4` tentativas com o motivo da recusa. Se alguma pergunta ficar sem reescrita válida, o script sai com código `2` e não grava nada. O tema sai da lista do gerador (`TEMAS`), e não de uma expressão regular, porque alguns temas têm dois-pontos. Um JSON inválido do modelo vira recusa com motivo, para não travar a retomada pelo cache. A pergunta gerada fica em `pergunta_original`, e rodar de novo dá o mesmo resultado.
- `07_evals_e_multimodal/montar_casos_ampliados.py` lê `pergunta_original` quando existe. Assim o P07 continua igual: com os dados atuais, o arquivo gerado é idêntico ao do Git, conferido por `git diff`.
- Teste novo `test_reescrita_tira_o_tema_sem_entregar_a_resposta`: confere as travas e verifica se toda pergunta já reescrita no arquivo congelado passa por elas.

**Por que a execução ficou pendente:** na primeira tentativa, a GPU estava ocupada por um jogo, com `15,1` GiB de `16` GiB de VRAM em uso. Só `2,3` GB do 27B couberam na GPU, cada chamada levou cerca de `17` s, e o restante rodaria por horas na CPU, disputando a máquina. A execução foi interrompida, o modelo foi descarregado, e os dados do P02 não mudaram (conferido por `cmp`). Na retomada com Hydrogen, o jogo seguia ativo usando `12,47` GiB de `15,92` GiB de VRAM (`rocm-smi`), mantendo apenas `~3,45` GiB livres — insuficiente para o modelo 27B (`10` GB). As reescritas vistas nessa tentativa motivaram a conferência de sentido: `qa015` trocou "ouvidoria" por "suporte interno", e `qa016` perdeu o assunto.

## Como concluir (com a GPU livre)

1. Reescrever:

   ```bash
   .venv-mercado/bin/python -I laboratorios-mercado/02_rag_producao/reescrever_perguntas.py --registrar
   ```

   O script usa o Ollama em `127.0.0.1:11434` e o `qwen3.8:27b-ud-iq3_xxs`.
2. Conferir, por modelo de fronteira, uma amostra das reescritas contra `pergunta_original`.
3. Subir o `pgvector` com `podman compose -f laboratorios-mercado/compose.yaml --profile rag up -d postgres`, só o banco, porque o perfil `rag` também sobe o `llama.cpp` em CPU, e rodar:

   ```bash
   PGVECTOR_DSN=postgresql://aurora:senha-local-de-laboratorio@127.0.0.1:5433/rag \
   .venv-mercado/bin/python -I laboratorios-mercado/02_rag_producao/executar_rag_real.py \
     --embed-base-url http://127.0.0.1:11434/v1 --embed-modelo qwen3-embedding:0.6b \
     --llm-base-url http://127.0.0.1:11434/v1 --llm-modelo qwen3.8:27b-ud-iq3_xxs \
     --llm-reasoning-effort none --cache-llm rascunho-local/p02-execucao/cache-llm.json --registrar
   ```

   As `28` perguntas base saem do cache. As `123` novas exigem cerca de `1.100` chamadas ao 27B.
4. Atualizar os números do P02 no README dele, em `laboratorios-mercado/README.md` e em `docs/preparacao-para-vaga/`. A diferença para o registro `p02-rag-pgvector-2026-11-26T06-21-09-0300.json` mede o efeito do prefixo.

**Aceite:** `123/123` reescritas válidas, um registro novo do P02 em `execucoes/` e os documentos com os números novos.

## Validação

- `executar_smoke.py`: `147` OK (era `146`). `laboratorios/executar_labs.py`: `84` OK. `testar-ferramentas.py`: `24` OK.
- `gerar-exercicios.py --checar` (`82` trechos em `27` labs) e `--verificar mercado`: OK.
- `montar_casos_ampliados.py` reproduz `casos_eval.json` sem diferença.
- Hashes de HTML (`da073a1210e36792`) e PDF (`8431be316ec3b881`) sem mudança.
