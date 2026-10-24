#!/usr/bin/env bash
#
# Checks the event schemas in docs/eventos/ before they get copied anywhere:
#
#   - each schema compiles as JSON Schema 2020-12, in strict mode;
#   - each example inside it validates against it;
#   - the file name, title, $id and the "type" constant name the same event;
#   - servicios.json names only schemas that exist, every schema appears there,
#     and each event has exactly one publisher, the one in its "source".
#
#   ./scripts/validar-esquemas.sh
#
# Needs jq and npx. The Contratos de eventos workflow runs it on every PR.

set -euo pipefail

SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMAS="$SOURCE/docs/eventos"
MANIFEST="$SCHEMAS/servicios.json"
AJV=(npx --yes -p ajv-cli@5 -p ajv-formats@3 ajv)
failed=0

fail() {
  if [ -n "${GITHUB_ACTIONS:-}" ]; then
    echo "::error file=docs/eventos/$1::$2"
  else
    echo "docs/eventos/$1: $2" >&2
  fi
  failed=1
}

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

shopt -s nullglob
schemas=()
for path in "$SCHEMAS"/*.json; do
  [ "$(basename "$path")" = "servicios.json" ] || schemas+=("$path")
done

for path in "${schemas[@]}"; do
  file="$(basename "$path")"
  event="${file%.json}"

  if ! jq -e --arg e "$event" \
    '.title == $e and ."$id" == "urn:udesa-x:eventos:\($e)" and .properties.type.const == $e' \
    "$path" > /dev/null; then
    fail "$file" "title, \$id y properties.type.const tienen que nombrar a $event."
  fi

  if ! "${AJV[@]}" compile --spec=draft2020 --strict=true -c ajv-formats -s "$path"; then
    fail "$file" "No compila como JSON Schema 2020-12."
    continue
  fi

  count="$(jq '.examples // [] | length' "$path")"
  if [ "$count" -eq 0 ]; then
    fail "$file" "Necesita al menos un mensaje en examples."
  fi
  for ((i = 0; i < count; i++)); do
    jq ".examples[$i]" "$path" > "$work/$event.example-$i.json"
    if ! "${AJV[@]}" validate --spec=draft2020 --strict=true -c ajv-formats \
      -s "$path" -d "$work/$event.example-$i.json"; then
      fail "$file" "examples[$i] no valida contra el esquema."
    fi
  done

  source="$(jq -r '.properties.source.const' "$path")"
  publishers="$(jq -r --arg e "$event" \
    '[to_entries[] | select((.value.publica // []) | index($e)) | .key] | join(" ")' "$MANIFEST")"
  if [ "$publishers" != "$source" ]; then
    fail "$file" "En servicios.json lo tiene que publicar solo $source, y lo publica: '${publishers}'."
  fi
done

while IFS= read -r event; do
  if [ ! -f "$SCHEMAS/$event.json" ]; then
    fail "servicios.json" "Nombra $event, que no tiene esquema."
  fi
done < <(jq -r '[.[] | (.publica // []) + (.consume // []) | .[]] | unique | .[]' "$MANIFEST")

if [ "$failed" -ne 0 ]; then
  exit 1
fi

echo "Esquemas de eventos válidos."
