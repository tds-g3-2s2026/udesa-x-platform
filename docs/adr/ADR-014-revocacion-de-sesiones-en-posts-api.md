# ADR-014: `posts-api` lee las revocaciones de sesión desde el Redis de `users-api`

**Fecha:** 2026-10-03 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

`posts-api` verifica el JWT por su cuenta: firma, expiración y emisor, sin pedirle nada a
`users-api`. Eso es lo que dice el diagrama de comunicación, pero deja un hueco que muestra
`udesa-x-posts-api#58`: un token revocado sigue funcionando en `posts-api` hasta que vence, que
son hasta 15 minutos.

Las revocaciones las escribe `users-api` en su Redis, y solo `users-api` las lee hoy:

- **Cierre de sesión.** `revoked:jti:<jti>` marca ese token.
- **Cambio de contraseña y cuenta en revisión.** `revoked:user:<id>` guarda el instante de corte,
  y un token queda revocado si se emitió en ese instante o antes.

Por eso el hueco alcanza a los tres casos. El que lo hace visible es `E3-H5 CA.4`, que pide
revocar todos los JWT de una cuenta cuando pasa a **En revisión** (ADR-011): `users-api` escribe
el corte, pero la cuenta sigue publicando, siguiendo y denunciando en `posts-api` hasta que el
token vence. Cerrar sesión o cambiar la contraseña tiene el mismo problema: el usuario cree que
cerró la sesión y el token robado sigue sirviendo para escribir.

La cola de mensajes, que sería el camino natural para avisar la revocación, todavía no existe en
el código de ningún servicio (`users-api#30`, `notifications-api#5`).

## Decisión

Se evaluaron cuatro caminos. Gana la opción A.

**`posts-api` consulta las marcas de revocación directamente en el Redis del cluster, en la base
lógica `/0` de `users-api`, y solo para leer. Las consulta en cada request autenticado, en un
único viaje.**

- **Una conexión más, a `/0`.** `posts-api` ya depende de ese mismo Redis por `REDIS_URL` (base
  `/1`). Se suma `AUTH_REDIS_URL`, con `redis://redis:6379/0`, que abre un segundo cliente para
  esta lectura. No aparece ningún pod ni ningún punto de falla nuevo: es un viaje más al mismo
  servidor.
- **Un solo viaje.** Las dos claves de un token, la del `jti` y la de su cuenta, se piden juntas
  con un `MGET`. La regla es la de `users-api`: el token está revocado si existe la marca del
  `jti`, o si existe el corte de la cuenta y `iat <= corte`.
- **Solo lectura.** `posts-api` no escribe, no borra ni cambia el TTL de ninguna clave de
  `users-api`. Las marcas siguen siendo de `users-api` en todo.
- **Falla cerrado.** Si ese Redis no responde, el request se rechaza con `503` en formato
  Problem Details. Dejar pasar el token sería devolver el hueco justo cuando la infraestructura
  anda mal.
- **Misma respuesta que `users-api`.** Un token revocado recibe `401` con `code="session-revoked"`
  y el mismo mensaje que da `users-api`, para que el cliente móvil lo maneje igual venga de donde
  venga.

## Alternativas descartadas

- **B. Llamada síncrona a `users-api` en cada request.** Cierra el hueco con la fuente de verdad,
  pero suma una llamada de red a cada request autenticado y acopla la disponibilidad de
  `posts-api` a la de `users-api`, que hoy es independiente. La excepción de `ADR-011` es una
  llamada por denuncia que llega al sexto denunciante; esta sería una por request.
- **C. Eventos de revocación por la cola.** Es la opción más desacoplada, pero RabbitMQ no
  existe todavía. `posts-api` tendría que mantener su propia lista de revocados con consumo,
  reintentos y orden, y esperar a que la cola esté para cerrar un defecto de seguridad que está
  abierto hoy.
- **D. Acortar la vida del access token.** Achica la ventana pero no la cierra: un token de 5
  minutos sigue siendo un token que sirve después de cerrar sesión. Además multiplica los
  refresh que hace el cliente.

## Consecuencias

- **Las claves pasan a ser un contrato de `users-api`.** Quedan fijas: `revoked:jti:<jti>` con el
  valor `"1"` y `revoked:user:<uuid>` con un entero de segundos Unix, sin fracción. La regla es
  `iat <= corte`, con `<=` a propósito: el corte se trunca al segundo, y con `<` un token emitido
  en ese mismo segundo sobreviviría al cambio que debía matarlo. El TTL de ambas es la vida
  restante del access token. Cambiar cualquiera de estas cosas en `users-api` obliga a cambiar
  `posts-api` en el mismo momento.
- **Excepción documentada al ADR-009.** Ese ADR separa `users-api` y `posts-api` por base lógica,
  y cada servicio es dueño de la suya. Acá `posts-api` entra a `/0`, y es lo único que puede hacer
  allí: leer las marcas de revocación. No lee ni escribe nada más de esa base. La separación
  sigue valiendo para todo lo demás, incluidos los contadores de rate limit y la caché.
- **El secreto nuevo.** `AUTH_REDIS_URL` va en el `Secret` de `posts-api`, con el valor desde
  GitHub Secrets, como `REDIS_URL`. No puede quedar sin definir: sin él el servicio no arranca,
  porque un valor por omisión dejaría pasar tokens revocados sin avisar.
- **Cada request autenticado suma un viaje a Redis.** Es un `MGET` dentro del cluster. Si el
  Redis cae, `posts-api` deja de aceptar requests autenticados. Ya dependía del mismo servidor
  por `/1`, pero ahora un fallo corta el acceso en lugar de degradar solo la caché y los
  contadores.
- **Un reinicio del pod de Redis borra las marcas**, como dice el ADR-009: un token revocado vuelve
  a ser válido hasta que vence, en `users-api` y en `posts-api` por igual. No empeora con esta
  decisión.
- **Cuando exista la cola**, `users-api` puede publicar un evento de revocación y `posts-api`
  mantener su propia copia local. Alcanza con reemplazar el lector, que está en una sola función
  que recibe `jti`, cuenta y `iat`, sin tocar ningún endpoint. En ese momento se retira
  `AUTH_REDIS_URL` y este ADR pasa a estar reemplazado.
