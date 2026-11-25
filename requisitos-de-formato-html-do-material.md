# Requisitos de formato HTML e leitura do material

Data: 13/10/2026. Autoria: codex - ap.

## 1. Finalidade e decisões confirmadas

Registro das decisões do operador para a produção do material. Complementa o [planejamento aprovado](docs/historico/planejamento-completo-estudos-engenharia-llms.md) e os contextos do [Router](contexto-de-estudo-ap-ai-router.md) e da [Nanda Mac](contexto-de-estudo-nanda-mac.md). Em 13/10/2026, o operador autorizou iniciar a estrutura do livro e as páginas prontas para leitura, começando pela capa. Laboratórios permanecem sujeitos a escopo próprio.

- Material completo em **HTML**, produzido por etapas na sequência dos 15 módulos acordados, distribuídos em três blocos.
- Aparência minimalista de livro/Kindle: fundo que lembre papel, texto preto, leitura confortável e uma hierarquia clara de blocos, módulos, capítulos/unidades, títulos e subtítulos.
- Capa contendo apenas o título e subtítulo definidos na seção 3.1, em texto preto e centralizados horizontalmente e verticalmente, com o mesmo fundo de papel claro do restante do livro.
- Fundo uniforme em todas as páginas, incluindo a capa; páginas numeradas a partir do sumário, com a capa sem numeração.
- Texto corrido justificado e primeira linha de cada parágrafo com recuo à esquerda. Títulos, subtítulos, listas e navegação mantêm sua organização própria; os dois textos da capa permanecem centralizados.
- Compatibilidade com Galaxy S24, Nitro 5 de 15 polegadas/1080p e APSRV com tela de 55 polegadas/4K.
- Cinco exercícios de múltipla escolha por módulo: dois fáceis, dois médios e um difícil, preservando a aplicação profissional e a cobertura conjunta dos tópicos.
- Seleção por controles HTML `radio`, com uma resposta por questão e retorno imediato ao marcar.
- Acerto: indicador textual em fundo verde. Erro: indicador textual em fundo vermelho. Seguir a paleta semântica do Bootstrap (`success`, `danger`; `warning` apenas quando houver aviso pertinente).
- Feedback com animação suave somente nas questões; nenhum movimento ornamental na leitura.
- Explicar por que a alternativa selecionada está correta ou incorreta; no erro, informar qual é a correta e por quê.
- **Links externos (regra do operador, 15/10/2026):** todo link para fora do livro (fontes, referências, documentação, vídeos) é criado com `target="_blank" rel="noopener noreferrer"`, abrindo em nova guia. Vale para todo link novo, em qualquer capítulo, glossário e referências. Links internos (`#id`, navegação entre páginas do livro) continuam na mesma guia, para não duplicar o livro. O `validar-guia.py` confere a regra.
- **Linguagem simples e notas de fonte (decisão do operador, 15/10/2026):** texto para leitor leigo (frases curtas, termo explicado na primeira vez, português antes do inglês). Citações, datas, "tradução nossa" e etiquetas de confiança ficam em "Notas de fonte", no fim de cada unidade, antes de "Fontes da unidade"; o botão das perguntas diz "Ver retorno". Detalhes em `changelog-revisoes-1-e-2.md`.

As questões substituem o formato dos cinco exercícios de fechamento descritos anteriormente. A pergunta curta de compreensão de cada unidade permanece no planejamento; não confundir cinco questões do módulo com cinco alternativas por questão.

- **Inclusão de programação (decisão do operador, 23/11/2026):** revoga a proibição de código de 15/10/2026. O material passa a combinar blocos curtos executáveis em Python padrão/`unittest.mock` dentro do HTML (validados por `ferramentas/executar-trechos-de-codigo.py` na convenção `<figure class="bloco-codigo">`) com uma trilha separada de laboratórios práticos (`laboratorios/`), preservando as partes curtas para TDAH. Ver `planejamento-reestruturado-2026-11-23.md`.

## 2. Telas e adaptação

