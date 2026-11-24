# Laboratórios Práticos — Guia para Engenharia de LLMs

Trilha prática complementar ao guia teórico ([guia-engenharia-llms.html](../guia-engenharia-llms.html)), estruturada com biblioteca padrão do Python 3 e mocks determinísticos para execução offline sem custo de API ou risco de vazamento de credenciais.

## Como executar os testes (offline e determinísticos)

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py
```

Para executar apenas um laboratório específico:

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo comum
```

## Uso opcional com provedores reais

O cliente neutro em `laboratorios/comum/cliente_llm.py` aceita um adaptador HTTP opcional para provedores compatíveis (OpenAI, Anthropic, Google Gemini ou Ollama local) via variáveis de ambiente (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `OLLAMA_HOST`). Os testes automatizados do repositório nunca acessam a rede: usam `ClienteMockDeterministico` e `unittest.mock`.

## Estrutura

- `comum/`: cliente neutro de LLMs, mocks determinísticos e testes.
- `dados/`: conjuntos sintéticos fictícios da **Aurora Educação** (sem dados pessoais reais).
- `lab_01_*` .. `lab_18_*`: um laboratório por capítulo do guia, cada um com `README.md`, código e testes.
- `projeto_integrador/`: assistente acadêmico completo que reúne RAG, ferramentas, guardrails, roteamento, rastros, avaliação e custo (estudo de caso final do Cap. 18).
