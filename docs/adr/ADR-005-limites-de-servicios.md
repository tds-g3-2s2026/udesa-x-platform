# ADR-005: Límites de servicios, contratos y dependencias de infraestructura

**Fecha:** 2026-08-30 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

`ARQUITECTURA.md` fija en A4b la cantidad de servicios backend (tres: `users-api`, `posts-api`,
`notifications-api`) y en A7 que el feed vive dentro de `posts-api`. Las dos están de facto
cerradas desde la revisión del equipo del 2026-08-20 y ninguna aparece marcada como abierta,
pero a diferencia de A17-A21 nunca pasaron por el circuito ADR: quedaron como filas de una tabla
de "pendientes de definir en S1", sin un documento propio que registre el porqué.

`T-02` pide definir límites, responsables y contratos de cada servicio. Esta decisión ya estaba
tomada en los hechos; lo que faltaba era consolidarla en un solo lugar, junto con qué expone
cada servicio hacia los demás y de qué depende en infraestructura, que hoy está disperso entre
`ARQUITECTURA.md` y ADR-002.

> A diferencia de ADR-001 a ADR-004, que registran una decisión puntual tomada en un momento
> dado, este ADR consolida decisiones que ya estaban tomadas pero dispersas entre varias
> secciones de `ARQUITECTURA.md`. Por eso incluye una sección "Fuera de alcance" que los otros
> cuatro no necesitaron: al reunir varios temas relacionados en un solo documento, hace falta
> decir explícitamente cuáles quedan afuera para que nadie asuma que este ADR los cierra.

## Decisión

### Tres servicios y sus límites

El sistema se divide en tres servicios backend:

- **`users-api`**: identidad, autenticación, perfiles, administradores y avatares.
- **`posts-api`**: contenido, grafo social, feed cronológico, búsqueda e imágenes de post.
- **`notifications-api`**: notificaciones push, historial in-app, emails y triage de denuncias
  con IA.

Identidad va junto con perfil, y grafo social va junto con contenido y feed. Separar el grafo
social de `posts-api` en un servicio aparte convertiría cada publicación en una transacción
distribuida: crear un post ya requiere validar al autor, actualizar contadores y proyectar el
feed de los seguidores, y hoy eso es una única transacción de base de datos. Partirlo exige
sagas o consistencia eventual para una operación que el usuario espera ver reflejada al
instante. La misma lógica aplica a identidad y perfil: separarlos duplicaría la tabla de
usuario entre dos servicios para ganar poco, porque casi todo lo que toca perfil necesita
primero resolver identidad.

No hay un cuarto servicio para media. La subida de archivos se resuelve dentro del servicio
dueño del dato (`users-api` para avatares, `posts-api` para imágenes de post), con el módulo de
streaming escrito una vez y copiado entre ambos — ver "Subida de archivos: módulo copiado, no
servicio" en `ARQUITECTURA.md`.

### Contratos entre servicios

**HTTP (síncrono).** Cada servicio expone su propia API versionada en el path (`/v1/...`), con
errores en formato Problem Details (RFC 9457) y un `/healthcheck` sin versionar. El detalle
completo de formato de error y versionado está en "Comunicación entre servicios" de
`ARQUITECTURA.md` y no se repite acá.

Los clientes REST no se escriben a mano: los tres servicios exponen OpenAPI y cada repo cliente
genera tipos, cliente y hooks contra ese esquema con Orval, commiteando lo generado. Un cambio
de contrato aparece como diff en el PR, sin necesidad de publicar nada — ver
`ARQUITECTURA.md`, sección "Aplicaciones cliente".

La única llamada síncrona entre servicios backend es `posts-api` → `users-api`, para hidratar
datos de autor. El resto de la comunicación entre servicios cruza por la cola.

**Eventos (asíncrono).** Los contratos de eventos se copian entre repositorios, no se
empaquetan — decisión ya registrada en [ADR-002](./ADR-002-contratos-de-eventos-copiados.md), que
no se repite acá. Lo que corresponde a este ADR es qué publica y consume cada servicio:

