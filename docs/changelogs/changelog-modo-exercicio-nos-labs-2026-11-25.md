# Changelog — modo exercício nos labs e mapa de vagas (25/11/2026)

Autoria: claude - pessoal. Etapa 1 do [plano de prontidão para vaga pleno](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md).

## Modo exercício

Os labs vinham resolvidos, sem nada para o estudante implementar. Agora:

- **Marcadores:** 79 trechos em 26 labs (18 labs + projeto integrador em `laboratorios/`, 7 projetos em `laboratorios-mercado/`), de 2 a 4 funções centrais por lab, entre `# EXERCICIO-INICIO: <dica>` e `# EXERCICIO-FIM`. Só comentários: 166 linhas adicionadas, nenhuma removida; o comportamento dos originais não muda (84 e 83 testes verdes).
- **Gerador `ferramentas/gerar-exercicios.py`** (biblioteca padrão):
  - copia `laboratorios/` e `laboratorios-mercado/` para `rascunho-local/exercicios/` (fora do Git) e troca cada corpo marcado por `raise NotImplementedError` com a dica; gera `EXERCICIOS.md` com a lista de trechos e o comando de teste de cada lab;
  - recusa sobrescrever a cópia sem `--forcar`; `--alvo <lab> --forcar` refaz só um lab; só apaga pasta vazia ou cópia própria (com `EXERCICIOS.md`); recusa destino que sobreponha o projeto fora de `rascunho-local/`;
  - `--checar` valida os marcadores (pares, recuo, dica, 2 a 4 por lab, saída que o Python lê);
  - `--verificar labs|mercado` troca um trecho por vez numa cópia temporária e exige que algum teste do lab falhe com `NotImplementedError`; a cópia sem troca tem de passar. Resultado: os 79 trechos são cobertos.
- **Testes:** classe `Exercicios` em `ferramentas/testar-ferramentas.py` (5 testes: marcadores, parser com 6 casos inválidos, cópia que falha antes e passa com a solução, destinos recusados e cobertura por trecho dos labs). O hash dos `.py` de `laboratorios/` é conferido antes e depois.
- **CI:** passo novo `gerar-exercicios.py --verificar mercado`, depois da instalação da Camada 3 (a suíte de ferramentas roda antes da instalação e cobre os labs).
- **Documentação:** roteiro de estudo em `README.md` (gerar → ler a parte → implementar → testar → comparar com `diff -ru`) e ponteiros em `laboratorios/README.md` e `laboratorios-mercado/README.md`. Corrigida a contagem antiga de `74` smoke-tests para `83` no `README.md`.

Verificado: a cópia da Camada 3 importa o `mercado_base` da própria cópia, não o pacote instalado em modo editável (o `--verificar mercado` detecta cada trecho trocado).

## Mapa de vagas e plano

- [mapa-de-vagas-linkedin-brasil-2026-11-25.md](../historico/mapa-de-vagas-linkedin-brasil-2026-11-25.md): 29 vagas únicas no Brasil (busca pública do LinkedIn, sem a conta do operador). Lacunas acima de um terço das vagas: frameworks de orquestração e agentes (55%) e nuvem com serviços gerenciados (52%).
- Plano atualizado: Etapa 5 com o mapa, a regra do terço, casos de system design com trade-off de bancos vetoriais e bloco de comunicação; nova **Etapa 5B** (Capítulos 19 e 20 e Langfuse), decidida pelo operador para logo depois da Etapa 2; Etapa 6 prioriza nuvem.

## Validação

- `python3 -I -W error::ResourceWarning laboratorios/executar_labs.py`: 84 OK.
- `.venv-mercado/bin/python -I -W error::ResourceWarning laboratorios-mercado/executar_smoke.py`: 83 OK.
- `python3 -I ferramentas/gerar-exercicios.py --checar`: 79 trechos em 26 labs; `--verificar labs` e `--verificar mercado`: todos cobertos.
- Cópia real: 66 erros em 84 testes dos labs e 48 em 83 da Camada 3, todos por `NotImplementedError`.
- `python3 -I ferramentas/testar-ferramentas.py` (com e sem `--rapido`): OK.
- HTML (`bb004776a6cdc9cb`) e PDF (`81d2fffd7394a880`) inalterados.
