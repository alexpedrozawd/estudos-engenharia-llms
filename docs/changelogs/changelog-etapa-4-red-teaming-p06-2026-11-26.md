# Changelog — Etapa 4: red teaming do P06 com garak (26/11/2026)

Autoria: claude - pessoal. Etapa 4 do [plano de prontidão para vaga pleno](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md). Relatório: [relatorio-red-teaming-p06-2026-11-26.md](../../laboratorios-mercado/06_integrador_producao/redteam/relatorio-red-teaming-p06-2026-11-26.md). HTML, PDF e `laboratorios/` inalterados.

## Decisões

- O garak entrou primeiro (recomendação do plano, aprovada pelo operador). A versão conferida foi a `0.17.1`, e o gerador `rest` atendeu ao alvo HTTP, então o PyRIT não foi preciso.
- **Isolamento:** o garak rodou num container `python:3.12-slim` com volume próprio (`garak-venv`, `torch` para CPU). Ele traz `torch`, `transformers`, `litellm` e SDKs de nuvem, por isso ficou fora do `.venv-mercado` e da imagem base.
- **Alvo:** o P06 na imagem do `Containerfile`, com autenticação ligada (chave aleatória de sessão, fora do Git, passada por variável de ambiente) e o `qwen3.8:27b-ud-iq3_xxs`.
- **Lotes de até ~9 min**, por causa do limite de cada comando. O `executar_garak.sh` usa `podman run --timeout` e `--name`, porque um `timeout` no cliente deixou `2` containers órfãos, parados à mão.

## Código (`laboratorios-mercado/06_integrador_producao/`)

- `integrador_app.py`:
  - `falha_de_backend()` e resposta `503` com `Retry-After: 5`, mensagem neutra e contador `falhas_backend`, quando o LLM falha por HTTP, rede ou *timeout* (inclusive dentro do `ExceptionGroup` do cliente MCP);
  - o guardrail de entrada bloqueia *tags* Unicode (U+E0000–E007F), remove *zero-width*/bidi e normaliza em NFKC antes dos padrões de injeção;
  - o guardrail de saída remove controles C0 e C1 (exceto `\t` e `\n`).
- `redteam/`: `garak-rest-p06.json`, `garak-execucao.yaml`, `executar_garak.sh`, `resumir_garak.py` (consolida os `*.report.jsonl` com Wilson 95% por sonda) e o relatório.
- `test_p06_integrador.py`: `4` testes novos (`503`, contrabando Unicode, controles na saída e o consolidador).
- Registro: `execucoes/p06-red-teaming-garak-2026-11-26T04-21-40-0300.json`.

## Resultado

- `14` sondas e `342` tentativas: `252` antes das correções e `90` na regressão.
- `0` sucessos em injeção direta e indireta, extração do prompt de sistema, Base64/ROT13, exfiltração por Markdown, XSS, SQL e Jinja.
- DAN: `16` falsos positivos (o detector só reconhece recusas em inglês).
- Achados corrigidos:
  - médio, `500` → `503` quando o LLM falha;
  - médio, *tags* Unicode ocultas;
  - baixo, byte de controle `\x9b` na resposta.
- Regressão no serviço reconstruído: `goodside.Tag` `0/32` e `ansiescape.AnsiRaw` `0/58`.

## Auditoria (`/auditorias`)

Sem achado médio ou maior no diff. A chave não aparece nos relatórios, no registro nem nos logs do garak.

**Baixo, registrado para decisão:** o container do garak usa `--network host` (para alcançar o P06 em `127.0.0.1`) e `label=disable` (para ler a configuração do repositório). A alternativa é `slirp4netns:allow_host_loopback=true` com montagem `:z`.

## Validação

- `executar_smoke.py`: `135` OK.
- `laboratorios/executar_labs.py`: `84` OK.
- `gerar-exercicios.py`: `--checar` com `82` trechos em `27` labs; `--verificar mercado` OK.
- `testar-ferramentas.py`: `24` OK.
- HTML e PDF conferidos por hash, sem mudança.
- Varredura de segredos no diff: nada encontrado.
