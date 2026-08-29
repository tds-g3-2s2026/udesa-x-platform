# AGENTS.md - udesa-x-platform

Repositorio central de udesa-x: documentación, infraestructura compartida, contratos de eventos, plantillas de CI y skills del equipo (sin código de servicio).

## Checks y comandos

```bash
./scripts/sync-comunes.sh ../udesa-x-*   # Sincroniza archivos y bloque común a los demás repositorios
./scripts/sync-comunes.sh templates/repo-servicio   # Deja la plantilla al día con los comunes
```

El CI de este repo verifica que `templates/repo-servicio/` no quede atrás de los archivos
comunes de la raíz. Si el check `Verificar plantilla` falla, correr el segundo comando.

Los workflows reusables que consumen los repos de servicio viven en `.github/workflows/`.

## Documentación (Progressive Disclosure)

- Arquitectura del sistema y componentes: `docs/ARQUITECTURA.md`
- Convenciones de equipo, ramas, PRs y estilo de código: `docs/CONVENCIONES.md`
- Planificación, sprints y roadmap: `docs/PLANIFICACION.md`
- Catálogo de issues y épicas: `docs/CATALOGO-ISSUES.md`
- Decisiones de arquitectura tomadas: `docs/adr/`
- Consigna general de la materia: `docs/CONSIGNA.md`

<!-- INICIO BLOQUE COMUN - sincronizado desde udesa-x-platform, no editar la copia local -->

## Reglas del equipo

- **Ramas e issues**: Rama base `main`. Ramas de trabajo `feature-<nombre>` (funcionalidad), `fix-<nombre>` (defecto) o `chore-<nombre>` (mantenimiento y tooling, etiqueta `tech debt`), siempre asociadas a un issue en el mismo repositorio.
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
