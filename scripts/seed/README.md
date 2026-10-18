# Datos para pruebas de carga

Requiere Python 3.13, `uv` y dos bases descartables con las migraciones de users-api
y posts-api aplicadas a `head`. Detener las APIs durante la carga. El seed escribe
directamente en PostgreSQL, rechaza tablas de destino ocupadas y nunca borra datos.

Definir `SEED_USERS_DATABASE_URL` y `SEED_POSTS_DATABASE_URL` con conexiones directas
`postgresql://usuario:clave@host:puerto/base`, sin el prefijo `postgresql+asyncpg://`.
Para TLS, usar `sslmode=verify-full` y `PGSSLROOTCERT`.

Desde la raíz de platform, esta corrida muestra todos los valores predeterminados:

```bash
uv run scripts/seed/seed.py \
  --seed 42 --batch-size 5000 \
  --users 10000 --follows 500000 --posts 200000 --replies 200000 --likes 700000
```

Los volúmenes son independientes. `--posts` cuenta originales: 200.000 originales
más 200.000 respuestas producen 400.000 filas en `posts`. Las interacciones suman
likes y respuestas: 900.000 por defecto. Retweets, borrado lógico y notificaciones
quedan fuera. Se rechazan cantidades negativas y relaciones imposibles; cero es
válido si no deja entidades sin sus referencias.

Las cuentas son públicas, activas, verificadas y con términos aceptados. Comparten
la contraseña de prueba `CampusSeed42!`; el primer email es
`seed0000000000@example.com` y su handle, `@seed0000000000`.

Los perfiles comparten ID con sus cuentas. Los seguimientos son únicos y excluyen
autofollows. Si alcanzan las cantidades, cada usuario sigue a alguien, tiene un
seguidor y publica un original. El resto concentra actividad en algunas cuentas.
Las respuestas apuntan a originales y conservan su tema; los likes pueden apuntar
a originales o respuestas, sin duplicar pares usuario/publicación. Se favorecen
interacciones con cuentas seguidas. Las fechas respetan el orden de los eventos
y los contadores se calculan desde las relaciones guardadas.

## Reproducibilidad y recuperación

Con la misma versión del generador y sus dependencias, la semilla reproduce IDs,
fechas, contenido y relaciones independientemente del tamaño del lote. Las fechas
parten del 1 de enero de 2026; los posts usan UUIDv7 deterministas. La salida JSON
informa los conteos reales y un SHA-256 de hasta 100 filas por tabla, ordenadas por
clave. Para comparar corridas, usar bases vacías equivalentes. Al terminar se
ejecuta `ANALYZE`; el hash de muestra no sustituye una comparación exhaustiva.

Se validan ambas bases antes de insertar y cada una usa una transacción. Un fallo
de carga revierte ambas mientras sus transacciones sigan abiertas. Sus commits
son independientes: si una desconexión deja una sola base cargada, recrear ambas,
migrar y repetir. Un fallo en `ANALYZE` puede ocurrir después de confirmar los datos.

## Tests

```bash
uv run --python 3.13 --with asyncpg==0.30.0 --with argon2-cffi==25.1.0 \
  python -m unittest discover -s scripts/seed -v
```

Para incluir los cuatro tests de PostgreSQL, definir `TEST_SEED_USERS_DATABASE_URL`
y `TEST_SEED_POSTS_DATABASE_URL` con bases locales descartables migradas a `head`.
**Los tests vacían esas bases con `TRUNCATE ... CASCADE`.** Sin esas variables se
omiten los tests de base. La suite verifica determinismo, referencias, unicidad,
fechas, contenido relacionado, volúmenes límite, contadores, contraseñas, rechazo
de bases ocupadas y rollback; compara todas las filas entre distintos lotes.
