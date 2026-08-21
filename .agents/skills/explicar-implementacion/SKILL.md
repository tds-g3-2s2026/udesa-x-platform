---
name: explicar-implementacion
description: Explica un cambio de código como a alguien que recién está aprendiendo, leyendo el diff y el mapa del repo en AGENTS.md. Usala SIEMPRE antes de abrir un Pull Request, y también cuando alguien pregunte "qué hace este código", "por qué está hecho así", "explicame este cambio", "no entiendo esta parte" o quiera preparar la defensa de una historia ante el tutor. Es obligatoria antes de cada merge en este proyecto.
---

# Explicar implementación

El objetivo de esta skill no es documentar. Es que la persona que va a mergear entienda lo
que está mergeando, y pueda defenderlo frente al tutor sin ayuda.

La consigna de la materia dice que cada estudiante debe ser capaz de explicar el
funcionamiento y justificar las decisiones de diseño de lo que entregó. Un cambio que
funciona pero que nadie del equipo puede explicar es un cambio que todavía no está listo,
por más que los tests pasen.

## Entrada

Antes de escribir nada, leé:

1. El diff completo del cambio (`git diff main...HEAD`).
2. El `AGENTS.md` del repositorio, para ubicar los archivos tocados dentro del mapa.
3. La issue asociada, sobre todo sus criterios de aceptación.

Si el diff toca archivos que no aparecen en el mapa de `AGENTS.md`, decilo: o el mapa quedó
viejo, o el cambio está tocando algo que no le corresponde. Las dos cosas importan.

## Salida

Usá exactamente estas cuatro secciones, en este orden:

```markdown
**Qué cambió**

**Por qué**

**Ventajas y desventajas**

**Mejoras posibles**
```

### Qué cambió

Los cambios reales, en lenguaje llano. Nombrá archivos y funciones concretas. Si el cambio
tiene varias partes, ordenalas por importancia, no por orden alfabético de archivo.

No describas el diff línea por línea: describí el cambio como unidad. "Se agregó validación
del handle en el registro" es útil; "se modificó `users/schemas.py` línea 42" no.

### Por qué

Por qué está hecho así y no de otra forma. Anclalo en algo concreto: un criterio de
aceptación de la issue, una regla del `AGENTS.md`, una decisión ya registrada como ADR.

Si una parte del cambio no responde a ninguna de esas tres cosas, decilo. Puede ser una
decisión legítima que todavía no se documentó, y esa es información valiosa.

### Ventajas y desventajas

Toda decisión tiene un costo. Nombralo.

Si escribís esta sección y no encontrás ninguna desventaja, no terminaste de pensarlo. Las
desventajas típicas en este proyecto: acopla dos módulos que estaban sueltos, agrega una
consulta más a la base por request, hace más difícil testear otra parte, deja un caso borde
sin cubrir a propósito.

### Mejoras posibles

Qué quedó afuera a propósito y qué se haría con más tiempo. Distinguí entre lo que falta
porque se decidió no hacerlo, y lo que falta porque no se llegó. Son cosas distintas y el
tutor va a preguntar por las dos.

## Nivel de la explicación

Escribí para alguien del equipo que no tocó este código y está aprendiendo. Concretamente:

- **Cero jerga sin definir.** Si aparece "idempotencia", "outbox" o "cursor pagination",
  explicá en media línea qué significa acá antes de seguir.
- **Mostrá el camino que sigue un dato.** Es más fácil entender "el request entra por el
  router, valida el esquema, llama al servicio, el servicio escribe en la base" que una
  descripción abstracta de la arquitectura.
- **Si algo del cambio es sutil, decí explícitamente que es sutil.** Lo que a vos te parece
  obvio es exactamente lo que la otra persona va a pasar por alto en la revisión.
- **No adornes.** Si el cambio es simple, la explicación es corta. Una explicación inflada
  esconde que no se entendió tanto como una vacía.

## Ejemplo

**Entrada:** un PR que agrega el like a un post (E2-H6).

**Salida:**

> **Qué cambió**
>
> Se agregó el endpoint `POST /posts/{id}/likes` en `routes/likes.py` y su lógica en
> `services/likes.py`. Hay una tabla nueva `post_likes` con clave primaria compuesta
> `(user_id, post_id)`, creada en la migración `0007_post_likes.py`. El contador
> `likes_count` de la tabla `posts` se actualiza en la misma transacción que el insert.
>
> **Por qué**
>
> La clave primaria compuesta es lo que cumple el CA.3 de la historia, que pide que el
> backend garantice que no existan likes duplicados. Con esa restricción, un segundo like
> del mismo usuario falla en la base y no hace falta chequear antes de insertar, que sería
> una consulta más y dejaría una ventana para que dos requests simultáneos pasen los dos.
>
> El contador se actualiza en la misma transacción porque si se actualizara aparte, un
> crash entre las dos operaciones dejaría el número mal para siempre.
>
> **Ventajas y desventajas**
>
> La ventaja es que la base garantiza la regla, no el código: no hay forma de saltearla
> desde otro endpoint que se escriba más adelante.
>
> La desventaja es que el contador en la tabla `posts` es dato duplicado. Si algún día
> alguien inserta en `post_likes` sin pasar por este servicio, el contador queda desfasado
> y no hay nada que lo detecte. La alternativa era contar con `COUNT(*)` en cada lectura,
> que nunca se desfasa pero hace lenta la carga del feed, que es la pantalla más usada.
>
> **Mejoras posibles**
>
> Quedó afuera a propósito la notificación al autor del post: es la historia E4-H2 y va en
> otro sprint. El endpoint ya publica el evento `interaction.created`, así que cuando esa
> historia se implemente no hay que tocar este código.
>
> No se llegó a agregar un job que recalcule los contadores. Con el volumen del proyecto no
> hace falta, pero es lo primero que agregaría si apareciera un desfasaje.

## Cuándo esta skill dice que algo no está listo

Frená y avisale a la persona si al escribir la explicación aparece alguna de estas señales:

- No podés explicar por qué un archivo del diff cambió.
- Aparece una librería o un patrón que no estaba en el repo y no hay ADR que lo respalde.
- Un criterio de aceptación de la issue no tiene ninguna parte del diff que lo cubra.
- La explicación de "por qué" termina siendo "porque así funciona".

Ninguna de esas cosas se arregla escribiendo mejor la explicación. Se arreglan volviendo al
código.
