# Observabilidad operativa

El rendimiento se mide desde el gateway para evaluar los flujos del producto. Las métricas
de cada backend permiten investigar dónde se consume el tiempo. Las duraciones están en
segundos; los percentiles se calculan después de sumar los buckets de todas las instancias.
La tasa de errores del sistema cuenta respuestas 5xx. Los rechazos 4xx siguen disponibles
en las métricas, pero no disparan esas alertas.

La primera página del feed y las siguientes son flujos distintos porque sus objetivos de
latencia difieren. Las consultas usan la etiqueta `job`: Grafana Cloud la obtiene de
`service.name`. Cada proceso conserva su propia identidad de instancia antes de agregarlo.

El panel de consumo cuenta intentos, incluidos los mensajes reentregados. Un ACK no prueba
que un correo se haya enviado: los resultados del proveedor se observan por separado.
La duración del handler no incluye espera en RabbitMQ. La profundidad de la cola, los
mensajes publicados y el volumen actual de la DLQ necesitan métricas del broker; no se
deducen de los contadores del consumidor. Los contadores de descarte indican envíos
solicitados a la DLQ, no su inventario actual.

## Preparar una importación

Primero exportar desde la cuenta existente los dashboards, las fuentes de datos y las
reglas que se van a modificar. Conservar sus UIDs, los chequeos de Synthetic Monitoring,
el contact point de email y la política de notificación. El dashboard permite seleccionar
los jobs reales de los chequeos de salud; no presupone sus nombres ni reemplaza sus alertas.

Con los UIDs reales de las tres fuentes de datos, una carpeta existente y el nombre del
contact point existente, generar payloads revisables:

```bash
python3 observability/render.py \
  --metrics-uid "$GRAFANA_METRICS_UID" \
  --tempo-uid "$GRAFANA_TEMPO_UID" \
  --loki-uid "$GRAFANA_LOKI_UID" \
  --folder-uid "$GRAFANA_FOLDER_UID" \
  --contact-point "$GRAFANA_CONTACT_POINT" \
  --output /tmp/udesa-observability
```

El render no se conecta a Grafana ni recibe credenciales. Rechaza una carpeta de salida
existente para conservar los payloads ya revisados. Las reglas se guardan en YAML usando
su subconjunto JSON, que permite validarlas sin otra dependencia.

Grafana Cloud no admite montar archivos de provisioning. El dashboard generado se importa
con `POST /api/dashboards/db`; cada regla generada se crea con
`POST /api/v1/provisioning/alert-rules`. Estos son payloads de la API, no el formato de los
endpoints de exportación. Si el UID ya existe, revisar el diff con su exportación y usar la
actualización de ese recurso: `overwrite: true` para el dashboard, o
`PUT /api/v1/provisioning/alert-rules/<uid>` para la regla. Los permisos de escritura de OTLP
no alcanzan para administrar dashboards o reglas.

El dashboard usa el UID estable `udesa-x-observability`. La URL se obtiene de la respuesta
de la importación; conservar ese enlace en el README y verificar que el tutor pueda abrirlo.
La importación local y las pruebas automáticas no demuestran acceso a la cuenta desplegada.

## Correlación

Aplicar los ajustes de correlación a las fuentes existentes desde Grafana o mediante su API,
mezclando solamente las claves indicadas de `jsonData` con la configuración exportada.
Conservar URL, autenticación, campos secretos y las demás opciones de cada fuente. Si una
fuente está administrada por Grafana Cloud y es de solo lectura, configurar una copia según
el procedimiento soportado por Grafana antes de referenciar su UID en los paneles.

Prometheus enlaza el exemplar `trace_id` con Tempo; Tempo busca en Loki por servicio y
`trace_id` en los metadatos estructurados. Loki ofrece el regreso a la traza. Un exemplar
identifica una observación de la distribución, no necesariamente el valor exacto del p95.
Las APIs Python exportan exemplars. El SDK JavaScript fijado no los serializa; los paneles
del gateway y de notifications no prometen ese enlace.

## Alertas y aceptación

Cada flujo tiene una regla de latencia y otra de errores, con una ventana de cinco minutos
y cinco minutos de incumplimiento sostenido. Sin tráfico, una regla no interpreta la
ausencia de métricas como caída; esa condición la cubren los chequeos externos existentes.
Un error al consultar la fuente sí conserva estado de error. El punto de contacto se
reutiliza por nombre, sin cambiar el árbol global de políticas. La repetición es de cuatro
días, igual que la política de caída: no se promete supresión indefinida.

Para aceptar el cambio en el entorno desplegado:

- Generar tráfico real y comprobar tasas, errores y percentiles por servicio y ruta.
- Abrir desde un exemplar de una API Python la traza de ese momento y sus logs.
- Comparar el contador de fallos y los resultados de email con casos controlados, sin enviar
  datos de usuarios a un proveedor real durante la prueba.
- Forzar de manera controlada el incumplimiento de un objetivo y confirmar el email de alerta
  y recuperación; restaurar la condición antes de terminar.
- Verificar el enlace y los permisos del tutor. Compartir únicamente paneles cuyos datos
  hayan sido revisados para esa audiencia.

Las consultas y las invariantes de importación se comprueban localmente:

```bash
python3 -m unittest discover -s observability -v
PROMETHEUS_URL=http://127.0.0.1:9090 python3 -m unittest discover -s observability -v
```

El segundo comando evalúa las consultas contra un Prometheus aislado. La validación en
Grafana debe importar el dashboard y las reglas en una instancia descartable, comprobar
su estado de evaluación y recorrer los enlaces de correlación con datos controlados.

Los contratos de importación y las limitaciones de Cloud están documentados en la
[API de alertas](https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/alerting_provisioning/)
y en [provisioning de archivos](https://grafana.com/docs/grafana/latest/alerting/set-up/provision-alerting-resources/file-provisioning/).
