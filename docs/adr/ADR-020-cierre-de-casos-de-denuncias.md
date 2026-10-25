# ADR-020: Cierre de casos de denuncias: el umbral cuenta lo pendiente y la revisión se levanta

**Fecha:** 2026-10-25 · **Estado:** aceptada · **Decide:** el equipo, con las recomendaciones de `E5-H7`

## Contexto

El ADR-011 decidió que `posts-api` le pide a `users-api` poner una cuenta en revisión cuando
junta denuncias de 6 cuentas distintas, y que esa condición se evalúa en cada denuncia nueva.
Cuenta todas las denuncias de la cuenta, desde siempre, y la revisión no tiene salida:
`users-api` solo sabe poner cuentas en revisión.

`E5-H7` suma la bandeja del backoffice y dos acciones sobre cada caso: **Descartar** y
**Resolver**. Con lo que dice el ADR-011, las dos chocan:

- **La revisión no se levanta.** Una cuenta en revisión queda bloqueada aunque el administrador
  descarte sus denuncias. Nada la vuelve a activar salvo editar la base a mano.
- **El umbral se vuelve a disparar.** Si la revisión se levantara, la primera denuncia nueva la
  pondría en revisión otra vez: los seis denunciantes del caso cerrado siguen contando.

Son las decisiones 3 y 4 de la historia (`udesa-x-posts-api#102`).

## Decisión

**El umbral cuenta solo los denunciantes de denuncias pendientes, y cerrar un caso levanta la
revisión con una ruta interna nueva de `users-api`.**

- **Estado de la denuncia.** Cada denuncia está pendiente, descartada o resuelta, y guarda quién
  y cuándo la decidió. Las que ya existían quedan pendientes: nadie las había mirado.
- **Umbral.** Sigue siendo el sexto denunciante distinto, pero solo entre las denuncias
  pendientes. Un caso cerrado deja de sumar: si la cuenta vuelve a juntar 6 denunciantes
  distintos, vuelve a revisión.
- **Levantar la revisión.** `users-api` expone `DELETE /internal/users/{id}/review`, fuera de
  `/api` y con el mismo `X-Internal-Token` del ADR-011. Una cuenta en revisión vuelve a activa.
  Una activa o suspendida no cambia: la suspensión es decisión de un administrador (`E5-H5`).
  Es idempotente, y las sesiones no vuelven: el dueño inicia sesión de nuevo.
- **Quién lo llama.** `posts-api`, al Descartar o Resolver, antes de confirmar el cambio de
  estado. Si `users-api` no responde, la acción falla con `503` y las denuncias siguen
  pendientes, para que el administrador la reintente. Una cuenta que `users-api` ya no tiene
  responde `404` y se toma como nada que levantar.
- **Al revés que el aviso del ADR-011.** Ahí la denuncia ya estaba guardada y un fallo podía
  esperar a la denuncia siguiente. Acá no hay siguiente: sin la llamada, el caso quedaría
  cerrado con la cuenta bloqueada y nadie volvería a mirarlo.
- **Suspender desde la bandeja.** El backoffice bloquea la cuenta con `E5-H5` y después resuelve
  el caso. Como la cuenta ya está suspendida, levantar la revisión no la toca.

## Alternativas descartadas

- **Mantener el umbral sobre todas las denuncias y mostrar en la bandeja que la cuenta ya lo
  superó.** No cambia el ADR-011, pero cada denuncia nueva a una cuenta con un caso descartado
  la vuelve a poner en revisión. Descartar dejaría de servir.
- **Resolver sin tocar la cuenta y dejar el levantamiento para una pieza aparte.** La historia
  quedaría con una acción que cierra el caso y deja la cuenta bloqueada para siempre.
- **Avisar por la cola.** El mismo motivo por el que la llamada sigue siendo síncrona: el
  resultado se necesita dentro del request, para no cerrar un caso con la cuenta todavía
  bloqueada.

## Consecuencias

- Ajusta dos puntos del ADR-011: el umbral pasa a contar solo denuncias pendientes, y la revisión
  tiene salida. El resto del ADR-011 sigue vigente.
- `posts-api` pasa a tener dos llamadas a `users-api` por denuncias, las dos internas y con el
  mismo secreto.
- Descartar y Resolver dependen de que `users-api` responda: con `users-api` caído, los casos no
  se pueden cerrar hasta que vuelva.
- La ruta de `users-api` tiene que estar desplegada antes que las acciones de `posts-api`. Si
  no, cada acción responde `503` y no cambia nada.
- Quién cerró cada caso y cuándo queda en las denuncias (`decided_by` y `decided_at`), y en la
  auditoría de `E5-H6` cuando exista.
