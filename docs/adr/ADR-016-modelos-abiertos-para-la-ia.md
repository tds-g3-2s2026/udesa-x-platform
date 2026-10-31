# ADR-016: modelos abiertos dentro del cluster para la funcionalidad de IA

**Fecha:** 2026-10-17 · **Estado:** propuesta, no se aceptó. Reemplazada por el ADR-023 ·
**Decide:** el equipo, con el tutor

## Contexto

`ARQUITECTURA.md` ("Integración de Inteligencia Artificial") y `PLANIFICACION.md` fijaron en
agosto la API de Claude con `claude-haiku-4-5` para el triage de denuncias, con la clave de API
guardada como Sealed Secret. Esa elección supone pagar por uso, y no sabemos si la cátedra da
créditos para APIs de modelos. El equipo no va a poner plata.

`docs/PROPUESTAS-IA.md` (`AI-01`) rearma las propuestas con modelos abiertos que corren en el
cluster: un mapa de la conversación con resumen por postura, un feed "Para vos" explicable y el
triage asistido de denuncias. Las tres usan los mismos dos tipos de modelo, así que esta
decisión vale para cualquiera que elija el tutor. Es la entrega de `AI-02`
(`udesa-x-platform#90`).

La cuota actual del namespace (`k8s/namespace.yaml`) limita cada contenedor a 500m de CPU y
512Mi de memoria y ya usa los cuatro `Service` que permite. El documento de propuestas incluye
un pedido de ampliación a la cátedra.

## Decisión

**La funcionalidad de IA usa modelos abiertos que corren dentro del namespace `tds-group-3`.
Ningún texto de usuario sale del cluster hacia un proveedor de modelos, y el equipo no paga por
uso.**

- **Embeddings dentro de `posts-api`.** Un modelo multilingüe chico, cuantizado a int8 y
  ejecutado con ONNX Runtime (`onnxruntime`) y el tokenizador de Hugging Face (`tokenizers`),
  sin PyTorch. La elección inicial es `intfloat/multilingual-e5-small` (MIT), con
  `paraphrase-multilingual-MiniLM-L12-v2` (Apache 2.0) como alternativa. Corre en el servicio
  dueño de los posts porque el vector se calcula sobre su texto y se guarda junto a él, y así
  funciona aunque no se amplíe la cuota.
- **Los vectores se guardan en la base de `posts-api` como arreglos.** Con el volumen del
  proyecto alcanza con compararlos en memoria, sin `pgvector`. Si la prueba de carga muestra lo
  contrario, RDS para PostgreSQL ofrece `pgvector` y el cambio es acotado.
- **El LLM corre en un servidor de modelos propio:** un `Deployment` nuevo con `llama-server`
  de llama.cpp (MIT), que expone una API HTTP y corre modelos cuantizados en CPU. La elección
  inicial es Qwen3 de 1.700 millones de parámetros (Apache 2.0), cuantizado a 4 bits y en modo
  sin razonamiento. Si la calidad no alcanza y la memoria lo permite, se pasa a Qwen3 de 4.000
  millones. Solo lo llaman los servicios que lo necesitan, a través de un `Service` interno y
  una `NetworkPolicy` que no deja entrar a nadie más. Depende del pedido de cuota.
- **Si se elige el mapa de la conversación, el agrupamiento usa scikit-learn (BSD-3).** HDBSCAN
  agrupa sin fijar de antemano cuántas posturas hay, y deja aparte las respuestas que no encajan
  en ninguna, como "jaja".
- **Los pesos de cada modelo se fijan por versión y hash en la imagen**, para que el modelo no
  cambie sin un commit.
- **El checkpoint exacto de cada modelo se fija en el documento de resultados de `AI-03`**, con
  las mediciones que lo justifican. Cambiar de familia de modelo o de lugar de ejecución es un
  ADR nuevo.

## Qué datos procesa cada propuesta

El modelo recibe texto, nunca identidades: no le llega ningún id, handle, nombre, email, foto ni
dato de cuenta. Las menciones dentro del texto (`@handle`) se reemplazan por un marcador antes de
pasárselo, para que un resumen no nombre a nadie.

