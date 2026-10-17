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
documento las revisa con una restricción que el plan no tenía: que no le cueste plata al
equipo. Los modelos son abiertos y corren en el cluster de la cátedra. Lo que hace falta es
cuota, y la sección "Qué le pedimos a la cátedra" la detalla.

## Sin costo para el equipo

No sabemos si la cátedra da créditos para APIs de modelos, así que las propuestas no dependen
de eso: usan modelos abiertos que corren dentro del namespace `tds-group-3`. Eso cambia lo que
fijaban `ARQUITECTURA.md` y `PLANIFICACION.md` (Claude API con `claude-haiku-4-5`), y el
cambio se registra en el ADR de `AI-02`. Tiene además una ventaja: ningún dato sale a un
tercero, así que la privacidad no depende de la política de retención de un proveedor.

Se usan dos tipos de modelo. Ninguno necesita GPU.

- **Un modelo de embeddings multilingüe**, por ejemplo `multilingual-e5-small` (licencia MIT)
  o `paraphrase-multilingual-MiniLM-L12-v2` (Apache 2.0). Tiene unos 118 millones de
  parámetros y ocupa del orden de 120 MB cuantizado a int8. Convierte un texto en un vector que
  representa lo que dice, de modo que dos frases distintas que dicen lo mismo quedan cerca. Es
  lo que no se puede hacer con reglas ni con búsqueda por palabras. En CPU tarda decenas de
  milisegundos por texto.
- **Un LLM chico para generar texto**: un modelo abierto de entre 1.000 y 4.000 millones de
  parámetros, por ejemplo de la familia Qwen3 (Apache 2.0), servido con un servidor de modelos
  abierto como llama.cpp. Cuantizado ocupa entre 1 y 3 GB, y en CPU escribe una oración en
  segundos. Por eso se usa solo en tareas en segundo plano, nunca mientras el usuario espera.

El modelo concreto se elige en `AI-02` y las mediciones de memoria y latencia son de `AI-03`.
Si no se pudiera correr el LLM en el cluster, algunas APIs ofrecen capas gratuitas de modelos
abiertos, con límites de uso y condiciones sobre los datos que habría que revisar en `AI-02`.
Es la opción de respaldo, no la principal.

## Qué le pedimos a la cátedra

La cuota actual (`k8s/namespace.yaml`) limita cada contenedor a 500m de CPU y 512Mi de memoria,
y el namespace entero a 4 CPU, 4Gi de memoria y 4 `Service`. Los cuatro `Service` ya están en
uso: Redis, `users-api`, `posts-api` y el gateway. El modelo de embeddings entra en un
contenedor de ese tamaño. El LLM no.

Pedido estimado, a confirmar con las mediciones de `AI-03`:

| Recurso | Hoy | Pedido | Para qué |
|---|---|---|---|
| Memoria por contenedor | 512Mi | 3Gi | Servidor de modelos, con el LLM y los embeddings |
| CPU por contenedor | 500m | 2 | Servidor de modelos |
| Memoria del namespace (límite) | 4Gi | 8Gi | Servidor de modelos, RabbitMQ y `notifications-api` |
| CPU del namespace (límite) | 4 | 6 | Servidor de modelos, RabbitMQ y `notifications-api` |
| `Service` | 4 | 7 | Servidor de modelos, RabbitMQ y `notifications-api` |

Dos de los tres `Service` nuevos no son de IA: la cola que exige la consigna (RabbitMQ) y
`notifications-api` los necesitan igual. Los 8 pods de la cuota alcanzan.

**Si la cátedra no puede ampliar la cuota**, la propuesta 1 sin resúmenes y la propuesta 2
entran igual, con el modelo de embeddings dentro del pod de `posts-api`. La propuesta 3 pierde
la justificación escrita y queda solo con precedentes.

## Propuesta 1: mapa de la conversación con resumen por postura

**Qué hace.** En el detalle de un post con muchas respuestas (E2-H4), la app muestra la
conversación agrupada en posturas: "En este hilo hay tres posturas". Cada grupo indica cuántas
respuestas tiene y muestra textual la que mejor lo representa. Tocar un grupo filtra el hilo a
esas respuestas. Agrupa por lo que dicen las respuestas, no por las palabras que usan: "no
llego con el TP" y "me falta un montón para la entrega" quedan juntas.

