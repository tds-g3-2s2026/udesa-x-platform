# ADR-027: Langfuse Cloud para las trazas del asistente por voz

**Fecha:** 2026-11-25 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

La entrega final pide observabilidad de la funcionalidad de IA en Langfuse, con acceso del
tutor, y que se pueda mostrar en la demo a partir de un pedido hecho en producción. Es lo que se
vio en la clase de observabilidad (`tds-udesa/clase-observabilidad`): la app manda los mismos
spans de OpenTelemetry a Grafana y a Langfuse, y en Langfuse se lee cada llamada al modelo con su
prompt, su respuesta, los tokens y el costo.

`assistant-api` ya manda trazas, logs y métricas a Grafana Cloud (ADR-013), pero el ADR-023 fijó
que nada del contenido va a las trazas. Sin el texto, una traza en Langfuse muestra que hubo una
llamada, pero no por qué el modelo eligió esa acción.

## Decisión

**Los spans del agente van también a un proyecto de Langfuse Cloud, con el texto.** Es el
proyecto del equipo y del tutor, en la región US, la misma del modelo (ADR-023).

- **Qué se manda.** Un span por paso (`assistant.step`, tipo *agent*) con lo que mandó la app y
  la acción que volvió, y uno por llamada al modelo (`assistant.model`, tipo *generation*) con
  los mensajes, el prompt de sistema, la respuesta, el modelo, los tokens y el costo. Es la misma
  información que ya recibe el modelo: nunca ids internos, emails, tokens ni audio.
- **Cómo.** Con el SDK de OpenTelemetry que el servicio ya usa: un segundo exportador OTLP hacia
  `/api/public/otel` de Langfuse, con las claves del proyecto como Basic auth. No suma ninguna
  dependencia ni ningún pod al namespace.
- **Grafana sigue sin el texto.** Antes de exportar a Grafana, un procesador le saca a cada span
  los dos atributos que lo llevan. Un test lo verifica.
- **Langfuse solo recibe los spans del agente**, sin los HTTP. El paso es la raíz de su traza, y
  conserva el trace id que muestra Grafana para el mismo request.
- **Retención.** El plan gratuito de Langfuse muestra los últimos 30 días.

Enmienda la regla de retención del ADR-023: el contenido sigue sin guardarse en la base, en los
logs ni en lo que llega a Grafana, pero llega a Langfuse.

## Alternativas descartadas

- **Mandar a Langfuse solo números**, sin el texto. Respeta el ADR-023 tal cual, pero la traza
  queda vacía: no muestra el prompt ni la respuesta, que es para lo que sirve Langfuse.
- **Langfuse dentro del cluster.** Necesita Postgres, ClickHouse, Redis, almacenamiento S3, la
  web y un worker. La cuota del namespace deja lugar para cuatro pods.
- **El SDK de Langfuse.** Suma una dependencia y su propia configuración de OpenTelemetry al lado
  de la que ya tiene el servicio, para algo que resuelve un exportador.

## Consecuencias

- **Dos claves más en los Secrets** de `assistant-api` (`LANGFUSE_PUBLIC_KEY` y
  `LANGFUSE_SECRET_KEY`). El deploy verifica que estén, así que se cargan antes de mergear.
- **El plan gratuito tiene dos usuarios**: una cuenta del equipo y el tutor. Incluye 50.000
  unidades por mes, y cada paso del asistente usa tres o cuatro: la traza, el paso y una o dos
  llamadas al modelo.
- **El costo se calcula en el servicio** con los precios de Claude Haiku 5.5
  (`ESTIMACION-COSTOS-IA.md`), que son la configuración por defecto. Si cambia el modelo, se
  cambian también `BEDROCK_INPUT_PRICE` y `BEDROCK_OUTPUT_PRICE`.
- **Si Langfuse no responde, el asistente sigue andando**: el exportador manda en lotes, en
  segundo plano, y descarta lo que no pudo mandar.
