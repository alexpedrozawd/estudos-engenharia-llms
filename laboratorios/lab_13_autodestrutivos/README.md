# Lab 13 — Atos Autodestrutivos e Proporcionalidade

Simulação de incidentes de agente com travas verificáveis: lista de permissão,
bloqueio de repetição idêntica, orçamento de tentativas e simulação (dry-run)
de ações destrutivas (mesmo cenário do bloco 13.3d); disjuntor (circuit
breaker) fechado → aberto → meio-aberto com relógio injetado; transação com
invariante que reverte (rollback) uma mudança ruim e desfaz a última boa; e a
conta de proporcionalidade, que mantém o agente só quando o valor líquido
esperado supera o de um script determinístico simples.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_13_autodestrutivos
```

Os valores de acerto, custo e perda são proposta didática; troque-os pelos
medidos no seu conjunto de avaliação.
