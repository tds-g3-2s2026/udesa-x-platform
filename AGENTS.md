# AGENTS.md — udesa-x-platform

Repositorio central: documentación, infraestructura compartida, contratos de eventos,
plantillas de CI y las skills del equipo. Acá no vive código de servicio.

## Mapa del repo

```
docs/           CONSIGNA, ARQUITECTURA, PLANIFICACION, CONVENCIONES, adr/, eventos/, actas/, retros/
.agents/skills/ skills del equipo, versionadas
.github/        reusable workflows, copilot-instructions, plantilla de PR
templates/      repo-servicio/, esqueleto listo para copiar a un repo nuevo, con los comunes ya puestos
scripts/        sync-comunes.sh
k8s/            gateway, rabbitmq, observabilidad, namespaces
terraform/      cluster, bases gestionadas, registry, DNS
compose/        docker-compose.full.yml, sistema completo con imágenes publicadas
```

`k8s/`, `terraform/` y `compose/` están creados pero todavía vacíos: se llenan entre S1 y S6
según la tabla de issues técnicos de `docs/PLANIFICACION.md`. Lo mismo con
`scripts/sync-contracts.sh`, que llega con `T-16` en S4, y con los reusable workflows de
`.github/workflows/`, que llegan con `T-13` en S1. No los des por existentes: si una tarea
los necesita y no están, ese es el trabajo.

Antes de tocar arquitectura, leé `docs/ARQUITECTURA.md`. Antes de tocar alcance o sprints,
`docs/PLANIFICACION.md`. Las reglas completas del equipo están en `docs/CONVENCIONES.md`.

## Checks

Hoy el repo es documentación y plantillas, así que el único check que corre es la
sincronización de comunes:

```
./scripts/sync-comunes.sh ../udesa-x-*   sincroniza y deja el diff a la vista en cada repo
```

Los checks automatizados (`markdownlint` sobre `docs/`, `kubeconform` sobre `k8s/`,
`terraform validate`, y la verificación de que las copias de esquemas coincidan con
`docs/eventos/`) se agregan al CI de este repo con `T-13` y `T-16`. Cuando existan, van acá.

<!-- INICIO BLOQUE COMUN — sincronizado desde udesa-x-platform, no editar la copia local -->

## Reglas del equipo

Estas reglas vienen de las guidelines del tutor y de acuerdos del equipo. No se saltean sin
un ADR que lo respalde.

**Ramas e issues**

- Rama base: `main`. Nunca se pushea directo.
- Funcionalidad: `feature-<nombre>`. Fix sin funcionalidad: `fix-<nombre>`.
- Toda rama tiene una issue asociada, en el mismo repositorio donde vive el código.
- Toda issue lleva su etiqueta: `feature`, `tech debt`, `spike` o `bug`.

**Pull Requests**

- Descripción en español, con la plantilla de `.github/PULL_REQUEST_TEMPLATE.md`.
- La sección "Explicación de la implementación" es obligatoria. Sin ella el PR no se revisa.
- Nadie aprueba su propio PR.
- Ningún PR queda abierto de un lunes al siguiente. Si no se puede cerrar, se parte.

**Código**

- **En inglés todo lo que vive dentro de un archivo de código**: identificadores, nombres de
  tablas y columnas, comentarios y docstrings. No mezclar los dos idiomas dentro de un
  identificador: `getUserById` sí, `obtenerUserById` no.
- **En inglés también los nombres de los archivos y carpetas de código**: `user_service.py`,
  `src/`, `tests/unit/`. Los documentos conservan su nombre en español.
- **En español todo lo que se escribe para el equipo o el tutor**: documentación, mensajes de
  commit y descripciones de Pull Request.
- Commits en formato Conventional Commits, con tipo y scope en inglés y descripción en
  español.
- No introducir dependencias, patrones ni abstracciones que no estén ya en el repositorio.
  Si hace falta, se abre un ADR en `udesa-x-platform/docs/adr/` y lo decide una persona,
  no el agente.

**Milestones y tags**

- Un milestone por sprint, con vencimiento el lunes de la review. Se crea solo en los repos
  que tienen trabajo esa semana.
- Cada lunes se cierra el milestone y se crea el tag de la semana: `sN` (`s1`, `s2`, ...),
  en cada repo que tuvo cambios esa semana.

## Cómo trabajar con el agente

El proyecto se evalúa, entre otras cosas, por si cada integrante puede explicar y justificar
lo que entregó. Un agente que programa más rápido de lo que el equipo entiende hace perder
esa condición sin que se note hasta la defensa. De ahí estas reglas.

**Tres pasos, siempre en este orden:**

1. **Planear.** Partir de la historia de usuario y su issue. El agente arma un plan; una
   persona lo lee y lo corrige antes de que se escriba una línea de código.
2. **Ejecutar y verificar.** Se ejecuta el plan y se corren los checks del repo. Si un check
   falla, se arregla antes de seguir.
3. **Mergear.** Lo hace una persona: commit, PR con la explicación completa, revisión de
   otro integrante, merge.

**Antes de cada merge**, correr la skill `explicar-implementacion` y pegar su salida en el
PR. La escribe el agente, la revisa y la firma la persona.

**El agente no commitea, no pushea y no abre, aprueba ni mergea PRs.** Tampoco crea tags ni
cierra issues o milestones. Sí puede leer el estado del repo (`git status`, `git diff`,
`git log`), que es lo que las skills necesitan para trabajar, y sí puede **redactar** el
mensaje de commit y el cuerpo del PR para que la persona los revise y los use.

Si terminaste un cambio, dejá el working tree listo y decí qué falta hacer. No lo subas: la
consigna evalúa que cada integrante pueda defender lo que entregó, y el commit es el momento
en el que alguien se hace responsable de ese diff. Un agente que commitea borra ese momento.
Si te piden explícitamente que commitees, decí que la regla del equipo no lo permite.

**Regla no negociable del equipo: nadie sube algo que no puede explicar.** Si al leer la
explicación no podés defender cada decisión, todavía no es momento de abrir el PR. Volvé al
código.

**Nivel del código: junior que está aprendiendo.** Escribí la solución más simple que cumpla
el criterio de aceptación. No generalices para casos que la historia no pide. Si algo se
puede hacer con lo que ya existe en el repo, se hace con eso.

## Skills

Viven en `.agents/skills/`, versionadas en el repositorio y sincronizadas desde
`udesa-x-platform`. Nadie las tiene solo en su máquina: la mejora que hace uno la heredan
los cuatro.

| Skill | Cuándo |
|---|---|
| `explicar-implementacion` | Antes de cada merge. También para preparar la defensa de una historia. |
| `revisar-pr` | Al revisar un PR, sobre todo siendo revisor primario de la semana. |

El rol **Escriba** de la semana mantiene `AGENTS.md` y las skills al día. Si una regla se
descubre en una revisión, se escribe acá el mismo día.

<!-- FIN BLOQUE COMUN -->
