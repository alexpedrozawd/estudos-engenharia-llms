# Changelog — portão estatístico do QLoRA e plano de prontidão para vaga (25/11/2026)

Autoria: claude - pessoal.

## Achado corrigido (médio)

O Projeto 04 registrava o QLoRA de 12 épocas como "aprovado". O teste tinha 12 casos e não havia validação, e as 12 épocas foram escolhidas depois de ver a reprovação de 3 épocas no mesmo teste. Isso contradiz as partes 5.6f e 6.4b do guia. Com 8/12 → 11/12, os intervalos de Wilson 95% são `[0,39; 0,86]` e `[0,65; 0,99]`, e o McNemar exato dá `p ≥ 0,25`.

- `laboratorios-mercado/04_qlora_peft/qlora_receita.py`: `wilson()`, `mcnemar_exato()`, `pareamento()` e o portão `comparar(..., alfa=0.05)` com vereditos `aprovado`, `reprovado` e `inconclusivo`. Os campos antigos ficam preservados. Também `fracao_validacao` e `dividir_com_validacao()`, que separa a validação do treino sem mudar o teste, e `ids_validacao` no manifesto.
- `treinar_qlora.py`: `--fracao-validacao` global, `avaliar --conjunto {teste,validacao}`, `comparar --alfa`, e recusa (código `2`) de comparação entre conjuntos diferentes.
- `test_p04_qlora.py`: os testes que codificavam o portão antigo foram ajustados (3 ganhos → `inconclusivo`; 6 ganhos → `aprovado`). Entraram testes de Wilson, McNemar, validação e CLI: 17 testes no projeto.
- `04_qlora_peft/README.md`, `laboratorios-mercado/README.md` e `roadmap.md`: o resultado de 12 épocas foi reclassificado como **inconclusivo**. O registro em `execucoes/` foi preservado como histórico.

## Reavaliação

A nota `9,1/10` do changelog de ROCm/BFLA mediu acabamento (testes, CI, acessibilidade, fontes), não prontidão para o mercado. A auditoria de 25/11/2026 deu `7/10` para o objetivo do operador. O plano para subir essa nota está em [plano-prontidao-para-vaga-pleno-2026-11-25.md](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md).

## Validação

`laboratorios/executar_labs.py`: 84 OK. `laboratorios-mercado/executar_smoke.py`: 83 OK (eram 77; +6 no P04). `ferramentas/testar-ferramentas.py`: OK. HTML (`bb004776a6cdc9cb`) e PDF (`81d2fffd7394a880`) inalterados. Contagens atualizadas em `README.md`, `roadmap.md` e `laboratorios-mercado/README.md`. Nenhum treino novo em GPU foi executado: a reclassificação usa o registro existente.
