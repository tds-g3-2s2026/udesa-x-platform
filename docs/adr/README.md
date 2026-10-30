# Registro de decisiones de arquitectura

Una decisión por archivo, numerada y con fecha. No se editan: si una decisión cambia, se
escribe una nueva que reemplaza a la anterior y se anota acá.

| ADR | Decisión | Fecha | Estado |
|---|---|---|---|
| [ADR-001](./ADR-001-un-repositorio-por-servicio.md) | Un repositorio por servicio | 2026-08-19 | Aceptada |
| [ADR-002](./ADR-002-contratos-de-eventos-copiados.md) | Contratos de eventos copiados entre repositorios | 2026-08-19 | Aceptada |
| [ADR-003](./ADR-003-repositorios-publicos.md) | Repositorios públicos | 2026-08-21 | Aceptada |
| [ADR-004](./ADR-004-alta-automatica-de-issues.md) | Alta automática de issues en el Project | 2026-08-21 | Aceptada |
| [ADR-005](./ADR-005-limites-de-servicios.md) | Límites de servicios, contratos y dependencias de infraestructura | 2026-08-30 | Aceptada |
| [ADR-006](./ADR-006-inversion-de-dependencias.md) | Inversión de dependencias en los servicios backend | 2026-09-03 | Reemplazada por ADR-007 |
| [ADR-007](./ADR-007-estructura-por-capas.md) | Estructura por capas en los servicios backend | 2026-09-04 | Aceptada |
| [ADR-008](./ADR-008-plataforma-de-despliegue.md) | Plataforma de despliegue sobre el cluster de la cátedra | 2026-09-14 | Aceptada |
| [ADR-009](./ADR-009-bases-gestionadas-y-migraciones.md) | Bases gestionadas en Neon, un Redis en el cluster y migraciones obligatorias | 2026-09-20 | Aceptada, PostgreSQL reemplazado por ADR-021 |
| [ADR-010](./ADR-010-proveedor-de-correo.md) | Proveedor de correo: Resend con dominio propio | 2026-09-23 | Aceptada |
| [ADR-011](./ADR-011-denuncias-y-cuenta-en-revision.md) | Denuncias en `posts-api` y aviso de cuenta en revisión a `users-api` | 2026-09-28 | Aceptada, ajustada por ADR-020 |
| [ADR-012](./ADR-012-monitoreo-de-servicios-y-alerta-de-caida.md) | Monitoreo de los servicios y alerta de caída con Grafana Cloud | 2026-10-01 | Aceptada |
| [ADR-013](./ADR-013-trazas-y-logs-con-opentelemetry.md) | Trazas y logs con OpenTelemetry, enviados directo a Grafana Cloud | 2026-10-01 | Aceptada |
| [ADR-014](./ADR-014-revocacion-de-sesiones-en-posts-api.md) | `posts-api` lee las revocaciones de sesión desde el Redis de `users-api` | 2026-10-03 | Aceptada |
| [ADR-015](./ADR-015-notifications-api-en-bun-y-hono.md) | `notifications-api` en Bun y Hono, igual que el gateway | 2026-10-14 | Aceptada |
| [ADR-016](./ADR-016-modelos-abiertos-para-la-ia.md) | Modelos abiertos dentro del cluster para la funcionalidad de IA | 2026-10-17 | Propuesta, no se aceptó. Reemplazada por ADR-023 |
| [ADR-017](./ADR-017-forma-y-versionado-de-eventos.md) | Forma, versionado y verificación de los contratos de eventos | 2026-10-23 | Aceptada |
| [ADR-018](./ADR-018-librerias-para-imagenes-en-publicaciones.md) | Librerías para imágenes en publicaciones: selector y visor en `mobile`, S3 y multipart en `posts-api` | 2026-10-23 | Aceptada |
| [ADR-019](./ADR-019-aio-pika-para-eventos-en-python.md) | `aio-pika` para publicar y consumir eventos en los servicios de Python | 2026-10-24 | Aceptada |
| [ADR-020](./ADR-020-cierre-de-casos-de-denuncias.md) | Cierre de casos de denuncias: el umbral cuenta lo pendiente y la revisión se levanta | 2026-10-25 | Aceptada |
| [ADR-021](./ADR-021-postgresql-en-rds.md) | PostgreSQL en RDS, una base y un rol por servicio | 2026-10-26 | Aceptada |
| [ADR-023](./ADR-023-bedrock-para-el-asistente-por-voz.md) | Amazon Bedrock para el asistente por voz, con el modelo más barato que pase la evaluación | 2026-10-30 | Aceptada |

