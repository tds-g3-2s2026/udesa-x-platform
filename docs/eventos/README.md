# Contratos de eventos

Acá viven los **esquemas fuente** de los eventos que viajan por la cola. Son la única
definición autoritativa: cualquier discrepancia entre un servicio y este directorio se
resuelve a favor de este directorio.

## Por qué acá y no en una librería

Por [ADR-002](../adr/ADR-002-contratos-de-eventos-copiados.md): los esquemas se **copian** a
cada repositorio de servicio en lugar de publicarse como paquete. Fue recomendación del tutor,
para no pelear con empaquetado y versionado. La forma de los mensajes, el versionado y los
checks están en el [ADR-017](../adr/ADR-017-forma-y-versionado-de-eventos.md).

## Qué hay

| Archivo | Qué es |
|---|---|
| `<type>.json` | Un JSON Schema 2020-12 por evento y versión, con mensajes de ejemplo en `examples` |
| `servicios.json` | Qué eventos publica y consume cada servicio. Define qué se copia a cada uno |

| Evento | Publica | Consume |
|---|---|---|
| `user.registered.v1` | users-api | notifications-api |
| `email_verification.requested.v1` | users-api | notifications-api |
| `password.reset_requested.v1` | users-api | notifications-api |
| `password.changed.v1` | users-api | notifications-api |
| `user.deleted.v1` | users-api | posts-api, notifications-api |
| `follow.created.v1` | posts-api | notifications-api |
| `interaction.created.v1` | posts-api | notifications-api |

El resto de la tabla de eventos de `ARQUITECTURA.md` se suma cuando su publicador lo necesite.

## Forma de un mensaje

Sobre de [CloudEvents 1.0](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md):

```json
{
  "specversion": "1.0",
  "id": "0199f3a2-7c41-7d2e-9a10-3b5c8e1f4a01",
  "source": "posts-api",
  "type": "follow.created.v1",
  "time": "2026-10-23T14:05:12Z",
  "data": { "follower_id": "…", "follower_handle": "juanperez", "followee_id": "…" }
}
```

- `id` es único por evento: el consumidor lo guarda para descartar entregas repetidas.
- `type` es también la routing key en el exchange y el nombre del archivo.
- Los campos de `data` van en `snake_case`, como en las APIs.

## Versionado

La versión es parte del `type`. Detalle y razones en el ADR-017.

- **Compatible, mismo `type`:** agregar un campo opcional en `data` o un valor a un enum. El
  consumidor ignora los valores de enum que no conoce.
- **Incompatible, `type` nuevo (`.v2`):** quitar o renombrar un campo, cambiarle el tipo o el
  formato, volver obligatorio uno opcional o cambiar su significado.
- **Convivencia:** el publicador manda `v1` y `v2` hasta que ningún servicio tenga `v1` en
  `consume`. El esquema `v1` se borra recién entonces.

## Cómo se propagan

| Origen | Destino |
|---|---|
| `docs/eventos/*.json` | `contracts/events/` en cada repositorio de servicio, solo los que publica o consume |

Las copias no se editan: se edita acá y se propaga.

```bash
./scripts/validar-esquemas.sh                  # esquemas, ejemplos y servicios.json
./scripts/sync-contracts.sh ../udesa-x-*       # copia a cada servicio lo suyo
./scripts/verificar-contratos.sh posts-api ../udesa-x-posts-api   # lo que corre el CI del servicio
```

Dos checks lo sostienen:

- **En este repo**, el workflow `Contratos de eventos` corre `validar-esquemas.sh` en cada PR
  que toca este directorio.
- **En cada servicio**, `ci-node.yml` y `ci-python.yml` corren `verificar-contratos.sh` contra
  el `main` de platform. Si una copia falta, se editó a mano, quedó atrás o sobra, el CI del
  servicio queda en rojo.

## Cómo cambiar o sumar un evento

1. Editar o crear `<type>.json` acá, con al menos un ejemplo, y anotarlo en `servicios.json`.
2. PR en platform. El check `Contratos de eventos` tiene que pasar.
3. Al mergear, correr `sync-contracts.sh` hacia cada servicio que lo usa y abrir ahí el PR de
   sincronización. Hasta que se mergea, el CI de ese servicio queda en rojo a propósito.
