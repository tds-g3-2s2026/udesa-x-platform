# ADR-009: Bases gestionadas en Neon, un Redis en el cluster y migraciones obligatorias

**Fecha:** 2026-09-20 · **Estado:** aceptada · **Decide:** el equipo

Cierra la parte de decisión de la issue [`udesa-x-platform#46`](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/46).
**Actualiza `A12`** del registro de `ARQUITECTURA.md` y la fila de PostgreSQL de la tabla de
"Vista general". **Reemplaza la política de crear las tablas desde los modelos** que fijó la
revisión del tutor del 8 de septiembre.

## Contexto

La cátedra pidió, para la clase del 21 de septiembre, tener las bases creadas, y nombró RDS,
Railway, Atlas, Supabase y Render. Hoy PostgreSQL y Redis existen solo en el `docker compose`
de cada repositorio: sirven para desarrollo y para el CI, y no son alcanzables desde
`tds-cluster`. Sin bases accesibles, los `Deployment` arrancan y se caen.

Cuatro restricciones salen del repositorio y no del catálogo de proveedores:

- **PostgreSQL 18.** `A19` fija `uuidv7()` nativo como PK de `posts`, y los dos `compose` usan
  `postgres:18-alpine`. Un proveedor que tope en 17 obliga a revisar la clave primaria.
- **La base tiene que durar hasta el 14 de diciembre**, el cierre de S15. No hasta la entrega
  intermedia del 28 de septiembre.
- **La cuota del namespace es de 8 pods**, con `maxSurge: 1` por Deployment y Jobs de migración
  que también consumen cuota.
- **Cada servicio es dueño de sus datos** y ningún servicio consulta la base de otro
  (`ADR-005`). No es una base compartida con dos esquemas.

No hay credenciales de AWS todavía: se sigue en la issue
[`#47`](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/47). RDS es la opción natural
para EKS y no se puede provisionar.

Lo que ya está resuelto y no hay que tocar: `secret.template.yaml` de cada servicio declara
`DATABASE_URL` y `REDIS_URL`, y `k8s/secret.yaml` está en `.gitignore`. Apuntar los servicios a
una base externa no es un cambio de código, es el valor de dos secretos.

## Decisión

### PostgreSQL: Neon, un proyecto por servicio

| Proveedor | Por qué queda o cae |
|---|---|
| **Neon** | **Elegido.** Sin tarjeta, 100 proyectos, 0.5 GB y 100 CU-hours por proyecto, TLS obligatorio. Postgres 18 disponible desde mayo de 2026 y por defecto desde junio. Suspende a los 5 minutos de inactividad y reanuda en ~500 ms, que no es lo mismo que pausar un proyecto |
| Render | Cae. Las bases del plan gratuito **expiran a los 30 días**, con 14 de gracia. Creada el 20 de septiembre, muere antes del 26 de octubre |
| Railway | Cae. No tiene capa gratuita permanente: 5 USD de crédito por 30 días y después 1 USD por mes. Es un servicio pago con un descuento inicial |
| Supabase | Cae. Es gratis y sin tarjeta, pero **pausa los proyectos con 7 días de baja actividad** y el plan libre admite un proyecto activo por organización: dos bases serían dos organizaciones, y una base pausada la mañana de una demo se restaura a mano |
| Atlas | No aplica. Es MongoDB, y sigue siendo la elección de `notifications-api` con M0. No resuelve PostgreSQL |
| RDS | No aplica hoy. Sin credenciales de AWS no hay nada que provisionar |

**Dos proyectos, no dos bases dentro de uno.** Cada uno tiene su URL, su rol y su cuota, así
que el aislamiento no depende de que nadie escriba el nombre de base equivocado en una
connection string. Esto reemplaza la fila "una instancia con dos bases" de la vista general,
que describía RDS.

