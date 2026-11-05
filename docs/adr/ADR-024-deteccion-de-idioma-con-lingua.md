# ADR-024: `lingua-language-detector` para detectar el idioma de los posts

**Fecha:** 2026-11-05 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

`E.1 H7 CA.2` deja elegir el idioma del feed, pero el feed no filtra: `posts-api` no sabe en qué
idioma está cada post (`D16`, `T-35`, `udesa-x-posts-api#127`). Hay que detectarlo al publicar,
sin servicios externos, y guardarlo como `es`, `en` u `other`. Lo que no se puede clasificar se
muestra siempre, así que el error caro es clasificar mal, no dejar un post en `other`. La regla
de simplicidad de los `AGENTS.md` pide un ADR aprobado antes de sumar una librería.

## Decisión

**`lingua-language-detector` en `posts-api`**, con estas condiciones:

- **Seis idiomas:** español, inglés, portugués, francés, italiano y alemán. Hacen falta más que
  los dos que se filtran: con solo español e inglés, un texto en francés sale inglés con
  confianza 1,0 y nunca se llegaría a `other`.
- **Modo de baja precisión**, que usa los modelos más chicos y alcanza para textos de post.
- **Umbral de confianza de 0,6:** por debajo, o si el idioma más probable no es español ni
  inglés, el post queda `other`.
- **La preferencia del lector llega por el evento `preferences.changed.v1`**, que `posts-api`
  copia en `user_profiles`. Quien cambia el idioma espera ver el efecto al volver al feed: un
  claim en el JWT tardaría hasta 15 minutos, y preguntar a `users-api` sumaría una llamada a cada
  pedido de feed.

Se probó con 19 textos cortos en español, inglés y otros idiomas. Es una muestra chica, útil para
comparar opciones y no como medición de precisión:

| Opción | Mal clasificados como `es` o `en` | Español o inglés que quedan en `other` | Memoria | Tamaño instalado |
|---|---|---|---|---|
| `lingua`, 6 idiomas, baja precisión | 0 | 1 de 8 | +11 MiB | 291 MB |
| `lingua`, 6 idiomas, alta precisión | 1 (`jaja`) | 3 de 8 | +10 MiB | 291 MB |
| `lingua`, todos los idiomas, alta precisión | 0 | 5 de 8 | +55 MiB | 291 MB |

## Alternativas descartadas

- **`langdetect`.** Pesa 2,4 MB, pero es aleatoria si no se fija una semilla y falla más en textos
  cortos: `Qué partido!` salió portugués, y `hola` salió galés con confianza 0,99.
- **Un servicio externo o el modelo de IA del ADR-023.** Agrega una llamada de red y un costo a
  cada post para una tarea que se resuelve localmente en menos de un milisegundo.

## Consecuencias

- La imagen de `posts-api` crece unos 291 MB: el paquete trae los modelos de todos los idiomas
  aunque se usen seis.
- Los posts anteriores quedan sin idioma y se muestran siempre: no se reprocesan.
- Las cuentas que ya habían elegido un idioma antes de este cambio no tienen copia en `posts-api`
  hasta que vuelvan a cambiarlo: mientras tanto ven todos los idiomas.
- El filtro depende de RabbitMQ en el cluster. Si el broker no está, el cambio de idioma espera en
  la `outbox` de `users-api` y el feed sigue con la preferencia anterior.
- Resuelve `D16`.
