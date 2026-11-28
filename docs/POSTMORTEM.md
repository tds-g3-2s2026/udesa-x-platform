# Post mortem de UdeSA-X

Los aportes del equipo reúnen las mejoras que quedaron pendientes y los incidentes que
resolvimos durante el semestre. En cada caso registramos qué pasó y qué haríamos distinto.

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

## Cuota de Neon y migración a RDS

*Aporte de `jleonalderete`.*

**Qué pasó.** El 20 de septiembre todavía no teníamos credenciales de AWS y elegimos la capa
gratuita de Neon para la entrega intermedia. El plan ofrecía 100 horas de cómputo por mes y
suspendía la base después de 5 minutos sin consultas. Los chequeos de disponibilidad hacían un
`SELECT 1` cada 5 a 10 segundos, así que la base seguía activa todo el día. Cerca del 17 de octubre,
`users-api` y `posts-api` se quedaron sin acceso a la base. El agotamiento de la cuota es la causa
probable según el ADR-021. Quedó sin confirmar en la consola de Neon.

**Cómo se resolvió.** Migramos a la instancia RDS de la cátedra, con una base y un rol por servicio.
Las conexiones usan TLS y verifican el certificado contra la autoridad de RDS.

**Qué haríamos distinto.** Evaluar los límites del plan con el uso real, incluidos los chequeos de
disponibilidad, y revisar la elección apenas llegan las credenciales de AWS. En este caso llegaron
el 22 de septiembre, antes de cargar los datos.

## Caída de producción detectada con demora

*Aporte de `jleonalderete`.*

**Qué pasó.** Desde alrededor del 17 de octubre, `users-api` y `posts-api` fallaban sus chequeos de
disponibilidad por la caída de la base. El incidente se abrió el 26, unos nueve días después. Desde
el 17 también fallaban los despliegues de `main` porque faltaba `RABBITMQ_URL` en ambos servicios
y las credenciales de AWS en `posts-api`. RabbitMQ todavía no estaba desplegado en el namespace.
La alerta de caída por correo existía desde el 1 de octubre. Quedó sin registrar si se disparó y si
el equipo la recibió.

**Cómo se resolvió.** La recuperación se completó el 10 de noviembre con la migración a RDS,
el despliegue de RabbitMQ en el clúster y el rol de acceso a S3 para `posts-api`.

**Qué haríamos distinto.** Avisar al equipo cuando falle un despliegue de `main`, comprobar que
la infraestructura requerida esté disponible antes de integrar código y simular periódicamente
una caída para confirmar que llega la alerta.

## Copias de seguridad y restauración de las bases

*Aporte de `jleonalderete`.*

**Qué se quería hacer.** Automatizar los respaldos de `users` y `posts` en RDS y de `notifications`
en DocumentDB. Para comprobar que un respaldo sirve, había que restaurarlo en una base temporal.

**Por qué quedó pendiente.** La tarea pasó al sprint 14 sin avances. Las instancias son de la
cátedra y quedó sin registrar si tenían respaldos automáticos y cuánto tiempo los guardaban.
La prueba de carga sembró 1.000 cuentas con sus posts e interacciones en producción sin un
respaldo previo.

**Qué habría hecho falta.** Consultar a la cátedra por los respaldos automáticos desde el inicio,
programar un Job con `pg_dump` y `mongodump` que guarde las copias en un bucket privado y probar
una restauración comparando la cantidad de filas. Los repositorios son públicos, así que los
respaldos deben quedar fuera de los artefactos de GitHub Actions.

## Alcance del rol de acceso a S3 de `posts-api`

*Aporte de `jleonalderete`.*

**Qué se quería hacer.** Reservar el rol de AWS que da acceso al bucket de imágenes a `posts-api`.

**Por qué quedó pendiente.** La política de confianza del rol no restringe qué ServiceAccount
puede usarlo y el clúster es compartido. El equipo no podía crear un ServiceAccount dedicado,
así que el Deployment monta el token de forma manual. Con las credenciales temporales que se
usaron en un principio, la carga de imágenes devolvía un 503 al vencer las claves y volvía a
funcionar al renovarlas y redesplegar.

**Qué habría hecho falta.** Pedirle a la cátedra que aplique un ServiceAccount dedicado y limite
el rol a esa identidad mediante la condición `sub`, como se hizo con el rol de Bedrock.

## Rendimiento del login y del feed bajo carga

*Aporte de `tommycass`.*

**Qué se quería hacer.** Cumplir los objetivos de p95 del plan, menos de 400 ms para el login con
10 usuarios y menos de 500 ms para la primera página del feed con 20 usuarios.