| Proyecto | ID | Servicio | Secreto |
|---|---|---|---|
| `users-api` | `mute-hat-57607938` | `users-api` | `DATABASE_URL` en `udesa-x-users-api` |
| `posts-api` | `floral-haze-34260608` | `posts-api` | `DATABASE_URL` en `udesa-x-posts-api` |

Región `aws-us-east-2`, la del cluster: `posts-api` hidrata autores contra `users-api` de forma
sincrónica y cada salto entre regiones se paga en cada request.

**La URL que entrega Neon no se copia tal cual.** Viene con `?sslmode=require&channel_binding=require`,
y SQLAlchemy 2.0.52 pasa los parámetros de query como kwargs a `asyncpg.connect`, que no tiene
ninguno de los dos: la conexión falla con `TypeError` antes de abrirse. La URL que va al secreto
es `postgresql+asyncpg://<rol>:<clave>@<host>/<base>?ssl=verify-full`, que es lo que ya pedía el
README de esta plataforma: validación de CA y hostname, no `require`, que cifra sin verificar
contra quién.

**`verify-full` necesita además `PGSSLROOTCERT`.** asyncpg no usa el almacén de certificados
del sistema: con `verify-full` y sin `sslrootcert` busca `~/.postgresql/root.crt`, y si no está
corta con `ClientConfigurationError` antes de abrir el socket. En el contenedor ese archivo no
existe. La solución es una variable en el ConfigMap de cada servicio, no un certificado
versionado ni un volumen: `PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt`, que es el bundle
que ya trae `python:3.13-slim` y que incluye la CA pública que firma el certificado de Neon.
Verificado contra las dos bases reales: `select version()` devuelve PostgreSQL 18.6 y
`select uuidv7()` responde.

**Endpoint directo, no el `-pooler`.** El pooler es PgBouncer en modo transacción y asyncpg
cachea 100 prepared statements por conexión: es la combinación que rompe de forma intermitente.
Con una réplica por servicio y `pool_pre_ping=True`, que ya está en los dos `main.py`, el pool
de SQLAlchemy alcanza.

### Redis: uno solo, dentro del cluster, con bases lógicas separadas

Confirma `A12` y el "Redis compartido" del diagrama de contenedores. No se contrata nada.

**Por qué no gestionado.** El free de Upstash es una base por cuenta y sin `SELECT`: dos
servicios serían dos cuentas a nombre de dos personas distintas, o una base compartida separada
solo por prefijo de clave. Las dos son peores que un pod.

**Por qué uno y no dos.** El escenario completo ya son cinco pods de aplicación (`users-api`,
`posts-api`, `api-gateway`, `notifications-api`, RabbitMQ) sobre una cuota de ocho, con el pod
extra del `maxSurge` y los Jobs de migración compitiendo por el mismo margen. Un segundo Redis
compra aislamiento que los datos no necesitan y gasta el margen que el rollout sí necesita.

**La separación es por base lógica**, que es lo que `Redis.from_url` lee del path:

| Servicio | `REDIS_URL` |
|---|---|
| `users-api` | `redis://redis:6379/0` |
| `posts-api` | `redis://redis:6379/1` |

Sin TLS: es tráfico dentro del namespace, no sale del cluster. Sin PVC y sin persistencia
(`--save ""`, `--appendonly no`): lo que guarda son revocaciones de JWT, contadores de rate
limit y caché, todo con TTL.

**El manifiesto compartido vive en `udesa-x-platform/k8s/redis.yaml`** y lo aplica el CD de
platform, que es parte de `T-14`. No puede aplicarlo una persona: el permiso del equipo sobre el
cluster es de solo lectura (`ADR-008`). Ponerlo en el repositorio de un servicio haría que
`posts-api` dependa del pipeline de `users-api` para arrancar.

**Consecuencia que hay que saber decir en la defensa:** si el pod de Redis se reinicia, se
pierden la denylist de JWT y los contadores de rate limit. Un token revocado vuelve a ser válido
hasta su expiración natural, y los contadores arrancan de cero. Es el precio de que sea efímero,
ya estaba implícito en `A12`, y es aceptable con tokens de vida corta.

