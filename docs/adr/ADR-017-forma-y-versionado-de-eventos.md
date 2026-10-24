# ADR-017: Forma, versionado y verificación de los contratos de eventos

**Fecha:** 2026-10-23 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

El [ADR-002](./ADR-002-contratos-de-eventos-copiados.md) decidió copiar los esquemas de eventos
desde `docs/eventos/` a cada servicio en lugar de publicarlos como librería, y dejó para `T-16`
el script de sincronización y el test que detecta copias divergentes. Faltaba además decidir
la forma de los mensajes, cómo cambian sin romper a quien los consume y qué copia recibe cada
servicio.

## Decisión

**Sobre de CloudEvents 1.0.** Todo mensaje es un JSON con los atributos de
[CloudEvents](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md), la
especificación de la CNCF: `specversion` (`"1.0"`), `id` (UUID), `source` (el servicio que
publica), `type`, `time` y `data`, que lleva lo propio de cada evento. Se sigue la forma, sin
sumar el SDK. El `id` es lo que usa el consumidor para descartar entregas repetidas.

**La versión va en el `type`**, como recomienda el
[primer de CloudEvents](https://github.com/cloudevents/spec/blob/main/cloudevents/primer.md#versioning-of-cloudevents):
`follow.created.v1`. Ese mismo valor es la routing key en el exchange topic y el nombre del
archivo, `docs/eventos/follow.created.v1.json`. No hay un campo `version` aparte, que podría
contradecir al `type`.

- **Cambio compatible**, el `type` no cambia: agregar un campo opcional en `data`, o agregar
  un valor a un enum. Lo segundo es compatible porque el consumidor está obligado a ignorar
  los valores que no conoce.
- **Cambio incompatible**, nace `follow.created.v2`: quitar o renombrar un campo, cambiarle
  el tipo o el formato, volver obligatorio uno opcional o cambiar lo que significa.
- **Convivencia.** Mientras haya consumidores de la versión anterior, el publicador manda las
  dos. Cada consumidor migra su binding de `v1` a `v2` en su propio PR. La versión vieja se
  deja de publicar cuando ya no aparece en ningún `consume` de `servicios.json`.

**Cada servicio recibe solo lo que publica o consume.** `docs/eventos/servicios.json` lo
declara por servicio, y `scripts/sync-contracts.sh` copia exactamente ese conjunto a
`contracts/events/`, borrando lo que sobre. El publicador necesita sus esquemas para validar lo
que manda, y el consumidor los suyos para validar lo que espera.

**El esquema se usa en los tests, no en producción.** El test del publicador valida contra el
esquema el mensaje que arma; los tests del consumidor arman sus mensajes desde los `examples`
del esquema o los validan contra él. Para eso entran como dependencias de desarrollo
`jsonschema[format-nongpl]` en los servicios de Python y `ajv` con `ajv-formats` en los de
TypeScript, con la validación de formatos activada: sin ella `uuid`, `email` y `date-time`
no se verifican.

**Dos checks.**

- En platform, el workflow `Contratos de eventos` corre `scripts/validar-esquemas.sh`: cada
  esquema compila como JSON Schema 2020-12 en modo estricto, sus ejemplos validan, el nombre
  del archivo coincide con el `type`, y cada evento tiene en `servicios.json` un único
  publicador, el de su `source`.
- En cada servicio, `ci-node.yml` y `ci-python.yml` suman el job `Contratos de eventos al dia`,
  que corre `scripts/verificar-contratos.sh` contra el `main` de platform. Falla si una copia
  falta, se editó a mano, quedó atrás o ya no corresponde. Es el mismo mecanismo que
  `verificar-plantilla.yml` aplica a los archivos comunes.

## Alternativas descartadas

- **Versión solo en un campo, con la routing key fija.** Nombres más cortos, pero cada
  consumidor recibe todas las versiones y tiene que distinguirlas a mano. El primer de
  CloudEvents la admite pero no la recomienda.
- **Todos los esquemas en todos los servicios.** Un script y un check más simples, pero cada
  repo carga esquemas que no usa, y el contrato deja de mostrar quién depende de qué evento.
- **Validar también en producción.** El consumidor rechazaría los mensajes inválidos, pero
  rechazarlos bien necesita la dead letter queue operativa, que está planificada para S11
  (`T-59`). Se puede sumar entonces sin tocar los esquemas.
- **Registry de esquemas o generación de tipos.** Lo descartó el ADR-002, y la issue de
  `T-16` lo deja explícitamente fuera.

## Consecuencias

- **Un cambio de contrato pone en rojo a sus servicios hasta que se sincronizan.** Es lo que
  se busca, pero obliga a un orden: primero el PR en platform, enseguida el PR de
  sincronización en cada servicio afectado. La primera vez, los PRs que agregan
  `contracts/events/` se mergean antes que el de platform que agrega el job.
- **Las colas se atan a `.v1`.** Los bindings de RabbitMQ usan el `type` completo, así que
  migrar de versión es cambiar un binding, no reinterpretar mensajes.
- **Hay eventos que llevan secretos en claro.** `user.registered.v1` y
  `email_verification.requested.v1` llevan la URL con el token de verificación, y
  `password.reset_requested.v1` el código de recuperación; `users-api` guarda los dos hasheados.
  La fila del outbox los tiene en claro hasta que se publica: `udesa-x-users-api#30` borra las
  filas ya publicadas, y ningún servicio loguea esos campos.
- **Los repos sin eventos no cambian.** `gateway`, `backoffice` y `mobile` pasan el check
  mientras no tengan `contracts/events/`.
- **Platform no suma dependencias.** `validar-esquemas.sh` corre `ajv-cli` con `npx`, con la
  versión fijada en el script.