| Ambiente | Base conhecida | Implicação para o HTML |
|---|---|---|
| Galaxy S24, modelo padrão | Samsung: tela de 6,2 polegadas no retângulo completo, 6,0 com cantos arredondados; 2340 × 1080 pixels físicos, AMOLED Dinâmico 2X, até 120 Hz | Projetar primeiro para largura pequena; respeitar barras do navegador, orientação, cantos e área disponível. Não depender de animações contínuas. |
| Nitro 5 | Operador: aproximadamente 15 polegadas, resolução 1080p | Coluna de leitura central, margens confortáveis e texto que não se estenda por toda a largura. |
| APSRV | Operador: 55 polegadas, resolução 4K | Texto maior conforme distância de leitura, mantendo coluna limitada. Uma tela larga não justifica linhas excessivamente longas. |

Resolução física não é largura útil em pixels CSS. Escala do sistema, zoom, orientação e barras do navegador alteram a área de leitura. Usar layout responsivo e viewport adequado; preservar zoom do usuário. Não fixar o S24 em uma largura CSS presumida nem prometer encaixe perfeito apenas com a ficha técnica.

A leitura deve ter rolagem vertical natural. Texto e alternativas se reorganizam sem corte ou rolagem horizontal da página; código e tabelas que precisem de largura maior podem ter rolagem dentro do próprio bloco. Blocos de código e de saída com rolagem levam `role="region"`, `tabindex="0"` e rótulo acessível (conferido pelo `validar-guia.py`). A linha de feedback pode quebrar no celular, preservando a informação completa.

## 3. Direção visual e tipografia

**Direção definida:** apresentação de livro, sem dashboard, cards decorativos ou animação de digitação. Margens, parágrafos curtos, espaçamento consistente e destaques moderados. Código e tabelas entram quando necessários ao conteúdo.

**Pontos de partida propostos para validação visual, não medidas já aprovadas:**

| Elemento | Proposta inicial |
|---|---|
| Fundo | Papel claro levemente quente; por exemplo, `#f5f1e8`. Evitar textura marcada atrás das letras. |
| Texto | Preto (`#000`), com contraste suficiente também nos estados das questões. |
| Fonte do corpo | Serifada com aparência de livro; candidata: `Georgia, "Noto Serif", serif`. Disponibilidade e aparência variam por ambiente e precisam ser conferidas. |
| Código | Fonte monoespaçada, em tamanho legível e com contraste equivalente. |
| S24 | Corpo de 18–20 pixels CSS como ponto de partida. |
| Nitro 5 | Corpo de 20–22 pixels CSS como ponto de partida. |
| APSRV | Corpo de 28–36 pixels CSS como ponto de partida; ajustar à distância e escala efetivas. |
| Entrelinhas | Aproximadamente 1,6; ajustar com a fonte escolhida. |
| Comprimento da linha | Coluna limitada; alvo aproximado de 55–70 caracteres quando houver espaço, reduzido naturalmente no celular. |

No conteúdo, títulos e subtítulos acompanham o tamanho do corpo por proporções moderadas, sem ocupar uma tela inteira. Por decisão posterior do operador, o texto corrido é justificado, com recuo de primeira linha de 1,5 em e hifenização automática em português quando suportada pelo navegador. A última linha de cada parágrafo mantém alinhamento natural à esquerda. Títulos e rótulos do sumário ficam alinhados à esquerda. Fontes/referências bibliográficas ficam em seção identificável, com links legíveis.

Um controle discreto de tamanho de texto é sugestão a discutir, não requisito confirmado. Zoom e aumento de fonte do navegador devem funcionar independentemente dele. A navegação necessária deve ser discreta, com indicação de módulo/unidade e acesso ao índice, preservando o foco no texto.

### 3.1. Capa

Conteúdo exato, confirmado pelo operador:

- **Título:** `Guia para Engenharia de LLMs`
- **Subtítulo:** `Criado por Alexandre Pedroza & LLMs`

A capa terá o mesmo fundo de papel claro das demais páginas e texto preto, conforme a decisão posterior de unificar o background. O conjunto de título e subtítulo ficará centralizado horizontalmente e verticalmente na área útil de leitura, com espaço entre os dois e margens responsivas. O título terá maior destaque; o subtítulo será menor, preservando legibilidade. Ambos poderão quebrar em linhas no celular, sem corte e sem recuo de parágrafo. A capa não recebe número.

