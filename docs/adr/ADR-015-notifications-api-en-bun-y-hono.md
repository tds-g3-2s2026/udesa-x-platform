# ADR-015: `notifications-api` en Bun y Hono, igual que el gateway

**Fecha:** 2026-10-14 · **Estado:** aceptada · **Decide:** el equipo

> `ci-node.yml` sumó después una opción, `mongodb-y-rabbitmq`, apagada por defecto, para que los
> tests y la imagen de este servicio corran contra MongoDB y RabbitMQ reales
> (`udesa-x-notifications-api#4`). El resto de la decisión sigue igual: mismo gestor de
> paquetes, mismos pasos y ningún workflow propio.

## Contexto

La decisión del 2026-08-20 (`A5` y `A25` de `ARQUITECTURA.md`) puso a `notifications-api` en
Node 24 con NestJS. En ese momento iba a ser el único servicio en TypeScript y el que cumplía
el requisito de la consigna de no tener el backend en una sola tecnología.

Un mes después eso cambió. El 17 de septiembre se sumó `udesa-x-api-gateway` en TypeScript
con Bun y Hono (`D27`, `udesa-x-platform#48`), justamente para cumplir el requisito antes de la
entrega intermedia. Desde entonces el requisito está cumplido y nadie revisó la elección de
`notifications-api`. Seguir el plan escrito deja tres stacks en el backend: Python, TypeScript
sobre Bun y TypeScript sobre Node.

El costo de ese tercer stack ya apareció. `T-03` (`udesa-x-notifications-api#4`) pide decidir
cómo correr el CI, porque `ci-node.yml` asume Bun: instala con `bun install`, corre el lint con
`bun run lint` y los tipos con `bun x tsc`. Ningún otro repo necesita otra cosa.

El servicio es chico: consume eventos de RabbitMQ, guarda en MongoDB, manda push por FCM y
emails, y expone tres endpoints del centro in-app (`E4-H3`).

## Decisión

**`notifications-api` usa el mismo stack que el gateway: TypeScript sobre Bun, con Hono para
HTTP y Vitest para los tests. MongoDB con el driver oficial, sin ORM, como ya estaba
decidido.**

- **Misma versión de Bun que el resto**, fijada en `.bun-version` y en la imagen
  `oven/bun`.
- **El CI es `ci-node.yml` sin cambios.** No hace falta parametrizar el gestor de paquetes ni
  un tercer workflow.
- **Capas e inversión de dependencias a mano, como en los servicios de Python** (ADR-006 y
  ADR-007). Hono no trae inyección de dependencias, y no hace falta: la regla de que un solo
  módulo conoce las implementaciones concretas se cumple igual que en FastAPI.
- **Errores en Problem Details** con el `onError` de Hono, equivalente al manejador de
  excepciones de `users-api` y `posts-api`.
- **Telemetría como en el gateway** (ADR-013): middleware propio con el SDK de
  OpenTelemetry y `AsyncLocalStorage`, sin instrumentación automática.
- **Librerías:** `amqplib` para RabbitMQ, `mongodb` para la base y `firebase-admin` para FCM.

## Verificación previa

Antes de decidir se probó con Bun 1.4.2, contra RabbitMQ 4.3 y MongoDB 8.3 levantados en
contenedores:

- `amqplib` declara el exchange `topic`, una cola `quorum` con `x-dead-letter-exchange`, la
  liga, publica y consume con `ack`.
- `mongodb` crea un índice único y descarta un evento repetido por el error `11000`, que es
  la idempotencia que pide `T-27`. También pagina por usuario y fecha.
- Hono sobre `Bun.serve` responde `/healthcheck` consultando las dos dependencias.
- `firebase-admin` 14.5 llega a FCM por HTTP/2 y por HTTP/1.1, y devuelve el error de
  autenticación esperado con una credencial falsa. El envío real recién se prueba con el
  proyecto de Firebase.

## Alternativas descartadas

- **NestJS sobre Node, el plan original.** Suma un tercer stack y un camino de CI propio, y
  trae inyección de dependencias y decoradores para un servicio con tres endpoints y un
  consumidor. El motivo escrito para Node, el cliente de FCM, también funciona sobre Bun.
- **Hono sobre Node.** Mismo framework, pero vuelve el problema del CI. Queda como plan B: si
  una librería falla en Bun, el código no cambia, solo el runtime y el workflow.
- **Go.** Encaja bien en un consumidor de cola, pero hay que armar desde cero el CI, el lint,
  el reporte de cobertura en formato Cobertura, la telemetría y la copia de los contratos de
  eventos. Con `T-03` y `T-27` atrasadas desde S7, no compensa.
- **Python con FastAPI.** Es lo más barato porque reutiliza la plantilla, pero dejaría el
  requisito de la consigna apoyado solo en el gateway, que no tiene lógica de dominio.

## Consecuencias

- El backend queda en dos stacks, Python y TypeScript sobre Bun, y el segundo tiene dos
  servicios: uno sin dominio y uno con cola, base y FCM.
- `notifications-api` copia del gateway el `Dockerfile`, la configuración de ESLint y Prettier
  y el middleware de telemetría.
- `T-03` deja de pedir una decisión sobre el CI y pasa a usar `ci-node.yml` como los demás.
- Bun no tiene versiones LTS como Node. Se actualiza a mano, junto con el gateway, el
  backoffice y mobile, con la misma versión en los cuatro.
- Si una librería de Node deja de andar en Bun, el plan B es Hono sobre Node, con el costo de
  adaptar `ci-node.yml` en ese momento.
