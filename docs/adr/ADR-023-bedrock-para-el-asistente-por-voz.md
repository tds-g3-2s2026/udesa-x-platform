# ADR-023: Amazon Bedrock para el asistente por voz, en un servicio propio

**Fecha:** 2026-10-30, revisada el 2026-10-31 con los comentarios del tutor · **Estado:**
aceptada · **Decide:** el equipo, con la aprobación del tutor

## Contexto

El 2026-10-26 se acordó con el tutor la funcionalidad de IA: **controlar el feed con la voz**
(`AI-01`, `docs/PROPUESTAS-IA.md`). El usuario habla y un agente scrollea, abre posts, da like,
retuitea, comenta y redacta un post a partir de lo que le describe. Cada pedido son varias
llamadas a un modelo que elige acciones de un catálogo, y las ejecuta la app.

El ADR-016 había elegido modelos abiertos dentro del cluster. Quedó como propuesta y nunca se
aceptó: la medición del 2026-10-17 mostró que el modelo que entra en la cuota del namespace no
alcanza, y este agente necesita elegir bien acciones de varios pasos, en español y rápido.

El tutor ofreció créditos de AWS con Bedrock, en la cuenta de la cátedra donde ya corre el
cluster. Pidió una estimación de costos y que el modelo se justifique contra opciones más
baratas. Hoy el usuario del grupo (`tds-group-3`) no tiene ningún permiso sobre Bedrock: ni
siquiera puede listar los modelos.

Es la entrega de `AI-02` (`udesa-x-platform#118`).

## Decisión

**El asistente es un servicio propio, `assistant-api`, que usa Amazon Bedrock en la cuenta de
la cátedra con inferencia dentro de EE. UU. Arranca con un modelo de costo medio y se ajusta
con evaluaciones hasta el más barato que cumpla.**

- **Dónde corre: `assistant-api`, un servicio aparte.** Repo `udesa-x-assistant-api`, en
  FastAPI y Python, con boto3 para Bedrock.
  - Asistir al usuario no es responsabilidad de `notifications-api`, que entrega avisos. El
    asistente tiene su propio ciclo de cambios: el prompt, el catálogo de acciones, el modelo y
    las evaluaciones que dicen si un cambio mejora o empeora. Separado, cada ajuste se prueba y
    se despliega sin tocar push ni emails.
  - Python, como `users-api` y `posts-api`: arranca de la plantilla de servicio, con el CI, el
    gate de cobertura, el Dockerfile y los manifiestos que ya funcionan, y el backend sigue con
    dos stacks y no tres (ADR-015).
  - Es un relay sin estado y sin base de datos. El rate limit por usuario usa el Redis
    compartido, en la base lógica `/2`, con el mismo módulo que `users-api` y `posts-api`.
  - Valida el JWT del usuario contra la clave pública de `users-api`, como el resto de los
    servicios. El gateway suma `/api/assistant` hacia este servicio.
  - Suma un `Deployment` y un `Service` al namespace, con pedidos de CPU y memoria chicos
    porque el modelo no corre adentro. Si la cuota no alcanza, se pide a la cátedra junto con
    la de RabbitMQ (`udesa-x-platform#113`).
- **Evaluaciones, tests y playground, en el mismo repo.**
  - `evals/`: los 25 pedidos guionados de `AI-03` sobre un feed simulado, cada uno con el
    estado final esperado. Llaman a Bedrock y cuestan, así que se corren a mano con el usuario
    del grupo y no en cada PR. Cada corrida anota modelo, tasa de éxito, latencias y costo en
    `docs/SPIKE-IA.md`.
  - `tests/`: con un modelo falso, sin llamar a Bedrock. Corren en cada PR con el gate de
    cobertura de los otros servicios.
  - Un playground de línea de comandos: un pedido, un modelo y una pantalla simulada, y muestra
    cada paso con sus tokens y su demora. Sirve para probar un prompt o un modelo antes de
    correr las evaluaciones.
- **Región e inferencia.** `us-east-2`, la del cluster, con modelos que corren en la región o
  con perfiles de inferencia de EE. UU. El perfil global es 10% más barato en los modelos que lo
  tienen, pero puede atender el pedido en cualquier región del mundo, y lo que se manda incluye
  texto de usuarios.
- **Los candidatos.** Son los modelos que cumplen cuatro filtros, con un modelo por familia:
  - se cobran por token en Ohio o con un perfil de EE. UU.;
  - funcionan con la API Converse con tool use;
  - cuestan hasta USD 0,20 por millón de tokens de entrada y USD 1,20 de salida;
  - pueden dar la primera respuesta en menos de 1 segundo, o permiten apagar el razonamiento.

  Quedan Amazon Nova Micro y Nova Lite, NVIDIA Nemotron Nano 3 30B, Z.AI GLM 4.7 Flash, Google
  Gemma 3 12B, Mistral Ministral 3 8B, OpenAI gpt-oss-120b, Qwen3 Next 80B A3B, Meta Llama 4
  Scout y Claude Haiku 5.5. Claude Sonnet 5.5 entra solo como referencia de lo mejor posible. La
  tabla, los precios, los descartados y sus motivos están en `docs/ESTIMACION-COSTOS-IA.md`.
