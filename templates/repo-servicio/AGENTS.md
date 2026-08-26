# AGENTS.md - udesa-x-<servicio>

<!-- INICIO BLOQUE PROPIO - completado en cada servicio -->

<Una línea: descripción del servicio, su alcance y épicas asociadas>

## Stack y herramientas

- Lenguaje y runtime: <ej. Python 3.12 / FastAPI / Node.js>
- Gestor de paquetes: <ej. uv / pnpm>
- Persistencia y migraciones: <ej. PostgreSQL / SQLAlchemy / Alembic>

## Checks y comandos

```bash
./scripts/lint.sh       # Linting y chequeo estático de tipos
./scripts/test.sh       # Tests unitarios con reporte de cobertura (mínimo 85%)
./scripts/test.sh -i    # Tests de integración contra dependencias en contenedores
```

## Arquitectura y particularidades locales

- Regla de capas: la lógica de negocio vive en `services/`, rutas HTTP en `routes/`, acceso a datos en `repositories/`.
- Documentación general del sistema: consultar `../udesa-x-platform/docs/` (`ARQUITECTURA.md`, `CONVENCIONES.md`, `PLANIFICACION.md`).

<!-- FIN BLOQUE PROPIO -->

<!-- INICIO BLOQUE COMUN - sincronizado desde udesa-x-platform, no editar la copia local -->

## Reglas del equipo

- **Ramas e issues**: Rama base `main`. Ramas de trabajo `feature-<nombre>` o `fix-<nombre>`, siempre asociadas a un issue en el mismo repositorio.
- **Idiomas**:
  - Código (`src/`, `tests/`), nombres de archivos, identificadores y comentarios en código: **inglés**.
  - Documentación (`docs/`, `README.md`), mensajes de commit y Pull Requests: **español**.
- **Commits**: Formato Conventional Commits (`feat:`, `fix:`, `docs:`, etc.) con descripción en español.
- **Simplicidad**: Soluciones mínimas y directas para el criterio de aceptación. No introducir librerías, patrones ni abstracciones nuevas sin un ADR aprobado en `docs/adr/`.

## Límites y flujo de trabajo del agente

- El agente inspecciona el repositorio (`git status`, `git diff`), edita archivos en el working tree, ejecuta checks locales y redacta propuestas de commit y PR.
- **El agente nunca commitea, pushea ni abre/aprueba/mergea Pull Requests.** La revisión y confirmación en Git la realiza siempre un integrante del equipo.
- **Sin firmas**: Nunca agregar `Co-Authored-By`, firmas o menciones del agente en commits, PRs ni código.

## Modo de planificación

- Planes extremadamente concisos: priorizar brevedad y concreción por sobre prosa formal.
- Al final de cada plan, incluir la lista de preguntas o dudas pendientes a resolver (si las hay).

## Skills (.agents/skills/)

- `explicar-implementacion`: Genera la explicación detallada del cambio para incluir en la descripción del PR.
- `revisar-pr`: Guía paso a paso para la revisión técnica de Pull Requests.

<!-- FIN BLOQUE COMUN -->
