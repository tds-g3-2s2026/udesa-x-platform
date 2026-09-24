# ADR-009: Proveedor de correo

**Fecha:** 2026-09-23 · **Estado:** propuesta · **Decide:** el equipo

## Contexto

Desde S2, `users-api` genera los tokens de verificación y de recuperación de contraseña, pero el
envío está detrás de un adaptador que escribe el link en el log. La decisión A14 de
`ARQUITECTURA.md` pedía "Resend o Brevo, con dominio verificado en S1", y el riesgo `R3` de
`PLANIFICACION.md` quedó abierto porque el equipo no tenía un dominio propio. El dominio de la
cátedra, `tds-linar.udesa.edu.ar`, lo comparten los cinco grupos y no es nuestro para cargarle
registros SPF, DKIM y DMARC.

Tres criterios de la consigna dicen "enviado al email" (`E1-H1 CA.1`, `E1-H1 CA.6` y `E1-H5`), y
en la entrega intermedia alguien tiene que poder registrarse en vivo y validar la cuenta.

## Decisión

**Resend, con el dominio propio `udesax.app` verificado, a través de su SDK oficial de Python
(`resend[async]`).**

- **Dominio propio.** Sin un dominio verificado, Resend solo entrega a la dirección dueña de la
  cuenta. Con `udesax.app` entrega a cualquier destinatario, y el SPF y el DKIM son nuestros.
  Esto cierra `R3`.
- **SDK y no HTTP a mano.** El SDK trae los tipos de los parámetros y traduce los errores de la
  API a excepciones propias (`ResendError`). La versión async usa `httpx`, que el proyecto ya
  tenía, así que no suma un cliente HTTP nuevo.
- **El envío nunca lanza una excepción.** El correo sale dentro del request, antes del commit:
  si fallara la operación entera, se desharía un registro que sí ocurrió. El adaptador registra
  el error sin el link y la cuenta queda creada; el usuario pide otro link desde la app.
- **El adaptador de consola se queda** para desarrollo y tests. Cuál se usa se elige con
  `EMAIL_PROVIDER`, y con `resend` el servicio no arranca si falta `RESEND_API_KEY`.

## Alternativas descartadas

- **Brevo sin dominio.** Entrega a cualquiera verificando solo una casilla de remitente, pero
  si esa casilla es de un proveedor gratuito la reemplaza por una propia y el correo tiende a
  caer en spam. Con un dominio disponible deja de tener ventaja.
- **Resend por HTTP directo con `httpx`.** Evita la dependencia, pero reimplementa el manejo de
  errores y los tipos que el SDK ya trae.

## Consecuencias

- `users-api` suma la dependencia `resend[async]`, que arrastra `requests` aunque no se use.
- El SDK guarda la clave y el cliente HTTP a nivel de módulo, no por instancia: alcanza porque
  hay un único proveedor por proceso.
- El plan gratuito permite 100 correos por día, suficiente para la demo. Un pico de registros
  por encima de eso deja cuentas sin correo, que se recuperan con el reenvío.
- La cuenta de Resend y el dominio `udesax.app` están a nombre de un integrante. El equipo tiene
  que tener acceso a los dos, o la continuidad del envío depende de una sola persona.
- Cuando exista `notifications-api`, el envío pasa a ese servicio consumiendo eventos de la cola
  (`user.registered`, `password.reset_requested`, `password.changed`). Esta decisión de
  proveedor se mantiene, y `users-api` deja de depender del SDK.