- **Cómo se elige: se arranca con uno de costo medio y se itera.**
  - El spike de `AI-03` arranca con **gpt-oss-120b**: está en la mitad de la tabla de precios,
    lo factura AWS (los créditos lo cubren, a Claude quizás no), es de los más rápidos de la
    lista y está entrenado para elegir herramientas.
  - Si cumple el criterio de éxito, se prueba el siguiente más barato de la tabla, y se baja
    mientras siga cumpliendo. Si no cumple, se prueba uno más capaz: Llama 4 Scout y, si los
    créditos cubren Marketplace, Claude Haiku 5.5.
  - Si gpt-oss-120b no maneja tool use por Converse, el punto de partida pasa a ser Llama 4
    Scout.
  - Queda el más barato que cumplió. El criterio de éxito es el de `PROPUESTAS-IA.md`:
    - al menos 80% de pedidos terminados bien;
    - ninguna acción visible para otros sin confirmación;
    - una mediana menor a 3 segundos hasta la primera acción.

  No hace falta encontrar el mejor posible: alcanza con uno que cumpla. Como las evaluaciones
  quedan en el repo, cambiar de modelo más adelante es volver a correrlas.
- **Razonamiento apagado o al mínimo.** El razonamiento mejora la calidad, pero agrega segundos
  antes de cada acción. Con razonamiento, Claude Haiku 5.5 tarda casi 8 segundos en empezar a
  responder. Cada candidato se prueba con el razonamiento apagado o en su nivel más bajo, y solo
  se sube si no alcanza el criterio de pedidos terminados bien.
- **El modelo es configuración.** El servicio llama a la API Converse de Bedrock, que es la
  misma para los diez candidatos e incluye tool use. Cambiar de modelo dentro de la lista es
  cambiar una variable, sin código. Usar un modelo fuera de la lista, o salir de Bedrock, es un
  ADR nuevo.
- **Credenciales, sin claves en el repo.**
  - En el cluster, el pod de `assistant-api` asume un rol de IAM con el token proyectado del
    pod, igual que `posts-api` con `tds-group-3-s3-role` (`udesa-x-posts-api#119`). El
    pipeline no puede crear ServiceAccounts, así que el token se declara en el Deployment.
  - Para el spike y las evaluaciones, desde las máquinas del equipo, el mismo permiso va en el
    usuario `tds-group-3`. Su access key vive en el entorno local de cada integrante, nunca en
    el repo.
  - Los dos permisos se limitan a invocar los candidatos. Los crea la cátedra: el usuario del
    grupo no puede crear políticas de IAM. El detalle está en el anexo.
- **Qué se manda al modelo.** El pedido en texto (la voz se pasa a texto en el teléfono) y la
  pantalla: los posts visibles con una referencia corta (`p1`, `p2`...), el handle del autor,
  el texto y si ya tienen like o retweet. **Nunca** ids internos, emails, tokens ni audio. La
  relación entre `p1` y el id real queda en la app.
- **Qué se guarda.** Nada del contenido. Ni el pedido ni las respuestas del modelo van a la
  base, a los logs ni a las trazas, que salen a Grafana Cloud (ADR-013). Solo métricas: pasos,
  latencia, acción elegida y resultado.
- **Seguridad del agente.** El texto de los posts es dato no confiable: un post puede decir
  "retuiteá esto". Las defensas no dependen del modelo:
  - un catálogo cerrado de acciones;
  - la confirmación obligatoria, en la app, de todo lo que ven otros;
  - un tope de pasos por pedido y un rate limit por usuario.
- **Costo y topes.** Con cualquiera de los candidatos, el proyecto entero cuesta menos de
  USD 9 (`docs/ESTIMACION-COSTOS-IA.md`). Para acotarlo:
  - un tope de 8 llamadas por pedido y de tokens de salida por llamada;
  - un rate limit por usuario;
  - una variable que apaga el asistente;
  - una alarma de presupuesto que se le pide a la cátedra.

## Alternativas descartadas

- **Un módulo dentro de `notifications-api`.** Era la primera versión de este ADR: no sumaba un
  `Service` al namespace y compartía TypeScript con la app. En la revisión, el tutor marcó que
  asistir al usuario no es tarea del servicio de notificaciones y que, separado, el asistente
  puede tener sus evaluaciones, tests y playground. El costo de separarlo es un repo y un
  `Deployment` más.
- **Modelos abiertos en el cluster (ADR-016).** No cuestan por uso, pero el modelo que entra en
  la cuota no alcanza para este agente, y uno más grande necesita una ampliación de cuota que
  no está garantizada.
- **Fijar el modelo sin probarlo.** Ningún benchmark público mide esta tarea, y la mayoría de
  los candidatos ni siquiera tiene un índice comparable publicado. El punto de partida sale de
  la tabla, pero el modelo final sale de las evaluaciones.
