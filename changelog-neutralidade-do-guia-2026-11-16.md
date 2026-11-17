# Changelog: neutralidade do guia em relação ao AP AI Router (16/11/2026)

Pedido do operador: o guia deve formar profissionais em arquitetura e engenharia de LLMs, sem se limitar ao AP AI Router.

## Evidência (leitura localizada, sem ler os capítulos inteiros)
- HTML `820e006c24e4a899`: "AP AI Router" tem 0 ocorrências; "plataforma interna" 8; "Aurora" 162. Validador: 16 OK, 0 FALHA (não alterado).
- Capítulo 2 (linhas 1956 a 3352): conceito geral com fontes de Anthropic, OpenAI, Ollama, llama.cpp, MDN, RFCs, Google SRE, AWS, NVIDIA e OpenTelemetry. A plataforma interna aparece como "desenho típico" e o banco como "proposta didática". O "cliente por assinatura" nasce da experiência do Router, mas o texto avisa que em empresas "o acesso mais comum é a API". Nenhuma alteração necessária no capítulo.
- Lacunas observadas: peso de Anthropic (199 menções) contra OpenAI (46), Google (13), Llama (5) e Mistral (0); módulos 6 a 15 ainda não escritos.

## Mudanças
- `planejamento-completo-estudos-engenharia-llms.md` (`fe0a68e40b768450` antes): trocado "O AP AI Router será o caso principal" por decisão de neutralidade e quatro regras para os módulos 6 a 15; exemplo resolvido sem Router; evidência local só como complemento rotulado. Backup em `arquivo/antes-plano-neutralidade-2026-11-16/`.
- `CLAUDE.md`: ponteiro para a decisão.
- Guia (HTML e PDF): não alterados nesta primeira etapa (ver a segunda etapa abaixo).

## Pendente
- Capítulos 1 a 5: reequilíbrio de fornecedores pedido e feito na segunda etapa (capítulos 3 a 5); resta o capítulo 1 e os modelos abertos.
- `contexto-de-estudo-ap-ai-router.md` segue como insumo de contexto, não como fonte do texto do guia.

## Segunda etapa: equilíbrio de fornecedores nos capítulos 3 a 5 (16/11/2026)
Autorizado pelo operador: "o objetivo é equilibrar mesmo e não focar apenas em uma fonte".
- Fontes novas (OpenAI e Google), baixadas e conferidas por busca literal: 43 citações, 0 ausentes. Pacote: `pacote-de-fontes-equilibrio-de-fornecedores-2026-11-16.md`.
- Texto alterado (sem páginas novas; 117 páginas lógicas): 3.4a, 4.2a, 4.2c, 4.5a (nova tabela com os três provedores e seção "E nos outros provedores"), 5.2a, 5.4a, 5.4c, 5.5c, 5.6a (remissão), "Aprofundar" das partes 4.2d, 4.5c, 5.2c, 5.4d e 5.5c, e as referências dos capítulos 3, 4 e 5.
- HTML `820e006c24e4a899` → `a9653bd34b819198`. Validador: 16 OK, 0 FALHA. PDF regerado com Chrome: 379 → 383 páginas A4, `535912f532726afd`. Backup: `arquivo/antes-equilibrio-fornecedores-2026-11-16/`.
- Achado relevante: Anthropic (rejeita com erro 400), Google (ignora com aviso) e OpenAI (retirar com esforço diferente de none) tratam temperature, top_p e top_k de modos diferentes; virou lição na 4.5a.
- Não feito: capítulo 1 (já cita Google, DeepSeek, Llama, Hugging Face, arXiv) e modelos abertos sem fonte conferida (feito na terceira etapa para Qwen e Gemma; Mistral dispensado pelo operador); reflow em 320 px e conferência visual do PDF (só contagem de páginas).

## Terceira etapa: modelos abertos Qwen3.8 e Gemma 4 (16/11/2026)
Autorizado pelo operador: buscar Qwen3.8 e Gemma 4, "os modelos principais que tenho aqui no servidor", e especializar por provedor.
- Fontes: fichas oficiais no Hugging Face (Qwen/Qwen3.8-27B e google/gemma-4-31B-it), baixadas e conferidas. Pacote: `pacote-de-fontes-equilibrio-de-fornecedores-2026-11-16.md`.
- Texto alterado: 1.3c (janelas de contexto), 1.4c (raciocínio ligado e desligado), 1.4d (remissão à amostragem), 1.7a (pesos abertos e licença Apache 2.0), 1.7c (denso contra mistura de especialistas, pequenos, texto e imagem), 4.5a (seção "Modelos abertos que rodam no seu servidor" e duas linhas novas na tabela dos parâmetros), referências.
- A lição "a mesma receita pode quebrar num provedor e não fazer nada em outro" já estava na 4.5a desde a segunda etapa (três APIs); agora vale também para fichas de modelos abertos, que recomendam valores em vez de rejeitar ou ignorar.
- HTML `b5a35d4dbf4782f5`; PDF `14551c0a3eef917a` (386 páginas A4). Validador: 16 OK, 0 FALHA.

## Quarta etapa: OSI e foco em Qwen e Gemma (16/11/2026)
- Verificação OSI (pedido do operador): pelas fichas, nem o Qwen3.8-27B nem o Gemma 4 demonstram o que a definição pede (dados e código completos de treino). 1.7a ajustada: "pesos abertos", sem afirmar nem negar conformidade. Detalhes no pacote de fontes.
- Mistral dispensado pelo operador; foco em modelos abertos: Qwen3.8 e Gemma 4 (regra no plano geral). 1.2d ganhou remissão ao Gemma 4 26B A4B.

Assinatura: claude - pessoal, 16/11/2026.
