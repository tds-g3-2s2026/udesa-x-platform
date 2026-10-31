# Línea base del feed en EKS

La corrida usa el ingreso público del cluster: login en users-api y lecturas de
posts-api a través del gateway. Se elige EKS como ambiente de medición. El compose
local de platform no incluye el feed.

## Preparar el ambiente

Los despliegues de users-api, posts-api y gateway deben estar operativos, con las
migraciones aplicadas. Cargar primero el seed chico con la semilla y cantidad de
usuarios que se usarán en la prueba. Las cuentas deben conservar la contraseña
del seed y tener publicaciones de cuentas seguidas. El script no crea datos.

Anotar los SHA **desplegados**, obtenidos de las imágenes de los deployments;
el último commit de `main` puede no coincidir si CD falló. Registrar también las
réplicas, recursos de los pods, volumen del seed y ubicación del generador para
poder comparar corridas. Ejecutar desde una sola instancia de k6, fuera del
cluster, sin otro tráfico de prueba simultáneo.

Requiere k6; también puede ejecutarse con `grafana/k6:1.3.0` en Docker. Primero
probar con un usuario y tiempos cortos:

```bash
export BASE_URL=https://tds-group-3.tds-linar.udesa.edu.ar/api
export SEED=42 SEED_USERS=100 SEED_PASSWORD='CampusSeed42!'
export USERS_SHA=REEMPLAZAR_SHA_DESPLEGADO_USERS
export POSTS_SHA=REEMPLAZAR_SHA_DESPLEGADO_POSTS
export GATEWAY_SHA=REEMPLAZAR_SHA_DESPLEGADO_GATEWAY

VUS=1 RAMP_SECONDS=1 DURATION_SECONDS=5 \
  SUMMARY_PATH=/tmp/feed-smoke.json k6 run loadtests/feed.js
```

Reemplazar los valores `REEMPLAZAR_...` antes de ejecutar. Para una línea base con
20 usuarios virtuales, una rampa de 30 segundos, 2 minutos de carga estable y
30 segundos de bajada:

```bash
VUS=20 RAMP_SECONDS=30 DURATION_SECONDS=120 \
  SUMMARY_PATH=/tmp/feed-baseline.json k6 run loadtests/feed.js
```

Alternativa Docker desde la raíz, con las mismas variables exportadas:

```bash
docker run --rm --user "$(id -u):$(id -g)" \
  -v "$PWD/loadtests:/work:ro" -v /tmp:/results \
  -e BASE_URL -e SEED -e SEED_USERS -e SEED_PASSWORD \
  -e USERS_SHA -e POSTS_SHA -e GATEWAY_SHA \
  -e VUS=20 -e RAMP_SECONDS=30 -e DURATION_SECONDS=120 \
  -e SUMMARY_PATH=/results/feed-baseline.json \
  grafana/k6:1.3.0 run /work/feed.js
```

`VUS` no debe superar `SEED_USERS`: cada usuario virtual usa una cuenta distinta,
desde el índice cero. `PAGES` limita las páginas consecutivas por iteración
(predeterminado: 5). Cada iteración vuelve a la primera página y espera un segundo
al terminar. El cursor opaco se envía como `cursor`; la respuesta debe incluir
`items` y `nextCursor`, que es `null` al terminar el feed.

El login y una lectura por cuenta ocurren antes de la carga. Una cuenta sin sesión
o con feed vacío detiene la preparación. Los tokens deben durar toda la corrida,
incluido el cierre de las iteraciones; reducir los tiempos si la preparación
rechaza su vigencia. No se hace login por página ni se renuevan tokens durante
la medición. La corrida produce refresh tokens como cualquier login de la app.

## Interpretar y guardar resultados

La salida JSON y `SUMMARY_PATH` incluyen fecha UTC, ambiente, URL, semilla,
usuarios, etapas, duración y SHA de los servicios. Los tres SHA completos son
obligatorios; el script valida su formato, pero el operador debe comprobar que
correspondan a las imágenes desplegadas.
`ENVIRONMENT` permite identificar una validación local sin etiquetarla como EKS.
El archivo de salida se sobrescribe; usar un nombre distinto por corrida.

- `duration`: latencia de todas las lecturas del feed, con p50 y p95 en ms.
- `first_page_duration` y `next_page_duration`: latencias separadas para la
  primera página y las siguientes.
- `requests`: cantidad de lecturas durante la carga.
- `errors`: proporción de respuestas que no son HTTP 200 o no cumplen el contrato
  de paginación; incluye errores de red, autenticación y servidor.
- `empty_pages`: páginas válidas sin elementos durante la carga.

Estas métricas excluyen login y lecturas de preparación. Las métricas HTTP
generales de k6 sí los incluyen. No hay umbrales de rendimiento que interrumpan
la prueba: un código de salida cero no implica que se haya cumplido un SLO.
Si faltan muestras o hay iteraciones interrumpidas, conservar esa limitación al
interpretar el resultado. Una preparación fallida no constituye una línea base.

Guardar el JSON junto con una tabla en `docs/` que indique fecha, SHA de cada
servicio, semilla y volúmenes, VUs, duración, solicitudes, p50, p95 y tasa de error.
Agregar réplicas, recursos, ubicación del generador e interrupciones observadas.
La medición refleja el feed desplegado, incluidos retweets y filtros de visibilidad.
Todavía no hay una medición EKS registrada por este cambio.

La salida se genera con [`handleSummary`](https://grafana.com/docs/k6/latest/results-output/end-of-test/custom-summary/)
y la carga usa [rampas de usuarios virtuales](https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/ramping-vus/).

## Validar el script sin EKS

Con Python 3 y Docker Desktop activos, desde la raíz:

```bash
python3 -B -m unittest discover -s loadtests -v
```

La suite ejecuta k6 contra un servidor HTTP descartable en la máquina local.
Comprueba cuentas distintas, el contrato de login, cursores opacos, fin de
paginación, exclusión de la preparación de las métricas y registro de errores
HTTP y de contrato. También verifica que configuración inválida, login fallido,
feed vacío o sesiones demasiado cortas impidan comenzar la carga. No accede al
cluster ni reemplaza una prueba con los servicios reales.
