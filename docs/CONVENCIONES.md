# Convenciones del equipo

Fuente única de las reglas de trabajo. El bloque común de los `AGENTS.md` sale de acá; si
una regla cambia, se cambia primero en este archivo y después se sincroniza con
`scripts/sync-comunes.sh`.

Las reglas marcadas con **(tutor)** vienen de las code guidelines que el tutor mandó el
2026-08-19. No se modifican sin hablarlo con él.

## Repositorios

Seis repositorios en `tds-g3-2s2026`:

| Repositorio | Contenido |
|---|---|
| `udesa-x-platform` | Documentación, infraestructura compartida, contratos, skills, CI reusable |
| `udesa-x-mobile` | App mobile |
| `udesa-x-backoffice` | Backoffice web |
| `udesa-x-users-api` | Identidad, perfiles, administradores, avatares |
| `udesa-x-posts-api` | Contenido, grafo social, feed, búsqueda, imágenes de post |
| `udesa-x-notifications-api` | Cola, push, emails, triage de IA |

**(tutor)** Cada servicio en su repositorio, con sus tests y coverage, sus pipelines y
scripts, su Docker y compose de desarrollo, y sus manifiestos de Kubernetes.

**(tutor)** Todos los repositorios tienen `README.md`, `.editorconfig`, linters y
formatters.

## Ramas

**(tutor)** Rama base `main`. Funcionalidad: `feature-<nombre>`. Fix sin funcionalidad:
`fix-<nombre>`.

```
feature-registro-usuarios
feature-feed-cronologico
fix-contador-retweets
```

`main` está protegida: sin push directo, CI en verde y al menos una aprobación de otra
persona.

Nota: el tutor escribió la convención como `/feature-[nombre]`. Git no admite nombres de rama
que empiecen con barra, así que se usa `feature-<nombre>`. Confirmarlo en la primera
reunión.

## Issues

**(tutor)** Toda rama tiene una issue asociada. **Las issues viven en el repositorio donde
vive el código**, no centralizadas: es lo que hace que el milestone semanal y el tag de esa
semana coincidan con lo que efectivamente se tocó.

Los issues transversales que no pertenecen a ningún servicio (infraestructura, documentación,
decisiones) van en `udesa-x-platform`.

**(tutor)** Cada issue lleva la información necesaria para implementar la tarea y su
etiqueta correspondiente.

### Etiquetas

Las cuatro de tipo son las que pidió el tutor y son obligatorias:

```
feature       funcionalidad nueva, incluye historias de usuario
tech debt     deuda técnica, refactors, mantenimiento
spike         investigación con tiempo acotado y resultado escrito
bug           defecto sobre algo ya entregado
```

Complementarias del equipo:

```
epic:e1-users   epic:e2-posts   epic:e3-social   epic:e4-notif   epic:e5-backoffice
scope:mandatory   scope:optional   scope:backlog
blocked   needs-tutor   carry-over   decision
```

`decision` marca las decisiones abiertas `Dxx` del plan, que viven como issues en
`udesa-x-platform`. No reemplaza a la etiqueta de tipo: cada una lleva además la que le
corresponda.

`carry-over` marca toda historia que se corrió de un sprint al siguiente. Si al cierre de un
sprint hay más de dos, el problema no es de esa semana sino de la estimación.

## Milestones y tags

**(tutor)** Un milestone por sprint. Cada lunes se cierra el milestone de la semana y se
crea el tag correspondiente.

- Nombre del milestone: `S1` a `S15`, con vencimiento el lunes de la review.
- El milestone se crea **solo en los repos que tienen trabajo esa semana**. Quince
  milestones por seis repos sería inmanejable y no aporta nada.
- Tag semanal: `sN` en cada repo que tuvo cambios esa semana, creado el lunes al cerrar el
  milestone.
- El facilitador de la semana es quien cierra los milestones y crea los tags.

El Project de la organización toma issues de todos los repos, así que el tablero funciona
igual con las issues distribuidas.

## Pull Requests

**(tutor)** Las descripciones van en español. Se logra con
`.github/copilot-instructions.md`, sincronizado a todos los repos.

Plantilla obligatoria en `.github/PULL_REQUEST_TEMPLATE.md`. La sección "Explicación de la
implementación" es obligatoria: **sin ella el PR no se revisa.**

Un PR por historia, o por criterio de aceptación si la historia es grande. Ningún PR queda
abierto de un lunes al siguiente.

## Código

