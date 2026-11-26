# Changelog — Etapa 7: encerramento do plano de prontidão (26/11/2026)

Autoria: claude - pessoal. Encerra o [plano de prontidão para vaga pleno](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md). HTML, PDF, código e `laboratorios/` inalterados.

## Decisões do operador (26/11/2026)

- A revisão amostral da Etapa 3 seria feita por Claude e registrada como **revisão por modelo de fronteira**, nunca como revisão humana.
- O `CLAUDE.md` seria enxugado. O conteúdo anterior foi copiado inteiro para [historico-de-atualizacoes-claude-md.md](../historico/historico-de-atualizacoes-claude-md.md) (só os links relativos foram ajustados para a nova pasta).

## Revisão amostral da Etapa 3 (modelo de fronteira, não humana)

Método: sorteio determinístico por `sha256("rev3|" + id)`. Os rótulos ficaram escondidos durante a revisão e só foram comparados depois. O veredito do juiz 27B do P07 foi reconstruído do cache da execução de 26/11 (`80` chamadas lidas do cache, `0` reais), e o *kappa* reproduzido bate com o registrado (`0,955`). Registro: [`execucoes/revisao-fronteira-etapa-3-2026-11-26.json`](../../laboratorios-mercado/execucoes/revisao-fronteira-etapa-3-2026-11-26.json), com os hashes dos arquivos revisados.

| Projeto | Amostra | Resultado (Wilson 95%) | Observações |
|---|---|---|---|
| P04 | `36` dos `324` sintéticos (`3` por estrato) | `36/36` categorias iguais às do conjunto, rotuladas às cegas [`0,90`; `1,0`] | `0` com PII; `3` ambíguos ou pouco naturais (`c163`, `c238`, `c295`) |
| P02 | `12` das `123` perguntas novas | `12/12` respondíveis pelo trecho esperado [`0,76`; `1,0`]; `10/12` referências sem imprecisão | `qa045` pergunta em dias e responde em horas úteis; `qa054` omite a condição de 15 minutos |
| P07 | `40/40` pares de calibração | `40/40` iguais à referência; contra o juiz 27B, `39/40` e *kappa* `0,955` [`0,86`; `1,0`] | única divergência: `cal-12`, um empate que o juiz deu a A |

Achados:

- **Médio, registrado como limite, sem correção nesta etapa:** as `123` perguntas do corpus ampliado do P02 começam por "Sobre <tema do documento>:", o que entrega o documento ao recuperador. Os números de recuperação do P02 tendem a ser otimistas. Corrigir exige reescrever as perguntas e rodar o P02 de novo, o que fica fora do escopo do encerramento. O limite foi anotado no README do P02.
- **Baixos:** as `2` referências imprecisas do P02 e os `3` chamados ambíguos do P04 foram listados no registro e não foram alterados, porque mudar os dados invalidaria as execuções registradas.

Limites: o revisor é um modelo de linguagem e não substitui a revisão humana. Os pares por construção têm defeitos óbvios, então a concordância alta neles era esperada. Com amostras pequenas, `36/36` não exclui uma taxa de erro perto de `10%` (limite inferior de Wilson `0,90`).

## Plano de prontidão: resumo por etapa

| Etapa | Entrega | Números principais | Changelog |
|---|---|---|---|
| 1 | Modo exercício nos labs | `79` trechos em `26` labs; gerador com `--verificar mercado` no CI | [modo exercício](changelog-modo-exercicio-nos-labs-2026-11-25.md) |
| 2 | Camada 3 na GPU (Ollama `/v1`) | 4B × 27B; juiz separado do gerador no P07 | [GPU Ollama](changelog-camada-3-gpu-ollama-2026-11-25.md) |
| 5B | Caps. 19 e 20, P08 LangGraph, P06 com nuvem testada offline, Langfuse | `20` capítulos, `502` questões, PDF com `736` páginas | [Cap. 19](changelog-capitulo-19-e-p08-langgraph-2026-11-25.md), [Cap. 20](changelog-capitulo-20-e-langfuse-2026-11-25.md) |
| 3 | Escala estatística em P02, P04 e P07 | P04 no teste: `0,610 → 0,976` (`123` casos); P07 com *kappa* `0,955`; P02 com acerto@4 de `63/74` | [Etapa 3](changelog-etapa-3-escala-estatistica-2026-11-26.md), [achados baixos](changelog-achados-baixos-etapas-3-e-4-2026-11-26.md) |
| 4 | Red teaming do P06 com garak | `14` sondas, `342` tentativas, `3` achados corrigidos | [Etapa 4](changelog-etapa-4-red-teaming-p06-2026-11-26.md) |
| 5 | Preparação para vaga | `10` casos de system design, bloco de entrevista e portfólio; `55` vagas no mapa | [Etapa 5](changelog-etapa-5-preparacao-para-vaga-2026-11-26.md) |
| 6a | Kubernetes local com kind | `12/12` verificações; `0` falhas no *rollout* | [Etapa 6a](changelog-etapa-6a-kubernetes-local-2026-11-26.md) |
| 6b | Deploy do P06 em nuvem | **bloqueada**: exige autorização, conta, provedor e teto de gasto | — |
| 7 | Encerramento | este changelog | — |

## Reavaliação (autoavaliação do autor, não medição externa)

Em 25/11 a auditoria realista deu `7/10` para o objetivo de vaga pleno (guia `8,5`, prática `6`, prontidão `6`). Hoje a estimativa é **cerca de `8/10`**: prática perto de `8`, prontidão perto de `7,5`.

O que subiu a nota: labs com exercício, modelo forte na GPU, amostras com intervalo de confiança e teste pareado, red teaming com correções, Kubernetes local, LangGraph e preparo de entrevista.

O que segue faltando:

- deploy real em nuvem: a nuvem aparece em `52%` das vagas e a 6b está bloqueada;
- dados revisados por pessoas e usuários reais;
- inglês, citado em `41%` das vagas e fora do guia.

## Documentação

- [`CLAUDE.md`](../../CLAUDE.md) enxugado: de `5.278` para `557` palavras (`wc -w`), com estado atual, pendências, regras fixas e validação. A regra de 15/10/2026 (guia sem programação) saiu do texto vigente, porque a decisão de 23/11/2026 a substituiu.
- `README.md`, `roadmap.md` e o plano de prontidão marcam o plano como encerrado. Os READMEs do P02, do P04, do P07 e de `laboratorios-mercado/`, além do guia de portfólio, passam a registrar a revisão por modelo de fronteira.

## Validação

- `laboratorios/executar_labs.py`: `84` OK. `executar_smoke.py`: `146` OK. `testar-ferramentas.py` completo: `24` OK (o teste de PDF trabalha numa cópia temporária; o PDF do guia não mudou).
- Links relativos dos `.md` alterados e criados: `0` quebrados.
- HTML (`da073a1210e36792`) e PDF (`8431be316ec3b881`) conferidos por hash, sem mudança. `guia.py fechar` dispensado, porque o HTML não mudou.
- Revisão por `/auditorias` (documentação): regra de imagens restaurada no `CLAUDE.md` e duas imprecisões deste changelog corrigidas.