Fonte escolhida para a capa: **Georgia**, com fallback `"Noto Serif", serif` quando indisponível. Usar a mesma família no título e subtítulo, com pesos e tamanhos diferentes. A escolha busca a aparência de livro e será conferida visualmente nas três telas. A capa contém somente os dois textos; a assinatura técnica deste Markdown não integra a capa.

## 4. Interação e feedback das questões

Fluxo confirmado:

1. Apresentar enunciado e alternativas claramente associadas aos respectivos `radio`.
2. Ao selecionar, calcular a correção localmente e exibir o feedback sem botão de envio nem chamada a uma LLM.
3. Mostrar `Correto` em fundo de sucesso ou `Incorreto` em fundo de erro, seguido da explicação pertinente e identificação da alternativa correta.
4. Manter o feedback visível para leitura e consulta; “aparecer rapidamente” significa resposta imediata, não desaparecer após poucos segundos.

Proposta de apresentação: indicador compacto em uma linha, com quebra natural quando necessário, e explicação curta logo abaixo. Cor complementa o texto; não é o único sinal de acerto/erro. A linha inteira da alternativa deve ser clicável, com espaço confortável para toque e foco visível para teclado.

Proposta de animação: transição discreta de opacidade em cerca de 150–200 ms, sem mover a página ou retirar o foco. Respeitar `prefers-reduced-motion`, exibindo o feedback sem animação quando solicitado pelo sistema. Anunciar o resultado a tecnologias assistivas sem interromper a leitura desnecessariamente.

Quantidade de alternativas, possibilidade de nova tentativa e regra para preservar a primeira resposta ainda não foram definidas. Sugestão inicial: quatro alternativas plausíveis, uma correta. Não introduzir pontuação, ranking, bloqueio de avanço ou gamificação por rotina.

As questões médias e difícil devem apresentar casos, restrições, textos de configuração ou resultados para analisar, evitando se limitar à memorização; desde a decisão de 23/11/2026, podem também envolver leitura e análise de snippets curtos em Python, enquanto exercícios práticos extensos ficam na trilha de laboratórios (`laboratorios/`). Escolher uma alternativa não demonstra, sozinho, capacidade de projetar ou operar sistemas.

## 5. Implementação e aceite futuros

**Implementação inicial:** HTML semântico e CSS no arquivo local `guia-engenharia-llms.html`, sem backend, banco, framework ou dependências externas. JavaScript será acrescentado quando as questões forem produzidas. A paleta Bootstrap pode ser reproduzida no CSS; seguir suas cores não exige carregar a biblioteca inteira.

Quando a produção do HTML for solicitada, validar:

- Hierarquia de conteúdo, fonte, margens e comprimento de linha nas três telas; retrato e paisagem no celular.
- Fundo uniforme, textos exatos da capa, centralização nos dois eixos e quebra de linhas legível nas três telas.
- Texto justificado e parágrafos com primeira linha recuada; números no rodapé das páginas de leitura, exceto a capa.
- Escala/zoom do usuário e reflow em largura equivalente a 320 pixels CSS, sem corte de conteúdo.
- Radios com toque e teclado; uma seleção por questão; retorno correto para todas as alternativas e explicações coerentes com o gabarito.
- Feedback imediato, persistente e distinguível por texto, com contraste e redução de movimento.
- Leitura de código, tabelas e referências sem alargar a página.

Simulação de viewport não substitui a avaliação de conforto nos dispositivos reais, especialmente na tela de 55 polegadas, cuja distância de leitura não foi informada. A confirmação do formato inicial deve anteceder a multiplicação das unidades, conforme o planejamento. Registros de validação devem indicar o que foi efetivamente conferido, sem alegar aprovação visual dos três dispositivos por uma simulação.

## 6. Ordem editorial e sequência de produção

Estrutura inicial proposta para leitura como livro:

