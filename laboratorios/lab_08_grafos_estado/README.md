# Lab 08 — Engenharia de Grafos Aplicada a LLMs

Workflow de reembolso da Aurora Educação (fictícia) como máquina de estados:
nós explícitos, aresta condicional por valor e prazo, pausa para aprovação
humana, checkpoint em SQLite após cada nó e efeito externo com chave de
idempotência. Um teste derruba o fluxo logo depois de gravar o pagamento e
confirma que a retomada não paga duas vezes. Um modelo simples compara o custo
em tokens com e sem subagentes (com uma subtarefa só, o subagente não compensa).

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_08_grafos_estado
```