Con el LLM, cada postura suma un título corto y un resumen de una oración, escritos solo a
partir de las respuestas de ese grupo. Se marcan como generados, y las respuestas en las que se
basan quedan a un toque.

**Por qué no inventa.** El resumen no es de todo el hilo sino de cada grupo, y se muestra al
lado de una respuesta real del grupo, así que quien lee lo puede contrastar. Sin el LLM, el
mapa funciona igual, solo con citas. La idea viene de herramientas de deliberación como Polis,
usada en consultas públicas de Taiwán (vTaiwan), que muestran los grupos de opinión de una
conversación en lugar de un único resumen. Acá el agrupamiento sale del texto.

**Dónde corre.** En `posts-api`. El vector de cada respuesta se calcula al publicarla, en
segundo plano, y se guarda. El agrupamiento se calcula a pedido sobre las respuestas que quien
pide puede ver (`visible_to`), con un endpoint nuevo del estilo de
`GET /api/posts/{id}/conversation-map`. Los resúmenes los genera el servidor de modelos en
segundo plano, cuando un hilo llega al mínimo de respuestas o recibe respuestas nuevas, y se
guardan.

**Qué entra y qué sale.** Entra el texto de las respuestas, que nunca sale del cluster. Sale
la lista de grupos, cada uno con su tamaño, los ids de sus respuestas y cuál es la
representativa, más el título y el resumen cuando existen.

**Riesgo principal: la calidad en textos cortos.** Respuestas como "jaja" o "esto" no tienen
postura, la ironía engaña a cualquier modelo de este tamaño, y un LLM chico resume peor en
español que uno grande. Se mitiga con un mínimo de respuestas para mostrar el mapa (por
ejemplo 10), dejando afuera las respuestas sin contenido y midiendo las dos cosas antes de
comprometerlas. Además, cada usuario ve un hilo distinto según bloqueos y cuentas protegidas:
el resumen se genera solo con respuestas públicas, y si quien mira bloqueó a alguien de un
grupo, ese grupo se muestra sin resumen.

**Criterio de éxito.** Dos números, medidos en `AI-03` sobre hilos sintéticos. Para el
agrupamiento, la coincidencia con un etiquetado a mano (índice de Rand ajustado). Para los
resúmenes, la proporción de resúmenes que afirman algo que no está en las respuestas del grupo,
revisada a mano.

**Falta para arrancar.** Las respuestas (E2-H4) y la pantalla de detalle de la app ya están en
`main`. La versión con citas no depende de nada más, y los resúmenes dependen del servidor de
modelos. Suma librerías nuevas, así que lleva su ADR.

## Propuesta 2: feed "Para vos" explicable

**Qué hace.** Una segunda pestaña del feed, junto al cronológico, con posts de cualquier
cuenta visible ordenados según cuánto se parecen a lo que el usuario likeó. Cada post dice por
qué aparece: "Parecido a un post que te gustó", con el enlace a ese post.

**Por qué vale la pena.** Es el centro del producto de una red como X, y la explicación es lo
que la distingue. La Ley de Servicios Digitales de la Unión Europea (artículo 27) les exige a
las plataformas explicar los parámetros principales de sus sistemas de recomendación. Acá se
explica cada post.

**Dónde corre.** En `posts-api`, con un vector por post calculado igual que en la propuesta 1.
Un endpoint nuevo del estilo de `GET /api/feed/for-you` compara los posts recientes que el
usuario puede ver con los últimos que likeó (los likes entraron con `posts-api#90`) y combina
parecido con antigüedad. Entra en la cuota actual.

**Qué entra y qué sale.** Entran los posts y los likes, que ya están en la base. Sale una
página del feed donde cada post trae el post likeado que lo explica.

**Riesgo principal: necesita volumen para verse bien.** Un usuario sin likes no tiene a qué
parecerse, así que arranca con las cuentas populares de `/users/suggested`. Ordenar solo por
parecido encierra al usuario en lo que ya le gusta, por eso se mezcla una parte de posts
populares. La demo depende de que el generador de datos de `T-39` cree posts de temas
variados.

