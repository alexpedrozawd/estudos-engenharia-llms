# Lab 16 — Seleção, Roteamento e Gateways

Gateway entre um modelo local rápido e um de fronteira: fora de escopo é
recusado sem chamar modelo; risco alto vai à fronteira e, se ela cair, à fila
humana (nunca é rebaixado); tarefa longa prefere a fronteira. Modelo e esforço
ficam fixos por conversa; troca no meio só como contingência ou por risco, com
registro e sessão nova (16.6). Cada decisão vira uma linha JSON, e o custo da
cascata (3,4 contra 12, como no bloco 16.4d) vem com a taxa de reprovação a
partir da qual mandar tudo à fronteira sai mais barato.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_16_roteamento
```

Custos são unidades relativas (proposta didática); registre a data da consulta
de preços ao trocá-los por valores reais.
