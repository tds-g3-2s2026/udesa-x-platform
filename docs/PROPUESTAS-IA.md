# Propuestas de funcionalidad de IA

**Fecha:** 2026-10-17 · **Estado:** para acordar con el tutor el 2026-10-19 · **Issue:**
`udesa-x-platform#88` (`AI-01`)

## Contexto

La consigna pide **al menos una funcionalidad que integre IA, acordada con el tutor**, y la
pone entre las condiciones de aprobación (`CONSIGNA.md`, "Inteligencia Artificial"). No le
asigna puntos: si se descuentan o no del alcance optativo es la decisión abierta `D9`.

El cronograma de la cátedra marca el lunes 19 de octubre, clase de AI Engineering II, como
inicio de la implementación, y el 26 de octubre como presentación formal de la propuesta. El
plan pone el spike en S8 (`AI-02`, `AI-03`) y la implementación en S10 (`AI-04` a `AI-06`).

`PLANIFICACION.md` propone el triage asistido de denuncias y lista tres alternativas. Este
documento las revisa con una restricción que el plan no tenía, que no le cueste plata al
equipo, y con una medición preliminar de los modelos sobre datos sintéticos.

## Sin costo para el equipo

No sabemos si la cátedra da créditos para APIs de modelos, así que las propuestas no dependen
de eso: usan modelos abiertos que corren dentro del namespace `tds-group-3`. Eso cambia lo que
fijaban `ARQUITECTURA.md` y `PLANIFICACION.md` (Claude API con `claude-haiku-4-5`), y el
cambio se registra en el ADR de `AI-02`. Tiene además una ventaja: ningún dato sale a un
tercero, así que la privacidad no depende de la política de retención de un proveedor.

Hay dos tipos de modelo a mano, y ninguno necesita GPU:

- **Un modelo de embeddings multilingüe**, `multilingual-e5-small` (licencia MIT). Convierte un
  texto en un vector que representa de qué habla, de modo que dos textos sobre lo mismo quedan
  cerca aunque usen otras palabras.
- **Un LLM chico para generar o clasificar texto**, por ejemplo Qwen3 de 1.700 millones de
  parámetros (Apache 2.0), servido con llama.cpp.

## Medición preliminar (2026-10-17)

Antes de recomendar, se midieron los modelos en una computadora del equipo, limitando el
proceso a uno o dos hilos de CPU para parecerse al namespace. Los datos son sintéticos: 3 hilos
con 55 respuestas cuyas posturas se etiquetaron a mano, y 30 posts sueltos de 5 temas. Los
scripts y los datos se versionan en `AI-03`. El índice de Rand ajustado (ARI) mide cuánto
coincide un agrupamiento con el etiquetado: 1 es perfecto y 0 es lo mismo que al azar.

| Qué se midió | Resultado |
|---|---|
| `multilingual-e5-small` cuantizado a int8 | 113 MB en disco, unos 385 MB de RAM, 4 ms por texto con un hilo |
| Temas entre posts sueltos, la base del feed "Para vos" | De los 5 posts más parecidos a cada uno, 0,52 son de su mismo tema; al azar sería 0,17 |
| Posturas dentro de un hilo, con embeddings | ARI medio de 0,15 en el mejor de tres modelos, y nunca más de 0,32 en un hilo |
| Posturas dentro de un hilo, con Qwen3 de 1.700 millones | ARI medio de 0,20; 30 segundos por hilo; 2,2 GB de RAM |

Dos conclusiones. Los embeddings encuentran bien de qué habla un post completo, pero no la
postura de una respuesta corta: "sí, por favor" y "no, mejor no" hablan de lo mismo. Y el LLM
chico propone bien cuáles son las posturas de un hilo, pero no asigna cada respuesta a la suya
con la confianza necesaria.

## Qué le pedimos a la cátedra

La cuota actual (`k8s/namespace.yaml`) limita cada contenedor a 500m de CPU y 512Mi de memoria,
y el namespace entero a 4 CPU, 4Gi de memoria y 4 `Service`, los cuatro ya en uso.

| Recurso | Hoy | Para la propuesta 1 | Si se elige la propuesta 2 |
|---|---|---|---|
| Memoria máxima por contenedor | 512Mi | 1Gi, para `posts-api` con el modelo de embeddings | 3Gi, para el servidor del LLM |
| CPU máxima por contenedor | 500m | Sin cambio | 2 |
| Memoria y CPU del namespace | 4Gi y 4 | Sin cambio | 8Gi y 6 |
| `Service` | 4 | 6 | 7 |

Los dos `Service` extra de la propuesta 1 no son de IA: la cola que exige la consigna
(RabbitMQ) y `notifications-api` los necesitan igual. La propuesta 2 suma uno para el servidor
del LLM.

## Propuesta 1: feed "Para vos" explicable

**Qué hace.** Una segunda pestaña del feed, junto al cronológico, con posts de cualquier
cuenta visible ordenados según cuánto se parecen a lo que el usuario likeó. Cada post dice por
qué aparece: "Parecido a un post que te gustó", con el enlace a ese post.

**Por qué vale la pena.** Es el centro del producto de una red como X, y la explicación es lo
que la distingue. La Ley de Servicios Digitales de la Unión Europea (artículo 27) les exige a
las plataformas explicar los parámetros principales de sus sistemas de recomendación. Acá se
explica cada post.

**Dónde corre.** En `posts-api`. El vector de cada post se calcula al publicarlo, en segundo
plano, con `multilingual-e5-small`, y se guarda junto al post. Un endpoint nuevo del estilo de
`GET /api/feed/for-you` compara los posts recientes que el usuario puede ver (`visible_to`) con
los últimos que likeó (los likes entraron con `posts-api#90`) y combina parecido con
antigüedad. No necesita LLM.

