# Lab 11 — Harnesses, Workflows e Agentes

Harness de agente ReAct com o cliente simulado do guia: o modelo devolve JSON
com pensamento, ação e argumento; o harness valida esse contrato, recusa
ferramenta inexistente, verifica cada observação (escalona quando reprovada),
grava cada passo em JSON, para no teto de passos e retoma do estado salvo. Inclui
a conta do erro composto (`0,95 ** 10 ≈ 0,60`).

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_11_agentes_harness
```

Para usar um modelo real, troque `ClienteMockDeterministico` por um adaptador
HTTP (ver `comum/cliente_llm.py`) e mantenha os testes com o cliente simulado.
