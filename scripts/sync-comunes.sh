#!/usr/bin/env bash
#
# Copies the shared files from udesa-x-platform to the other repos.
#
#   ./scripts/sync-comunes.sh ../udesa-x-users-api
#   ./scripts/sync-comunes.sh ../udesa-x-*     # all of them at once
#
# In CI this runs as repo-file-sync-action, configured in .github/sync.yml. The
# script exists to test a sync by hand and to fix one repo without the workflow.
#
# Copied verbatim: .editorconfig, .gitattributes, .github/copilot-instructions.md,
# .github/PULL_REQUEST_TEMPLATE.md and .agents/skills/.
#
# AGENTS.md is the exception: only the delimited block is replaced, because the
# rest of that file is each repo's own map.
#
# CLAUDE.md is written as a text pointer to AGENTS.md, not a symlink: on Windows
# without privileges a versioned symlink materialises as a frozen copy.

set -euo pipefail

SOURCE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ $# -eq 0 ]; then
  echo "Uso: $0 <ruta-al-repo> [<ruta-al-repo> ...]" >&2
  exit 1
fi

# Extracts the shared block from an AGENTS.md, delimiters included.
extract_block() {
  awk '
    index($0, "<!-- INICIO BLOQUE COMUN") { inside = 1 }
    inside { print }
    index($0, "<!-- FIN BLOQUE COMUN -->") { inside = 0; found = 1 }
    END { if (!found) exit 1 }
  ' "$1"
}

copy_shared_block() {
  local target_agents="$1"

  if [ ! -f "$target_agents" ]; then
    echo "  AGENTS.md no existe, se omite. Crealo desde templates/repo-servicio/AGENTS.md"
    return
  fi

  local new_block old_block
  if ! new_block="$(extract_block "$SOURCE/AGENTS.md")"; then
    echo "No se encontraron los delimitadores del bloque comun en $SOURCE/AGENTS.md" >&2
    exit 1
  fi
  if ! old_block="$(extract_block "$target_agents")"; then
    echo "No se encontraron los delimitadores del bloque comun en $target_agents" >&2
    exit 1
  fi

  if [ "$new_block" = "$old_block" ]; then
    echo "  bloque comun de AGENTS.md ya estaba al dia"
    return
  fi

  # Through a temp file so a failure halfway does not truncate the destination.
  local tmp
  tmp="$(mktemp)"
  awk -v block="$new_block" '
    index($0, "<!-- INICIO BLOQUE COMUN") { print block; inside = 1; next }
    index($0, "<!-- FIN BLOQUE COMUN -->") { inside = 0; next }
    !inside { print }
  ' "$target_agents" > "$tmp"

  mv "$tmp" "$target_agents"
  echo "  bloque comun de AGENTS.md actualizado"
}

for target in "$@"; do
  if [ ! -d "$target" ]; then
    echo "No existe el directorio: $target" >&2
    exit 1
  fi

  if [ "$(cd "$target" && pwd)" = "$SOURCE" ]; then
    echo "==> $(basename "$target") (origen, se omite)"
    continue
  fi

  echo "==> $(basename "$target")"

  mkdir -p "$target/.github" "$target/.agents"

  cp "$SOURCE/.editorconfig" "$target/.editorconfig"
  cp "$SOURCE/.gitattributes" "$target/.gitattributes"
  cp "$SOURCE/.github/copilot-instructions.md" "$target/.github/copilot-instructions.md"
  cp "$SOURCE/.github/PULL_REQUEST_TEMPLATE.md" "$target/.github/PULL_REQUEST_TEMPLATE.md"

  rm -rf "$target/.agents/skills"
  cp -r "$SOURCE/.agents/skills" "$target/.agents/skills"

  echo "  archivos comunes copiados"
  copy_shared_block "$target/AGENTS.md"
  if [ -f "$target/AGENTS.md" ]; then
    cp "$SOURCE/CLAUDE.md" "$target/CLAUDE.md"
    echo "  CLAUDE.md escrito"
  fi
done

echo
echo "Listo. Revisa el diff en cada repo antes de commitear."
