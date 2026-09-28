# ADR-011: Denuncias en `posts-api` y aviso de cuenta en revisión a `users-api`

**Fecha:** 2026-09-28 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

`E3-H5` pide denunciar una cuenta o una publicación con un motivo de una lista cerrada
(`CA.1`), limitar a una denuncia por día del mismo usuario a la misma cuenta (`CA.3`), pasar a
**En revisión** la cuenta que junta denuncias de más de 5 cuentas distintas (`CA.2`) y, en ese
momento, revocar todos sus JWT activos (`CA.4`).

Las denuncias son de `posts-api` desde el ADR-005, y `report.created` lo publica ese servicio.
Pero la cuenta y la revocación son de `users-api`: el estado de la cuenta está en su base y el
corte de sesiones, `revoked:user:<id>`, en su Redis. `posts-api` no puede escribir ninguno de
los dos. La cola de mensajes todavía no existe en el código de ningún servicio.

La decisión abierta `D1` de `PLANIFICACION.md` preguntaba además si el umbral es 5 o 6.

## Decisión

**Las denuncias se quedan en `posts-api`, que avisa a `users-api` con una llamada REST interna
protegida por un secreto compartido. El umbral es 6 denunciantes distintos.**

- **Qué se denuncia.** Siempre una cuenta. Si se denuncia desde un post, la denuncia guarda
  además cuál post. El umbral cuenta por cuenta, sin importar desde dónde se denunció.
- **Umbral.** "Más de 5" se lee literal: la cuenta pasa a revisión con el sexto denunciante
  distinto. Lo que se cuenta son denunciantes únicos, no filas. Esto cierra `D1`.
- **El aviso.** `users-api` expone `POST /internal/users/{id}/review`, que pone la cuenta en
  revisión y revoca sus sesiones con el `revoke_all` que ya usa el cierre de sesión.
  `posts-api` lo llama por el DNS del cluster (`http://users-api`), sin pasar por el gateway.
- **Fuera de `/api`.** El `Ingress` solo manda `/api` al gateway, y el gateway solo rutea
  prefijos de `/api`. La ruta interna no es alcanzable desde afuera por construcción.
- **Secreto compartido.** Aun así, cada llamada lleva el header `X-Internal-Token`, y
  `users-api` lo compara en tiempo constante contra `INTERNAL_API_TOKEN`. Los dos servicios lo
  reciben en su `Secret`, con el valor desde GitHub Secrets, como el resto. No depende de que
  el gateway o la `NetworkPolicy` estén bien configurados.
- **Idempotente.** Poner en revisión una cuenta que ya lo está no falla ni cambia nada.
- **Ante un fallo.** La llamada sale después del commit de la denuncia, con timeout y un
  reintento con backoff, como pide "Comunicación entre servicios". Si `users-api` no responde,
  la denuncia queda guardada, el error va al log y el request responde igual. Como la
  condición se evalúa en cada denuncia nueva, la próxima denuncia a esa cuenta vuelve a avisar.

## Alternativas descartadas

- **Mover las denuncias a `users-api`.** El dueño de la cuenta tendría el umbral y la
  revocación juntos, sin llamada entre servicios. Contradice el ADR-005 y la tabla de eventos,
  donde `report.created` sale de `posts-api`, y deja la denuncia de un post lejos del post.
- **Avisar por la cola.** Es lo más desacoplado, pero la cola no está en el código de ninguno
  de los dos servicios, y montarla es más trabajo que la historia entera.
- **Endpoint interno sin secreto.** Alcanza con el ruteo de hoy, pero un prefijo mal agregado
  en el gateway lo dejaría abierto a cualquiera.

## Consecuencias

- `posts-api` pasa `httpx` de dependencia de desarrollo a dependencia del servicio, para
  hacer la llamada. Ya es el cliente de los tests y el que usa `users-api` por el SDK de
  Resend, así que no suma una librería nueva al proyecto.
- Es la primera llamada síncrona entre `posts-api` y `users-api` que existe en el código. Si
  `users-api` está caído, las denuncias siguen funcionando, pero ninguna cuenta pasa a revisión
  hasta que llegue otra denuncia.
- Si la llamada del sexto denunciante falla y no llega ninguna denuncia más, la cuenta queda
  fuera de revisión. Se acepta: cerrarlo exige un reintento persistente, que es lo que va a
  dar la cola con el patrón outbox.
- `INTERNAL_API_TOKEN` hay que cargarlo en GitHub Secrets antes del primer deploy que lo use,
  y rotarlo implica actualizar los dos servicios juntos.
- La pantalla del backoffice para ver las denuncias no entra en `E3-H5`. En esta historia la
  denuncia queda guardada y consultable.
- Cuando exista la cola, el aviso puede pasar a ser un evento consumido por `users-api`. El
  endpoint interno y el secreto se retiran en ese momento.
