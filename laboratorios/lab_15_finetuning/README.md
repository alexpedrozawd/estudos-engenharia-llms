# Lab 15 — Fine-tuning, Quantização e Destilação

Ajuste fino em miniatura, sem bibliotecas externas: calculadora de memória de
treino (completo, LoRA e QLoRA, com ativações; 7B em 16 bits dá 14 + 42 GB como
no bloco 15.2), um **LoRA de verdade em escala de brinquedo** (matriz base
congelada, adaptador A·B de posto 1, B iniciando em zero, 10% para validação e
parada quando a validação deixa de melhorar), quantização int8 com escala única
e por bloco, comparação antes/depois por fatia (reprova se alguma fatia piora)
e manifesto com hash do conjunto, modelo base, adaptador e hiperparâmetros.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_15_finetuning
```

Para um ajuste real, use uma biblioteca de PEFT num modelo pequeno e mantenha
estes testes como regressão do protocolo (validação, parada, fatias, manifesto).
