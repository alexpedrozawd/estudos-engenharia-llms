# Lab 10 — Ferramentas, Protocolos e Integrações

Registro de ferramentas da Aurora Educação (fictícia) com JSON Schema estrito
(`additionalProperties: false`), despacho que recusa ferramenta inexistente,
argumento a mais, a menos ou de tipo errado com erro legível ao modelo, aprovação
humana obrigatória para ações de escrita e chave de idempotência. Um servidor
JSON-RPC 2.0 mínimo expõe `tools/list` e `tools/call` no estilo do MCP.

O servidor é didático: não implementa transporte, inicialização nem negociação
de capacidades do protocolo. Para um servidor MCP real, use o SDK oficial e
mantenha estes testes como contrato.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_10_ferramentas_mcp
```