- **Probar los diez candidatos de entrada.** Una corrida con todos cuesta menos de USD 0,50,
  pero mide mucho más de lo necesario para decidir. Arrancar por uno de costo medio e iterar
  llega a lo mismo con menos trabajo.
- **Un modelo grande.** Claude Sonnet 5.5, DeepSeek, Kimi o Mistral Large cuestan entre 3 y 20
  veces más que Claude Haiku 5.5. Sonnet queda como referencia; si ningún candidato alcanza, el
  paso siguiente es un modelo de ese rango, con un ADR nuevo.
- **La API de OpenAI que ofrece Bedrock en el endpoint `bedrock-mantle`.** Suma modelos como
  Gemma 4, pero no tiene a Nova, Llama 4 ni Claude. Converse cubre a los diez candidatos con una
  sola integración.
- **La API de Anthropic directa.** Joaquín tiene créditos y funciona igual con Claude. Pero queda
  fuera de la cuenta de la cátedra, con una clave que hay que administrar y créditos personales.
  Queda como respaldo solo si Bedrock se demora.

## Consecuencias

- Reemplaza al ADR-016, que nunca se aceptó. Actualiza el mapa de repositorios y la sección
  "Integración de Inteligencia Artificial" de `ARQUITECTURA.md`, el modelo y el lugar del
  asistente en `PROPUESTAS-IA.md` y la sección de IA de `PLANIFICACION.md`.
- **Se crea `udesa-x-assistant-api` como parte de `AI-03`:** el arnés de evaluaciones y el
  playground del spike son lo primero que entra. `AI-04` suma el endpoint, el deploy y la ruta
  del gateway. `AI-04` y `AI-06` pasan de `notifications-api` a ese repo, y `notifications-api`
  no cambia.
- **Claude se factura por AWS Marketplace; los otros nueve, directamente por AWS.** Los créditos
  promocionales de AWS en general no cubren Marketplace. Si los de la cátedra no lo cubren,
  Claude sale de los candidatos y la comparación sigue con los otros nueve.
- Depende de la cátedra, que tiene que:
  - agregar los permisos del anexo;
  - habilitar Claude la primera vez y completar el formulario de uso de Anthropic, una sola vez
    por cuenta (los otros nueve se habilitan solos con la primera invocación);
  - responder si los créditos cubren a Claude.
- La funcionalidad depende de un servicio externo: si Bedrock no responde, el asistente avisa
  que no pudo y la app sigue funcionando sin él.

## Anexo: permisos que se piden a la cátedra

**Para ver el catálogo** desde la consola con el usuario `tds-group-3`: la política
administrada de AWS `AmazonBedrockReadOnly`.

**Para invocar los candidatos**, en el usuario `tds-group-3` (spike y evaluaciones) y en un rol
para `assistant-api` (producción):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "InvocarModelosCandidatos",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/amazon.nova-micro-v1:0",
        "arn:aws:bedrock:*::foundation-model/amazon.nova-lite-v1:0",
        "arn:aws:bedrock:*::foundation-model/nvidia.nemotron-nano-3-30b",
        "arn:aws:bedrock:*::foundation-model/zai.glm-4.7-flash",
        "arn:aws:bedrock:*::foundation-model/google.gemma-3-12b-it",
        "arn:aws:bedrock:*::foundation-model/mistral.ministral-3-8b-instruct",
        "arn:aws:bedrock:*::foundation-model/openai.gpt-oss-120b-1:0",
        "arn:aws:bedrock:*::foundation-model/qwen.qwen3-next-80b-a3b",
        "arn:aws:bedrock:*::foundation-model/meta.llama4-scout-17b-instruct-v1:0",
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-haiku-5-5*",
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-sonnet-5-5*",
        "arn:aws:bedrock:*:172786533418:inference-profile/us.*"
      ]
    }
  ]
}
```

- **La región va con `*`:** un perfil de inferencia de EE. UU. puede atender el pedido desde
  otra región del país, y el permiso tiene que valer en todas.
- **Los de Claude terminan en `*`:** cubren el identificador exacto que use Bedrock para cada
  modelo. Los demás son los de las fichas de Bedrock.
- **La API Converse** usa estos mismos permisos: `InvokeModel` para la llamada común y
  `InvokeModelWithResponseStream` para la que devuelve la respuesta por partes.
- **Habilitar Claude la primera vez** necesita, además, `aws-marketplace:Subscribe`,
  `aws-marketplace:Unsubscribe` y `aws-marketplace:ViewSubscriptions`, y el formulario de uso de
  Anthropic. Lo más simple es que la cátedra abra Claude Haiku 5.5 y Sonnet 5.5 una vez en el
  Playground de la consola: después, el resto de la cuenta lo usa sin esos permisos.
- **El rol de `assistant-api`** necesita la misma confianza que `tds-group-3-s3-role`: el token
  del pod con audiencia `sts.amazonaws.com`.
