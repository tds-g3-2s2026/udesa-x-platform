# ADR-023: Amazon Bedrock para el asistente por voz, con el modelo más barato que pase la evaluación

**Fecha:** 2026-10-30 · **Estado:** aceptada · **Decide:** el equipo, con la aprobación del
tutor

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

**El asistente usa Amazon Bedrock en la cuenta de la cátedra, con inferencia dentro de
EE. UU. El modelo es el más barato de diez candidatos que pase la evaluación del spike.**

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
- **Cómo se elige.** El spike de `AI-03` corre los mismos 25 pedidos guionados con todos los
  candidatos. Gana el más barato que cumpla el criterio de éxito de `PROPUESTAS-IA.md`:
  - al menos 80% de pedidos terminados bien;
  - ninguna acción visible para otros sin confirmación;
  - una mediana menor a 3 segundos hasta la primera acción.

  Si gana uno, se prueba su hermano más barato de la misma familia. Un candidato que en la
  práctica no maneje tool use por Converse queda afuera. El resultado y las mediciones quedan en
  `docs/SPIKE-IA.md`.
- **Razonamiento apagado o al mínimo.** El razonamiento mejora la calidad, pero agrega segundos
  antes de cada acción. Con razonamiento, Claude Haiku 5.5 tarda casi 8 segundos en empezar a
  responder. Cada candidato se prueba con el razonamiento apagado o en su nivel más bajo, y solo
  se sube si no alcanza el criterio de pedidos terminados bien.
- **El modelo es configuración.** El relay llama a la API Converse de Bedrock, que es la misma
  para los diez candidatos e incluye tool use. Cambiar de modelo dentro de la lista es cambiar
  una variable, sin código. Usar un modelo fuera de la lista, o salir de Bedrock, es un ADR
  nuevo.
- **Dónde corre.** En el módulo `assistant` de `notifications-api`, en TypeScript con el SDK de
  AWS para JavaScript (`@aws-sdk/client-bedrock-runtime`). No suma `Service` al namespace.
- **Credenciales, sin claves en el repo.**
  - En el cluster, el pod de `notifications-api` asume un rol de IAM con el token proyectado del
    pod, igual que `posts-api` con `tds-group-3-s3-role` (`udesa-x-posts-api#119`). El
    pipeline no puede crear ServiceAccounts, así que el token se declara en el Deployment.
  - Para el spike, desde las máquinas del equipo, el mismo permiso va en el usuario
    `tds-group-3`. Su access key vive en el entorno local de cada integrante, nunca en el repo.
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

- **Modelos abiertos en el cluster (ADR-016).** No cuestan por uso, pero el modelo que entra en
  la cuota no alcanza para este agente, y uno más grande necesita una ampliación de cuota que
  no está garantizada.
- **Fijar el modelo de antemano.** Ningún benchmark público mide esta tarea, y la mayoría de los
  candidatos ni siquiera tiene un índice comparable publicado. Probar los diez cuesta menos de
  USD 0,50 por corrida, así que no hace falta adivinar.
- **Un modelo grande.** Claude Sonnet 5.5, DeepSeek, Kimi o Mistral Large cuestan entre 3 y 20
  veces más que Claude Haiku 5.5. Sonnet entra al spike como referencia; si ningún candidato
  alcanza, el paso siguiente es un modelo de ese rango, con un ADR nuevo.
- **La API de OpenAI que ofrece Bedrock en el endpoint `bedrock-mantle`.** Suma modelos como
  Gemma 4, pero no tiene a Nova, Llama 4 ni Claude. Converse cubre a los diez candidatos con una
  sola integración.
- **La API de Anthropic directa.** Joaquín tiene créditos y funciona igual con Claude. Pero queda
  fuera de la cuenta de la cátedra, con una clave que hay que administrar y créditos personales.
  Queda como respaldo solo si Bedrock se demora.

## Consecuencias

- Reemplaza al ADR-016, que nunca se aceptó. Actualiza la sección "Integración de Inteligencia
  Artificial" de `ARQUITECTURA.md`, el modelo en `PROPUESTAS-IA.md` y la sección de IA de
  `PLANIFICACION.md`.
- **Claude se factura por AWS Marketplace; los otros nueve, directamente por AWS.** Los créditos
  promocionales de AWS en general no cubren Marketplace. Si los de la cátedra no lo cubren,
  Claude sale de los candidatos y la comparación sigue con los otros nueve.
- Depende de la cátedra, que tiene que:
  - agregar los permisos del anexo;
  - habilitar Claude la primera vez y completar el formulario de uso de Anthropic, una sola vez
    por cuenta (los otros nueve se habilitan solos con la primera invocación);
  - responder si los créditos cubren a Claude.
- `notifications-api` suma `@aws-sdk/client-bedrock-runtime` y, para producción, las
  variables del rol en su Deployment.
- La funcionalidad depende de un servicio externo: si Bedrock no responde, el asistente avisa
  que no pudo y la app sigue funcionando sin él.

## Anexo: permisos que se piden a la cátedra

**Para ver el catálogo** desde la consola con el usuario `tds-group-3`: la política
administrada de AWS `AmazonBedrockReadOnly`.

**Para invocar los candidatos**, en el usuario `tds-group-3` (spike) y en un rol para
`notifications-api` (producción):

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
- **El rol de `notifications-api`** necesita la misma confianza que `tds-group-3-s3-role`: el
  token del pod con audiencia `sts.amazonaws.com`.
