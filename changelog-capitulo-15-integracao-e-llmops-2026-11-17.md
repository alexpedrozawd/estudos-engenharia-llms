# Changelog: Capítulo 15 — Integração empresarial e LLMOps (17/11/2026)

Autoria: deepseek - painel. Quarto capítulo da Parte III.

## O que mudou
- `guia-engenharia-llms.html`: Capítulo 15 (abertura, 18 partes `15.1a`–`15.6c`, 6 questões `c15q1`–`c15q6`, 3 molduras de imagem sem geração), 11 termos novos no Glossário (361 no total), bloco *Fontes do capítulo 15* nas Referências, Sumário com as seis unidades e listas de `@media print` com `#capitulo-15` e `#questoes-capitulo-15`. Glossário passou para a p. 316 e Referências para a 317.
- `pacote-de-fontes-capitulo-15-integracao-e-llmops-2026-11-17.md`: 18 fontes, 69 trechos literais, 0 reprovados.
- `planejamento-completo-estudos-engenharia-llms.md`, `CLAUDE.md` e `README.md`: Módulo 15 concluído e contagens atualizadas.

## Decisões e ressalvas
- As convenções semânticas de GenAI do OpenTelemetry saíram do site principal para o repositório `open-telemetry/semantic-conventions-genai`; os trechos vêm de arquivos Markdown crus. O status é *Development*, e o capítulo apresenta os nomes de atributos como padrão em evolução, não como contrato estável.
- As URLs do Google Cloud para monitoramento de modelo e gerenciamento de prompt responderam 404 e ficaram fora. O capítulo trata de observabilidade por OpenTelemetry e de registro de prompt por MLflow e Langfuse, sem atribuir práticas ao Google Cloud.
- O termo "Canário" já existia no Glossário (Cap. 8); não foi duplicado, e o capítulo usa a definição existente.
- O capítulo não repete segurança e retenção (Cap. 7), idempotência e retomada (Cap. 2), contratos de ferramenta (Cap. 10) nem contexto e cache (Cap. 9); remete a eles.

## Validação (17/11/2026)
- `conferir-trechos.py`: 69 aprovados, 0 reprovados. `validar-guia.py`: 16 OK, 0 FALHA.
- Verificação estrutural: 20 seções, nenhuma parte acima de 500 palavras (maior: 377), 128/128 tabelas com `.rolagem`, `page-nav` sequencial, níveis 2/3/1, zero termos proibidos, Glossário sem duplicatas e em ordem.
- Chrome em 320 px: `clientWidth` 305 = `scrollWidth` 305, 0 estouros em 23 seções; retorno interativo conferido.

## Hashes (16)
`guia-engenharia-llms.html` `60c5d9ab233d80bd`; pacote do Cap. 15 `4e667c0f6db5e441`; `planejamento-completo-estudos-engenharia-llms.md` `0527929e17af9715`; `CLAUDE.md` `530fe855880caf0c`; `README.md` `596b7c112e9f1b7d`.

Assinatura: deepseek - painel, 17/11/2026.
