# Changelog: ajustes de impressão e troca dos exemplos (13/11/2026)

Autoria: deepseek - conta não verificada. Projeto: a raiz deste projeto (não é repositório Git). Base: HTML de 13/11/2026, hash `3bfbea0ae27668a9`, guardado em `arquivo/antes-ajustes-visuais-e-exemplos-2026-11-13/`.

## 1. O que mudou

**Impressão.** O PDF passa a ser A4, com margens de 20 mm no topo e 22 mm nas laterais e no pé, e nenhum bloco dividido entre páginas:

- título, legenda, figura, fluxo, quadro de resumo, analogia, caixa, questão, bloco de código e navegação de pé de página: `break-inside: avoid` e `break-after: avoid` no que vem antes;
- tabelas: linha a linha inteira, com o cabeçalho repetido quando a tabela continua;
- parágrafos: no mínimo três linhas no fim e no começo da página (órfãs e viúvas);
- tabelas e código não rolam nem são cortados no papel: a tabela se ajusta à largura e o código quebra linha;
- só sumário, introdução, capítulos, questões de fechamento, glossário e referências começam em página nova; as partes curtas seguem o fluxo, o que evita páginas quase vazias (eram 31, ficaram 3: capa, fim do capítulo 1 e última página);
- capa ocupa a página inteira, sem margem;
- sumário com fonte menor (0,82 em) cabe em duas páginas.

**Exemplos.** Saíram o AP AI Router e a Nanda Mac.

- AP AI Router: trocado por descrições genéricas do mercado — plataforma interna de IA, assistente de programação, API de pagamentos e de pedidos, trava de inferência local. Os fatos que vinham da documentação e do código internos passaram a *proposta didática*.
- Nanda Mac: trocada por **Aurora Educação**, empresa fictícia de educação digital e consultoria. Nome, pessoas e processos são inventados.
- As notas de fonte que citavam documentos de estudo e código internos foram reescritas; as etiquetas "verificado no código local", "observado em ata" e "histórico ou desativado" saíram do guia, e a legenda das etiquetas foi encurtada nos dois capítulos.
- A seção de referências não lista mais os documentos internos; ganhou um parágrafo dizendo que os exemplos de empresa são fictícios.

## 2. Arquivos alterados

- `guia-engenharia-llms.html` — SHA-256 `dfddc29b34cc3fda…` (2.829 linhas, 37 páginas lógicas).
- `guia-engenharia-llms.pdf` — SHA-256 `409485402bd67700…` (141 páginas, A4, texto a 12 pt).
- `requisitos-de-formato-html-do-material.md` — §9, regras de impressão e de exemplos.
- `CLAUDE.md` — estado novo e ponteiro para o handoff desta rodada.
- Novos: este changelog e `handoff-ajustes-visuais-e-exemplos-2026-11-13.md`.
- Backup: `arquivo/antes-ajustes-visuais-e-exemplos-2026-11-13/` (HTML `3bfbea0ae27668a9`, PDF `079a8b94d8648a10`).

## 3. Validações executadas

- `python3 -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: **16 OK, 0 FALHA**.
- PDF gerado com Chrome headless (`--print-to-pdf`), 141 páginas A4; conferência visual de 26 páginas renderizadas em PNG: capa, sumário, tabelas, fluxos, questões, blocos de código, glossário e referências.
- Contagem de páginas com menos de 500 caracteres: 3 (capa, 77 e 141). Antes eram 31 com menos de 700.
- Não executado: impressão em papel, leitor de tela, aparelhos reais.

## 4. Pendências

- Imagens: continuam só molduras, conforme a regra fixa; a geração é a última etapa.
- Conferir a leitura em papel, se o operador quiser.
- Fontes dos capítulos 4, 8, 13 e 15 seguem sem trecho literal conferido.
- Commit e push: bloqueados, porque o projeto não é repositório Git.

Assinatura: deepseek - conta não verificada.

## Ajuste final: capa, justificação e imagens (13/11/2026)

- Capa: fundo branco, sem a cor de papel; texto passa a "Criado por Alexandre Pedroza & LLMs" (sem "(Claude e GPT)"). Validador e `requisitos-de-formato-html-do-material.md` atualizados.
- Texto justificado também em listas, resumos, analogias, caixas, questões, glossário e fontes. Cabeçalhos, legendas, tabelas e código continuam à esquerda.
- Molduras de imagem centralizadas (120 mm no papel; a altura máxima antiga encolhia a moldura para a esquerda).
- PDF: 140 páginas A4; validador 16 OK, 0 FALHA. Backup anterior em `arquivo/antes-capa-justificado-2026-11-13/`.

claude - pessoal

## Revisão e correção dos achados (13/11/2026)

Revisão adversarial do trabalho do DeepSeek, com conferência na web, e correção de todos os achados. Backup anterior: `arquivo/antes-revisao-correcoes-2026-11-13/`.

**Conferido nas fontes (71 links buscados):** 28 de 30 trechos literais em inglês bateram; os 2 divergentes foram corrigidos ("50 percent"; "might not match"). Datas do arXiv (16 artigos) conferem. Título e canal dos 5 vídeos conferem; data e duração não foram reconferidas. Também conferem: livro de Jurafsky e Martin (19/08/2026), Jev, Radar da Thoughtworks (nov/2026), Kev, MCP 2026-07-28, DeepSeek-R1 v2, OSAID 1.0, cache e lote da Anthropic, OpenAI, Ollama, llama.cpp, SRE e Fowler.

**Corrigido:**
- PDF: gabarito impresso abaixo de cada questão (34), blocos "ver retorno" e caixa query/key/value abertos na impressão, numeração de páginas no rodapé (navegação web não imprime mais), identificadores da tabela da 2.2 sem quebra.
- Idempotency-Key: rascunho ativo (rev. 08, 22/10/2026); recusa de chave reutilizada: 422 (e 409 só para pedido em andamento), com Stripe como exemplo de resposta salva.
- TTFT, latência entre tokens e tokens por segundo (NVIDIA) no lugar de "termo do livro".
- Questões: letra correta balanceada (A 9, B 8, C 8, D 9) e alternativa correta a mais longa em 13 de 34 (antes 25), nenhuma com mais de 25% de folga; legenda "Escolha uma alternativa" (antes repetia "Pergunta").
- Capítulo 2: texto da abertura e da introdução agora diz que o formato é o anterior (unidades inteiras e mais longas). **Não reestruturado:** reestruturar em partes curtas depende de decisão do operador.
- Referência do Willison com o título real; Gemini Robotics 2 (VLA restrito, ER 2 no AI Studio); pesos abertos com a ressalva de licença e a nota de que os grupos se cruzam; escolha gulosa sem a afirmação de que "não é usada com LLMs" e sem prometer determinismo.
- Resíduos do Router: trava "um pedido por vez" reescrita com a fonte do llama.cpp; frase sem fonte sobre janela em servidor local removida; "cliente por assinatura" com aviso sobre termos do plano; exemplo da 2.2 agora leva o valor calculado no pedido.
- Fonte interna `docs/09…` não aparece mais; fica "documento não público", e os termos do autor (fine-tuning prematuro, prompt patching, código primeiro) são marcados como tal no glossário.

**Validação:** `validar-guia.py` 16 OK, 0 FALHA; PDF de 143 páginas conferido em PNG (capa, páginas 8, 9, 10, 93); reflow em 320 px sem rolagem horizontal.

**Não executado:** impressão em papel, leitor de tela, aparelhos reais (S24, Nitro 5, APSRV).

claude - pessoal
