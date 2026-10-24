#!/usr/bin/env bash
#
# Copies the event schemas from docs/eventos/ to contracts/events/ of each
# service, only the ones that service publishes or consumes according to
# docs/eventos/servicios.json.
#
#   ./scripts/sync-contracts.sh ../udesa-x-posts-api
#   ./scripts/sync-contracts.sh ../udesa-x-*     # all of them at once
#
# The service name is the directory name without the "udesa-x-" prefix, the
# same key servicios.json uses. A service missing from servicios.json uses no
# events and ends up without contracts/events/.
#
# The destination is rewritten whole, so a schema that stopped applying to the
# service is removed instead of lingering as a stale copy.
# scripts/verificar-contratos.sh is the check that CI runs against the result.

set -euo pipefail

SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMAS="$SOURCE/docs/eventos"
MANIFEST="$SCHEMAS/servicios.json"

if [ $# -eq 0 ]; then
  echo "Uso: $0 <ruta-al-repo> [<ruta-al-repo> ...]" >&2
  exit 1
fi

for target in "$@"; do
  if [ ! -d "$target" ]; then
    echo "No existe el directorio: $target" >&2
    exit 1
  fi

  if [ "$(cd "$target" && pwd)" = "$SOURCE" ]; then
    echo "==> $(basename "$target") (origen, se omite)"
    continue
  fi

  service="$(basename "$(cd "$target" && pwd)")"
  service="${service#udesa-x-}"
  echo "==> $service"

  events="$(jq -r --arg s "$service" \
    '.[$s] // {} | ((.publica // []) + (.consume // [])) | unique | .[]' "$MANIFEST")"

  rm -rf "$target/contracts/events"

  if [ -z "$events" ]; then
    rmdir "$target/contracts" 2>/dev/null || true
    echo "  no publica ni consume eventos"
    continue
  fi

  mkdir -p "$target/contracts/events"
  while IFS= read -r event; do
    if [ ! -f "$SCHEMAS/$event.json" ]; then
      echo "servicios.json nombra $event pero no existe $SCHEMAS/$event.json" >&2
      exit 1
    fi
    cp "$SCHEMAS/$event.json" "$target/contracts/events/$event.json"
    echo "  $event"
  done <<< "$events"
done

echo
echo "Listo. Revisa el diff en cada repo antes de commitear."