**Qué entra y qué sale.** Entran los posts y los likes, que ya están en la base y nunca salen
del cluster. Sale una página del feed donde cada post trae el post likeado que lo explica.

**Recursos.** Medidos: 4 ms por post con un hilo y unos 385 MB de RAM para el modelo. Por eso
el contenedor de `posts-api` tiene que pasar de 512Mi a 1Gi.

**Riesgo principal: la calidad con pocos datos.** En la medición, la mitad de los posts más
parecidos eran del mismo tema: es tres veces mejor que el azar, pero no perfecto. Un usuario
sin likes no tiene a qué parecerse, así que arranca con las cuentas populares de
`/users/suggested`, y ordenar solo por parecido lo encierra en lo que ya le gusta, por eso se
mezcla una parte de posts populares. La demo depende de que el generador de datos de `T-39`
cree posts de temas variados. Es la más grande de las dos, así que para S10 se acota a lo
mínimo: el orden y la explicación, sin ajustes por usuario.

**Criterio de éxito.** Sobre datos generados, esconder una parte de los likes y medir cuántos
de esos posts aparecen entre los primeros 20 del feed "Para vos", contra el cronológico.

**Falta para arrancar.** Los likes ya están en `main`. El generador de datos de `T-39` es de
S8 y no arrancó; si no llega, `AI-03` genera su propio set chico.

## Propuesta 2: triage asistido de denuncias

**Qué hace.** Es la propuesta original de `PLANIFICACION.md`, con el modelo corriendo en el
cluster. Cuando se denuncia un post (E3-H5), el LLM sugiere una categoría entre las cuatro de
E3-H5 CA.1, una severidad, una justificación breve y un nivel de confianza. Con embeddings se
suman los precedentes: las denuncias ya resueltas más parecidas y lo que se decidió en cada
una. La bandeja del backoffice (E5-H7) ordena por severidad, el moderador decide y su decisión
queda registrada junto a la sugerencia. La IA nunca sanciona.

**Dónde corre.** Como fija `ARQUITECTURA.md`: un consumidor de `report.created` dentro de
`notifications-api` llama al servidor del LLM. Como el trabajo es asincrónico, que tarde unos
segundos en CPU no afecta a nadie. Los precedentes los busca `posts-api` al armar la bandeja.

**Qué entra y qué sale.** Entran el texto del post denunciado y el motivo, que nunca salen del
cluster. Sale un JSON con `category`, `severity`, `justification` y `confidence`, más los
precedentes. E3-H5 denuncia a un usuario y el post es opcional (`post_id` puede ser nulo en
`reports`): una denuncia sin post queda sin sugerencia.

**Riesgo principal: es la que más depende de piezas que no existen.** Hoy `posts-api` no
publica ningún evento, `notifications-api` no tiene código, la cola no entra en la cuota actual
y la bandeja del backoffice muestra datos de prueba porque E5-H7 es de S9. Además, la medición
de posturas muestra que un LLM chico clasifica de forma poco confiable; la severidad no se
midió todavía.

**Criterio de éxito.** La coincidencia entre la sugerencia y la decisión del moderador, que se
puede medir porque las dos quedan registradas.

## Probada y descartada: mapa de la conversación

Era la recomendación de la primera versión de este documento: agrupar las respuestas de un
hilo largo por postura, con una respuesta real de cada grupo y, si había LLM, un resumen por
grupo. La medición lo descarta con los modelos a nuestro alcance: los embeddings no distinguen
posturas y el LLM chico las asigna casi al azar. Haría falta un modelo bastante más grande, con
más memoria, y sin garantía de que alcance. Se puede revisar si la cátedra da créditos para una
API comercial.

## Alternativas descartadas

- **Detección de idioma para el filtro del feed.** Una librería lo resuelve sin IA (`D16`).
- **Recomendación de cuentas en el onboarding.** E1-H14 CA.3 pide sugerir cuentas populares, y
  `GET /api/users/suggested` ya las devuelve.

## Comparación

| | Feed "Para vos" | Triage asistido |
|---|---|---|
| Se apoya en | Likes y feed | E3-H5 y E5-H7, obligatorias |
| Modelos | Embeddings | LLM y embeddings |
| Medición preliminar | Base medida: 0,52 contra 0,17 al azar | Sin medir; el LLM chico clasificó mal posturas |
| Pedido de cuota | 1Gi para `posts-api` | Servidor de 3Gi y 2 CPU, y un `Service` |
| Falta para arrancar | Datos de `T-39` | Cola, `report.created`, E5-H7 y el servidor del LLM |
| Tamaño | Grande, acotado a lo mínimo | Grande |

## Recomendación

**La propuesta 1, el feed "Para vos" explicable**, como funcionalidad comprometida para S10.
Es la única con una base medida, no necesita LLM, así que no puede inventar contenido, pide
la menor ampliación de cuota y no depende de la cola ni de la bandeja de denuncias. La
explicación de cada post le da algo para defender más allá de que funcione.

Si el tutor prefiere apoyarse en historias obligatorias, la propuesta 2, sabiendo que antes
hay que medir la severidad con el LLM.

## Preguntas para el tutor

1. ¿Cuál de las dos propuestas?
2. ¿Pueden ampliar la cuota del namespace como detalla "Qué le pedimos a la cátedra"? Dos de
   los `Service` hacen falta igual para la cola que exige la consigna.
3. ¿La cátedra da créditos para usar APIs de modelos? Con un modelo comercial se podría
   retomar el mapa de la conversación.
4. `D9`: ¿la funcionalidad de IA suma puntos o se descuenta del alcance optativo?

## Decisión

Se completa después de la reunión del 2026-10-19.
