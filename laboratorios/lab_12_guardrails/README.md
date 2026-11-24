# Lab 12 — Segurança, Guardrails e IA Responsável

Camada de guardrails da Aurora Educação: máscara de CPF, e-mail e telefone antes
do provedor (o mapa reverso fica no servidor), guardrail de entrada (injeção,
extração do prompt, dado de terceiro, escopo), guardrail de saída (vazamento do prompt de sistema, detectado
por um marcador-canário, e dado pessoal sem máscara), isolamento da saída de
ferramentas como dado marcado e uma bateria adversarial que mede **violação**
(ataque que passou) e **recusa indevida** (pedido legítimo barrado). A bateria
inclui de propósito um ataque que passa e um legítimo barrado: regras por
expressão regular têm limites e precisam de medida, não de confiança.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_12_guardrails
```

Regras por regex não substituem privilégio mínimo, isolamento de ferramentas e
classificadores dedicados (Cap. 12); use a bateria como regressão ao trocá-las.