| Evento                     | Publica | Consume                               |
| --------------------------- | ------- | -------------------------------------- |
| `user.registered`          | users   | notifications (email de verificación) |
| `user.deleted`              | users   | posts, notifications                  |
| `user.profile_updated`     | users   | posts                                 |
| `password.reset_requested` | users   | notifications                         |
| `password.changed`         | users   | notifications                         |
| `feedback.submitted`       | users   | notifications                         |
| `post.created`              | posts   | notifications (menciones)             |
| `follow.created`             | posts   | notifications                         |
| `interaction.created`      | posts   | notifications                         |
| `report.created`            | posts   | notifications, triage de IA           |

`posts-api` publica y también consume: reacciona a `user.deleted` y `user.profile_updated` para
mantener consistente el autor denormalizado en cada post. `notifications-api` no publica
eventos propios, solo consume.

### Dependencias de infraestructura por servicio

| Servicio             | Base de datos          | Caché / clave-valor                                                                              | Almacenamiento | Cola                          |
| --------------------- | ----------------------- | -------------------------------------------------------------------------------------------------- | -------------- | ------------------------------ |
| `users-api`           | PostgreSQL (relacional) | Redis — revocación de JWT, rate limiting                                                            | S3 (`avatars/`) | Publica en RabbitMQ           |
| `posts-api`           | PostgreSQL (relacional) | Redis — rate limiting, caché de trending                                                            | S3 (`posts/`)   | Publica y consume en RabbitMQ |
| `notifications-api`   | MongoDB (documental)   | No usa                                                                                               | No usa         | Consume de RabbitMQ           |

Redis corre **dentro del cluster**, no como servicio gestionado aparte — posición actualizada
tras la revocación de A20, commit `f2282ae`. Sus datos son efímeros (TTL en revocación de JWT,
contadores de rate limit, caché de trending) y perderlos ante un reinicio no rompe nada, así que
no justifica pagar un servicio gestionado. PostgreSQL y MongoDB sí corren fuera del cluster, como
servicios gestionados, según A12.

### Responsables

Ningún servicio tiene un dueño fijo. No es una omisión de este ADR: es una decisión de proceso
que el equipo ya tomó, registrada en el commit `a41dcdf` — *"los cuatro integrantes del reparto
nunca se acordaron"*. Este ADR documenta esa regla existente, no decide una nueva.

La responsabilidad se asigna por historia, no por servicio: cada issue lleva su propio
"Responsable primario" y "Revisor" en la metadata, y tenerlos asignados es requisito de
Definition of Ready (`PLANIFICACION.md`). A eso se suma el rol de **Revisor primario**, que
rota semanalmente entre los cuatro integrantes y es quien aprueba todos los PR de la semana,
sea cual sea el servicio que tocan (`PLANIFICACION.md`, sección "Roles rotativos semanales").

## Fuera de alcance

Dos decisiones abiertas tocan estos mismos servicios y **no se resuelven acá**:

- **A22 — Manejo de tokens.** JWT con lista de revocación en Redis vs. token opaco con sesión en
  Redis. Sigue abierta, el equipo la decide antes de S3.
- **A23 — Subida de media.** Stream por el servicio vs. URL prefirmada de S3 con validación
  posterior. Sigue abierta, se decide en S6.

Este ADR fija los límites entre servicios y sus contratos; no fija cómo cada servicio maneja
sesiones ni cómo sube archivos. Cuando A22 y A23 se cierren, se registran como ADR propios.

## Consecuencias

- A4b y A7 dejan de vivir solo como filas de una tabla de pendientes: quedan como decisión
  registrada y justificada, consultable sin reconstruir el argumento de memoria.
- Cambiar los límites de un servicio (por ejemplo, separar el grafo social de `posts-api`) pasa
  a requerir un ADR que reemplace a este, no un edit silencioso de `ARQUITECTURA.md`.
- La tabla de eventos y la de dependencias de infraestructura quedan en dos lugares
  (`ARQUITECTURA.md` para el detalle operativo, este ADR para la decisión de fondo). Si diverge
  una de la otra, es una señal de que alguna quedó desactualizada.
- A22 y A23 quedan explícitamente pendientes: alguien que lea este ADR sabe que faltan sin tener
  que cruzarlo contra `PLANIFICACION.md`.
