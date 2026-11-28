# Post mortem de UdeSA-X

Al cierre del semestre quedaron pendientes estas mejoras. Los aportes del equipo recogen qué
queríamos hacer, qué nos frenó y qué habría hecho falta para completarlas.

## Métricas de base de datos y de CPU en Grafana

*Aporte de `varbelaiz`.*

**Qué se quería hacer.** Ver en Grafana el uso de CPU y las conexiones de RDS, y el uso de CPU
de los pods de `posts-api` y `users-api`, junto con las métricas HTTP.

**Por qué quedó pendiente.** El tablero mostraba la duración de las solicitudes HTTP. Durante
la prueba de carga consultamos los datos de infraestructura a mano en CloudWatch y en el HPA.
El profesor prefirió centrar el tablero en las APIs y en los modelos de lenguaje con Langfuse,
sin configurar servicios de terceros.

**Qué habría hecho falta.** Configurar CloudWatch como fuente de datos de Grafana. Para eso, la
cátedra tendría que haber creado un usuario de IAM con permisos de solo lectura.

## Sistema completo en local y pruebas de punta a punta

*Aporte de `FedeTrejo`.*

**Qué se quería hacer.** Levantar todo el sistema con un solo comando usando las imágenes de ECR
y correr pruebas de punta a punta (E2E) de los flujos críticos. La idea era usar Maestro para la
app y Playwright para el backoffice.

**Por qué quedó pendiente.** Nuestros usuarios de IAM no podían descargar las imágenes de ECR,
así que Docker Compose no podía levantar el sistema completo en las máquinas del equipo. Correr
las pruebas contra el clúster habría creado usuarios en producción y enviado correos reales.
Por eso se cerraron ambas tareas sin completar.

**Qué habría hecho falta.** Permisos de lectura de ECR para el grupo o un entorno separado de
producción con el envío de correos desactivado.

## Pendientes de la revisión de seguridad

*Aporte de `FedeTrejo`.*

**Qué se quería hacer.** Resolver los hallazgos del análisis de amenazas. La revisión identificó
que producción no enviaba cabeceras de seguridad como HSTS y CSP, que el gateway no limitaba
las solicitudes por IP ni tenía un tiempo de espera máximo para el proxy, y que las imágenes
se desplegaban sin un escaneo previo.

**Por qué quedó pendiente.** La revisión terminó el 17 de noviembre. Los hallazgos quedaron
registrados en [la documentación de arquitectura](./ARQUITECTURA.md), pero no llegamos a abrir
las tareas antes de la entrega.

**Qué habría hecho falta.** Configurar una política de cabeceras en CloudFront, agregar un
contador de solicitudes por IP en el gateway e incorporar un paso de escaneo en CI.

## Limpieza de imágenes en S3 al borrar un post o una cuenta

*Aporte de `FedeTrejo`.*

**Qué se quería hacer.** Borrar del bucket de S3 las imágenes asociadas cuando se borra un post
o se da de baja una cuenta.

**Por qué quedó pendiente.** Las imágenes de los posts se incorporaron después de implementar
el borrado. En la baja de una cuenta, la operación se resuelve en la base de datos y deja a S3
afuera de la transacción. Los archivos quedan almacenados en el bucket privado y dejan de verse
en la app porque ya no tienen referencias. La mejora quedó registrada en el README de `posts-api`.

**Qué habría hecho falta.** Borrar las imágenes después de confirmar la transacción en la base de
datos y reintentar si falla el borrado en S3.

## Reintentos con espera en el consumidor de `posts-api`

*Aporte de `FedeTrejo`.*

**Qué se quería hacer.** Esperar antes de reintentar un evento que falló por un problema
transitorio, como una caída de la base de datos.

**Por qué quedó pendiente.** El consumidor devuelve el mensaje a la cola de inmediato. Si la
base sigue caída, vuelve a procesarlo una y otra vez sin pausa. La mejora quedó registrada
y no se retomó durante el semestre.

**Qué habría hecho falta.** Usar una cola con un tiempo de expiración (TTL) para demorar los
reintentos. También sería útil que cada servicio recibiera solo sus propios mensajes fallidos en
su cola de mensajes muertos (DLQ). El exchange actual es de tipo `fanout` y los entrega a todas
las colas asociadas. Cambiar ese enrutamiento requiere coordinar a todos los servicios.

## Autoescalado de `notifications-api` según la cola

*Aporte de `jleonalderete`.*

**Qué se quería hacer.** Usar KEDA para ajustar la cantidad de réplicas de `notifications-api`
según los mensajes pendientes en su cola de RabbitMQ y bajar a cero réplicas si la cola está vacía.

**Por qué quedó pendiente.** El clúster no tiene KEDA y el equipo no tiene permisos para instalar
componentes a nivel de clúster. `users-api` y `posts-api` quedaron con autoescalado por CPU
mediante HPA.

**Qué habría hecho falta.** Que la cátedra instale KEDA en el clúster.