### Migraciones: desde el primer deploy, Alembic es el único camino

La regla anterior era crear las tablas desde los modelos con `Base.metadata.create_all()`
mientras no hubiera base desplegada. **Esa regla se termina acá**, y el código ya se adelantó:
los dos servicios tienen Alembic, `posts-api` lo incorporó con `alembic.ini` y
`migrations/versions/0001_esquema_actual.py`, y los dos `conftest.py` levantan el esquema con
`alembic upgrade head` en vez de `create_all`. No queda una sola llamada a `create_all` en
`src/` ni en `tests/`.

Lo que cambia con una base real:

- **La `0001` de cada servicio queda congelada con el primer deploy.** De ahí en más, todo
  cambio de modelo es una revisión nueva con `alembic revision --autogenerate`. Editar la
  `0001` o correr `alembic stamp` contra una base con datos queda prohibido.
- El Job de migración corre antes del rollout, toma `pg_advisory_lock`, los cambios van en
  expand y contract, y el rollback es forward-only. Ya estaba en `ARQUITECTURA.md`, ahora aplica
  de verdad.
- **El corte es el deploy, no la creación de la base ni el primer `upgrade head` contra ella.**
  La diferencia no es teórica: el 20 de septiembre la `0001` de `posts-api` se aplicó contra
  Neon y ese mismo día `main` sumó tres índices de cursor que esa revisión no tenía. Con las dos
  bases vacías y ningún servicio desplegado, lo correcto fue completar la `0001` y volver a
  aplicarla sobre el esquema borrado, no arrastrar un `0002` que solo existía por el desfasaje
  de unas horas. Mientras no haya datos ni pods corriendo, recrear la base desde cero es gratis
  y es la opción más limpia.
- **Lo que sí es permanente desde hoy:** cualquier cambio de modelo tiene que llegar con su
  migración en el mismo PR. `alembic check` lo detecta, y el CI ya lo prueba porque los tests de
  integración levantan el esquema con `alembic upgrade head` y no con `create_all`.

### Secretos

Cada URL va como GitHub Secret del repositorio que la usa, nunca en un archivo del repositorio.
`DATABASE_URL` y `REDIS_URL` en `udesa-x-users-api` y en `udesa-x-posts-api`. Es el mismo
mecanismo que fijó el `ADR-008`: plantilla versionada sin valores, valores inyectados por el
pipeline.

## Consecuencias

| Qué | Qué pasa |
|---|---|
| `A12` | Se mantiene, con el proveedor concreto: las persistentes fuera, ahora en Neon; Redis adentro |
| Fila "RDS, una instancia con dos bases" de la vista general | Se reemplaza por dos proyectos de Neon |
| "Las tablas se crean desde los modelos" | Se termina. Alembic en los dos servicios, siempre |
| `posts-api` arranca sin Alembic | Desactualizado: ya lo tiene |
| `T-14` (CD) | Suma el apply de `k8s/redis.yaml` desde el repositorio de platform |

**Volver a RDS cuando lleguen las credenciales cuesta un `pg_dump` y dos secretos, y no se hace
salvo que la cátedra lo exija.** La base gestionada no es lo que se evalúa, y mudarla la semana
de una entrega es riesgo sin premio.

**El free de Neon no da garantías de recuperación que el equipo pueda asumir.** No hay datos de
valor: el superadmin se recrea con `seed_superadmin` y el resto es contenido de demo. Si eso
deja de ser cierto, hay que volver sobre esta decisión.

**Riesgo abierto: la salida a internet del namespace.** Si `tds-group-3` no puede abrir
conexiones salientes al puerto 5432, ninguna de estas URLs sirve y hay que pedírselo al docente.
Se verifica en el primer deploy, no antes: nadie del equipo puede correr un pod de prueba a mano.
