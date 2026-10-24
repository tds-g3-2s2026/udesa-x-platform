# ADR-019: `aio-pika` para publicar y consumir eventos en los servicios de Python

**Fecha:** 2026-10-24 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

`ARQUITECTURA.md` fija RabbitMQ como cola y dice que tiene clientes maduros en Node y en
Python. El ADR-015 registró `amqplib` para `notifications-api`, pero ningún ADR nombra el
cliente de Python.

`users-api` ya lo necesita para publicar la tabla `outbox` en el exchange `udesa-x.events`
(`udesa-x-users-api#82`), y `posts-api` lo necesita para consumir `user.deleted.v1`
(`E1-H4`, `udesa-x-posts-api#84`). La regla de simplicidad de los `AGENTS.md` pide un ADR
aprobado antes de sumar una librería.

## Decisión

**`aio-pika` (`>=10.1.1`) en `users-api` y `posts-api`.**

- Es el cliente asyncio de RabbitMQ, así que encaja con FastAPI y SQLAlchemy async sin hilos
  aparte.
- `connect_robust` restaura la conexión, el canal, los exchanges, las colas y los consumidores
  después de una caída del broker, así que no hace falta escribir lógica de reconexión.
- `users-api` publica con confirmaciones del broker y `mandatory`: si ninguna cola liga el
  evento, la fila espera en la `outbox` en vez de perderse.
- `posts-api` consume con ack manual y `prefetch`. Declara la misma topología que
  `notifications-api`: exchange `udesa-x.events` de tipo `topic`, cola propia `quorum` con
  `x-dead-letter-exchange`, una dead letter queue por servicio y un binding por tipo de evento.

## Alternativas descartadas

- **`pika`.** Su conexión habitual es bloqueante, y su adaptador asyncio es de más bajo nivel y
  no reconecta por sí solo.
- **`kombu` o Celery.** Abstraen tareas, no mensajes: esconden el exchange, los bindings y la
  dead letter queue, que acá hay que mostrar, y traen su propio modelo de workers.
- **`FastStream`.** Corre encima de `aio-pika`: suma una capa y más dependencias para dos
  consumidores y un publicador.

## Consecuencias

- Hay un cliente de RabbitMQ por lenguaje: `amqplib` en Bun y `aio-pika` en Python.
- `aio-pika` trae `aiormq` y `pamqp` como dependencias de runtime en los dos servicios.
- Los tests de integración de un servicio que publica o consume necesitan un RabbitMQ real:
  para eso existe el input `rabbitmq` de `ci-python.yml`.
- Declarar un exchange que ya existe con otro tipo hace que RabbitMQ rechace la declaración
  (`PRECONDITION_FAILED`). El exchange compartido de mensajes muertos tiene que declararse con
  el mismo tipo y los mismos argumentos en todos los servicios, los de Bun y los de Python.
