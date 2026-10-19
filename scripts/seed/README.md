# Datos para pruebas de carga

Requiere Python 3.13, `uv` y las migraciones de users-api y posts-api aplicadas a
`head`. Puede ejecutarse contra bases con datos existentes: inserta sus filas
faltantes sin borrar ni sobrescribir usuarios, administradores o contenido.

Definir `SEED_USERS_DATABASE_URL` y `SEED_POSTS_DATABASE_URL` con conexiones directas
`postgresql://usuario:clave@host:puerto/base`, sin el prefijo `postgresql+asyncpg://`.
Para TLS, usar `sslmode=verify-full` y `PGSSLROOTCERT`. El rol necesita permisos de
inserción, actualización de contadores y creación de tablas temporales.

Por defecto se carga el 1% del volumen objetivo. Desde la raíz de platform:

```bash
uv run scripts/seed/seed.py \
  --seed 42 --batch-size 5000 \
  --users 100 --follows 5000 --posts 2000 --replies 2000 --likes 7000 \
  --retweets 1000 --deleted-posts 100
```

Para el volumen completo, pasar `--users 10000 --follows 500000 --posts 200000
--replies 200000 --likes 700000 --retweets 100000 --deleted-posts 10000`.

Los volúmenes son independientes. `--posts` cuenta originales: 2.000 originales
más 2.000 respuestas producen 4.000 filas en `posts`. Likes, respuestas y retweets
suman 10.000 interacciones. Los 100 eliminados son parte de los originales, dejando
1.900 activos. El borrado no agrega filas ni interacciones. Notificaciones queda
fuera. Se rechazan cantidades negativas y relaciones imposibles.

## Repetir la carga en un ambiente desplegado

Con las mismas versiones, semilla y volúmenes se generan las mismas claves.
Repetir el comando inserta solamente las que faltan. Los emails y handles también
dependen de la semilla, permitiendo que convivan distintas cargas y cuentas reales.
Una colisión de email o handle con otra cuenta aborta la transacción; no adopta
esa cuenta ni cambia sus credenciales. No hay tablas permanentes nuevas.

La carga usa tablas temporales y `ON CONFLICT` sobre la clave primaria para omitir
filas existentes. Los contadores se incrementan solo por relaciones efectivamente
insertadas, conservando los aportes de usuarios reales. Las ejecuciones del seed
se serializan y las publicaciones se bloquean durante la carga para coordinarse
con su borrado. Las APIs pueden permanecer levantadas, aunque una operación sobre
esas publicaciones puede esperar a que termine la transacción.

No se resetean contraseñas, perfiles ni contenido modificado, ni se revierten
borrados. Las reacciones no se reinsertan sobre publicaciones eliminadas. Una
relación faltante sobre una publicación activa puede volver a insertarse al
repetir el seed. Los originales eliminados conservan texto y respuestas previas,
sin likes ni retweets. Su borrado se fecha al día 15 y las respuestas dentro de
los primeros 7 días. Los pares de seguimiento y reacción son únicos y se favorece
interactuar con cuentas seguidas.

Las cuentas nuevas son públicas, activas y verificadas. Comparten la contraseña
`CampusSeed42!`; con `--seed 42`, el primer email es
`seed.42.0000000000@example.com`. Las cuentas existentes conservan sus atributos.

Cambiar volúmenes no elimina sobrantes ni redimensiona una carga existente; puede
agregar filas. Para repetir una carga, conservar su semilla y volúmenes; para
crear otro conjunto independiente, elegir otra semilla.

## Reporte y recuperación

La salida JSON distingue `counts` (filas de la carga solicitada), `inserted`
(filas nuevas de esta ejecución) y `totals` (filas totales, incluidas las ajenas).
Una repetición sin cambios muestra ceros en `inserted`. Si la aplicación modificó
los datos del seed, los conteos reales pueden diferir de los volúmenes solicitados.
El hash SHA-256 toma hasta 100 filas reales por tabla, limitadas a las claves de la
carga y ordenadas por clave; también refleja modificaciones sobre esos datos.

Los IDs, fechas y contenido generados son independientes del tamaño del lote.
Las fechas parten del 1 de enero de 2026 y los posts usan UUIDv7 deterministas.
El hash de muestra no sustituye una comparación exhaustiva. Al terminar se
ejecuta `ANALYZE` para actualizar las estadísticas del planificador.

Cada base usa una transacción y sus commits son independientes. Si una queda
confirmada y la otra falla, repetir el mismo comando completa lo que falta sin
duplicar las filas confirmadas ni volver a incrementar sus contadores. Un fallo
en `ANALYZE` también puede ocurrir después de confirmar los datos.

## Tests: solo en bases descartables

```bash
uv run --python 3.13 --with asyncpg==0.30.0 --with argon2-cffi==25.1.0 \
  python -m unittest discover -s scripts/seed -v
```

Para incluir PostgreSQL, definir `TEST_SEED_USERS_DATABASE_URL` y
`TEST_SEED_POSTS_DATABASE_URL` con bases locales descartables migradas a `head`.
**Los tests vacían esas bases con `TRUNCATE ... CASCADE`: no apuntarlos al ambiente
desplegado.** Sin esas variables se omiten los tests de base. La suite verifica
reproducibilidad, relaciones, contadores, convivencia, reintentos, concurrencia,
preservación de modificaciones y recuperación de cargas parciales.
