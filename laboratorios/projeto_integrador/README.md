# Projeto integrador — assistente acadêmico da Aurora Educação

Esqueleto do estudo de caso final (Cap. 18): responde com fontes, abre
chamados, protege dados de alunos, escolhe o modelo pelo risco, é avaliado
antes de cada versão e projeta o custo mensal. Reúne os laboratórios:

| Peça | Origem |
|---|---|
| Guardrails de entrada e saída, máscara de dados pessoais | `lab_12_guardrails` (Cap. 12) |
| RAG híbrido com citação conferida contra o recuperado | `lab_07_rag_hibrido` (Cap. 7) |
| Chamado com aprovação humana e chave de idempotência | `lab_10_ferramentas_mcp` (Cap. 10) |
| Roteamento pelo risco, contingência e conversa estável | `lab_16_roteamento` (Cap. 16) |
| Rastros com atributos GenAI | `lab_17_llmops` (Cap. 17) |
| Custo médio e orçamento mensal | `lab_18_economia` (Cap. 18) |
| Portão de versão pelo limite inferior de Wilson | `lab_05_avaliacao` (Caps. 5 e 6) |

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo projeto_integrador
```

Os testes cobrem o caminho feliz com dado pessoal mascarado, bloqueio de
injeção, risco alto sem rebaixamento (e fila humana quando a fronteira cai),
resposta com fonte não recuperada barrada, chamado sem duplicar, portão de
versão e projeção de custo. Para produção, troque `ModeloSimulado` por
adaptadores reais (`comum/cliente_llm.py`) e amplie o conjunto de avaliação.
