# Contratos de eventos

Acá viven los **esquemas fuente** de los eventos que viajan por la cola. Son la única
definición autoritativa: cualquier discrepancia entre un servicio y este directorio se
resuelve a favor de este directorio.

## Por qué acá y no en una librería

Por [ADR-002](../adr/ADR-002-contratos-de-eventos-copiados.md): los esquemas se **copian** a
cada repositorio de servicio en lugar de publicarse como paquete. Fue recomendación del tutor,
para no pelear con empaquetado y versionado.

El costo es el riesgo de divergencia, que se mitiga con `scripts/sync-contracts.sh` y un test
que compara las copias contra esta fuente. Ambos llegan con `T-16` en S4.

## Cómo se propagan

| Origen | Destino |
|---|---|
| `docs/eventos/*.json` | `contracts/events/` en cada repositorio de servicio |

Las copias no se editan: se edita acá y se propaga. Si alguien edita una copia, el CI de este
repositorio lo detecta.

## Convenciones

- Un archivo por evento, en formato JSON Schema.
- Nombre del archivo igual al nombre del evento: `user.registered.json`.
- El evento lleva su versión adentro. Un cambio incompatible es un evento nuevo, no una
  edición del anterior.

Todavía no hay esquemas: el primero llega con la cola, en S4.