**Criterio de éxito.** Sobre los datos generados, esconder una parte de los likes y medir
cuántos de esos posts aparecen entre los primeros 20 del feed "Para vos", contra el feed
cronológico.

**Falta para arrancar.** Los likes ya están en `main`. El generador de datos de `T-39` es de
S8 y no arrancó.

## Propuesta 3: triage asistido de denuncias

**Qué hace.** Es la propuesta original de `PLANIFICACION.md`, con el modelo corriendo en el
cluster. Cuando se denuncia un post (E3-H5), el LLM sugiere una categoría entre las cuatro de
E3-H5 CA.1, una severidad, una justificación breve y un nivel de confianza. Con embeddings se
suman los precedentes: las denuncias ya resueltas más parecidas y lo que se decidió en cada
una. La bandeja del backoffice (E5-H7) ordena por severidad, el moderador decide y su decisión
queda registrada junto a la sugerencia. La IA nunca sanciona.

**Dónde corre.** Como fija `ARQUITECTURA.md`: un consumidor de `report.created` dentro de
`notifications-api` llama al servidor de modelos. Como el trabajo es asincrónico, que el LLM
tarde unos segundos en CPU no afecta a nadie. Los precedentes los busca `posts-api` al armar la
bandeja.

**Qué entra y qué sale.** Entran el texto del post denunciado y el motivo, que nunca salen del
cluster. Sale un JSON con `category`, `severity`, `justification` y `confidence`, más los
precedentes. E3-H5 denuncia a un usuario y el post es opcional (`post_id` puede ser nulo en
`reports`): una denuncia sin post queda sin sugerencia.

**Riesgo principal: es la que más depende de piezas que no existen.** Hoy `posts-api` no
publica ningún evento, `notifications-api` no tiene código (`T-03` y `T-27`, en S8), la cola no
entra en la cuota actual y la bandeja de moderación del backoffice muestra datos de prueba
porque E5-H7 es de S9. Además, los precedentes sirven recién cuando hay denuncias resueltas, así
que al principio se siembran casos sintéticos.

**Criterio de éxito.** La coincidencia entre la sugerencia y la decisión del moderador, que se
puede medir porque las dos quedan registradas.

## Alternativas descartadas

- **Detección de idioma para el filtro del feed.** Una librería lo resuelve sin IA (`D16`).
- **Recomendación de cuentas en el onboarding.** E1-H14 CA.3 pide sugerir cuentas populares, y
  `GET /api/users/suggested` ya las devuelve.

## Comparación

| | Mapa con resumen | Feed "Para vos" | Triage asistido |
|---|---|---|---|
| Se apoya en | E2-H4, obligatoria | Likes y feed | E3-H5 y E5-H7, obligatorias |
| Modelos | Embeddings, y LLM para los resúmenes | Embeddings | LLM y embeddings |
| Entra en la cuota actual | Sin resúmenes, sí | Sí | No |
| Falta para arrancar | Nada | Datos de `T-39` | Cola, `report.created` y E5-H7 |
| Tamaño | Mediano | Grande | Grande |

## Recomendación

**La propuesta 1 completa, mapa de la conversación con resumen por postura**, como
funcionalidad comprometida para S10, junto con el pedido de cuota para el servidor de modelos.
Junta lo que hace atractivo a un LLM, resumir una conversación larga, con la garantía de que
cada resumen se puede contrastar con respuestas reales. No depende de trabajo pendiente de
nadie y se mide con dos números. Si la cuota no se amplía, la versión con citas entra igual, así
que el compromiso no queda en riesgo. Además deja armado lo que necesita la propuesta 2, un
vector por post, para construir el feed "Para vos" encima si queda tiempo.

## Preguntas para el tutor

1. ¿Cuál de las tres propuestas?
2. ¿Pueden ampliar la cuota del namespace como detalla "Qué le pedimos a la cátedra"? Dos de
   los tres `Service` nuevos hacen falta igual para la cola que exige la consigna.
3. ¿La cátedra da créditos para usar APIs de modelos? Las propuestas no los necesitan, pero
   cambiaría qué LLM conviene usar.
4. `D9`: ¿la funcionalidad de IA suma puntos o se descuenta del alcance optativo?

## Decisión

Se completa después de la reunión del 2026-10-19.
