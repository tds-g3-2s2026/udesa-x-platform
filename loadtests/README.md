# Pruebas de carga en EKS

Un script de k6 por flujo: login, feed, búsqueda, perfil y creación de posts. Cada uno
mide contra el ingreso público del cluster, con la concurrencia y los umbrales de su
flujo definidos en el propio script. Se elige EKS como ambiente de medición porque el
compose local de platform no incluye el feed.

## Preparar el ambiente

Los despliegues de users-api, posts-api y gateway deben estar operativos, con las
migraciones aplicadas. Cargar primero el seed (`scripts/seed/README.md`) con la semilla
y una cantidad de usuarios que alcance para la concurrencia del flujo: cada usuario
virtual usa una cuenta distinta, desde el índice cero, y `VUS` no puede superar
`SEED_USERS`. Las cuentas deben conservar la contraseña del seed y tener publicaciones
de cuentas seguidas. Los scripts no crean datos.

## Correr desde Actions

El workflow manual `Prueba de carga` (`prueba-de-carga.yml`) corre un flujo o todos desde
un runner de GitHub, fuera del cluster y sin otro tráfico de prueba, así cada corrida sale
del mismo lugar y se puede comparar con la anterior. Guarda como artifact un JSON por
flujo y el estado del ambiente antes y después: SHA desplegados, réplicas, recursos y
autoscaler. Los SHA salen de los tags que ECR guarda para el digest de cada deployment,
porque el despliegue es por digest. El resumen del job dice, por flujo, si cumple los
umbrales. Con `todos`, create-post corre al final porque agrega posts.

## Correr a mano

Requiere k6; también puede ejecutarse con `grafana/k6:1.3.0` en Docker. Primero probar
con un usuario y tiempos cortos:

```bash
export BASE_URL=https://tds-group-3.tds-linar.udesa.edu.ar/api
export SEED=42 SEED_USERS=200 SEED_PASSWORD='<PASSWORD de scripts/seed/seed.py>'
export USERS_SHA=REEMPLAZAR_SHA_DESPLEGADO_USERS
export POSTS_SHA=REEMPLAZAR_SHA_DESPLEGADO_POSTS
export GATEWAY_SHA=REEMPLAZAR_SHA_DESPLEGADO_GATEWAY

VUS=1 RAMP_SECONDS=1 DURATION_SECONDS=5 \
  SUMMARY_PATH=/tmp/feed-smoke.json k6 run loadtests/feed.js
```

Reemplazar los valores `REEMPLAZAR_...` antes de ejecutar. Sin `VUS`, cada flujo usa su
concurrencia; la rampa es de 30 segundos, la carga estable de 120 y la bajada de 30
(`RAMP_SECONDS`, `DURATION_SECONDS`). Alternativa Docker desde la raíz, con las mismas
variables exportadas:

```bash
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/loadtests:/work:ro" -v /tmp:/results \
  -e BASE_URL -e SEED -e SEED_USERS -e SEED_PASSWORD \
  -e USERS_SHA -e POSTS_SHA -e GATEWAY_SHA \
  -e SUMMARY_PATH=/results/feed.json \
  grafana/k6:1.3.0 run /work/feed.js
```

## Qué mide cada flujo

- **Login:** k6 inicia sesión una vez con cada cuenta antes de medir. El servicio
  actualiza los hashes anteriores en esa preparación. El JSON registra esos primeros
  ingresos en `preparation_duration`.
  Durante la carga cada usuario virtual sigue con la misma cuenta. El umbral se
  aplica a `duration`, que mide ese login habitual. Se puede reutilizar la semilla.
- **Feed:** `PAGES` limita las páginas consecutivas por iteración (predeterminado: 5);
  cada iteración vuelve a la primera página. La primera página y las siguientes tienen
  umbrales propios. El cursor opaco se envía como `cursor` y la respuesta debe incluir
  `items` y `nextCursor`, que es `null` al terminar el feed.
- **Búsqueda:** recorre los términos de `search-terms.json`, que tienen que aparecer en
  el vocabulario del seed (un test lo verifica). Si el primer término no devuelve
  resultados, la preparación se detiene: no se mide una búsqueda vacía.
- **Perfil:** abre el encabezado y la lista de posts de autores que aparecen en los feeds
  de las cuentas, con métricas y umbrales separados para cada uno.
- **Crear post:** publica sin imagen, una vez cada `THINK_SECONDS` por usuario (10 por
  defecto). posts-api limita los posts por cuenta y hora (`POST_RATE_LIMIT`, 30): una
  corrida que lo supere no empieza, y repetirla dentro de la hora reutiliza las cuentas y
  puede recibir 429, que se cuentan aparte en `rate_limited`. Cada corrida agrega posts,
  así que cambia el volumen de datos: anotar cuántos.

Los flujos con sesión hacen el login de todas las cuentas antes de la carga. Una cuenta
sin sesión, o sin datos que leer, detiene la preparación. Los tokens deben durar toda la
corrida, incluido el cierre de las iteraciones; reducir los tiempos si la preparación
rechaza su vigencia. No se hace login por página ni se renuevan tokens durante la
medición. La corrida produce refresh tokens como cualquier login de la app.

## Interpretar y guardar resultados

La salida JSON y `SUMMARY_PATH` incluyen fecha UTC, ambiente, URL, semilla, usuarios,
etapas, duración y SHA de los servicios. Los tres SHA completos son obligatorios; el
script valida su formato, pero el operador debe comprobar que correspondan a las
imágenes desplegadas. `ENVIRONMENT` permite identificar una validación local sin
etiquetarla como EKS. El archivo de salida se sobrescribe; usar un nombre distinto por
corrida.

- `requests`: cantidad de pedidos medidos durante la carga.
- `errors`: proporción de respuestas que no cumplen el contrato del flujo; incluye
  errores de red, autenticación y servidor.
- `duration`: latencia con p50 y p95 en ms. El feed la separa en `first_page_duration` y
  `next_page_duration`, y el perfil en `header_*` y `posts_*`.

El p95 y la tasa de errores de cada flujo corresponden a la carga medida. En el flujo de
login, `preparation_duration` registra por separado los ingresos de preparación. Las
métricas HTTP generales de k6 incluyen ambas fases. Cada script falla con código 99 si algún
umbral de su flujo se cruza, y el JSON se escribe igual. Si faltan muestras o hay
iteraciones interrumpidas, conservar esa limitación al interpretar el resultado: una
preparación fallida no constituye una medición. El informe va en
`loadtests/RESULTADOS.md`, con réplicas, recursos, ubicación del generador e
interrupciones observadas.

## Validar los scripts sin EKS

Con Python 3 y Docker Desktop activos, desde la raíz:

```bash
python3 -B -m unittest discover -s loadtests -v
```

La suite ejecuta k6 contra un servidor HTTP descartable en la máquina local. No accede al
cluster ni reemplaza una prueba con los servicios reales.
