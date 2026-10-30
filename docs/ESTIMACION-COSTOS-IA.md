# Estimación de costos del asistente por voz

**Fecha:** 2026-10-30 · **Issue:** `udesa-x-platform#118` (`AI-02`) · **Decisión:** ADR-023

Qué modelos de Amazon Bedrock pueden mover el asistente por voz (`PROPUESTAS-IA.md`), cuánto
cuesta cada uno y cómo se elige. La pidió el tutor para justificar el modelo antes de habilitar
Bedrock.

## Cómo se armó la lista de candidatos

Bedrock tiene más de cien modelos. Para este agente sirven los que cumplen todo esto:

1. **Se cobran por token en Ohio**, la región del cluster, o con un perfil de inferencia de
   EE. UU. Nada de capacidad reservada ni de endpoints propios que se pagan por hora.
2. **Funcionan con la API Converse y soportan tool use.** El agente elige acciones de un
   catálogo, y Converse es la misma API para todos los proveedores, así que el modelo queda
   como configuración.
3. **Cuestan hasta USD 0,20 por millón de tokens de entrada y USD 1,20 de salida**, el rango de
   Claude Haiku 5.5 y por debajo. Para elegir entre una docena de acciones simples no hace falta
   un modelo grande, y uno grande cuesta entre 3 y 20 veces más.
4. **Pueden dar la primera respuesta en menos de 1 segundo**, según mediciones públicas, o
   permiten apagar el razonamiento. El objetivo es una mediana de menos de 3 segundos hasta la
   primera acción en pantalla, y cada pedido son varias llamadas al modelo.

De cada familia entra un modelo, salvo Amazon, que entra con los dos por ser los más baratos
del catálogo. Quedan diez candidatos, más Claude Sonnet 5.5, que entra solo como referencia de
lo mejor posible.

| Modelo | Entrada | Salida | Razona | Primera respuesta | Velocidad | Factura |
|---|---:|---:|---|---:|---:|---|
| Amazon Nova Micro | 0,035 | 0,14 | No | 0,83 s | 310 t/s | AWS |
| Amazon Nova Lite | 0,06 | 0,24 | No | sin dato | sin dato | AWS |
| NVIDIA Nemotron Nano 3 30B | 0,06 | 0,24 | Se puede apagar | 0,55 s | 241 t/s | AWS |
| Z.AI GLM 4.7 Flash | 0,07 | 0,40 | No | sin dato | sin dato | AWS |
| Google Gemma 3 12B | 0,09 | 0,29 | No | sin dato | sin dato | AWS |
| Mistral Ministral 3 8B | 0,15 | 0,15 | No | 0,84 s | 98 t/s | AWS |
| OpenAI gpt-oss-120b | 0,15 | 0,60 | Sí, con esfuerzo bajo | 0,75 s | 253 t/s | AWS |
| Qwen3 Next 80B A3B | 0,14 | 1,20 | No (instruct) | 0,89 s | 140 t/s | AWS |
| Meta Llama 4 Scout | 0,17 | 0,66 | No | 0,79 s | 130 t/s | AWS |
| Claude Haiku 5.5 | 0,11 | 0,55 | Se puede apagar | 7,82 s razonando | 166 t/s | Marketplace |
| *Claude Sonnet 5.5 (referencia)* | *2,20* | *11,00* | *Esfuerzo bajo* | *1,26 s* | *108 t/s* | *Marketplace* |

- **Precios:** dólares por millón de tokens, bajo demanda, región Ohio, con el precio dentro de
  EE. UU. y no el global (ver el ADR-023).
- **Primera respuesta y velocidad:** las mide Artificial Analysis con el mismo método para todos
  los modelos, pero no necesariamente sobre Bedrock. Sirven para descartar, no para elegir.
- **Claude Haiku 5.5 razona por defecto**, y así tarda casi 8 segundos en empezar a responder,
  incluso con esfuerzo bajo. Para este agente se prueba con el razonamiento apagado, que Bedrock
  permite.
- **Factura:** Bedrock cobra a Claude como software de AWS Marketplace. Los otros los factura
  AWS directamente, sin suscripción a Marketplace.
- **Tool use:** las fichas de Bedrock lo declaran para todos, pero en varios de los modelos
  abiertos lo documentan para el otro endpoint (`bedrock-mantle`). El spike lo confirma con
  Converse: el que no lo maneje bien queda afuera.

**Los hermanos de cada familia** se prueban según cómo le vaya al representante:
- si un candidato gana, se prueba su hermano más barato: gpt-oss-20b, Nemotron Nano 9B v2 o
  Ministral 3 3B;
- si queda cerca del criterio sin llegar, el más grande dentro del límite de precio: Nemotron 3
  Super 120B, Ministral 3 14B o Qwen3 32B.

## Los que no entran, y por qué

- **Gemma 4 (Google):** solo funciona en el endpoint `bedrock-mantle`, con la API de OpenAI, y no
  con Converse. De Google entra Gemma 3 12B.
- **Nova 2 Lite:** la salida cuesta 2,75, cinco veces la de Haiku 5.5.
- **Claude Haiku 4.5:** cuesta diez veces más que Haiku 5.5, que lo reemplaza.
- **Los grandes:** DeepSeek V3.2, Kimi K2.5, GLM 4.7 y 5, MiniMax M2.5, Mistral Large 3,
  Qwen3 235B y Llama 4 Maverick cuestan entre 2 y 9 veces más y no aportan para elegir acciones
  simples. Si ningún candidato alcanza, son el paso siguiente.
- **Los más chicos:** Gemma 3 4B, Llama 3.2 de 1B y 3B y Ministral 3 3B son baratísimos, pero es
  poco probable que encadenen bien varios pasos en español. Ministral 3 8B los representa.
