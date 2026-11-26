#!/bin/bash
# Roda uma lista de sondas do garak 0.17.1 (container, volume garak-venv) contra o P06 em 127.0.0.1:8001.
# Uso: executar_garak.sh <prefixo> <sonda1,sonda2,...>
# O container para sozinho após GARAK_TIMEOUT_S (padrão 570 s), mesmo se o cliente cair.
# Isolamento: rede própria (pasta) com só a porta do P06 (P06_PORTA, padrão 8001) encaminhada ao loopback
# do host, em vez de --network host; montagens com rótulo SELinux (:z) em vez de label=disable.
# A chave vem de REST_API_KEY no ambiente (nunca no repositório); os relatórios vão para rascunho-local/redteam/.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/../../.." && pwd)"
: "${REST_API_KEY:?defina REST_API_KEY com uma chave aceita pelo P06}"
mkdir -p "$RAIZ/rascunho-local/redteam/saida"
exec podman run --rm --name "garak-$1" --timeout "${GARAK_TIMEOUT_S:-570}" --network "pasta:-T,${P06_PORTA:-8001}" -e REST_API_KEY -e HOME=/opt/garak/home \
  -v garak-venv:/opt/garak -v "$RAIZ/laboratorios-mercado/06_integrador_producao/redteam:/cfg:ro,z" \
  -v "$RAIZ/rascunho-local/redteam/saida:/saida:z" docker.io/library/python:3.12-slim \
  /opt/garak/venv/bin/python -m garak --target_type rest -G /cfg/garak-rest-p06.json \
  --config /cfg/garak-execucao.yaml --report_prefix "$1" --probes "$2"