Solo se registran decisiones ya tomadas y que el equipo pueda justificar, numeradas en el
orden en que se toman. Lo que todavía está por definirse vive como decisión abierta `Dxx` en
`PLANIFICACION.md`, con fecha límite, y pasa a ADR recién cuando se resuelve.

La plataforma de despliegue quedó registrada en el ADR-008, con la clase de Cloud Computing I
cursada. Cerró `D21` y reemplazó las decisiones `A17` y `A18` del registro de
`ARQUITECTURA.md`.

El proveedor de bases quedó registrado en el ADR-009, antes de crear nada. Actualiza `A12` del
registro de `ARQUITECTURA.md` y termina con la política de crear las tablas desde los modelos.

El proveedor de correo quedó registrado en el ADR-010. Cierra `A14` del registro de
`ARQUITECTURA.md` y el riesgo `R3` de `PLANIFICACION.md`.

Las denuncias y el paso a revisión quedaron registrados en el ADR-011. Cierra `D1` de
`PLANIFICACION.md` y suma una llamada síncrona a "Comunicación entre servicios" de
`ARQUITECTURA.md`.

El monitoreo de los servicios quedó registrado en el ADR-012. Cubre `E5-H11 CA.4` y el
dashboard de healthchecks de `T-21`.

Las trazas y los logs quedaron registrados en el ADR-013. Precisa `A13` de `ARQUITECTURA.md`:
cómo llegan los datos a Grafana Cloud y qué identifica a un request.

La revocación de sesiones en `posts-api` quedó registrada en el ADR-014. Cierra el hueco de
`udesa-x-posts-api#58` y deja una excepción de solo lectura a la separación por base lógica del
ADR-009.

El stack de `notifications-api` quedó registrado en el ADR-015. Actualiza `A5` y `A25` de
`ARQUITECTURA.md`: Bun y Hono en vez de Node y NestJS, y `ci-node.yml` como CI, sin un workflow
propio.

La forma y el versionado de los eventos quedaron registrados en el ADR-017. Cierra `D22` de
`PLANIFICACION.md` y completa el ADR-002 con el sobre de CloudEvents, la versión en el `type`,
la copia por servicio y los checks de `T-16`.

Las librerías de imágenes quedaron registradas en el ADR-018. Cubre `E2-H7` y la regla de los
`AGENTS.md` que pide un ADR antes de sumar una librería: selector y visor en `mobile`, cliente de
S3 y lector multipart en `posts-api`.

El cliente de RabbitMQ para los servicios de Python quedó registrado en el ADR-019. Complementa
al ADR-015 (`amqplib` en Bun) y cubre la regla de los `AGENTS.md` que pide un ADR antes de sumar
una librería: `aio-pika` publica la `outbox` en `users-api` y consume `user.deleted.v1` en
`posts-api`.

La base de PostgreSQL de producción quedó registrada en el ADR-021. Reemplaza la parte de
PostgreSQL del ADR-009 (Neon pasa a RDS, una base y un rol por servicio) y deja vigentes Redis en
el cluster y las migraciones obligatorias. Actualiza `A12` y `A19` de `ARQUITECTURA.md`.

El proveedor y el modelo de la funcionalidad de IA quedaron registrados en el ADR-023.
Reemplaza al ADR-016, que no se aceptó, cierra `AI-02` y reescribe la sección "Integración
de Inteligencia Artificial" de `ARQUITECTURA.md`. La estimación de costos que lo justifica
está en `docs/ESTIMACION-COSTOS-IA.md`.