- **GPT-6 Luna y GPT-5.6 Luna (OpenAI):** figuran en el catálogo, pero no tienen precio por token
  ni en Ohio ni en Virginia.

## Cuántos tokens usa un pedido

Un pedido como "dale like al último post de Tomi" son varias llamadas al modelo: elige una
acción, la app la ejecuta y le devuelve qué pasó, y vuelve a elegir hasta terminar.

| Supuesto | Valor |
|---|---:|
| Llamadas al modelo por pedido | 4 |
| Entrada por llamada: instrucciones y catálogo de acciones | ~2.000 tokens |
| Entrada por llamada: pantalla e historial del pedido | ~1.000 tokens |
| Salida por llamada: la acción elegida y su razonamiento breve | ~250 tokens |
| **Total por pedido** | **~12.000 de entrada y ~1.000 de salida** |

## Costo

En dólares, sin caché de prompt.

| Modelo | Por pedido | Proyecto (3.000 pedidos) | Uso real (30.000 pedidos por mes) |
|---|---:|---:|---:|
| Amazon Nova Micro | 0,00056 | 1,68 | 16,80 |
| Amazon Nova Lite | 0,00096 | 2,88 | 28,80 |
| NVIDIA Nemotron Nano 3 30B | 0,00096 | 2,88 | 28,80 |
| Z.AI GLM 4.7 Flash | 0,00124 | 3,72 | 37,20 |
| Google Gemma 3 12B | 0,00137 | 4,11 | 41,10 |
| Claude Haiku 5.5 | 0,00187 | 5,61 | 56,10 |
| Mistral Ministral 3 8B | 0,00195 | 5,85 | 58,50 |
| OpenAI gpt-oss-120b | 0,00240 | 7,20 | 72,00 |
| Meta Llama 4 Scout | 0,00270 | 8,10 | 81,00 |
| Qwen3 Next 80B A3B | 0,00288 | 8,64 | 86,40 |
| *Claude Sonnet 5.5 (referencia)* | *0,03740* | *112,20* | *1.122,00* |

- **Proyecto:** el spike de `AI-03`, la evaluación de `AI-06`, el desarrollo y las pruebas de la
  app, y la demo. Suman unos 2.500 pedidos; se redondea a 3.000.
- **Uso real:** 100 usuarios que hacen 10 pedidos por día durante un mes. No es un escenario del
  proyecto: sirve para ver cómo escala cada modelo.
- **Caché de prompt:** Claude y Nova permiten guardar en caché las instrucciones y el catálogo,
  que se repiten en cada llamada. Con caché, su costo baja alrededor de 40%.

**Conclusión:** con cualquiera de los diez candidatos, el proyecto entero cuesta menos de
USD 9. Entre ellos la diferencia es de centavos por día de uso. Lo que decide es si el modelo
resuelve bien los pedidos en español y en cuánto tiempo, y eso no sale de ningún benchmark
público: Artificial Analysis, por ejemplo, no publica todavía su índice de inteligencia para
la mayoría de estos modelos. Lo medimos nosotros.

## Cómo se prueban

1. **A mano, en la consola de Bedrock.** El Playground permite probar un pedido con un modelo,
   y "Compare models" (en Labs) manda el mismo pedido a varios modelos a la vez y muestra la
   respuesta, los tokens y la demora de cada uno. Sirve para descartar rápido.
2. **En serio, con el spike de `AI-03`.** Los mismos 25 pedidos guionados, sobre un feed
   simulado, contra cada candidato por Converse. Para cada modelo mide:
   - cuántos pedidos terminan bien (se compara el estado final con el esperado);
   - cuántos pasos usa;
   - cuánto tarda hasta la primera acción;
   - cuántos tokens gasta y cuánto cuesta.

   Una corrida con los diez cuesta unos USD 0,42, más USD 0,94 si se suma Sonnet. Probar todos
   sale más barato que discutir cuál probar.

Gana el más barato que cumpla el criterio de éxito (ADR-023).

## Cómo se mantiene acotado

- Tope de 8 llamadas al modelo por pedido y un límite de tokens de salida por llamada.
- Rate limit por usuario en el relay de `notifications-api`.
- Una variable de configuración apaga el asistente sin cambiar código.
- Pedimos a la cátedra una alarma de presupuesto sobre Bedrock en la cuenta.

## Pendiente con la cátedra

- **Si los créditos cubren a Claude.** Los créditos promocionales de AWS en general no cubren lo
  que se factura por Marketplace. Si no lo cubren, Claude sale de los candidatos y quedan los
  otros nueve, que factura AWS.
- **Los permisos** para hacer la comparación: están en el anexo del ADR-023.

## Fuentes

- [Precios de Amazon Bedrock](https://aws.amazon.com/es/bedrock/pricing/), región Este de EE. UU.
  (Ohio). Para Anthropic, la tabla **Geo and In-region Cross-region Inference**. Consultados el
  2026-10-30, también por la lista de precios pública de AWS.
- [Fichas de los modelos en Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html):
  APIs, tool use, razonamiento y regiones de cada uno.
- [Acceso a modelos en Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html):
  qué modelos se venden por Marketplace y qué hace falta para habilitarlos.
- [Artificial Analysis](https://artificialanalysis.ai/leaderboards/models): primera respuesta
  y velocidad, consultados el 2026-10-30.

## Cómo recalcularlo

Costo por pedido = tokens de entrada × precio de entrada + tokens de salida × precio de salida,
con los precios por millón divididos por 1.000.000. La [calculadora de AWS](https://calculator.aws/)
acepta Bedrock con estos volúmenes y da un link para compartir.