1. Capa.
2. Sumário (índice de conteúdos).
3. Introdução: visão geral, propósito e uso do material.
4. Parte I: capítulos/módulos 1–5.
5. Parte II: capítulos/módulos 6–10.
6. Parte III: capítulos/módulos 11–15.
7. Glossário, ampliado com os termos apresentados.
8. Referências, com fontes pertinentes e identificáveis.

Cada módulo corresponde a um capítulo; as unidades serão suas seções, como 1.1, 1.2 e assim por diante. As cinco questões encerram o módulo. O sumário apresenta a sequência completa desde a primeira versão, mas só páginas prontas têm links; não criar páginas vazias para aparentar conteúdo concluído.

Numeração inicial: sumário = página 1; introdução = página 2; capa sem número. Os números identificam as seções/páginas de leitura do HTML, não cada tela percorrida na rolagem; a extensão visual varia com dispositivo e zoom. Manter a sequência ao acrescentar unidades.

Produção: entregar capa, sumário e introdução; ajustar a apresentação com o operador; acrescentar uma unidade pronta por vez na sequência aprovada; fechar cada módulo com as questões; manter glossário/referências e revisar a coerência do conjunto. Não gerar todos os capítulos antes da avaliação do formato inicial.

Entrega inicial: [livro em HTML](guia-engenharia-llms.html), com capa, sumário e introdução. Próximo conteúdo curricular: capítulo 1, unidade 1.1, “O que é um modelo de linguagem e como ele produz uma resposta?”. A estrutura editorial não altera o currículo aprovado.

Validação da entrega inicial: idioma e viewport presentes, textos exatos da capa, 15 capítulos na ordem do planejamento, seis links internos válidos e nenhuma dependência externa. Links locais dos documentos de estudo conferidos. Conferência visual pendente: os navegadores do controle de interface estavam indisponíveis nesta sessão. Não foram validados o conforto nem a apresentação nos três dispositivos reais.

## 7. Fontes técnicas

Consultadas em 13/10/2026:

- [Samsung — especificações oficiais do Galaxy S24](https://www.samsung.com/br/smartphones/galaxy-s/galaxy-s24-5g-grey-256gb-with-galaxy-watch6-lte-40mm-graphite-f-921bza935fzk/), seção Tela. A página inclui um bundle; as características citadas são do telefone.
- [Bootstrap 5.3 — alertas e significado das cores](https://getbootstrap.com/docs/5.3/components/alerts/).
- [MDN — viewport e pixels CSS](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport).
- [W3C — reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).

Assinatura: codex - ap.

## 8. Parte curta, com resumo, analogia e imagem (13/11/2026)

Decisões do operador em 13/11/2026, por causa do TDAH declarado. Valem para os capítulos seguintes e foram aplicadas ao capítulo 1 e, em 13/11/2026, ao capítulo 2 (20 partes curtas, 2.1a a 2.6d).

- **Estrutura:** cada unidade é dividida em partes curtas, com identificação `1.1a`, `1.1b`. Cada parte tem, nesta ordem: resumo de três linhas ("Em 3 linhas"), imagem opcional, analogia do dia a dia, texto, uma pergunta de múltipla escolha, ponto de retomada e "Notas de fonte". A última parte da unidade traz também "Fontes da unidade" com as linhas *Ler*, *Assistir* e *Aprofundar*.
- **Tamanho:** meta estimada de 400 a 500 palavras por parte; substitui o teto de 1.350 palavras por unidade. No máximo uma tabela por parte.
- **Navegação:** cada parte tem âncoras `#unidade-1-1a` e navegação no pé da página para a parte anterior, a seguinte e o sumário. O sumário lista as unidades e aponta para a primeira parte de cada uma.
- **Imagens e diagramas técnicos (atualizado em 24/11/2026 — Fase 5C; em 25/11/2026 — Cap. 19):**
  - **Aquarelas de abertura:** exatamente **uma imagem por capítulo**, hoje **19** (`figure.imagem` com `data-imagem="cap-1"` .. `"cap-19"`), na abertura de cada capítulo (`#capitulo-1` .. `#capitulo-19`, logo após o `<h2>`): aquarelas de fantasia medieval, 1056×704, sem texto, letras, logotipos ou personagens reconhecíveis, embutidas como `<img src="data:image/jpeg;base64,…" alt="…" width="1056" height="704">` para manter o HTML em arquivo único (JPEG, porque o Chrome repassa JPEG ao PDF sem recodificar; WebP inflava o PDF). Desde a Fase 5E (24/11/2026); antes eram molduras com `role="img"` e `aria-label`. Em 25/11/2026 o CSS `.moldura`/`.moldura-texto`, já sem uso, saiu do HTML.
  - **Diagramas técnicos inline (`<svg>`):** de **18 a 24 diagramas** (hoje 23; `figure.diagrama` com `<figcaption>`) inseridos nas unidades estruturais centrais. Todo `<svg>` é inline (sem fontes, `<script>`, `<image>` ou URLs externas, exceto o namespace `xmlns="http://www.w3.org/2000/svg"`), possui `role="img"`, `viewBox` explícito, `<title id="...">`, `<desc id="...">`, `aria-labelledby` e `aria-describedby` apontando para IDs únicos no documento, alto contraste em tela e papel e largura fluida (`width: 100%; height: auto; max-width: 100%`) sem estouro horizontal em `320 px`.
- **Questões de fechamento:** de cinco a seis por módulo (duas fáceis, as médias e uma difícil). O `validar-guia.py` confere esse intervalo por capítulo.
- **Adaptação de leitura:** frases curtas, listas curtas e troca de assunto controlada; o resumo de três linhas e a analogia abrem cada parte.

## 9. Impressão e exemplos (atualizado em 18/11/2026 e 24/11/2026)

Pedido do operador em 13/11/2026, com compactação tipográfica e de quebra de questões aprovada em 18/11/2026 e suporte a diagramas técnicos SVG inline em 24/11/2026 para manter legibilidade de livro sem páginas quase vazias:

- **Página:** A4, margens de `15 mm` no topo, `17 mm` nas laterais e `17 mm` no pé (reduzidas de `20 mm / 22 mm`). O texto fica centralizado na coluna (`max-width: 100%`), justificado, a `10,5 pt` (`--reading-size: 10.5pt`) e entrelinha `1.42` (CSS de tela preservado intacto em `--reading-size: 1.08rem` / `1.7`).
- **Blocos inteiros e quebra de questões:** título (sem órfãos), legenda, tabela (linha a linha, repetindo `<thead>`), figura (`figure.imagem` com `width: 92mm`; `figure.diagrama` com `max-width: 168mm`, fundo `#fff`, borda `#8a8577`, `padding: 4mm` e `svg { max-height: 115mm }`), fluxo, quadro de resumo, analogia, caixa, bloco de código e navegação de pé de página não se partem entre páginas (`break-inside: avoid`). Em `fieldset.questao`, o enunciado (`> p`) fica preso à primeira alternativa, e cada `.alternativa` bem como o `.gabarito-impresso` permanecem inteiros (`break-inside: avoid`), permitindo quebra apenas entre alternativas para evitar saltos grandes em branco.
- **Fluxo:** só sumário, introdução, capítulos, questões de fechamento, glossário e referências começam em página nova. As partes curtas seguem o fluxo, com `margin-top: 1.15rem`.
- **Capa:** ocupa a página inteira, sem margem.
- **Tabelas e código:** na impressão, a tabela se ajusta à largura da página e o código quebra linha, em vez de rolar ou ser cortado pelo papel.
- **Sumário:** fonte menor na impressão (`0.82em`), para caber em poucas páginas.
- **Exemplos:** nenhum nome de sistema ou de empresa real do autor aparece no guia. Os exemplos de plataforma usam descrições genéricas do mercado (plataforma interna de IA, assistente de programação, API de pagamentos). Os exemplos de empresa usam a Aurora Educação, fictícia, e todos os trechos correspondentes são marcados como *proposta didática*.

Assinatura: claude - pessoal (interrompido por cota), deepseek - conta não verificada; §9 atualizado em 18/11/2026 e §8–§9 atualizados em 24/11/2026 por agy - ap; §8 atualizado em 25/11/2026 por claude - pessoal (Cap. 19).
