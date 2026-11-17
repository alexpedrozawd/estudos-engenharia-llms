# Changelog: reestruturação do capítulo 1 em partes curtas (13/11/2026)

Autoria: claude - pessoal (interrompido por cota) e deepseek - conta não verificada. Projeto: `/var/home/apsrv/Documentos/Projetos/estudos-engenharia-llms` (não é repositório Git). Base: HTML de 15/10/2026, hash `6136c61124752bf0`, guardado em `arquivo/antes-da-reestruturacao-em-partes-curtas/`.

## 1. O que mudou

- **Capítulo 1 reescrito em 23 partes curtas.** As sete unidades agora se dividem em partes `1.1a` a `1.7c`. Cada parte tem resumo de três linhas, imagem opcional (só moldura), analogia, texto, uma pergunta, ponto de retomada e notas de fonte. A última parte de cada unidade traz "Fontes da unidade" com *Ler*, *Assistir* e *Aprofundar*.
- **Unidade 1.7, "Tipos de modelos", criada** em três partes: acesso e função; treino e dados; arquitetura, tamanho e além do texto. O parágrafo de tipos de modelo saiu da 1.2, que aponta para a 1.7.
- **Questões do capítulo:** a sexta questão (nível médio) entrou; a página diz "duas fáceis, três médias e uma difícil". O validador passou a aceitar de cinco a seis questões de fechamento por capítulo.
- **Sumário:** lista 1.1 a 1.7 e as questões, com link para a primeira parte de cada unidade; as descrições dos capítulos 4, 7, 8, 13 e 15 ganharam os temas novos (técnicas de prompt, entupimento de contexto, ciclo de vida da sessão, troca de modelo ou esforço, cache e esforço).
- **Introdução e abertura do capítulo 1:** explicam o formato em partes, o resumo de três linhas e as cinco ou seis questões.
- **Glossário:** 111 entradas (eram 93), incluindo modelos de decisão, gerativo, de fronteira, local, instruído, multimodal, de raciocínio, de guarda, embeddings, reranker, SLM, VLM, VLA, Mamba, modelo de mundo, pesos abertos e proprietário.
- **Referências:** seção nova com as fontes lidas para a 1.7 (Ouyang, Llama Guard, Belcak, LLaDA, Mercury, Mamba, Sentence-BERT, MTEB, reranker, π0, OSI, Thoughtworks, Willison, TypeSafe, InfoQ, Kev, Genie 3, Gemini Robotics 2), com data e ressalvas.
- **CSS:** estilos de `.rotulo-unidade`, `.resumo`, `.analogia` e `.moldura`; moldura tracejada 3:2, limitada a 36 rem.

## 2. Imagens (regra fixa do operador, 13/11/2026)

- Poucas imagens, não uma por página. Nesta versão, seis molduras: 1.1a, 1.2b, 1.3b, 1.4b, 1.6b e 1.7a.
- Cada moldura tem `role="img"` e `aria-label` com o texto alternativo; nenhuma imagem foi embutida.
- A geração fica para o fim: só depois de o texto estar finalizado, revisado e validado. As imagens já geradas em 13/11/2026 (piloto e seguintes) não entraram no HTML.

## 3. Arquivos alterados

- `guia-engenharia-llms.html` — SHA-256 `3bfbea0ae27668a9…` (2.789 linhas, 37 páginas).
- `guia-engenharia-llms.pdf` — SHA-256 `079a8b94d8648a10…` (147 páginas impressas).
- `ferramentas/validar-guia.py` — SHA-256 `ed11cfd777d3827d…` (checagem de 5 ou 6 questões por capítulo).
- `planejamento-completo-estudos-engenharia-llms.md` — `fe0a68e40b768450…` (módulos 4, 7, 8, 13 e 15; linhas novas na tabela de referências públicas).
- `requisitos-de-formato-html-do-material.md` — `de60ad56358fba1a…` (§8, formato de parte curta).
- `tabela-de-lacunas-capitulo-1.md` — `16d42cdc14116208…` (registro de aplicação).
- `CLAUDE.md` — `9362691133ef97b3…` (estado novo do projeto).
- `roteiro-de-aprofundamento-prompts-contexto-e-sessoes.md` — `d79da88700c19749…` (marcado como integrado).
- Novos: este changelog e `handoff-reestruturacao-capitulo-1-2026-11-13.md`.

## 4. Validações executadas

- `python -I ferramentas/validar-guia.py --guia guia-engenharia-llms.html`: **16 OK, 0 FALHA**.
- Conferência própria: 112 `id` sem duplicata; nenhum link interno quebrado; 37 seções com 37 navegações; cadeia de partes 1.1a→1.7c→questões; cada parte com resumo de três itens, analogia, pergunta, retomada e notas; fechamento de tags sem erro; captura em 900 px e 360 px sem corte visível.
- Não validado: aparelhos reais, leitor de tela e reflow medido em 320 px.

## 5. Pendências

- Gerar e embutir as imagens (última etapa, depende do aval do operador).
- PDF: gerado em 13/11/2026 (`guia-engenharia-llms.pdf`, 147 páginas impressas, texto a 12 pt). A paginação de impressão não foi conferida em papel.
- Aparelhos reais e navegador com leitor de tela.
- Fontes candidatas dos capítulos 4, 8 e 15 seguem sem trecho literal conferido.
- Commit e push: bloqueados, porque o projeto não é repositório Git.

Assinatura: claude - pessoal (interrompido por cota), deepseek - conta não verificada.
