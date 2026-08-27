#!/usr/bin/env bash
#
# Sincroniza los archivos comunes desde udesa-x-platform hacia los demas repositorios.
#
# Uso local:
#   ./scripts/sync-comunes.sh ../udesa-x-users-api
#   ./scripts/sync-comunes.sh ../udesa-x-*     # todos a la vez
#
# En CI corre con repo-file-sync-action, configurado en .github/sync.yml.
# Este script existe para poder probar la sincronizacion antes de automatizarla,
# y para arreglar un repo suelto sin esperar al workflow.
#
# Lo que se copia tal cual:
#   .editorconfig
#   .gitattributes
#   .github/copilot-instructions.md
#   .github/PULL_REQUEST_TEMPLATE.md
#   .agents/skills/
#
# AGENTS.md es distinto: solo se reemplaza el bloque delimitado por
#   <!-- INICIO BLOQUE COMUN --> y <!-- FIN BLOQUE COMUN -->
# El resto del archivo, que es el mapa propio de cada repo, no se toca.
#
# CLAUDE.md se escribe solo si el destino ya tiene AGENTS.md: es un puntero de texto a
# ese archivo, no un symlink. En Windows sin privilegios un symlink versionado se
# materializa como una copia congelada; el puntero de texto no tiene ese problema.

set -euo pipefail

ORIGEN="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ $# -eq 0 ]; then
  echo "Uso: $0 <ruta-al-repo> [<ruta-al-repo> ...]" >&2
  exit 1
fi

# Extrae el bloque comun de un AGENTS.md, delimitadores incluidos.
extraer_bloque() {
  awk '
    index($0, "<!-- INICIO BLOQUE COMUN") { dentro = 1 }
    dentro { print }
    index($0, "<!-- FIN BLOQUE COMUN -->") { dentro = 0; encontrado = 1 }
    END { if (!encontrado) exit 1 }
  ' "$1"
}

copiar_bloque_comun() {
  local destino_agents="$1"

  if [ ! -f "$destino_agents" ]; then
    echo "  AGENTS.md no existe, se omite. Crealo desde templates/repo-servicio/AGENTS.md"
    return
  fi

  local bloque_nuevo bloque_viejo
  if ! bloque_nuevo="$(extraer_bloque "$ORIGEN/AGENTS.md")"; then
    echo "No se encontraron los delimitadores del bloque comun en $ORIGEN/AGENTS.md" >&2
    exit 1
  fi
  if ! bloque_viejo="$(extraer_bloque "$destino_agents")"; then
    echo "No se encontraron los delimitadores del bloque comun en $destino_agents" >&2
    exit 1
  fi

  if [ "$bloque_nuevo" = "$bloque_viejo" ]; then
    echo "  bloque comun de AGENTS.md ya estaba al dia"
    return
  fi

  # Reescribe el archivo: todo lo anterior al delimitador, el bloque nuevo, y todo
  # lo posterior al cierre. Se hace con un archivo temporal para no truncar el
  # destino si algo falla a mitad de camino.
  local tmp
  tmp="$(mktemp)"
  awk -v bloque="$bloque_nuevo" '
    index($0, "<!-- INICIO BLOQUE COMUN") { print bloque; dentro = 1; next }
    index($0, "<!-- FIN BLOQUE COMUN -->") { dentro = 0; next }
    !dentro { print }
  ' "$destino_agents" > "$tmp"

  mv "$tmp" "$destino_agents"
  echo "  bloque comun de AGENTS.md actualizado"
}

for destino in "$@"; do
  if [ ! -d "$destino" ]; then
    echo "No existe el directorio: $destino" >&2
    exit 1
  fi

  if [ "$(cd "$destino" && pwd)" = "$ORIGEN" ]; then
    echo "==> $(basename "$destino") (origen, se omite)"
    continue
  fi

  echo "==> $(basename "$destino")"

  mkdir -p "$destino/.github" "$destino/.agents"

  cp "$ORIGEN/.editorconfig" "$destino/.editorconfig"
  cp "$ORIGEN/.gitattributes" "$destino/.gitattributes"
  cp "$ORIGEN/.github/copilot-instructions.md" "$destino/.github/copilot-instructions.md"
  cp "$ORIGEN/.github/PULL_REQUEST_TEMPLATE.md" "$destino/.github/PULL_REQUEST_TEMPLATE.md"

  rm -rf "$destino/.agents/skills"
  cp -r "$ORIGEN/.agents/skills" "$destino/.agents/skills"

  echo "  archivos comunes copiados"
  copiar_bloque_comun "$destino/AGENTS.md"
  if [ -f "$destino/AGENTS.md" ]; then
    cp "$ORIGEN/CLAUDE.md" "$destino/CLAUDE.md"
    echo "  CLAUDE.md escrito"
  fi
done

echo
echo "Listo. Revisa el diff en cada repo antes de commitear."