| Propuesta | Llega al modelo | No llega nunca |
|---|---|---|
| Mapa de la conversación | El texto de cada respuesta, para su vector, y el de las respuestas públicas de un grupo, para su resumen | El autor de cada respuesta. Las respuestas de cuentas protegidas, en los resúmenes |
| Feed "Para vos" | El texto de cada post, para su vector | Likes, seguidos y datos del usuario: el parecido se calcula en `posts-api` con vectores ya guardados |
| Triage asistido | El texto del post denunciado y el motivo elegido | Denunciante, denunciado, su perfil y su historial |

## Privacidad y retención

- **Nada sale del cluster.** El servidor de modelos no tiene salida a internet y se configura
  para no registrar los pedidos: recibe texto, responde y no guarda nada.
- **Ningún texto de usuario va a los logs ni a las trazas.** Los logs y las trazas se envían a
  Grafana Cloud (ADR-013), que es un tercero. Solo se registran ids, duración y tamaño de cada
  llamada.
- **Lo derivado se borra con su origen.** Cuando se borra un post o una respuesta (política de
  borrado de publicaciones, `udesa-x-platform#93`), se borra su vector y se invalidan los
  resúmenes de su hilo, porque un resumen escrito con una respuesta borrada seguiría mostrando
  lo que decía. El borrado de cuentas sigue la misma regla cuando se defina (`D19`).
- **Lo generado se muestra como generado.** El triage nunca sanciona: la decisión es siempre de
  una persona y queda registrada junto a la sugerencia.

## Si algo sale mal

- **Un resumen o una sugerencia indebida.** Una variable de configuración apaga la generación
  sin cambiar código, y los resúmenes guardados se borran. El mapa y el feed siguen
  funcionando sin el LLM.
- **El servidor de modelos se cae o tarda.** Las llamadas tienen tiempo límite y lo que depende
  del LLM degrada: el mapa se muestra sin resúmenes y la denuncia entra sin sugerencia. Nada que
  vea el usuario espera al LLM.
- **Un texto de usuario aparece en un log.** Es un defecto: se corrige el punto que lo registró
  y se suma un test que lo cubra.

## Lo que mide `AI-03` antes de implementar

- La memoria de `posts-api` con el modelo de embeddings cargado: tiene que entrar en 512Mi, o
  el pedido de cuota tiene que cubrir el aumento.
- La memoria y la latencia del servidor de modelos con cada tamaño de Qwen3, que confirman el
  pedido de cuota.
- La calidad sobre datos sintéticos, con el criterio de éxito de la propuesta elegida.

## Alternativas descartadas

- **La API de Claude, el plan original.** Da mejor calidad y no necesita infraestructura
  propia, pero se paga por uso y no sabemos si hay créditos. Si la cátedra los da, se reevalúa
  con un ADR nuevo.
- **Capas gratuitas de proveedores que sirven modelos abiertos.** No cuestan, pero tienen
  límites de uso que pueden cambiar, algunas condiciones permiten usar los datos, y el texto
  saldría del cluster. Solo como respaldo y con un ADR nuevo.
- **Ollama en lugar de llama.cpp.** Facilita descargar y cambiar de modelo, algo que acá no
  hace falta porque el modelo queda fijo en la imagen.
- **PyTorch con `sentence-transformers` para los embeddings.** Es lo más común, pero PyTorch
  agranda la imagen y la memoria del contenedor, y ONNX Runtime corre el mismo modelo con mucho
  menos.
- **Embeddings también en el servidor de modelos.** Concentraría todo en un lugar, pero el mapa
  y el feed dejarían de funcionar si la cátedra no amplía la cuota.
- **vLLM.** Está pensado para GPU y en CPU no compensa.

## Consecuencias

- Reemplaza la elección de la API de Claude en la tabla de IA de `ARQUITECTURA.md` y el costo
  estimado de `PLANIFICACION.md`. Desaparece la clave de API como Sealed Secret: no hay clave.
- `posts-api` suma `onnxruntime` y `tokenizers` (y `scikit-learn` si se elige el mapa), una
  columna o tabla para los vectores, y unos 120 MB de modelo en la imagen.
- El namespace suma un `Deployment` y un `Service` para el servidor de modelos, que entran
  solo si se amplía la cuota.
- La calidad depende de modelos chicos. Por eso nada de lo generado decide sin una persona o
  sin poder contrastarse con contenido real.
- `AI-03` deja de medir costo por llamada y pasa a medir memoria, latencia y calidad.
