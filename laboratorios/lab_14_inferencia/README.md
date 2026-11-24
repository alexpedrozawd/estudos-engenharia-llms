# Lab 14 — Inferência Local e Otimização de Serviço

Calculadora de memória (pesos + KV cache com GQA por contexto e usuários, como
no bloco 14.6a), estimativa de camadas que cabem na GPU antes da descarga para
a CPU e medição a partir de carimbos de tempo por token: TTFT, TPOT, ITL,
percentis por posto mais próximo (p50, p95, p99) e goodput dentro do SLO. O
servidor simulado tem semente fixa e um pedido em cada dez preso na fila, para
mostrar que a cauda aparece no p95 e some na mediana.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_14_inferencia
```

Para medir um servidor real (Ollama, llama.cpp ou vLLM), grave o instante de
cada pedaço do stream e passe a lista a `medir_pedido`; os percentis e o
goodput não mudam de código.
