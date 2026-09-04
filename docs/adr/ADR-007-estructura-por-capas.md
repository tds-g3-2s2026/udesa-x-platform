# ADR-007: Estructura por capas en los servicios backend

**Fecha:** 2026-09-04 · **Estado:** aceptada · **Decide:** el equipo, confirmado por el tutor

**Reemplaza al [ADR-006](./ADR-006-inversion-de-dependencias.md).** La inversión de
dependencias que aquel decidió se mantiene sin cambios; lo que cambia es cómo se agrupan los
archivos.

## Contexto

El ADR-006 decidió invertir las dependencias y, en la misma decisión, conservar el
agrupamiento por feature que venía del PR `udesa-x-users-api#17`. La inversión respondía a un
pedido explícito del tutor; el agrupamiento, en cambio, era una elección del equipo: se eligió
por feature para que `users-api` y `udesa-x-mobile` se leyeran igual.

Esa segunda parte se le consultó al tutor el 3 de septiembre, antes de replicarla en
`posts-api` y `notifications-api`. Su respuesta:

> ¿Cómo manejarían aquellos features que comparten servicios, repos y demás clases? Para lo
> mobile lo veo más lógico porque lo ordenan por pantallas. Para los servicios backends,
> seguir esa estructura les va a generar un spaghetti de archivos y se pierde el responsable
> de esa capa.

La objeción ya era verificable en el código, con solo dos features implementadas.
`features/password_reset/` importaba tres cosas de `features/auth/`: el modelo `User`, la
interfaz `UserRepository` y la política de contraseñas.

Y la proyección lo agrava. De las historias que quedan en las épicas de usuarios y backoffice,
prácticamente todas operan sobre `User`: editar perfil, cambiar contraseña, eliminar cuenta,
crear administradores, iniciar sesión como administrador, seguir y dejar de seguir usuarios.
Con el agrupamiento por feature, `features/auth/` terminaba siendo *la carpeta dueña de
`User`* y las demás importando de ahí. El nombre de la carpeta habría dejado de describir su
contenido.

La diferencia con mobile es real y no es una cuestión de gusto: allá las features son
pantallas y no comparten estado entre sí. Acá comparten la entidad central del servicio.

## Decisión

Los servicios backend se organizan **por capa**, siguiendo la estructura del repositorio de
referencia de la cátedra, `tds-udesa/clase-testing-fullstack`.

```text
src/<servicio>/
├── api/              rutas, esquemas de entrada y salida, y el wiring
├── app/              el negocio: modelos de dominio, interfaces y casos de uso
│   ├── models/
│   ├── repositories/   interfaces de dónde vive el estado
│   ├── clients/        interfaces de lo que habla con afuera
│   └── services/
├── config/
└── infrastructure/   las implementaciones, agrupadas por tecnología
```

**La inversión de dependencias del ADR-006 se mantiene entera.** El tutor la confirmó en el
mismo intercambio: *"los servicios no dependen de implementaciones sino de abstracciones, es
decir, las interfaces"*. Siguen valiendo sus cuatro reglas: la interfaz se declara del lado del
negocio, el modelo de dominio se separa del de persistencia, un solo módulo conoce las
implementaciones concretas, y los repositorios no confirman la transacción.

La regla que ordena todo es una sola y se puede verificar leyendo imports: **`app/` no importa
nada de `api/` ni de `infrastructure/`.**

Dos precisiones sobre dónde cae cada interfaz:

- `app/repositories/` guarda las interfaces de todo lo que **almacena estado**: usuarios,
  tokens, contadores de intentos y revocaciones de sesión. Que unas vivan en PostgreSQL y
  otras en Redis es problema de `infrastructure/`.
- `app/clients/` guarda las interfaces de lo que **habla con un tercero**. Hoy es solo el
  envío de correo.

El ADR-006 necesitaba una excepción para el healthcheck, que le habla a PostgreSQL y a Redis
directamente. Con esta estructura deja de hacer falta: la verificación vive en
`infrastructure/`, y que la infraestructura le hable a la infraestructura no rompe ninguna
regla. La ruta HTTP queda en `api/`, como todas las demás.

## Consecuencias

- **Cada capa tiene un responsable claro.** `User` vive en un solo lugar y no le pertenece a
  ninguna feature en particular, que era la objeción del tutor.
- **`users-api` se reorganiza una segunda vez.** Es trabajo mecánico —mover archivos y
  corregir imports— con la suite de tests como red, pero es tiempo que se paga por haber
  elegido antes de consultar.
- **`posts-api` y `notifications-api` arrancan con la forma definitiva**, que es lo que se
  buscaba al preguntar antes de replicarla.
- **`udesa-x-mobile` conserva su agrupamiento por pantallas.** Los dos repos dejan de leerse
  igual, y está bien: son problemas distintos. Perder esa simetría es el costo aceptado.
- **La regla sigue dependiendo de la revisión.** Nada impide todavía que un archivo de `app/`
  importe `infrastructure/`; está escrito en el `AGENTS.md` de cada repo y se controla al
  revisar. Un test que falle ante ese import sigue pendiente, igual que en el ADR-006.

## Lección

El ADR-006 mezcló dos decisiones de naturaleza distinta en un solo documento: una pedida por
el tutor y otra elegida por el equipo. La primera estaba fuera de discusión y la segunda no,
pero al quedar juntas la segunda entró sin que nadie la revisara con esa mirada.

Cuando una decisión propia viaja pegada a un requisito externo, conviene separarlas o al menos
señalar cuál es cuál.
