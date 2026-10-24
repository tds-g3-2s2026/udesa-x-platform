#!/usr/bin/env bash
#
# Fails when a service's contracts/events/ is not exactly what
# scripts/sync-contracts.sh would write: a schema missing, edited by hand,
# behind the source or no longer used by the service.
#
#   ./scripts/verificar-contratos.sh posts-api ../udesa-x-posts-api
#
# ci-node.yml and ci-python.yml run it on every service, against platform's
# main, so a contract change that was not synced turns that service's CI red.

set -euo pipefail

SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMAS="$SOURCE/docs/eventos"
MANIFEST="$SCHEMAS/servicios.json"

if [ $# -ne 2 ]; then
  echo "Uso: $0 <servicio> <ruta-al-repo>" >&2
  exit 1
fi

service="$1"
copies="$2/contracts/events"
failed=0

fail() {
  if [ -n "${GITHUB_ACTIONS:-}" ]; then
    echo "::error file=contracts/events/$1::$2"
  else
    echo "contracts/events/$1: $2" >&2
  fi
  failed=1
}

expected="$(jq -r --arg s "$service" \
  '.[$s] // {} | ((.publica // []) + (.consume // [])) | unique | .[]' "$MANIFEST")"

while IFS= read -r event; do
  [ -n "$event" ] || continue
  if [ ! -f "$copies/$event.json" ]; then
    fail "$event.json" "Falta: $service publica o consume $event."
  elif ! diff -u "$SCHEMAS/$event.json" "$copies/$event.json"; then
    fail "$event.json" "Difiere de docs/eventos/$event.json en udesa-x-platform."
  fi
done <<< "$expected"

if [ -d "$copies" ]; then
  for copy in "$copies"/*; do
    [ -e "$copy" ] || continue
    name="$(basename "$copy")"
    if ! grep -qxF "${name%.json}" <<< "$expected"; then
      fail "$name" "Sobra: $service no lo publica ni lo consume según servicios.json."
    fi
  done
fi

if [ "$failed" -ne 0 ]; then
  echo "Los contratos de eventos de $service no coinciden con udesa-x-platform." >&2
  echo "Corré desde udesa-x-platform: ./scripts/sync-contracts.sh <ruta-a-este-repo>" >&2
  exit 1
fi

echo "Contratos de eventos de $service al día."