**Qué pasó.** En la prueba del 24 de noviembre, con 1.000 cuentas de prueba, el p95 fue de 5,3 s
para el login y de 2 s para el feed, sin errores en ninguno de los dos flujos. Argon2 verificaba
las contraseñas de forma sincrónica, bloqueaba el bucle de eventos y el login se atendía de a uno
con un tope de 500m de CPU por contenedor. En el feed, la consulta unía todos los posts y
retweets de las cuentas seguidas antes de ordenar y quedarse con 21 filas, y pasar de una a dos
réplicas no cambiaba el rendimiento.

**Cómo se resolvió.** Argon2 pasó a correr en un hilo aparte, con un límite de verificaciones
simultáneas y con los parámetros mínimos que recomienda OWASP. Con 10 usuarios, el p95 del login
bajó a 164 ms, dentro del objetivo. La consulta del feed ahora aplica los filtros y corta cada
rama antes de unirlas, con dos índices cronológicos. Con 20 usuarios, el p95 bajó de 2 s a 1,2 s.

**Qué habría hecho falta.** Para llevar el feed a 500 ms, medir dónde se va el tiempo que queda,
empezando por el pool de conexiones de `posts-api`, que se agotó en la corrida con 200 usuarios.

## Bloqueo de cuentas por denuncias coordinadas

*Aporte de `tommycass`.*

**Qué pasa.** Con seis denunciantes distintos, una cuenta pasa a revisión, pierde sus sesiones
abiertas y queda sin acceso hasta que un administrador revise el caso. Como el registro admite
cualquier dominio de correo, una sola persona podría controlar las cuentas verificadas que
presentan las denuncias.

**Por qué quedó así.** El umbral y el bloqueo forman parte de la consigna. Aceptar cualquier
dominio facilitó las pruebas y la demo.

**Qué habría hecho falta.** Limitar el registro a `@udesa.edu.ar` o contar solo las denuncias de
cuentas que cumplan un mínimo de antigüedad o actividad.

## Persistencia y disponibilidad de Redis y RabbitMQ

*Aporte de `tommycass`.*

**Qué pasa.** Redis tiene una réplica y guarda las revocaciones de sesión en memoria. Si el pod se
reinicia, un token de acceso revocado puede volver a valer hasta que expire. Esos tokens tienen
una vigencia de 15 minutos. Los tokens de renovación se guardan en la base. RabbitMQ también
tiene una réplica y guarda sus colas en un volumen temporal (`emptyDir`), por lo que puede perder
los mensajes pendientes si se reemplaza el pod. El outbox asegura la publicación del evento.
La persistencia una vez encolado depende de RabbitMQ.

**Por qué quedó así.** Ambos se desplegaron como Deployments simples dentro de la cuota del
namespace.

**Qué habría hecho falta.** Darle un volumen persistente a cada servicio o migrar a servicios
gestionados como ElastiCache y Amazon MQ. Las dos opciones dependen de la cátedra.

## Diferencias entre la evaluación local y la de producción del asistente

*Aporte de `tommycass`.*

**Qué pasó.** La evaluación en producción del 20 de noviembre aprobó 28 de 30 casos. Ante
«seguí a Fede», el asistente eligió una cuenta sin aclarar a quién se refería el pedido. Ante
«contestale a Tomi», redactó un mensaje que el usuario no había dictado. Los dos casos pasaban en
local porque la evaluación armaba la conversación de otra manera que el endpoint de producción.

**Cómo se resolvió.** La evaluación local pasó a usar el mismo recorrido que producción y se ajustó
el prompt para manejar la ambigüedad. El resultado fue 90 de 90 en tres vueltas locales y 30 de 30
en producción el 22 de noviembre.

**Qué haríamos distinto.** Evaluar desde el principio por el recorrido de producción y repetir
cada caso varias veces.

## Dependencias de infraestructura de la cátedra

*Aporte de `jleonalderete`.*

**Qué pasó.** El acceso de administración del equipo al clúster era de solo lectura. Los cambios
fuera del namespace y los permisos sobre la cuenta de AWS dependían de la cátedra.

- Las credenciales de AWS llegaron el 22 de septiembre, seis días antes de la entrega intermedia.
- Incorporar servicios requirió ampliaciones de cuota aplicadas por la cátedra. La cuota ajustada
  llegó a impedir despliegues simultáneos y el gateway quedó en `Pending` el 16 de noviembre.
- La cátedra tenía que crear los ServiceAccounts. El clúster tampoco tenía KEDA ni aplicaba
  NetworkPolicies.
- Los usuarios de IAM del equipo no podían descargar imágenes de ECR y habilitar CloudWatch en
  Grafana requería que la cátedra creara un usuario de solo lectura.
- El límite de 500m de CPU por contenedor también condicionó el rendimiento del login.

**Qué haríamos distinto.** Relevar al comienzo del cuatrimestre la cuota, los ServiceAccounts,
los operadores como KEDA, la lectura de ECR y CloudWatch, y los respaldos. Pedir en la primera
reunión todo lo que dependa de la cátedra y diseñar desde el comienzo dentro de los límites
acordados.
