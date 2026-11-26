# Kubernetes local com kind (Etapa 6a)

P05 (`api-llmops`), P06 (`integrador`) e `pgvector` no namespace `aurora`, em um cluster [kind](https://kind.sigs.k8s.io/) rodando no Podman rootless. Sem custo e sem nuvem. O deploy em nuvem (antiga Etapa 6b) foi descartado pelo operador em 26/11/2026: o material é de uso pessoal.

## O que os manifests mostram

| Recurso | Arquivo | Ponto de produção |
|---|---|---|
| Namespace | `manifests/namespace.yaml` | Pod Security `restricted`: nada roda como root |
| ConfigMap | `manifests/configmap.yaml` | Configuração sem segredo |
| Secret `aurora-segredos` | gerado pelo script | Valores aleatórios, enviados por stdin; nunca no Git |
| StatefulSet + PVC | `manifests/pgvector.yaml` | Banco com volume persistente, uid `999`, *probes* `pg_isready` |
| Deployments + Services | `manifests/api-llmops.yaml`, `manifests/integrador.yaml` | 2 réplicas, `maxUnavailable: 0`, `preStop` de 5 s, raiz somente leitura, limites de CPU e memória |
| NetworkPolicy | `manifests/networkpolicy.yaml` | Só o integrador alcança o banco |

## Uso

Pré-requisitos: `kind` e `kubectl` (`brew install kind kubernetes-cli`; nada na imagem base), Podman rootless com cgroup v2 delegando `cpu`, `memory`, `io` e `pids`, e a imagem da Camada 3 construída:

```bash
podman build -f laboratorios-mercado/Containerfile -t localhost/laboratorios-mercado:dev .
.venv-mercado/bin/python -I laboratorios-mercado/k8s/executar_k8s_local.py subir     # cria o cluster, carrega imagens, aplica
.venv-mercado/bin/python -I laboratorios-mercado/k8s/executar_k8s_local.py validar   # 12 verificações; registro em execucoes/
.venv-mercado/bin/python -I laboratorios-mercado/k8s/executar_k8s_local.py remover   # apaga o cluster
```

O `validar` confere: pods prontos; namespace `restricted`; `/saude` de P05 e P06; `401` sem chave; `403` anti-BFLA; `503` com `Retry-After` quando o backend está fora; o bloqueio da NetworkPolicy; um dado que sobrevive à recriação do pod do banco; *rollout* v1 → v2 sem falha; e uma imagem quebrada que trava o *rollout* sem derrubar o serviço, seguida de *rollback*. A disponibilidade é medida de dentro do cluster, com uma sonda que chama o Service a cada 0,25 s.

Testes offline dos YAML (sem cluster, também no CI): `executar_smoke.py --alvo k8s`.

## Limites

- O Ollama do host escuta só em `127.0.0.1` e não é alcançável do kind rootless (`host.containers.internal` nem resolve nos pods). Por isso, no cluster, `/v1/assistente` responde `503`; o caminho com LLM real foi validado fora do cluster, na Etapa 2. Para respostas reais, aponte as URLs do ConfigMap para um serviço alcançável.
- Um só nó, sem Ingress, sem HPA e sem backup do volume: o objetivo é estudo de deploy, não alta disponibilidade.
