# Changelog: Encerramento da etapa `L2` — 24/11/2026

Registra a conclusão da etapa `L2` conforme validação realizada e decisão do operador em 24/11/2026.

## Autoria

- **24/11/2026, `agy - ap` (Gemini 4 Hydrogen High):** registro de encerramento da etapa `L2` em [roteiro-piloto-e-validacao-em-telas-2026-11-24.md](../historico/roteiro-piloto-e-validacao-em-telas-2026-11-24.md), [roadmap.md](../../roadmap.md), [README.md](../../README.md) e [CLAUDE.md](../../CLAUDE.md).

## O que mudou

- **Encerramento da etapa `L2` ([roteiro-piloto-e-validacao-em-telas-2026-11-24.md](../historico/roteiro-piloto-e-validacao-em-telas-2026-11-24.md)):**
  - **Galaxy S24:** layout validado e aprovado pelo operador em 24/11/2026, sem apontamentos ou solicitações de ajuste no HTML/CSS.
  - **Acer Nitro 5:** explicitamente ignorado por decisão do operador.
  - **Demais itens (`LG OLED EVO C5 4K 55"`, leitor de tela manual e piloto com leitores):** registrados de forma factual como não executados em separado / dispensados pelo operador no encerramento da etapa (mantendo-se as evidências automatizadas de `320 px` e `axe-core` com `0` violações).
- **Documentação atualizada:** [roadmap.md](../../roadmap.md), [README.md](../../README.md) e [CLAUDE.md](../../CLAUDE.md) atualizados para refletir a conclusão de `L1` e `L2`.

## Validações (após a última edição)

- `python3 -I ferramentas/guia.py fechar`: `0` falhas (`377` partes, `445` questões, `149` tabelas com `.rolagem`, `501` termos no Glossário; HTML `sha256` `7be9d212a6cb82e8`; PDF `654` páginas, `sha256` `8f4a584ed20fe8e1`).
- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: `82` testes OK.
- `python3 -I ferramentas/testar-ferramentas.py --rapido`: `13` testes OK.
- `python3 -I -W error::ResourceWarning ferramentas/testar-fontes.py`: `14` testes OK.
- `python3 -I ferramentas/testar-livros.py`: `2` testes OK.

Assinatura: agy - ap (24/11/2026).
