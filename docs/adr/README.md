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
| [ADR-009](./ADR-009-bases-gestionadas-y-migraciones.md) | Bases gestionadas en Neon, un Redis en el cluster y migraciones obligatorias | 2026-09-20 | Aceptada |
| [ADR-010](./ADR-010-proveedor-de-correo.md) | Proveedor de correo: Resend con dominio propio | 2026-09-23 | Aceptada |
| [ADR-011](./ADR-011-denuncias-y-cuenta-en-revision.md) | Denuncias en `posts-api` y aviso de cuenta en revisión a `users-api` | 2026-09-28 | Aceptada |
| [ADR-012](./ADR-012-monitoreo-de-servicios-y-alerta-de-caida.md) | Monitoreo de los servicios y alerta de caída con Grafana Cloud | 2026-10-01 | Propuesta |

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
