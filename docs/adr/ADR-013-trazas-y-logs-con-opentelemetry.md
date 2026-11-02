# ADR-013: Telemetría con OpenTelemetry, enviada directo a Grafana Cloud

**Fecha:** 2026-10-01 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

`T-21` pide logs estructurados y un identificador que permita seguir un request de punta a
punta por los servicios que atraviesa. Hoy `users-api` y `posts-api` escriben texto plano en la
salida del pod, el gateway no escribe nada, y ningún servicio comparte un identificador con el
siguiente. Esos logs solo se ven con `kubectl logs` y se pierden cuando el pod se reinicia.

`A13` de `ARQUITECTURA.md` ya eligió OpenTelemetry hacia Grafana Cloud, pero no dice cómo llegan
los datos, qué identifica a un request ni qué se manda. Tres restricciones salen del cluster:

- **La cuota del namespace no tiene margen** para un pod más, que es lo que ocupa un colector.
- **El equipo tiene permisos de solo lectura** fuera de su namespace (ADR-008). Un recolector de
  logs a nivel de cluster, o un rol de IAM para escribir en CloudWatch, los da la cátedra.
- **El gateway corre en Bun**, donde la instrumentación automática de OpenTelemetry para Node no
  está garantizada.

## Decisión

**Los cuatro servicios usan el SDK de OpenTelemetry y mandan trazas, logs y métricas por OTLP directo a
Grafana Cloud, sin colector. El identificador de un request es su `trace_id`, que viaja entre
servicios en el header `traceparent` de W3C.**

- **Envío directo.** Cada servicio exporta por OTLP/HTTP con protobuf al endpoint de Grafana
  Cloud, autenticado con un token de solo escritura. No suma pods al namespace.
- **El `trace_id` como identificador de correlación.** Cada servicio lee el `traceparent` del
  request que recibe, o empieza una traza si no viene, y lo pasa en cada llamada a otro
  servicio. Todo log que se escribe durante un request lleva ese `trace_id`.
- **Tres señales, un destino.** Las métricas reutilizan el endpoint y las credenciales de
  trazas y logs. Cada proceso tiene una identidad de instancia distinta; los contadores y
  buckets se agregan entre instancias al consultar, no antes de exportar.
- **Métricas HTTP acotadas.** Un histograma en segundos registra método, ruta parametrizada
  y código. El gateway usa el prefijo de su tabla de ruteo y clasifica los flujos con objetivos
  de servicio, distinguiendo primera página del feed y siguientes. IDs, cursores, URLs crudas,
  usuarios y `trace_id` no son etiquetas de métricas. Los healthchecks quedan excluidos.
- **Métricas de consumo y envío.** Cada entrega del broker cuenta como intento; fallos de
  procesamiento, descartes permanentes y resultados del proveedor se miden por separado.
  Un ACK no significa un email enviado. El tiempo del handler excluye la espera en la cola.
- **Exemplars.** Las APIs Python exportan observaciones con contexto de traza. El SDK de
  JavaScript fijado no serializa exemplars; no se modifica su serializador para suplirlo.
  Los enlaces de métrica a traza se verifican sobre las mediciones de Python.
- **Objetivos y alertas.** Los flujos se evalúan desde el gateway, con percentiles de buckets
  agregados y errores 5xx. Las reglas usan ventanas de cinco minutos y cinco minutos de
  incumplimiento sostenido. La ausencia de tráfico queda a cargo del monitoreo externo de
  salud; un fallo de consulta de la fuente conserva estado de error. Las reglas reutilizan
  el contact point y la repetición de cuatro días del monitoreo de salud.
- **Qué se loguea de cada request.** Una línea con método, ruta, código de respuesta y duración
  como campos. La ruta va sin el query string, que puede llevar un token. Los healthchecks de
  Kubernetes no generan ni traza ni log.
- **Qué no se manda nunca.** Tokens, contraseñas, ni los links que manda el correo.
- **Solo con endpoint.** Un servicio exporta únicamente si tiene `OTEL_EXPORTER_OTLP_ENDPOINT`.
  En desarrollo y en los tests no se manda nada, y la traza igual existe dentro del proceso.
- **Configuración estándar.** El endpoint va en el `ConfigMap` de cada servicio y el token en
  `OTEL_EXPORTER_OTLP_HEADERS`, en el `Secret`, desde un secreto de GitHub. Los exportadores
  leen las variables `OTEL_EXPORTER_OTLP_*` por su cuenta.
- **El SDK no exporta sus propios logs.** Cuando una exportación falla, el SDK lo registra con
  `logging`; reenviar ese registro por el mismo exportador lo reintenta sin fin y el proceso no
  termina. Esos registros siguen saliendo por la salida del pod.
- **En Python, un módulo copiado.** `infrastructure/telemetry.py` es el mismo en `users-api` y
  `posts-api`, salvo el nombre del servicio, copiado como el resto del código común.
- **En el gateway, a mano.** Un middleware de Hono abre la traza y escribe el log, y el proxy
  inyecta el `traceparent` antes de reenviar. El contexto se mantiene con `AsyncLocalStorage`,
  que Bun soporta.
- **Configuración revisable.** Dashboards, reglas y ajustes de correlación se versionan.
  Grafana Cloud recibe payloads de su API; no se asume soporte para montar provisioning de
  archivos. Se conservan las fuentes, las credenciales y los chequeos existentes al importar.

## Alternativas descartadas

- **CloudWatch y X-Ray.** Están en la misma cuenta que el cluster y el tutor ya tiene acceso,
  pero escribir ahí exige un rol de IAM para cada pod, que crea la cátedra, y firmar cada pedido
  con SigV4, que en la práctica pide un colector.
- **Instrumentación automática (`opentelemetry-instrument` en Python, `sdk-node` en
  JavaScript).** Instrumenta más cosas sin código, pero esconde qué se manda, y en Bun no está
  garantizada.

## Consecuencias

- Dependencias nuevas. En Python: `opentelemetry-sdk`, `opentelemetry-exporter-otlp-proto-http`,
  `opentelemetry-instrumentation-fastapi`, `opentelemetry-instrumentation-logging` y, en
  `posts-api`, `opentelemetry-instrumentation-httpx`. En el gateway: la API, el SDK de trazas y
  de logs, los exportadores OTLP con protobuf y el administrador de contexto de
  `AsyncLocalStorage`.
- Las métricas de Python reutilizan el SDK y el exportador HTTP existentes. Los servicios
  de Bun incorporan `@opentelemetry/sdk-metrics` y
  `@opentelemetry/exporter-metrics-otlp-proto`, con versiones compatibles fijadas.
- Un lector periódico exporta las métricas y se vacía al apagar el proceso. El fallo de
  Grafana no impide responder peticiones ni cambia el resultado de una operación.
- La API de logs del SDK de Python todavía es experimental y cambia entre versiones. Una
  actualización de esas dependencias se prueba antes de mergear.
- El gateway pasa a tener un `Secret`, solo para el token. Es un objeto más en la cuota del
  namespace.
- Un solo token sirve para los cuatro servicios, cargado como secreto de la organización. Tiene
  solo permisos de escritura: filtrado, no permite leer nada.
- Si Grafana no responde, los datos de ese momento se pierden después del reintento, y un pod
  que se apaga tarda a lo sumo el timeout del exportador. Los servicios siguen funcionando.
- Cambiar de destino es cambiar el endpoint y el token. Mudarse a AWS además pide el colector
  que hoy se descarta.
- Las migraciones de Alembic dejan de desactivar los loggers existentes, porque los tests las
  corren en el mismo proceso que el servicio.
