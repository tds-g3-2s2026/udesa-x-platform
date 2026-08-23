# AGENTS.md — udesa-x-<servicio>

<!--
PLANTILLA. Al crear el repo, completá el bloque propio de abajo y dejá el bloque común tal
como viene: lo sincroniza `scripts/sync-comunes.sh` desde udesa-x-platform y cualquier
edición local se pierde en la próxima sincronización.
-->

<!-- INICIO BLOQUE PROPIO — se completa en cada repo -->

<una línea: qué hace este servicio y qué épicas cubre>

## Mapa del repo

```
src/
  routes/        entrada HTTP, validación de esquema, nada de lógica de negocio
  services/      lógica de negocio, transacciones
  repositories/  acceso a datos
  events/        publicación y consumo de eventos
tests/unit/         unitarios
tests/integration/  contra base y cola reales en contenedores
contracts/events/   copia de los esquemas, sincronizada desde platform, no editar a mano
docker/             Dockerfile y docker-compose.dev.yml
k8s/                base/ y overlays/
scripts/            test.sh, lint.sh, migrate.sh
```

Regla de capas: la lógica de negocio vive en `services/`. Un `route` que consulta la base
directamente es un error de revisión.

## Stack

- <lenguaje y framework>
- <base de datos>
- <herramienta de migraciones>

## Checks

```
./scripts/lint.sh      lint y chequeo de tipos
./scripts/test.sh      unitarios con reporte de cobertura
./scripts/test.sh -i   integración, levanta dependencias en contenedores
```

**Cobertura mínima: 85%.** El gate está activo desde <S3 para backend | S5 para mobile y
backoffice> y falla el PR si baja.

## Cosas propias de este servicio

<Lo que sorprendería a alguien que llega de otro repo. Ejemplos: los contadores se
actualizan en la misma transacción que el insert; la clave primaria de posts es UUIDv7; los
eventos se publican con patrón outbox, nunca directo al broker.>

<!-- FIN BLOQUE PROPIO -->

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

- Código, identificadores y nombres de base de datos en inglés. Comentarios en español.
  No mezclar los dos idiomas dentro de un identificador.
- Comentarios cortos y sobre el porqué, no sobre el qué. Nada de bloques de varios renglones
  explicando lo que el código ya dice. Si hace falta un párrafo para entender una función,
  el problema es la función.
- Commits en formato Conventional Commits.
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

**Cuatro pasos, siempre en este orden:**

1. **Situarse.** Antes de escribir nada, traer el estado remoto y mirar `main`, las ramas
   abiertas y los Pull Requests abiertos. No solo los del repositorio propio: el trabajo
   transversal aparece en `udesa-x-platform` y puede tocar los seis. Si ya hay una rama o un
   PR sobre los mismos archivos, se habla con quien lo abrió antes de empezar. Repetir el
   chequeo antes de commitear, porque el estado pudo cambiar mientras tanto.
2. **Planear.** Partir de la historia de usuario y su issue. El agente arma un plan; una
   persona lo lee y lo corrige antes de que se escriba una línea de código.
3. **Ejecutar y verificar.** Se ejecuta el plan y se corren los checks del repo. Si un check
   falla, se arregla antes de seguir.
4. **Mergear.** Lo hace una persona: commit, PR con la explicación completa, revisión de
   otro integrante, merge.

Saltear el primer paso ya costó trabajo duplicado: dos personas editaron los mismos archivos
porque había una rama pusheada que nadie miró. Con seis repositorios y cuatro personas, el
estado del proyecto nunca es el que uno recuerda.

**Antes de cada merge**, correr la skill `explicar-implementacion` y pegar su salida en el
PR. La escribe el agente, la revisa y la firma la persona.

**El agente no commitea, no pushea y no abre, aprueba ni mergea PRs.** Tampoco crea tags ni
cierra issues o milestones. Sí puede leer el estado del repo (`git status`, `git diff`,
`git log`), que es lo que las skills necesitan para trabajar, y sí puede **redactar** el
mensaje de commit y el cuerpo del PR para que la persona los revise y los use.

**Nada de lo que se versiona lleva rastros del agente.** Sin `Co-Authored-By`, sin firmas ni
marcas de herramienta en commits, PRs, documentación o código. Lo que se sube va a nombre de
quien lo entrega, porque es quien lo va a tener que defender.

**La documentación no promete de más.** Un entregable escrito por comodidad, que el equipo no
va a cumplir, es deuda que se paga en la review delante del tutor. Si un documento compromete
algo irreal, se corrige el documento.

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
