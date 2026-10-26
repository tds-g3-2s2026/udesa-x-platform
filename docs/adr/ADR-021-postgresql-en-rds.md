# ADR-021: PostgreSQL en RDS, una base y un rol por servicio

**Fecha:** 2026-10-26 · **Estado:** aceptada · **Decide:** el equipo

**Reemplaza la parte de PostgreSQL del ADR-009** (Neon, un proyecto por servicio). El resto del
ADR-009 sigue vigente: Redis dentro del cluster y migraciones obligatorias con Alembic. Sale del
incidente [`udesa-x-platform#111`](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/111).

## Contexto

Desde el 17 de octubre, aproximadamente, `users-api` y `posts-api` no pasan el readiness probe:
`/healthcheck` devuelve 503 y los dos servicios quedan fuera del tráfico. El chequeo prueba
PostgreSQL y Redis, y el pod de Redis está sano: la que no responde es la base.

La causa probable, no verificada en la consola de Neon, es la capa gratuita: 100 CU-hours por mes
y por proyecto, y la suspensión solo llega tras 5 minutos sin consultas. El readiness probe hace
un `SELECT 1` cada 5 a 10 segundos, así que la base nunca se suspende y la cuota se consume las 24
horas. Desde el 20 de septiembre, eso se agota cerca del 17 de octubre.

La razón por la que el ADR-009 descartó RDS era que no había credenciales de AWS. Ahora la cátedra
provee una instancia: `tds-group-3-db`, en `us-east-2`, PostgreSQL 18.3, sin acceso público, con un
security group que acepta el 5432 solo desde los pods del cluster.

El equipo tiene acceso de solo lectura al cluster (ADR-008): nadie puede abrir un `psql` contra la
instancia, ni desde afuera ni desde un pod a mano. El único que crea Jobs y Secrets en
`tds-group-3` es el rol de CI.

## Decisión

### Una instancia, una base y un rol por servicio

| Base | Rol | Servicio | Secreto |
|---|---|---|---|
| `users` | `users` | `users-api` | `DATABASE_URL` en `udesa-x-users-api` |
| `posts` | `posts` | `posts-api` | `DATABASE_URL` en `udesa-x-posts-api` |

Cada base es propiedad del rol de su servicio y tiene `CONNECT` revocado a `PUBLIC`: `posts` no
puede entrar a `users` ni al revés. El aislamiento que el ADR-009 buscaba con dos proyectos se
sostiene con permisos de la base, no con que nadie se equivoque de nombre en una connection
string (ADR-005). El usuario administrador de la instancia no lo usa ninguna aplicación.

### Las bases se crean con un workflow, no a mano

`.github/workflows/crear-bases-postgres.yml` es manual e idempotente. Corre `psql` como Job dentro
del namespace con el rol de CI, crea los roles y las bases si no existen, fija las claves y
verifica que cada rol entra a su base y no a la otra. La clave del administrador viaja en un
Secret temporal que el workflow borra al terminar.

Rotar una clave es: cambiar el secret del repositorio de plataforma (`USERS_DB_PASSWORD` o
`POSTS_DB_PASSWORD`) y el `DATABASE_URL` del servicio, correr el workflow y redesplegar el
servicio.

### TLS: `ssl=require`, no `verify-full`

El certificado de la instancia lo firma la CA de Amazon RDS (`rds-ca-rsa2048-g1`), que no está en
el bundle del sistema al que apunta `PGSSLROOTCERT`. Con `verify-full`, asyncpg no puede validar y
no conecta. La URL queda:

```
postgresql+asyncpg://<rol>:<clave>@tds-group-3-db.cze2woweg3po.us-east-2.rds.amazonaws.com:5432/<base>?ssl=require
```

`require` cifra pero no verifica contra quién se conecta. El riesgo es un intermediario dentro de
la VPC, acotado porque la instancia es privada y solo la alcanzan los pods. Volver a
`verify-full` es sumar el bundle de RDS a la imagen de cada servicio y apuntar `PGSSLROOTCERT` a
ese archivo.

### Se arranca con las bases vacías

Los datos de Neon no se migran. El primer deploy corre `alembic upgrade head`, que crea el
esquema, y en `users-api` el seed del superadmin. Los proyectos de Neon quedan como estaban; no se
borran.

## Consecuencias

- Neon deja de usarse en producción. El CI no cambia: levanta su propio PostgreSQL en el runner.
- Sin cuota de horas de cómputo, el readiness probe ya no puede dejar a los servicios sin base.
- Los usuarios y publicaciones cargados hasta el 17 de octubre no están en producción. Para
  demos se recargan con `scripts/seed`.
- Mientras corre, el workflow ocupa el último Secret libre de la cuota del namespace (4). Si
  otro objeto lo ocupa, el workflow falla al crear el Secret, antes de tocar la base.
- La clave del administrador de la instancia se compartió fuera de GitHub durante el incidente:
  hay que rotarla en la consola de RDS y actualizar `RDS_ADMIN_PASSWORD`.
