# Plano de reestruturação do material e adaptação de leitura (TDAH)

Data: 13/11/2026. Autoria: claude - pessoal. Origem: conversa com o operador no painel (ap-ai-router).
Estado: decisões do operador registradas; **nada aplicado ao guia, aos requisitos ou ao handoff ainda**. Este arquivo não autoriza ações: revalide o estado antes de agir. Ao aplicar, ele passa a valer sobre o teto de palavras e a estrutura de unidade de `requisitos-de-formato-html-do-material.md` e do plano mestre.

## 1. Decisão geral
- Reestruturar o guia **por completo, por partes, um capítulo por vez**. Para cada capítulo: (1) tabela do que o texto diz, lacunas e fontes; (2) o operador decide o que entra; (3) só então reescrever.
- Começar pelo capítulo 1. Recomendado: tabela de lacunas do capítulo 1 inteiro antes de escrever a 1.7 (aguarda confirmação do operador).
- "Parte I" do guia = capítulos 1 a 5; só 1 e 2 estão escritos.

## 2. Adaptação de leitura (TDAH declarado pelo operador)
Base: o operador respondeu a uma entrevista em 13/11/2026.
- **Foco:** 5 a 10 minutos, às vezes menos, conforme o assunto. Desatenção é a dificuldade principal.
- **Derrubam a leitura:** texto longo, muitos termos novos, tabelas densas, troca de assunto. Retomar depois de pausa **não** é problema.
- **Ajudam:** resumo de 3 linhas no topo, listas curtas, analogias do dia a dia, imagens que chamem a atenção.
- **Formato aprovado: todos os subitens (1.1, 1.2, 2.1 etc.) viram partes curtas.** Cada parte tem:
  1. resumo de 3 linhas no topo;
  2. listas curtas e frases de até 15 palavras (regra de linguagem simples mantida);
  3. uma analogia do dia a dia, de preferência de RPG, jogos ou cultura pop;
  4. uma imagem (seção 3);
  5. uma pergunta;
  6. ponto de retomada de uma linha;
  7. "Notas de fonte" no fim, como já era.
- **Tamanho:** meta proposta de 400 a 500 palavras por parte (estimativa, não medida). Substitui o teto de 1.350 palavras por unidade. Tabelas pequenas, no máximo uma por parte.
- Termos novos: poucos por parte, cada um explicado na primeira vez.

## 3. Imagens
- Uma imagem por parte, **gerada por IA no Qwen-Image 2.1 local**, com ajustes pequenos (poucos tokens). O operador aprova cada uma.
- Estilo base: aquarela de fantasia medieval, tons quentes de papel (combina com o fundo `#f5f1e8` do guia), sem texto nem letras na imagem, formato 3:2 (1056×704).
- Texto alternativo (`alt`) em cada imagem. Embutir no HTML em WebP leve, sem dependência externa (regra do guia).
- Checar a saída: tema, texto indevido, cortes, personagens ou logotipos reconhecíveis.

### Referências de interesse do operador
- **Animes:** Attack on Titan, Jujutsu Kaisen, Fullmetal Alchemist: Brotherhood, Pokémon.
- **Jogos:** The Last of Us, Diablo, The Witcher, God of War, Cyberpunk 2077, Tomb Raider, Doom, Warcraft, Skyrim.
- **Séries e filmes:** O Senhor dos Anéis, Game of Thrones, Harry Potter, Star Wars, IT, Hellraiser, Jurassic Park.
- Também: RPG, época medieval, cultura geek/pop.
- **Como usar:** ao gerar qualquer imagem, escolher um ou mais mundos da lista como inspiração de ambiente, clima e estética, ligados à analogia da parte. **Regra fixa (confirmada pelo operador em 13/11/2026):** não pedir personagens nominais, logotipos, texto nem cenas icônicas reconhecíveis; revisar a saída. Direitos autorais importam se o guia for compartilhado ou publicado. Para estudo pessoal o risco é baixo.
- A licença do Qwen-Image 2.1 é a "Qwen Research" (restritiva), segundo o registro interno do painel (não verificada na fonte). Reler antes de publicar.

### Como gerar (fora do painel, testado em 13/11/2026)
O motor é `media_engine.generate_image` do AP AI Router. Imagem de teste de 1056×704 levou 57 s. Chamar com o Python da venv do painel, em primeiro plano, com `timeout`, sem deixar serviço em segundo plano:
```
sys.path.insert(0, ".../ap-ai-router/panel/backend"); import media_engine
asyncio.run(media_engine.generate_image(prompt, workdir, width=1056, height=704, seed=N))
```
Fluxo: eu escrevo o pedido, gero, confiro a imagem, ajusto uma vez se preciso, converto para WebP e embuto. O motor recusa se a GPU estiver ocupada (mais de 4 GiB em uso) ou se faltar memória. Alternativa do operador: Modo mídia do painel (botão **+**).

