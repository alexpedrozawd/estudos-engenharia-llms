#!/bin/bash
# Roda uma lista de sondas do garak 0.17.1 (container, volume garak-venv) contra o P06 em 127.0.0.1:8001.
# Uso: executar_garak.sh <prefixo> <sonda1,sonda2,...>
# O container para sozinho após GARAK_TIMEOUT_S (padrão 570 s), mesmo se o cliente cair.
# A chave vem de REST_API_KEY no ambiente (nunca no repositório); os relatórios vão para rascunho-local/redteam/.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/../../.." && pwd)"
: "${REST_API_KEY:?defina REST_API_KEY com uma chave aceita pelo P06}"
mkdir -p "$RAIZ/rascunho-local/redteam/saida"
exec podman run --rm --name "garak-$1" --timeout "${GARAK_TIMEOUT_S:-570}" --network host --security-opt label=disable -e REST_API_KEY -e HOME=/opt/garak/home \
  -v garak-venv:/opt/garak -v "$RAIZ/laboratorios-mercado/06_integrador_producao/redteam:/cfg:ro" \
  -v "$RAIZ/rascunho-local/redteam/saida:/saida" docker.io/library/python:3.12-slim \
  /opt/garak/venv/bin/python -m garak --target_type rest -G /cfg/garak-rest-p06.json \
  --config /cfg/garak-execucao.yaml --report_prefix "$1" --probes "$2"
