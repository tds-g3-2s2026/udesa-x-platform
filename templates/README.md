# Plantillas

## `repo-servicio/`

Esqueleto para arrancar un repositorio de servicio en Python. Sale de `udesa-x-users-api`,
que es donde se probó primero: no es código inventado.

### Cómo usarla

1. Copiar todo el contenido de `repo-servicio/` a la raíz del repositorio nuevo.
2. Renombrar `src/servicio/` por el nombre real del paquete, en `snake_case`.
3. Ajustar `name`, `description` y el bloque `[tool.hatch.build.targets.wheel]` de
   `pyproject.toml`.
4. Ajustar en `docker/docker-compose.dev.yml` el nombre del proyecto, el del servicio y las
   credenciales de la base.
5. Reemplazar el mapa del repositorio en `AGENTS.md`. El bloque delimitado por
   `<!-- INICIO BLOQUE COMUN -->` no se toca: lo sincroniza `scripts/sync-comunes.sh`.
6. Escribir el `README.md`, que la plantilla no trae a propósito porque es propio de cada
   servicio.

El repositorio queda con `docker compose -f docker/docker-compose.dev.yml up` funcionando y
con el CI conectado al workflow reusable, sin pasos adicionales.

### Qué no incluye

No hay plantilla para servicios en TypeScript. `notifications-api` es el primero, en S4, y su
plantilla sale de ese código una vez probado, con el mismo criterio.