## 4. Nova unidade 1.7, "Tipos de modelos" (fim do capítulo 1, depois da 1.6)
Motivo: usa conceitos de 1.2 a 1.5; não renumera 1.1 a 1.6 (links internos e `validar-guia.py`). O parágrafo "Dois tipos de modelo…" da 1.2 (pesos abertos, proprietários, fronteira, local) muda para a 1.7.

| Parte | Assunto | Analogia (proposta) |
|---|---|---|
| 1.7a | Por acesso (fronteira, pesos abertos, local) e por função (gerativo ou de decisão) | Três construções: castelo distante, biblioteca, cabana |
| 1.7b | Por treino e dados: instruído, raciocínio, multimodal, embeddings, reranker, guarda | Classes de RPG: mago, bardo, arquivista, guarda do portão |
| 1.7c | Por arquitetura e tamanho (MoE, SLM, difusão) e além do texto (mundo, VLA) | Grupo de aventureiros de tamanhos diferentes |

Imagem de teste da 1.7a: aprovada como estilo; ajuste pedido: "exatamente três construções" (a saída trouxe cabanas a mais). Tabela de tipos por eixo: saída, treino e uso, dados que entram, arquitetura, tamanho e local de execução. Em volta: uma questão nova no capítulo 1, termos no glossário, sumário e ponteiro na 1.6.
O uso prático de decisão, embeddings e rerankers entra quando os capítulos 5, 10 e 13 forem escritos.

### Fontes conferidas em 13/11/2026 (leitura da página)
- Decisão: [Thoughtworks Radar, 04/11/2026, anel Assess](https://www.thoughtworks.com/radar/platforms/decision-models); [Simon Willison, 21/09/2026](https://simonwillison.net/2026/Sep/21/jev/); [TypeSafe, Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) (15/09/2026; números de velocidade e custo são da empresa, sem avaliação independente); [InfoQ, 01/10/2026](https://www.infoq.com/news/2026/10/typesafe-ai-jev-released); [Kev, repositório](https://github.com/jaredpalmer/kev) (Apache-2.0; 1.0 com 0,8B, 4B, 9B e 27B; limites declarados pelos autores).
- Modelo instruído: [Ouyang et al., 04/03/2022](https://arxiv.org/abs/2203.02155). Raciocínio: [DeepSeek-R1, 22/01/2025](https://arxiv.org/abs/2501.12948). SLM: [Belcak et al., 02/06/2025](https://arxiv.org/abs/2506.02153) (artigo de posição). Difusão para texto: [LLaDA, 14/02/2025](https://arxiv.org/abs/2502.09992); [Mercury, 17/06/2025](https://arxiv.org/abs/2506.17298). Mamba: [Gu e Dao, 01/12/2023](https://arxiv.org/abs/2312.00752). Guarda: [Llama Guard, 07/12/2023](https://arxiv.org/abs/2312.06674).
- Embeddings e rerankers: [Sentence-BERT, 27/08/2019](https://arxiv.org/abs/1908.10084); [MTEB, 13/10/2022](https://arxiv.org/abs/2210.07316); [Passage Re-ranking with BERT, 13/01/2019](https://arxiv.org/abs/1901.04085).
- Robótica: [π0, 31/10/2024](https://arxiv.org/abs/2410.24164); [Gemini Robotics 2, 30/07/2026](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots). Modelo de mundo: [Genie 3, 05/08/2025](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/).
- "Aberto": [Open Source AI Definition 1.0 (OSI)](https://opensource.org/ai/open-source-ai-definition) (a página não traz data).
- **Só fonte secundária (não usar como fato):** Microsoft Decision-1 (blog Towards AI); "DiffusionGemma"; valores e datas de AMI Labs e World Labs; Mercury 3 sem data de lançamento na página oficial.
- **Lacunas:** data da OSAID 1.0 (o link do anúncio deu 404); data de lançamento do Kev; fonte primária de modelos de mundo além do Genie 3.
- Sem número de fabricante (velocidade, preço, valuation) no guia, sem fonte e data.

## 5. Pendências
1. Ponto de partida: recomendação do claude (13/11/2026) = tabela de lacunas do capítulo 1, depois um piloto do formato novo em uma parte curta (1.1a) antes de multiplicar; aguarda o "sim" do operador.
2. Confirmar o estilo de imagem (aquarela medieval). A regra das referências já é fixa.
3. Ao aplicar: atualizar `requisitos-de-formato-html-do-material.md`, o plano mestre, `validar-guia.py` (se contar unidades) e o handoff; refazer sumário, glossário e questões.
4. Imagem teste da 1.7a está só na pasta de entrega do painel (`img-1-7a-teste.png`); ainda não entrou no HTML.

claude - pessoal, 13/11/2026
