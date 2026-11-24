# Lab 09 — Contexto, Memória e Feedback do Usuário

Compara o corte da janela por recência (que separa pergunta e resposta) com o
corte por pares de turno, mantendo instruções fixas e resumindo o que sai pelo
cliente simulado. Guarda notas de sessão em SQLite com consolidação de fatos que
mudam (memória de longo prazo) e extrai sinais implícitos de feedback
(correção, pedido de fonte, interrupção, agradecimento), com taxas por versão
do prompt.

```bash
python3 -I -W error::ResourceWarning laboratorios/executar_labs.py --alvo lab_09_contexto_memoria
```
