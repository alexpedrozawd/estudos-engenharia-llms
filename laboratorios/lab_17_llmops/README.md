# Lab 17 — LLMOps, Monitoramento, Shifts e Testes em Produção

Rastros aninhados com atributos das convenções GenAI do OpenTelemetry
(`gen_ai.operation.name`, `gen_ai.request.model`, `gen_ai.usage.*`) sem
depender do SDK, com erro registrado no span; PSI entre distribuições de tipos
de pergunta (0,002 e 0,443, como no bloco 17.6e), contando faixas novas;
sorteio determinístico do canário por hash com sal da rodada; decisão de
promover, reverter ou esperar mais dados; e MTTD, MTTR e CFR a partir de uma
lista de incidentes.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_17_llmops
```

O limiar de 0,2 do PSI e as tolerâncias do canário são proposta didática;
confirme olhando os casos antes de agir.
