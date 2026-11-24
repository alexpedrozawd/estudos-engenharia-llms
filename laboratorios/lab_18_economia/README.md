# Lab 18 — Eficiência, Cache e Economia de Escala

Custo de uma sessão em tokens equivalentes de entrada, com e sem cache de
prefixo e com invalidações (657 mil, 140 mil e 370 mil, como no bloco 18.5d);
leituras mínimas para o cache compensar; quantas invalidações a sessão aguenta
antes de a economia sumir; decisão de lote (só fora do interativo e com prazo
que comporte a janela); varredura de sensibilidade; e conversão para orçamento
mensal com o preço de entrada do modelo.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_18_economia
```

Multiplicadores (1,25 de gravação, 0,1 de leitura, 50% de lote) são proposta
didática na ordem de grandeza do capítulo; confira a página de preços vigente.
