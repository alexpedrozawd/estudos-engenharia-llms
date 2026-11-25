# 03 — MCP com sandbox e aprovação humana

Servidor e cliente MCP reais com o SDK oficial `mcp` 2.x, nos dois transportes padrão (stdio e Streamable HTTP).

- `mcp_ferramentas.py`: `consultar_prazo` e `calcular_media_ponderada` (somente leitura; entradas validadas por Pydantic: nota 0–10, peso > 0) e `executar_python_isolado` (risco alto, `destructiveHint`).
- Aprovação humana: o servidor pede confirmação ao cliente por *elicitation*, mostrando o código exato e o hash. Sem suporte do cliente, recusa ou cancelamento, **nega por padrão** e registra a decisão.
- `mcp_sandbox_exec.py`: cada execução em container descartável: `--network=none`, `--read-only`, `--cap-drop=ALL`, `no-new-privileges`, usuário 65534, limites de memória, CPU, processos e tempo (remove o container pelo nome se expirar); o código vai como argumento, sem shell.
- `mcp_cliente_aurora.py`: lista ferramentas, chama as de leitura, testa a validação e pede a execução isolada; aprovação `terminal` (padrão), `negar` ou `aprovar-automatico` (só demonstração).

## Execução real

```bash
.venv-mercado/bin/python -I laboratorios-mercado/03_mcp_sandbox/mcp_cliente_aurora.py --stdio
.venv-mercado/bin/python -I laboratorios-mercado/03_mcp_sandbox/mcp_ferramentas.py --transporte streamable-http --porta 8765 &
.venv-mercado/bin/python -I laboratorios-mercado/03_mcp_sandbox/mcp_cliente_aurora.py --url http://127.0.0.1:8765/mcp
```

Em 24/11/2026 (registros em [`../execucoes/`](../execucoes/)), os dois transportes passaram; o código aprovado rodou em `python:3.13-alpine` e a tentativa de conexão de rede falhou com `Network unreachable`.

Limites: o cliente usa `mode="legacy"` (handshake de inicialização), porque o modo moderno em processo do SDK 2.3 não tem canal de volta para *elicitation*; em produção, o cliente precisa encaminhar a confirmação a uma pessoa, não a um agente.