**(tutor)** Código en inglés o en español, pero no espanglish. El equipo eligió que la
frontera sea el archivo de código: **todo lo que vive dentro de un archivo de código va en
inglés, y todo lo que se escribe para el equipo o el tutor va en español.**

| En inglés | En español |
|---|---|
| Identificadores: variables, funciones, clases | Documentación: `docs/`, `README.md` |
| Nombres de tablas y columnas | Mensajes de commit |
| Comentarios dentro del código | Descripciones de Pull Request |
| Docstrings | Comentarios de revisión en los PR |
| Nombres de archivos y carpetas de código | |

No mezclar los dos idiomas dentro de un identificador: `getUserById` está bien,
`obtenerUserById` no.

**Alcance de los nombres de archivo.** La regla aplica a los archivos y carpetas de código:
`user_service.py`, `likes.py`, `src/`, `tests/unit/`. Los documentos conservan su nombre en
español, que es coherente con que su contenido también lo esté: `CONVENCIONES.md`,
`PLANIFICACION.md`, `docs/actas/`, `scripts/sync-comunes.sh` y las skills
`explicar-implementacion` y `revisar-pr` se quedan como están.

La regla es una sola y es fácil de recordar: **si lo lee un intérprete o un compilador, está
en inglés; si lo lee una persona fuera del código, está en español.** Un archivo de código
queda entonces íntegramente en un solo idioma, que es lo que el tutor pidió al prohibir el
espanglish.

**(tutor, opcional)** Commits en formato Conventional Commits. El equipo lo adopta:

```
feat(users): agregar validacion de handle unico
fix(posts): corregir contador de retweets al deshacer
test(users): cubrir CA.4 de E1-H1
```

## Qué no hace un agente

Claude Code y cualquier otro agente pueden escribir código, correr los checks y redactar
textos. **No commitean, no pushean y no abren, aprueban ni mergean Pull Requests.** Esas
cuatro acciones las ejecuta siempre una persona, desde su cuenta.

| Puede | No puede |
|---|---|
| Leer el repo, `git status`, `git diff`, `git log` | `git commit`, `git push`, `git merge`, `git rebase`, `git tag` |
| Editar archivos en el working tree | Crear, aprobar o mergear un PR |
| Correr lint, tests y los scripts del repo | Cerrar issues o milestones |
| Redactar el mensaje de commit y el cuerpo del PR, para que la persona los revise y los use | Publicar ese texto por su cuenta |

**Por qué.** La consigna evalúa que cada integrante pueda explicar y justificar lo que
entregó. El commit y el PR son el registro de quién se hace responsable de qué: si los firma
el agente, la autoría deja de significar algo y la regla de "nadie sube algo que no puede
explicar" se queda sin el momento en el que se verifica. Que la persona tenga que escribir
`git commit` es justamente el punto donde tiene que haber leído el diff.

También es lo que mantiene honesto el historial que se muestra en la defensa: el tutor
puede pedir el `git log` de una semana y lo que ahí figura es lo que cada uno sostuvo.

Es una regla del equipo, no una configuración: si el día de mañana se automatiza algo que
la toque, se decide con un ADR primero.

## Sincronización entre repos

El tutor recomendó `repo-file-sync-action` para no repetir archivos entre repos. El equipo lo
usa para los archivos comunes, y usa reusable workflows de GitHub para el CI, que es lo que
GitHub ya resuelve de fábrica. La diferencia se plantea en la primera reunión; queda
registrada como decisión A30 en [`ARQUITECTURA.md`](./ARQUITECTURA.md).

Se sincronizan desde `udesa-x-platform`:

| Archivo | Destino |
|---|---|
| `.editorconfig` | todos los repos |
| `.github/copilot-instructions.md` | todos los repos |
| `.github/PULL_REQUEST_TEMPLATE.md` | todos los repos |
| `.agents/skills/` | todos los repos |
| bloque común de `AGENTS.md` | todos los repos |
| `docs/eventos/*.json` → `contracts/events/` | repos de servicio |

El CI de `udesa-x-platform` verifica que las copias coincidan con la fuente. Si alguien edita
una copia local sin propagar, el pipeline lo detecta.

## Trazabilidad de criterios de aceptación

Cada criterio de aceptación tiene al menos un test cuyo nombre lo referencia, con el formato
`E1-H1.CA3`.

Esto hace que la defensa ante el tutor sea mecánica: se corre la suite filtrando por
identificador y se muestra el criterio verificado. Y obliga a que cada criterio sea
verificable: si no se puede escribir el test, el criterio está mal entendido y hay que
consultarlo antes de programar.
