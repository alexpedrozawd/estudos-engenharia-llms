# Changelog — Etapa 6a: Kubernetes local com kind (26/11/2026)

Autoria: claude - pessoal. Etapa 6 do [plano de prontidão](../historico/plano-prontidao-para-vaga-pleno-2026-11-25.md), planejada e executada com autorização do operador para agir de forma autônoma até o fim da etapa. HTML, PDF e `laboratorios/` inalterados.

## Entregas

1. **Ferramentas no perfil do usuário:** `kind` `0.33.0` e `kubectl` `1.37.3` pelo Homebrew. Imagem base intocada. O Podman `6.2.0` rootless já delegava `cpu`, `memory`, `io` e `pids`, então o cluster (Kubernetes `v1.37.0`) subiu sem mudança no sistema.
2. **Manifests em [`laboratorios-mercado/k8s/`](../../laboratorios-mercado/k8s/README.md)** (Kustomize):
   - namespace com Pod Security `restricted`;
   - ConfigMap;
   - `pgvector` em StatefulSet com PVC, rodando como uid `999`;
   - P05 e P06 em Deployments com 2 réplicas, `maxUnavailable: 0`, `preStop` de 5 s, raiz somente leitura, `/tmp` em `emptyDir` e limites de CPU e memória;
   - Services com portas nomeadas;
   - NetworkPolicy que só deixa o integrador falar com o banco.
3. **Segredos fora do Git:** o script gera o Secret com valores aleatórios e o envia ao cluster por stdin, nunca por argumento. Ele é lido de volta só em memória. Uma varredura confirmou que nenhum valor aparece nos registros nem nos arquivos de `k8s/`.
4. **[`executar_k8s_local.py`](../../laboratorios-mercado/k8s/executar_k8s_local.py)** com os comandos `subir`, `validar` e `remover`. O `validar` faz 12 verificações e grava o resultado em `laboratorios-mercado/execucoes/k8s-local-*.json`. A disponibilidade é medida de dentro do cluster, com uma sonda que chama o Service a cada 0,25 s durante cada *rollout*.
5. **Testes offline dos manifests:** 9 testes em `k8s/test_k8s_manifests.py`, rodados pelo `executar_smoke.py` (novo alvo `k8s`) e pelo CI. Eles conferem:
   - contexto de segurança, *probes* e limites;
   - *rollout* seguro;
   - fábrica e porta de cada comando;
   - segredos só por `secretKeyRef`;
   - Services ligados aos pods;
   - a NetworkPolicy;
   - a coerência do Secret gerado com o carregador de chaves do P06.
   
   `pyyaml>=6.0` virou dependência declarada (antes chegava só de forma indireta, pelo LangChain).

## Achados no cluster (corrigidos e revalidados)

- **Médio — P06 devolvia `500` quando a recuperação falhava.** Com o embedder inalcançável, o `httpx.ConnectError` escapava, porque só a chamada ao LLM estava protegida desde a Etapa 4. Correção: a recuperação também passa por `falha_de_backend`, que agora inclui `psycopg.OperationalError`, e responde `503` + `Retry-After`. Erro de SQL ou de código continua visível. O teste de regressão falha no código antigo e passa no novo.
- **Médio — requisições falhavam durante o *rollout*:** `3` falhas na troca v1 → v2 e `1` no *rollback*, porque o pod antigo parava antes de sair dos endpoints do Service. Correção: `preStop` de 5 s e `terminationGracePeriodSeconds: 20`. Depois: `0` falhas em `179` e `239` chamadas da sonda.

## Validação

- `validar` aprovado três vezes seguidas (`12/12`): pods prontos; namespace `restricted`; `/saude` de P05 e P06; `401` sem chave; `403` anti-BFLA; `503` + `Retry-After` com backend fora; NetworkPolicy (P05 bloqueado, P06 conecta); dado persistido após recriar o pod do banco; *rollout* v2 em cerca de 12 s sem falha; imagem quebrada (`ErrImageNeverPull`) trava o *rollout* com `2` réplicas prontas e o *rollback* volta à v2 sem falha.
- `executar_smoke.py`: `146` testes OK. `executar_labs.py` OK. `testar-ferramentas.py --rapido` OK. `gerar-exercicios.py --verificar mercado` e `--checar` OK. `compose.yaml` válido no `podman-compose`. `podman build` do `Containerfile` OK.

## Limites e pendências

- O Ollama do host escuta só em `127.0.0.1` e não é alcançável do kind rootless. Por isso, no cluster, só o caminho de degradação (`503`) foi exercitado. A rede do Ollama não foi alterada: isso seria uma mudança de segurança no host, fora do escopo.
- **6b (deploy em nuvem) bloqueada.** Criar conta, cadastrar cobrança e publicar exigem autorização explícita do operador e cadastro feito por ele. Para destravar, é preciso decidir: o provedor (pelo mapa de vagas, AWS aparece em `45%` das vagas e Azure em `41%`), o teto de gasto e a criação da conta. O P06 já aceita Azure, Bedrock e Vertex como fronteira (Cap. 20).
- Revisão humana da Etapa 3 segue com o operador.
