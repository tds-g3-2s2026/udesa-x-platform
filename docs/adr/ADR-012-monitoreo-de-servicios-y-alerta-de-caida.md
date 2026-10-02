# ADR-012: Monitoreo de los servicios y alerta de caída con Grafana Cloud

**Fecha:** 2026-10-01 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

`E5-H11 CA.4` pide que, si un servicio se cae, todos los administradores reciban una alerta por
email. La pantalla de estado del backoffice ya cumple `CA.1` a `CA.3`, pero el backoffice es una
SPA estática en S3: consulta la salud solo mientras alguien la tiene abierta, así que no puede
detectar una caída ni avisar a nadie.

El chequeo tiene que correr solo, y fuera del navegador. Dentro del cluster no hay lugar: la
cuota del namespace no tiene margen de Services ni de ConfigMaps, y los pods ya están contados
en el ADR-009. `notifications-api`, que es donde iría el envío de correos según el ADR-010,
todavía no existe.

`A13` de `ARQUITECTURA.md` ya eligió Grafana Cloud para la observabilidad, y `T-21` pide un
dashboard con los healthchecks de los servicios desplegados.

## Decisión

**Synthetic Monitoring de Grafana Cloud chequea desde afuera la salud de cada servicio en
`/api/health/<servicio>`, y Grafana Alerting avisa por email a una lista fija de
administradores.**

- **Qué se chequea.** Un chequeo HTTP por servicio, contra la URL pública: los servicios de
  `HEALTH_TARGETS` del gateway y el gateway mismo. Un servicio está sano si responde 200 con
  `status: ok` en menos de 5 segundos, el mismo criterio que usa la pantalla para `CA.3`.
- **Desde dónde y cada cuánto.** Desde una sola probe, la más cercana a `us-east-2`, cada 2
  minutos. El plan gratuito permite 100.000 ejecuciones por mes, que se cuentan por chequeo,
  por probe y por corrida: cuatro chequeos cada 2 minutos son 86.400.
- **Cuándo avisa.** Con dos fallas seguidas, para que un corte de red de un minuto no
  dispare un mail. Manda un mail cuando el servicio pasa a caído y otro cuando vuelve, y
  ninguno en el medio: una política de notificación propia sube el `repeat_interval` a 4
  días, más que cualquier caída esperable.
- **A quién.** Un contact point de email con la lista de administradores y la opción "Single
  email", que manda un solo correo para todos. Los destinatarios no necesitan cuenta en
  Grafana, y el envío sale por el SMTP de Grafana, no por Resend.

## Alternativas descartadas

- **Un CronJob con la imagen de `users-api`.** Tiene la lista de admins y Resend a mano, y
  sería la lista real de la base y no una copia. Pero suma un objeto nuevo al namespace, ocupa
  un pod de la cuota en cada corrida y hay que escribirle tests y despliegue a un caso que
  Grafana resuelve con configuración.
- **Un loop en background dentro de `users-api` o del gateway.** No suma recursos, pero un
  servicio no puede avisar de su propia caída.
- **Esperar a `notifications-api`.** Ata `CA.4` al nacimiento de un servicio nuevo y de la
  cola, que es el trabajo más grande pendiente. Además seguiría vigilando desde adentro del
  sistema que vigila.
- **Un workflow de GitHub Actions con `schedule`.** No usa cuota, pero el cron de Actions
  corre como mucho cada 5 minutos, se atrasa con frecuencia y necesitaría la clave de correo
  fuera del cluster.
- **Métricas propias en el backoffice, o las probes de Kubernetes.** El backoffice no
  recolecta ni guarda nada, y las probes reinician el pod o lo sacan del Service, pero no
  avisan a nadie. Prometheus con Alertmanager son pods que la cuota no tiene.

## Consecuencias

- La lista de destinatarios es fija: un administrador creado desde el panel no recibe la
  alerta hasta que alguien lo suma al contact point. El equipo lo acepta como forma de cumplir
  `CA.4`.
- La lista de servicios vive en dos lugares, `HEALTH_TARGETS` y los chequeos de Grafana. Un
  servicio nuevo necesita su chequeo, y con `notifications-api` el intervalo pasa a 3 minutos
  para seguir dentro del cupo (cinco chequeos son 72.000 ejecuciones).
- Los chequeos pasan por el gateway. Si se cae el gateway, fallan todos y llegan las alertas
  de todos los servicios, aunque los backends sigan vivos.
- La cuenta de Grafana Cloud está a nombre de un integrante. Como con Resend en el ADR-010, el
  resto del equipo tiene que tener acceso, o el monitoreo depende de una sola persona.
- Depende de que la ruta `/api/health/:service` del gateway esté desplegada en producción.
- Con una sola probe, un problema de red de esa ubicación puede verse como una caída. Si
  aparecen falsas alarmas, se pasa a dos probes cada 4 minutos, que también entra en el cupo.
- El dashboard de Synthetic Monitoring cubre el dashboard de healthchecks que pide `T-21`. La
  historia de los chequeos dura los 14 días de retención del plan gratuito.
