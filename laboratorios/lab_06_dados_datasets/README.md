# Lab 06 — Engenharia de Dados e Datasets para IA

Monta um conjunto de avaliação da Aurora Educação (fictícia) com o fluxo do
capítulo 6: validação de JSONL (*schema-on-write*), deduplicação exata por hash
e aproximada por similaridade de Jaccard, amostragem estratificada e por
reservatório, divisão por aluno sem vazamento, detector de quase duplicatas
entre ajuste e teste e manifesto de versão com contagens por estrato.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_06_dados_datasets
```

Exercício sugerido: troque o limiar de vazamento (0,5) e observe, em pares
reais da sua base, quantos falsos positivos e falsos negativos aparecem.
