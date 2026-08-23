# Planificación de UdeSA-X

## Propósito

Este documento baja a un plan ejecutable la consigna de UdeSA-X para un equipo de cuatro integrantes, sobre el calendario real de la cursada, con quince sprints semanales y gestión mediante GitHub Issues, Milestones y GitHub Projects.

Las fechas salen de `Cronograma Taller de Desarrollo de Software.pdf`. Cada sprint es una semana y termina en la reunión del lunes, que es donde el tutor revisa lo hecho y se acuerda lo que viene.

La fuente de requisitos es `UdeSA-X.pdf`. La transcripción depurada está en [`CONSIGNA.md`](./CONSIGNA.md). La propuesta técnica que acompaña a este plan está en [`ARQUITECTURA.md`](./ARQUITECTURA.md), y las reglas de trabajo del equipo en [`CONVENCIONES.md`](./CONVENCIONES.md).

## Estado del documento

Versión del 2026-08-21.

El trabajo se organiza en **sprints de una semana anclados a los lunes**, que es cuando el equipo se reúne con el tutor. El calendario sale de cruzar el `Cronograma Taller de Desarrollo de Software.pdf`: el semestre son veinte semanas con tres feriados y tres fechas duras que no se mueven.

La infraestructura de nube va en S5 y S6, sincronizada con las clases de Cloud Computing y llegando al despliegue productivo para la entrega intermedia del 28 de septiembre. Es lo que absorbe la semana de atraso de gestión sin recortar alcance.

## Cómo leer este documento

- Las secciones "Alcance", "Reparto" y "Sprints" son el compromiso del equipo. Cambiarlas requiere acuerdo del equipo y aviso al tutor.
- La sección "Riesgos" y la sección "Decisiones abiertas" son documentos vivos: se revisan en el planning de cada lunes.
- Todo lo que dice "propuesta" está sujeto a validación con el tutor. Está escrito para tener algo concreto que discutir, no para cerrar la discusión.
- Las fechas duras del semestre son tres: **28 de septiembre** entrega intermedia con el sistema productivo en AWS, **26 de octubre** todas las historias obligatorias aceptadas, **30 de noviembre** entrega final. Nada de lo que dice este documento las mueve.

## Alcance de aprobación

La consigna exige implementar las 30 historias obligatorias, que suman 82 puntos, y 15 puntos de historias optativas por cada integrante. Para cuatro integrantes, el mínimo optativo de aprobación es 60 puntos.

El equipo compromete deliberadamente **por encima del mínimo**:

| Concepto | Historias | Puntos |
|---|---:|---:|
| Obligatorias | 30 | 82 |
| Optativas comprometidas | 23 | 73 |
| **Total comprometido** | **53** | **155** |
| Mínimo exigido por la consigna | - | 142 |
| Colchón sobre el mínimo | - | +13 (21% del alcance optativo) |

El colchón no es capricho. Comprometer exactamente 60 puntos optativos significa que si una sola historia se cae por un criterio de aceptación rechazado, el grupo queda por debajo del umbral de aprobación sin margen de reacción. Con 73 puntos repartidos en 18-19 por integrante, cada uno puede perder una historia de 3 puntos y seguir cumpliendo los 15.

Además del alcance puntuado, el compromiso incluye una funcionalidad de Inteligencia Artificial acordada con el tutor y todos los requisitos técnicos y no funcionales de la consigna, que no otorgan puntos pero son condición de aprobación.

## Inventario de historias

| Épica | Historias | Obligatorias | Optativas | Total |
|---|---:|---:|---:|---:|
| E.1 Usuarios | 14 | 7 / 16 pts | 7 / 20 pts | 36 pts |
| E.2 Publicaciones | 15 | 9 / 27 pts | 6 / 22 pts | 49 pts |
| E.3 Interacciones Sociales | 10 | 5 / 14 pts | 5 / 21 pts | 35 pts |
| E.4 Notificaciones | 5 | 3 / 7 pts | 2 / 8 pts | 15 pts |
| E.5 Administradores | 12 | 6 / 18 pts | 6 / 20 pts | 38 pts |
| **Total** | **56** | **30 / 82 pts** | **26 / 91 pts** | **173 pts** |

## Reparto de historias optativas

Las optativas están agrupadas en cuatro bloques por afinidad técnica, no por reparto ciego de puntos. Cada bloque concentra historias que comparten modelo de datos, servicio y pantallas, de modo que el costo de contexto se paga una sola vez y los conflictos de merge se minimizan.

**Un bloque no es una persona.** Quién toma cuál se decide en el planning, cuando el equipo lo acuerde; hasta entonces cualquiera puede agarrar lo que esté libre. Los bloques existen para que ese acuerdo, cuando llegue, reparta trabajo coherente y no historias sueltas.

Cada bloque incluye una historia marcada como **flex**: es la primera que se sacrifica si el sprint se atrasa, y quitarla deja al bloque en 15 puntos, el mínimo que la consigna pide por integrante.

La columna `Sprint` es la que hace verificable el compromiso: sin ella el agrupamiento dice cuánto pesa cada bloque pero no cuándo, y el riesgo de que alguien llegue a noviembre con 15 puntos sin empezar queda invisible.

### Bloque 1: contenido y descubrimiento

| Historia | Puntos | Sprint | Nota |
|---|---:|---|---|
| E.2 H8. Hashtags | 3 | S8 | |
| E.2 H9. Menciones a Usuarios | 3 | S8 | |
| E.4 H4. Notificación de Mención | 5 | S10 | |
| E.2 H11. Trending Topics | 3 | S11 | **flex** |
| E.2 H13. Citar Post | 5 | S12 | |
| **Total** | **19** | | mínimo tras flex: 16 |

E.4 H4 entra al alcance porque E.2 H9 CA.3 ya exige notificar al usuario mencionado. Dejarla en el backlog sería hacer el trabajo sin cobrar los puntos.

### Bloque 2: identidad y experiencia mobile

| Historia | Puntos | Sprint | Nota |
|---|---:|---|---|
| E.1 H13. Cambiar Contraseña | 3 | S3 | |
| E.1 H7. Preferencias | 2 | S4 | |
| E.1 H10. Tema de la Aplicación | 1 | S4 | |
| E.1 H8. Foto de Perfil | 3 | S6 | |
| E.1 H14. Onboarding Inicial | 3 | S11 | |
| E.1 H11. Enviar Feedback o Reportar Error | 3 | S10 | |
| E.2 H12. Guardar Posts | 3 | S12 | **flex** |
| **Total** | **18** | | mínimo tras flex: 15 |

### Bloque 3: grafo social y notificaciones

| Historia | Puntos | Sprint | Nota |
|---|---:|---|---|
| E.5 H9. Registro de Última Conexión | 2 | S6 | |
| E.3 H9. Invitar Usuarios Externos | 2 | S7 | |
| E.4 H5. Configurar Preferencias de Notificación | 3 | S9 | |
| E.3 H10. Silenciar Usuario | 5 | S10 | |
| E.3 H7. Usuarios en Línea | 3 | S11 | |
| E.3 H8. Listas Personalizadas | 3 | S12 | **flex** |
| **Total** | **18** | | mínimo tras flex: 15 |

E.3 H10 entra al alcance porque E.4 H4 CA.2 exige no notificar menciones de usuarios silenciados. Sin silenciar implementado, ese criterio de aceptación no se puede demostrar.

### Bloque 4: backoffice y plataforma

| Historia | Puntos | Sprint | Nota |
|---|---:|---|---|
| E.5 H11. Estado de los Microservicios | 5 | S6 | |
| E.5 H8. Exportar Datos | 2 | S7 | |
| E.5 H3. Visualización de Métricas | 5 | S11 | |
| E.5 H12. Gestión de Feedback/Reportes | 3 | S8 | |
| E.5 H10. Borrado Forzado de Contenido | 3 | S12 | **flex** |
| **Total** | **18** | | mínimo tras flex: 15 |

E.5 H12 entra al alcance porque E.1 H11 CA.2 exige que el envío de feedback genere un registro. Sin la bandeja del backoffice, ese registro no tiene consumidor y el flujo queda a medias.

E.5 H11 se adelanta a S6 a propósito: la entrega intermedia del 28 de septiembre exige demostrar un sistema productivo, y una pantalla que muestra el estado de los microservicios es la forma más directa de demostrarlo. Es una historia optativa que además hace de evidencia.

### Acumulación de puntos optativos a lo largo del semestre

La consigna evalúa 15 puntos optativos **por integrante**. Un bloque que concentre sus puntos en las últimas tres semanas se vuelve un riesgo individual de aprobación para quien lo tome, no solo del equipo. Este es el acumulado al cierre de cada hito de control:

| Bloque | 28 sept (entrega intermedia) | 26 oct (obligatorias cerradas) | 16 nov (cierre de optativas) |
|---|---:|---:|---:|
| Bloque 1 | 0 | 6 | 19 |
| Bloque 2 | 9 | 9 | 18 |
| Bloque 3 | 2 | 7 | 18 |
| Bloque 4 | 5 | 10 | 18 |

El Bloque 1 arranca en cero porque sus historias (hashtags, menciones, citas, trending) dependen del modelo de post, que recién se estabiliza en S5. Es una dependencia real, no un descuido, pero hay que vigilarla: si S8 se atrasa, el Bloque 1 es el que queda más expuesto. Mitigación registrada como R13.

### Historias fuera de alcance

Solo tres historias quedan fuera, y las tres tienen riesgo técnico genuino, no solo volumen:

| Historia | Puntos | Razón |
|---|---:|---|
| E.1 H9. Social Login | 5 | Sign in with Apple exige cuenta de Apple Developer paga y configuración de dominio. Dependencia externa de plazo incierto. |
| E.2 H15. Post con Video | 5 | Transcodificación, validación de duración y almacenamiento de 512 MB por archivo. Multiplica el costo de infraestructura y de las pruebas de carga. |
| E.3 H6. Mensajes Directos | 8 | Requiere WebSockets o polling, un modelo de conversación propio, y arrastra E.3 H7 y las notificaciones de DM. Es prácticamente una épica entera. |

Estas historias deben permanecer visibles en el backlog con `scope:optional-backlog`, sin fecha ni asignación. Si el equipo cierra S12 con holgura, la candidata natural a incorporar es E.1 H9 limitada solo a Google, que elimina el bloqueo de Apple.

## Calendario de la cátedra

Fuente: `Cronograma Taller de Desarrollo de Software.pdf`. Todas las clases son los lunes. El semestre son 20 semanas calendario, no 16: del 3 de agosto al 14 de diciembre, con tres feriados y cuatro fechas de entrega o notas.

| Lunes | Clase | Avance esperado por la cátedra |
|---|---|---|
| 3 ago | Introducción + AI Engineering I | Armado de grupos |
| 10 ago | Desarrollo Backend | Organización de GitHub creada, tablero Kanban con épicas e historias, comienzo del primer sprint |
| 17 ago | **Feriado** | - |
| 24 ago | Desarrollo Frontend | Primera API REST creada y dockerizada para desarrollo local |
| 31 ago | Testing | Backoffice web creada y dockerizada para desarrollo local |
| 7 sept | Arquitectura | API testeada y pipeline de CI corriendo. % de avance acordado con el tutor. **Desde acá, todo el código que se sube va testeado.** |
| 14 sept | Cloud Computing I (k8s) | Flujo completo end to end desde el backoffice hasta el backend. Inicio del desarrollo mobile. Inicio de los nuevos microservicios acordados con el tutor. |
| 21 sept | Cloud Computing II (AWS, EKS) | % de avance acordado con el tutor. Flujo end to end desde la app mobile hasta el backend. |
| 28 sept | **Entrega intermedia** | Sistema funcionando en forma productiva, desplegado en AWS, con toda la funcionalidad comprometida y acordada con el tutor |
| 5 oct | **Entrega intermedia** | (segunda fecha) |
| 12 oct | **Feriado** | - |
| 19 oct | AI Engineering II | % de avance acordado con el tutor. Inicio de la implementación de la feature de IA. |
| 26 oct | Observabilidad | **Finalización de las historias de usuario obligatorias.** Presentación de la propuesta de la feature de IA. |
| 2 nov | Escalabilidad | Observabilidad agregada al sistema e integración con herramienta de visualización |
| 9 nov | System Design | Implementación de historias de usuario optativas y documentación |
| 16 nov | Retro | Carga de usuarios y testing de la aplicación |
| 23 nov | **Feriado** | - |
| 30 nov | **Entrega final** | Proyecto y documentación finalizados |
| 7 dic | **Entrega final** | (segunda fecha) |
| 14 dic | Recuperatorios y entrega de notas | Proyecto y documentación finalizados **más una funcionalidad extra comprometida con el tutor** |

Tres cosas de esta tabla gobiernan todo el resto del documento:

1. **El 26 de octubre es la fecha dura del semestre.** Las 30 historias obligatorias tienen que estar aceptadas ese día. Todo lo anterior se planifica hacia atrás desde ahí.
2. **La entrega intermedia del 28 de septiembre exige un sistema productivo desplegado en AWS.** No es una demo local. Eso fija cuándo hay que tener el cluster andando.
3. **Hay dos fechas de entrega intermedia y dos de entrega final.** Hay que preguntarle al tutor cuál le toca al grupo 3 en cada caso, y hasta que responda se planifica contra la fecha temprana. Planificar contra la tardía y descubrir que toca la temprana cuesta una semana que no hay.

### Estado al 19 de agosto y cómo se recupera

El avance esperado del 10 de agosto está incumplido: la organización de GitHub existe con cuatro repositorios vacíos, pero el tablero no tiene ni un item, no hay issues, no hay milestones y el primer sprint no arrancó. El atraso es de una semana **de gestión, no de desarrollo**, que es la forma barata de atrasarse.

Este plan no descuenta alcance para pagar esa semana. Se recupera de otro lado: **el walking skeleton no se despliega en la nube en las primeras dos semanas** sino en la ventana del 14 al 27 de septiembre, sincronizada con las clases de Cloud Computing I y II, y llegando al despliegue productivo justo para la entrega intermedia. Pelear con EKS la semana del 24 de agosto garantizaría no entregar la API dockerizada que la cátedra espera ese día.

El costo de esa decisión es que el riesgo de infraestructura vive un mes más de lo ideal. La mitigación es arrancar el spike de EKS el 7 de septiembre, sin esperar a la clase del 14, con un integrante dedicado.

### Dónde el plan se adelanta al temario, y por qué

El plan sigue el orden de las clases en casi todo, pero hay cuatro puntos donde se adelanta. Están acá para que sean una decisión y no una sorpresa: adelantarse a una clase significa resolver ese tema sin la ayuda del docente.

| Tema | Clase que lo cubre | Cuándo lo hace el plan | Por qué |
|---|---|---|---|
| Provisionar EKS, Gateway API, CD | Cloud Computing II, 21 sept | S5, del 14 al 20 sept, con spike desde el 7 | **Forzado por la cátedra.** La entrega intermedia del 28 de septiembre exige el sistema desplegado en AWS y la clase de EKS es el 21. Son siete días entre una cosa y la otra. La única alternativa es apostar la entrega a esa semana. |
| Observabilidad mínima: logs estructurados y dashboard de healthchecks | Observabilidad, 26 oct | S6, del 21 al 27 sept | **Forzado por la cátedra.** No se puede demostrar un sistema productivo sin poder mostrar que está vivo. Es lo mínimo, no lo de la clase: métricas y trazas completas van en S10, alineadas con el 26 de octubre. La cuenta de Grafana Cloud y el acceso del tutor se verifican ya en S6, porque el free tier son 3 asientos para cinco personas. |
| Prueba de carga de línea base | Retro y carga, 16 nov | S6 | Elección del equipo. Una prueba de carga final sin línea base contra qué comparar no demuestra que se hizo ingeniería. Es la corrida barata, con el seed chico. La grande va en S12, alineada. |
| Spike de IA: prompt, salida estructurada, costo | AI Engineering II, 19 oct | S8, del 5 al 18 oct | Adelanto de días, y sobre la base de AI Engineering I del 3 de agosto. El cronograma pone el inicio de la implementación el 19 de octubre y el plan lo respeta: en S8 solo se mide y se decide proveedor. |

Todo lo demás va detrás de su clase o el mismo día:

| Tema | Clase | Sprint |
|---|---|---|
| Docker y API REST | Desarrollo Backend, 10 ago | S1 |
| React y frontend web | Desarrollo Frontend, 24 ago | S2 |
| Tests, cobertura, CI | Testing, 31 ago | S3 |
| API Gateway, load balancer, C4 | Arquitectura, 7 sept | S4 |
| Kubernetes | Cloud Computing I, 14 sept | S5 |
| Métricas, logs, trazas, dashboards | Observabilidad, 26 oct | S10 |
| Colas y mensajería asincrónica | Escalabilidad, 2 nov | S4 la cola mínima, S11 outbox bajo carga y HPA |
| Autoescalado horizontal | Escalabilidad, 2 nov | S11 |
| Diseño de sistemas y volumen de datos | System Design, 9 nov | S12 |

La cola es el único caso donde el plan se adelanta de forma significativa a la clase sin estar forzado: entra en S4, el 7 de septiembre, y la clase de Escalabilidad es el 2 de noviembre. La razón es de dependencia, no de temario: los emails de verificación, las notificaciones y el triage de IA la necesitan, y las tres cosas ocurren antes de noviembre. Lo que sí se difirió es todo lo sofisticado: outbox bajo carga, reintentos, dead letter queue y autoescalado quedan en S11, alineados con la clase.

## Cobertura de los requisitos de la consigna

Los 17 requisitos de `CONSIGNA.md`, con el sprint donde quedan demostrables. Ninguno queda sin dueño ni sin fecha.

| Requisito de la consigna | Cómo se cumple | Sprint |
|---|---|---|
| App principal exclusivamente mobile | React Native con Expo | S2 esqueleto, S5 flujo completo |
| Backoffice como aplicación web | React con Vite | S2 |
| Arquitectura de microservicios | 3 servicios, un repositorio cada uno, despliegue independiente | S1 a S4 |
| Al menos dos tipos de base de datos | PostgreSQL, MongoDB y Redis | S2 |
| Backend en más de una tecnología | FastAPI con Python en `users` y `posts`, NestJS con TypeScript en `notifications` | S1 y S4 |
| Desplegada en entorno productivo en la nube | EKS en AWS | S5 cluster, S6 productivo |
| Cada microservicio contenedorizado con Docker | Dockerfile por repo, imágenes versionadas por SHA | S1 a S4 |
| Buenas prácticas de seguridad, OWASP Top 10 | Threat model y primera revisión en S7, segunda en S13 | S7 y S13 |
| Enfoque iterativo e incremental, metodologías ágiles | 15 sprints semanales, Project con board, actas y retros | Continuo |
| Documentación técnica y funcional | `T-49`, más ADR y C4 | S11 a S13 |
| Testing unitario, de integración y de estrés con volumen | `T-36`, `T-37`, `T-40` y `T-41` | S3 continuo, S6 y S12 |
| Tests de integración en todos los servicios backend | `T-37` | Continuo desde S3 |
| Cobertura del 85% por microservicio, frontend incluido, en CI | Gate que falla el PR. Backend desde S3, clientes desde S5 | S3 y S5 |
| Pipeline de CD con GitHub Actions | `T-14`, build, push y despliegue con rollback | S5 |
| Observabilidad con métricas, logs y trazas, con acceso del tutor | `T-42`, Grafana Cloud, acceso verificado con `T-43` | S6 acceso, S10 completo |
| Rate limiting en al menos un microservicio | Por IP en el Gateway, por usuario en `users-api` y `posts-api` | S3 y S5 |
| Al menos una cola entre dos microservicios | RabbitMQ: `users-api` publica, `notifications-api` consume | S4 |
| Buena experiencia de usuario | Sistema de componentes en S3, revisión de UX y accesibilidad en S13 | S3 y S13 |

Y las cuatro condiciones de aprobación:

| Condición | Estado en el plan |
|---|---|
| Cumplir todos los requisitos anteriores | Los 17, con sprint asignado |
| Las 30 historias obligatorias con todos sus criterios de aceptación | 82 puntos, cerradas el 26 de octubre |
| 15 puntos optativos por integrante | 19, 18, 18 y 18. Mínimo exigido: 60. Comprometido: 73 |
| Al menos una funcionalidad con Inteligencia Artificial | Triage asistido de denuncias, propuesta en S7, acordada en S9, implementada en S10 |

Las tres historias fuera de alcance (Social Login, Post con Video y Mensajes Directos) son optativas, están declaradas y suman 18 puntos que el equipo no necesita. No dejarlas fuera obligaría a comprometer 91 puntos optativos para no "tener huecos", que es exactamente el error que hunde proyectos de cursada.

## Capacidad y velocidad requerida

Este es el número que hace honesta a toda la planificación.

- 155 puntos comprometidos.
- 12 semanas efectivas de entrega de historias (S2 a S12; S1 es fundaciones y S13 a S15 son estabilización y defensa).
- **12,9 puntos por semana.**
- Con 4 integrantes: **3,2 puntos por persona por semana.**

Ese es el ritmo que hay que sostener, no un promedio deseable.

**Mecanismo de control semanal.** Cada lunes, en la reunión, se registra en el issue del sprint los puntos aceptados reales frente a los planificados. La regla:

| Señal | Acción |
|---|---|
| Un sprint por debajo del 70% | Se anota, no se actúa. Una semana mala pasa. |
| Dos sprints consecutivos por debajo del 80% | Se recorta la primera historia **flex** del backlog y se avisa al tutor. |
| Menos de 60 puntos aceptados al 28 de septiembre | Revisión formal de alcance con el tutor en el checkpoint del 19 de octubre. |
| Menos de 82 puntos obligatorios al 26 de octubre | Situación crítica. Se congelan todas las optativas hasta cerrarlas. |

Recortar tarde es lo que hace fracasar los proyectos de cursada. Los checkpoints de "% de avance acordado con el tutor" del 7 de septiembre, 21 de septiembre y 19 de octubre son la vía legítima para renegociar, y están en el cronograma de la cátedra precisamente para eso.

## Participación pareja de los cuatro integrantes

La consigna exige que cada estudiante pueda explicar y justificar lo que hizo. Un reparto que encierre a alguien en una capa lo perjudica en la defensa, y un reparto que cargue a uno con el 40% de los puntos de un sprint hace que el resto no tenga qué contar. Tres reglas resuelven esto sin pelearse con la especialización:

**1. Propiedad vertical, no por capa.** El dueño de una historia la lleva de punta a punta: migración, endpoint, tests unitarios y de integración, pantalla en mobile o en backoffice, y la demo del lunes. No existe "el del backend" y "el del front". Esto garantiza que los cuatro toquen FastAPI, NestJS, React y Expo a lo largo del semestre.

**2. La especialización vive en las optativas y en los roles, no en las obligatorias.** Cada bloque de optativas se mantiene junto, que es donde se concentra su área y donde se paga una sola vez el costo de contexto. Las obligatorias se reparten en el planning de cada lunes con dos objetivos: nivelar los puntos de la semana y cubrir el hueco de stack de quien lo tenga.

**3. Roles rotativos semanales.** Cada semana los cuatro roles rotan una posición, así en cuatro semanas todos pasaron por los cuatro:

| Rol | Responsabilidad de la semana |
|---|---|
| Facilitador | Modera el planning del lunes y el daily escrito. Mantiene el board limpio. Persigue bloqueos. |
| Guardián de CI | El pipeline queda verde. Cobertura por encima del gate. Tests intermitentes arreglados o dados de baja con issue. |
| Revisor primario | Primer revisor de todos los PR de la semana. Nadie mergea sin su aprobación o la de un suplente. |
| Escriba | Acta del lunes en `docs/actas/`. ADRs de las decisiones de la semana. Documentación que el sprint haya generado. |

**Techo y piso de carga.** Nadie cierra más del 40% ni menos del 15% de los puntos de un sprint. Si alguien va a pasarse del techo, se le pasa una historia a quien esté por debajo del piso. Se verifica cada lunes en la vista `Por integrante` del Project, que suma Story Points por asignado filtrando por el sprint actual. Es una vista, no una planilla aparte: si el control vive fuera del board, no se hace.

La regla mide puntos de historia, que no son todo el trabajo. Quien lidera una issue técnica grande, como provisionar el cluster o correr la prueba de carga, puede quedar legítimamente por debajo del piso esa semana. Cuando pasa, se anota en el acta del lunes con la issue técnica que lo justifica. Sin esa anotación, quedar por debajo del piso es un problema, no una excepción. Los cuatro casos previstos en este plan son S1 y S2, donde casi no hay historias, S6 con el Bloque 1 en el 14% mientras corre la línea base de carga, y S12 con el Bloque 2 en cero mientras lidera el seed y la prueba de carga final.

## Sprints

Un sprint es una semana. Empieza el lunes después del planning y se revisa el lunes siguiente, en la reunión donde el tutor mira lo hecho y se acuerda lo que viene. Cada sprint tiene que terminar con **algo demostrable**, no con trabajo en curso: esa es la única forma de que la reunión de los lunes sirva para algo.

Dos sprints duran dos semanas porque caen sobre feriados: S8 sobre el 12 de octubre y S13 sobre el 23 de noviembre.

El orden de las historias no sigue el orden de las épicas de la consigna sino el de las dependencias reales del sistema. En particular el grafo social se construye antes que el feed, porque un feed "con las publicaciones de los usuarios que sigo" no se puede aceptar sin la relación de seguimiento.

| Sprint | Trabajo | Se revisa | Puntos | Foco |
|---|---|---|---:|---|
| S1 | 19 - 23 ago | 24 ago | 0 | Tablero y API dockerizada |
| S2 | 24 - 30 ago | 31 ago | 8 | Backoffice dockerizado y registro |
| S3 | 31 ago - 6 sept | 7 sept | 15 | Testing, CI y administradores |
| S4 | 7 - 13 sept | 14 sept | 13 | Grafo social y E2E backoffice |
| S5 | 14 - 20 sept | 21 sept | 11 | Posts, feed y E2E mobile |
| S6 | 21 - 27 sept | **28 sept** | 14 | Despliegue productivo en AWS |
| S7 | 28 sept - 4 oct | 5 oct | 15 | Interacciones y media |
| S8 | 5 - 18 oct | 19 oct | 24 | Búsqueda, notificaciones y spike de IA |
| S9 | 19 - 25 oct | **26 oct** | 14 | Cierre de obligatorias |
| S10 | 26 oct - 1 nov | 2 nov | 13 | Observabilidad e IA |
| S11 | 2 - 8 nov | 9 nov | 14 | Escalabilidad y optativas |
| S12 | 9 - 15 nov | 16 nov | 14 | Carga, documentación y últimas optativas |
| S13 | 16 - 29 nov | **30 nov** | 0 | Endurecimiento y release |
| S14 | 30 nov - 6 dic | 7 dic | 0 | Entrega final y correcciones |
| S15 | 7 - 13 dic | 14 dic | 0 | Recuperatorio y funcionalidad extra |
| | | **Total** | **155** | |

---

### S1 - Tablero y walking skeleton backend

**Trabajo:** miércoles 19 - domingo 23 de agosto · **Se revisa:** lunes 24 de agosto · **Clase de ese lunes:** Desarrollo Frontend

**Compromiso con la cátedra:** primera API REST creada y dockerizada para desarrollo local. Más el tablero Kanban que quedó pendiente del 10 de agosto.

**Entregable demostrable:** `docker compose up` en `udesa-x-users-api` levanta el servicio y `GET /healthcheck` responde. El Project está configurado y tiene cargadas las issues de S1 y S2, cada una en su repositorio, con épica, puntos, dueño y sprint. Los seis repos tienen `AGENTS.md`, `.editorconfig` y las dos skills. El tutor entra al board, ve la semana cerrada y la siguiente comprometida, y encuentra el alcance completo del semestre en este documento.

**Por qué no se carga el backlog entero en S1.** Una issue de S8 escrita en agosto se reescribe en septiembre: el modelo de datos, los contratos y el alcance todavía se están decidiendo. Un tablero con ciento y pico de tarjetas que nadie tocó no muestra un plan, muestra una lista de deseos, y vuelve invisible el trabajo de la semana en curso. El alcance comprometido del semestre está en el inventario de este documento, que es donde tiene que estar; el tablero refleja lo que está en ejecución. Cada lunes, en el planning, se cargan las issues del sprint que arranca. Eso es lo que la consigna llama enfoque iterativo e incremental.

**Por qué las skills y los `AGENTS.md` van en S1 y no más adelante.** Si el equipo arranca a programar sin ellos, cada uno adopta su propia forma de trabajar con el agente durante las primeras semanas, y después no se corrige: se corrige el proceso, no lo ya mergeado. La condición de que cada uno pueda explicar lo suyo se gana o se pierde en las primeras dos semanas.

Sprint de cinco días sin puntos de historia. Todo el esfuerzo va a destrabar a los otros tres integrantes: hasta que exista la plantilla de repositorio de servicio, nadie puede empezar una historia sin inventar su propia estructura.

| Trabajo | Dueño |
|---|---|
| `T-00` Configurar el Project y cargar las issues de S1 y S2 | Tomás |
| `T-01` Crear `udesa-x-platform` y registrar los ADR de lo ya decidido | Joaquín, ADR por Tomás |
| `T-63` `AGENTS.md` base y por repositorio | Fede |
| `T-64` Skills `explicar-implementacion` y `revisar-pr` | Fede |
| `T-65` `.editorconfig`, linters y formatters en los seis repos | sin asignar, faltan linters |
| `T-66` Instrucciones de Copilot y plantilla de PR en español | Fede |
| `T-67` Script de sincronización de comunes y convención de tags | Fede |
| `T-02` Definir límites, responsables y contratos de cada servicio | Los cuatro, sesión conjunta |
| `T-05` Plantilla de repositorio de servicio: estructura, Dockerfile, scripts, reusable workflows | Fede |
| `T-06` `docker-compose.dev.yml` en `users-api` con PostgreSQL y Redis | Tomás |
| `T-08` `/healthcheck` estandarizado, con dependencias verificadas | sin asignar |
| `T-13` CI mínimo vía reusable workflow: lint, build y test en cada PR | sin asignar |
| `T-17` Ramas protegidas y convención de ramas `feature-`/`fix-` | Tomás |
| `T-23` Presupuesto del cluster y alertas de gasto | sin asignar |
| `T-24` Formato de error con Problem Details | Tomás |
| `T-25` Versionado de API y política de cambios | Tomás |
| `T-61` Cuentas de AWS con plan pago, budget con alertas | Los cuatro |

**Consultas al tutor esta semana:** qué fecha de entrega intermedia y final le toca al grupo 3, si hay créditos de AWS disponibles o aplica AWS Academy Learner Lab, y validación de los ADR y del alcance comprometido.

---

### S2 - Backoffice dockerizado y registro de usuarios

**Trabajo:** 24 - 30 de agosto · **Se revisa:** lunes 31 de agosto · **Clase previa:** Desarrollo Frontend (24 ago)

**Compromiso con la cátedra:** backoffice web creado y dockerizado para desarrollo local.

**Entregable demostrable:** `docker compose -f compose/docker-compose.full.yml up` desde `udesa-x-platform` levanta `users-api`, `posts-api`, el backoffice, las bases y RabbitMQ. Un usuario se registra desde la app, recibe el email de verificación y hace login.

| Historia | Pts | Dueño |
|---|---:|---|
| E.1 H1. Registro de Usuarios | 3 | sin asignar |
| E.1 H2. Inicio de Sesión | 3 | sin asignar |
| E.1 H3. Cierre de Sesión | 1 | sin asignar |
| E.1 H12. Aceptación de Términos y Privacidad | 1 | sin asignar |

**Técnicas:** `T-04` bases gestionadas fuera del cluster · `T-05` y `T-06` replicados en `posts-api`, `backoffice` y `mobile` · `T-07` compose integrado en platform · `T-15` registry e imágenes por SHA · `T-22` definición de entornos · `T-51` navegación y tabs de la app · `T-52` splash, sesión persistente y refresco de token · `T-58` textos de Términos y Privacidad.

**Puntos por bloque:** 1 · 3 · 1 · 3. Está desparejo en historias a propósito: en S1 y S2 el grueso del trabajo son issues técnicas, y ahí la carga sí está repartida. El techo y el piso de carga empiezan a aplicar en S3.

**Decisión de la semana:** el email de verificación se manda **sincrónico** desde `users-api`, con un adaptador detrás de una interfaz. No se levanta la cola todavía, por dos razones. La consigna exige una cola "para comunicar dos microservicios", y en S2 el único consumidor posible sería el propio `users-api`, así que no cumpliría el requisito. Y la clase de Escalabilidad con la demo de colas es el 2 de noviembre: adelantarse diez semanas no aporta nada. La cola entra en S4, cuando nace `notifications-api` y hay dos servicios de verdad. El adaptador es lo que hace que ese cambio sea de una tarde.

---

### S3 - Testing, CI y administradores

**Trabajo:** 31 de agosto - 6 de septiembre · **Se revisa:** lunes 7 de septiembre · **Clase previa:** Testing (31 ago)

**Compromiso con la cátedra:** API testeada y pipeline de CI implementado y corriendo. Primer checkpoint de porcentaje de avance acordado con el tutor. **A partir del 7 de septiembre, todo el código que se sube va testeado.**

**Entregable demostrable:** el pipeline de `users-api` corre unitarios e integración, publica cobertura y **falla el PR si baja del 85%**. En mobile y backoffice el mismo pipeline publica cobertura pero todavía no bloquea: ese gate se enciende en S5. Un SuperAdmin crea un moderador desde el backoffice y el moderador entra con su cuenta.

| Historia | Pts | Dueño |
|---|---:|---|
| E.5 H1. Creación de Administradores | 5 | sin asignar |
| E.1 H5. Olvidé Mi Contraseña | 3 | sin asignar |
| E.1 H13. Cambiar Contraseña (optativa) | 3 | sin asignar |
| E.5 H2. Inicio de Sesión como Administrador | 2 | sin asignar |
| E.1 H6. Editar mi perfil | 2 | sin asignar |

**Técnicas:** `T-13` gate de cobertura del 85% activo en los repos backend · `T-36` y `T-37` suites unitarias y de integración en los dos servicios backend · `T-26` rate limiting por usuario reutilizable, que E.1 H5 CA.8 ya exige · `T-29` RBAC de SuperAdmin y Moderador · `T-19` sistema de componentes de mobile y backoffice.

**Puntos por bloque:** 4 · 3 · 3 · 5.

**Decisión de la semana:** mobile arranca directo en React Native Testing Library 14, con las APIs core async desde el primer test, y el E2E de mobile es Maestro, no Detox, que está abandonado.

---

### S4 - Grafo social y flujo end to end del backoffice

**Trabajo:** 7 - 13 de septiembre · **Se revisa:** lunes 14 de septiembre · **Clase previa:** Arquitectura (7 sept)

**Compromiso con la cátedra:** flujo completo end to end desde el backoffice hasta el backend. Inicio del desarrollo mobile. Los microservicios acordados con el tutor ya están creados desde S1; en S4 entra en producción el tercero, `notifications-api`, con la cola.

**Entregable demostrable:** el backoffice hace login, lista usuarios y crea administradores contra `users-api` real, sin mocks. `notifications-api` consume su primer evento de la cola y manda el email de verificación. En mobile se sigue y se deja de seguir a un usuario.

| Historia | Pts | Dueño |
|---|---:|---|
| E.3 H1. Seguir a un Usuario | 5 | sin asignar |
| E.3 H3. Listado de Seguidores y Seguidos | 3 | sin asignar |
| E.1 H7. Preferencias (optativa) | 2 | sin asignar |
| E.3 H2. Dejar de Seguir a un Usuario | 2 | sin asignar |
| E.1 H10. Tema de la Aplicación (optativa) | 1 | sin asignar |

**Técnicas:** `T-27` cola con contratos de eventos versionados: `users-api` publica y `notifications-api` consume el envío de emails, que es el requisito de la consigna cumplido con un caso de uso real · `T-16` script de sincronización de contratos y test de divergencia · `T-28` patrón outbox para publicación confiable de eventos · `T-30` paginación por cursor como estándar transversal · `T-50` primera versión de los diagramas C4 · `T-56` pantalla de solicitudes de seguimiento pendientes.

**Puntos por bloque:** 3 · 3 · 5 · 2.

**Spike en paralelo:** el Bloque 4 arranca el spike de EKS esta semana, sin esperar a la clase de Cloud Computing II del 21 de septiembre. Es lo que evita que la entrega intermedia dependa de aprender AWS en siete días.

---

### S5 - Publicaciones, feed y flujo end to end de mobile

**Trabajo:** 14 - 20 de septiembre · **Se revisa:** lunes 21 de septiembre · **Clase previa:** Cloud Computing I, Kubernetes (14 sept)

**Compromiso con la cátedra:** flujo end to end desde la app mobile hasta el backend. Segundo checkpoint de porcentaje de avance con el tutor.

**Entregable demostrable:** desde el teléfono, un usuario se registra, sigue a otro, publica, ve su feed cronológico con scroll infinito y visita un perfil. El cluster de EKS existe y sirve el healthcheck de los tres servicios a través del Gateway con TLS.

| Historia | Pts | Dueño |
|---|---:|---|
| E.2 H1. Crear Post | 3 | sin asignar |
| E.2 H2. Feed Principal | 3 | sin asignar |
| E.2 H14. Visualización de Perfil de Usuario | 3 | sin asignar |
| E.2 H3. Eliminar Post | 2 | sin asignar |

**Técnicas:** `T-09` provisionar el cluster de EKS · `T-10` Gateway API con NGINX Gateway Fabric: TLS, routing y rate limiting por IP · `T-11` manifiestos base con Kustomize y overlays · `T-12` SOPS con age y configuración por entorno · `T-14` workflow de CD con despliegue, rollback y OIDC hacia AWS · `T-53` estados de carga, vacío y error en todas las pantallas · `T-54` pull to refresh en el feed.

**Puntos por bloque:** 3 · 3 · 3 · 2.

---

### S6 - Despliegue productivo y entrega intermedia

**Trabajo:** 21 - 27 de septiembre · **Se revisa:** lunes 28 de septiembre, **entrega intermedia** · **Clase previa:** Cloud Computing II, AWS y EKS (21 sept)

**Compromiso con la cátedra:** sistema funcionando en forma productiva, desplegado en AWS, con toda la funcionalidad comprometida y acordada con el tutor.

**Entregable demostrable:** la app instalada en un teléfono pega contra el backend desplegado en EKS, no contra localhost. El backoffice está publicado con dominio y TLS. La pantalla de estado de los microservicios muestra los tres servicios en verde, con su versión desplegada.

| Historia | Pts | Dueño |
|---|---:|---|
| E.5 H11. Estado de los Microservicios (optativa) | 5 | sin asignar |
| E.1 H8. Foto de Perfil (optativa) | 3 | sin asignar |
| E.5 H9. Registro de Última Conexión (optativa) | 2 | sin asignar |
| E.3 H4. Bloquear Usuario | 2 | sin asignar |
| E.3 H5. Denunciar Usuario | 2 | sin asignar |

**Técnicas:** `T-20` walking skeleton completo desplegado y accesible · `T-21` observabilidad mínima con logs estructurados y dashboard de healthchecks · `T-43` cuenta de Grafana Cloud y acceso del tutor verificado, dado el límite de 3 asientos del free tier · `T-31` servicio de media con subida por streams y validación por magic numbers · `T-39` seed de datos y generador de volumen · `T-40` primera prueba de carga con línea base sobre el feed.

**Nota operativa:** pasar el nodegroup a on-demand antes de la entrega y dejarlo así hasta el 28 de septiembre; una interrupción de Spot durante la defensa no vale el ahorro.

**Puntos por bloque:** 2 · 3 · 4 · 5. El Bloque 1 queda por debajo del piso del 15% porque lidera `T-39` y `T-40`, el seed y la prueba de carga de línea base. Queda registrado en el acta.

**Estado al cerrar S6:** 45 de 82 puntos obligatorios (55%) y 16 de 73 optativos. Ese es el número que se lleva a la entrega intermedia y el que hay que acordar con el tutor en el checkpoint del 21 de septiembre, antes de la entrega, no después.

---

### S7 - Interacciones y contenido con media

**Trabajo:** 28 de septiembre - 4 de octubre · **Se revisa:** lunes 5 de octubre, segunda fecha de entrega intermedia

**Entregable demostrable:** el hilo de conversación funciona de punta a punta: responder, retweetear, dar like y publicar con imagen, todo desde mobile y visible en el feed de los seguidores.

| Historia | Pts | Dueño |
|---|---:|---|
| E.2 H7. Post con Imagen | 5 | sin asignar |
| E.2 H4. Responder a un Post | 2 | sin asignar |
| E.2 H6. Like a un Post | 2 | sin asignar |
| E.3 H9. Invitar Usuarios Externos (optativa) | 2 | sin asignar |
| E.2 H5. Retweet / Repost | 2 | sin asignar |
| E.5 H8. Exportar Datos (optativa) | 2 | sin asignar |

**Técnicas:** `T-18` primera revisión OWASP completa sobre los flujos implementados · `T-32` política de soft-delete y retención documentada · `T-55` pantalla de detalle de post e hilo de conversación · idempotencia verificada en likes y retweets.

**Puntos por bloque:** 5 · 2 · 4 · 4, sobre 15.

**Por qué esta semana bajó de 18 a 15 puntos.** S7 arranca el lunes de la entrega intermedia y termina en la segunda fecha de entrega. Es la semana donde con más probabilidad hay que corregir lo que el tutor observe, y además lleva `T-18`, la primera revisión OWASP completa. Cargarla al 40% por encima del promedio del semestre era planificar el atraso. E.1 H14, Onboarding Inicial, se corrió a S11.

El Bloque 2 queda en el 13%, por debajo del piso, porque lidera las correcciones de la entrega intermedia y `T-55`, la pantalla de detalle de post e hilo. Queda registrado en el acta.

**Propuesta de IA:** `AI-01`, propuesta informal al tutor esta semana. La presentación formal es el 26 de octubre, pero llegar a esa fecha con la propuesta recién pensada deja sin margen para cambiarla.

---

### S8 - Búsqueda, notificaciones y spike de IA

**Trabajo:** 5 - 18 de octubre, dos semanas por el feriado del 12 · **Se revisa:** lunes 19 de octubre · **Clase de ese lunes:** AI Engineering II

**Compromiso con la cátedra:** tercer checkpoint de porcentaje de avance. Inicio de la implementación de la feature de IA.

**Entregable demostrable:** buscar posts y usuarios con resultados paginados. Recibir una notificación push en el teléfono al ganar un seguidor y verla en el centro de notificaciones, con deep link a la pantalla correcta.

| Historia | Pts | Dueño |
|---|---:|---|
| E.2 H8. Hashtags (optativa) | 3 | sin asignar |
| E.2 H9. Menciones a Usuarios (optativa) | 3 | sin asignar |
| E.1 H4. Eliminación de Cuenta | 3 | sin asignar |
| E.4 H3. Centro de Notificaciones In-App | 3 | sin asignar |
| E.4 H1. Notificación de nuevo seguidor | 2 | sin asignar |
| E.4 H2. Notificación de interacción | 2 | sin asignar |
| E.2 H10. Búsqueda de Posts y Usuarios | 5 | sin asignar |
| E.5 H12. Gestión de Feedback/Reportes (optativa) | 3 | sin asignar |

**Técnicas:** `T-33` FCM con registro, actualización y depuración de device tokens · `T-34` deep linking en la app instalada · `T-38` suite E2E de los flujos críticos · `AI-02` datos enviados, privacidad, proveedor y modelo · `AI-03` spike técnico con prompt, salida estructurada y costo medido.

**Puntos por bloque:** 6 · 6 · 4 · 8, sobre dos semanas y 24 puntos. Son 12 por semana, por debajo del promedio del semestre: S8 parece el sprint más grande y no lo es, porque dura el doble. E.5 H12 se adelantó desde S11 aprovechando esa holgura.

E.1 H4 va acá y no antes porque sus criterios de aceptación dependen de que ya existan seguidores (CA.2), respuestas y retweets (CA.5). Ubicarla antes garantiza que quede a medias.

---

### S9 - Cierre de las historias obligatorias

**Trabajo:** 19 - 25 de octubre · **Se revisa:** lunes 26 de octubre · **Clase previa:** AI Engineering II (19 oct)

**Compromiso con la cátedra:** **finalización de las historias de usuario obligatorias.** Presentación de la propuesta de la feature de IA.

**Entregable demostrable:** el flujo completo de moderación de punta a punta: un usuario denuncia desde mobile, la denuncia aparece en la bandeja del backoffice, un moderador bloquea al denunciado y la acción queda en el log de auditoría. Y las 30 historias obligatorias aceptadas por el tutor.

| Historia | Pts | Dueño |
|---|---:|---|
| E.5 H7. Gestión de Denuncias | 3 | sin asignar |
| E.5 H5. Bloqueo de Usuarios por Admin | 2 | sin asignar |
| E.5 H6. Logs de Auditoría | 3 | sin asignar |
| E.4 H5. Configurar Preferencias de Notificación (optativa) | 3 | sin asignar |
| E.5 H4. Buscador y Detalles de Usuarios | 3 | sin asignar |

**Técnicas:** `AI-01` presentación formal de la feature de IA al tutor · arranque de `T-42`, instrumentación de métricas y trazas.

**Puntos por bloque:** 5 · 3 · 3 · 3.

**Este es el hito que hay que defender.** 82 de 82 puntos obligatorios aceptados, 26 de octubre. Si el 19 de octubre el equipo tiene más de 8 puntos obligatorios abiertos, se congela toda historia optativa hasta cerrarlos.

---

### S10 - Observabilidad y feature de IA

**Trabajo:** 26 de octubre - 1 de noviembre · **Se revisa:** lunes 2 de noviembre · **Clase previa:** Observabilidad (26 oct)

**Compromiso con la cátedra:** observabilidad agregada al sistema e integración con herramienta de visualización.

**Entregable demostrable:** un dashboard con métricas, logs y trazas correlacionadas de los tres servicios, con acceso verificado del tutor. Una denuncia entra por la cola, el modelo la clasifica y el moderador ve la sugerencia en su bandeja, con la decisión final siempre humana.

| Historia | Pts | Dueño |
|---|---:|---|
| E.4 H4. Notificación de Mención (optativa) | 5 | sin asignar |
| E.3 H10. Silenciar Usuario (optativa) | 5 | sin asignar |
| E.1 H11. Enviar Feedback o Reportar Error (optativa) | 3 | sin asignar |

**Técnicas:** `T-42` métricas, logs y trazas distribuidas con correlación entre servicios · `T-44` alertas y notificación de incidentes · `AI-04` implementar el triage asistido · `AI-05` integrar la sugerencia en la bandeja · `AI-06` tests de casos válidos, errores, timeout y baja confianza.

**Puntos por bloque:** 5 · 3 · 5 · 0, sobre 13.

**Por qué esta semana bajó de 18 a 13 puntos.** S10 es la semana de la feature de IA completa (`AI-04`, `AI-05`, `AI-06`) más métricas, logs y trazas distribuidas (`T-42`, `T-44`). Ese trabajo técnico no da puntos de historia pero es el entregable que la cátedra espera el 2 de noviembre. Sumarle 18 puntos encima era la sobrecarga más clara del plan. E.5 H3 se corrió a S11, donde además llega después de que exista la observabilidad de la que se alimenta.

El Bloque 4 queda en cero puntos de historia porque lidera `T-42` y `T-44`, que es el compromiso de la semana con la cátedra. Queda registrado en el acta.

E.3 H10 va antes que E.4 H4 en la misma semana por dependencia: E.4 H4 CA.2 exige no notificar menciones de usuarios silenciados.

---

### S11 - Escalabilidad y optativas de plataforma

**Trabajo:** 2 - 8 de noviembre · **Se revisa:** lunes 9 de noviembre · **Clase previa:** Escalabilidad (2 nov)

**Compromiso con la cátedra:** implementación de historias de usuario optativas y documentación.

**Entregable demostrable:** el sistema escala horizontalmente bajo carga, con HPA por servicio y KEDA escalando `notifications-api` a cero y de vuelta según la cola de RabbitMQ. Los servicios publican eventos con el patrón outbox y ninguno se pierde al reiniciar un pod.

| Historia | Pts | Dueño |
|---|---:|---|
| E.5 H3. Visualización de Métricas (optativa) | 5 | sin asignar |
| E.2 H11. Trending Topics (optativa) | 3 | sin asignar |
| E.1 H14. Onboarding Inicial (optativa) | 3 | sin asignar |
| E.3 H7. Usuarios en Línea (optativa) | 3 | sin asignar |

**Técnicas:** `T-59` HorizontalPodAutoscaler por servicio, más KEDA escalando `notifications-api` por profundidad de cola con `minReplicaCount: 0` · `T-35` detección de idioma del contenido para el filtro de feed de E.1 H7 CA.2 · revisión del outbox bajo carga · arranque de `T-49`, documentación técnica y funcional.

**Puntos por bloque:** 3 · 3 · 3 · 5, sobre 14. Una historia por integrante y por área, sin dependencias entre ellas. E.5 H3 llegó desde S10 y encaja mejor acá: el dashboard de métricas del backoffice se apoya en la observabilidad que se terminó de instrumentar la semana anterior.

---

### S12 - Carga, testing y últimas optativas

**Trabajo:** 9 - 15 de noviembre · **Se revisa:** lunes 16 de noviembre · **Clase previa:** System Design (9 nov)

**Compromiso con la cátedra:** carga de usuarios y testing de la aplicación.

**Entregable demostrable:** la prueba de carga corrida contra los SLOs con el volumen sembrado completo, comparada contra la línea base de S6, con el informe de qué se optimizó y por qué. Y los últimos 14 puntos optativos aceptados: **73 de 73**.

| Historia | Pts | Dueño |
|---|---:|---|
| E.2 H13. Citar Post (optativa) | 5 | sin asignar |
| E.2 H12. Guardar Posts (optativa) | 3 | sin asignar |
| E.3 H8. Listas Personalizadas (optativa) | 3 | sin asignar |
| E.5 H10. Borrado Forzado de Contenido (optativa) | 3 | sin asignar |

**Técnicas:** `T-39` seed con el volumen completo, 10.000 usuarios y 500.000 follows · `T-41` prueba de carga final contra los SLOs · `T-49` documentación técnica y funcional · tuning de índices según lo que muestre la prueba.

**Puntos por bloque:** 5 · 3 · 3 · 3, sobre 14. El Bloque 2 lidera además la prueba de carga y el seed, que es el avance que la cátedra espera el 16 de noviembre; por eso toma una sola historia de 3 puntos y no dos.

**Tres de las cuatro historias de esta semana son flex** (E.2 H12, E.3 H8 y E.5 H10). Es deliberado: el último sprint con puntos es el más recortable de todos, y si el semestre se atrasó, acá se corta sin tocar nada anterior.

---

### S13 - Endurecimiento y release

**Trabajo:** 16 - 29 de noviembre, dos semanas por el feriado del 23 · **Se revisa:** lunes 30 de noviembre, **entrega final** · **Clase previa:** Retro (16 nov)

Sin puntos nuevos. Este sprint se reserva íntegro para estabilizar. Si se usa para desarrollar, la planificación falló.

**Entregable demostrable:** el sistema completo en producción, sin defectos críticos abiertos, con la documentación entregada y cada integrante capaz de explicar y justificar sus decisiones.

- Regresión completa de los 56 conjuntos de criterios de aceptación.
- `T-45` distribución del build mobile al tutor y verificación de que puede instalarlo.
- `T-46` runbook de despliegue, rollback y recuperación, probado en staging.
- `T-47` backup y restore de las bases de datos, con restauración verificada.
- `T-48` revisión de UX, accesibilidad y consistencia visual en mobile y backoffice.
- `T-49` documentación técnica y funcional cerrada.
- `T-50` diagramas C4 finales, alineados con lo que está desplegado.
- `T-60` NetworkPolicies entre pods.
- `T-62` Pinnear GitHub Actions por SHA, SBOM con syft y attestations de build.
- `AI-07` documentar intervención humana, límites y sesgos del modelo.
- Segunda revisión OWASP, con foco en todo lo agregado desde S7.
- Corrección de vulnerabilidades críticas y altas.
- Smoke tests en producción.
- Evidencias consolidadas de CI/CD, cobertura y observabilidad.
- Retrospectiva del semestre y ensayo de la exposición.

**Reparto:** los cuatro tienen el mismo tipo de trabajo. Cada uno se hace cargo de la regresión y la documentación de sus propias historias, más un ítem transversal de la lista.

---

### S14 - Entrega final y correcciones

**Trabajo:** 30 de noviembre - 6 de diciembre · **Se revisa:** lunes 7 de diciembre, segunda fecha de entrega final

Corrección de lo que el tutor haya observado el 30 de noviembre. Si al grupo le tocó la primera fecha, este sprint es margen puro y hay que tratarlo como tal, no como semana de descanso: es el colchón que absorbe cualquier cosa que se haya corrido.

---

### S15 - Recuperatorio y funcionalidad extra

**Trabajo:** 7 - 13 de diciembre · **Se revisa:** lunes 14 de diciembre, entrega de notas

Solo aplica si algo quedó pendiente. El cronograma de la cátedra es explícito: la recuperación exige el proyecto y la documentación finalizados **más una funcionalidad extra comprometida con el tutor**. Llegar acá con deuda no cuesta una semana, cuesta una funcionalidad que nadie planificó. Está registrado como R14.

## Funcionalidad de Inteligencia Artificial

### Propuesta: triage asistido de denuncias en el backoffice

Al llegar una denuncia (E.3 H5), un consumidor de la cola envía el contenido reportado a un modelo de lenguaje que devuelve una clasificación estructurada:

- Categoría sugerida entre las de E.3 H5 CA.1: Spam, Acoso, Contenido inapropiado, Suplantación de identidad.
- Severidad sugerida: baja, media, alta.
- Una justificación breve.
- Un nivel de confianza.

El resultado se persiste junto a la denuncia y se muestra al moderador en E.5 H7 como una sugerencia, ordenando la bandeja por severidad.

### Restricciones de diseño no negociables

- **La IA nunca sanciona.** El moderador confirma o corrige. La acción disciplinaria siempre la ejecuta una persona.
- **Se registra la decisión humana** junto a la sugerencia de la IA, incluyendo cuándo el moderador la contradijo. Esto da material para la exposición y es la práctica correcta.
- **Minimización de datos**: se envía el texto reportado y el motivo, nunca email, handle ni identificadores del denunciante o denunciado.
- **Degradación controlada**: timeout definido, y si el proveedor no responde la denuncia entra sin sugerencia. El backoffice nunca se bloquea por la IA.
- **Costo acotado**: la clasificación de texto corto es la tarea de LLM más barata que existe. Con `claude-haiku-4-5` a 1 USD por millón de tokens de entrada y 5 USD por millón de salida, y denuncias de unos cientos de tokens, el costo del proyecto entero es de centavos.

### Por qué esta funcionalidad y no otra

Se apoya en E.3 H5 y E.5 H7, que son obligatorias, así que no agrega superficie nueva de producto. Tiene un criterio de éxito medible: se puede comparar la sugerencia contra la decisión del moderador y reportar una tasa de acierto. Y tiene una historia de riesgo clara para defender en la exposición: sesgo, falsos positivos, y por qué la decisión final es humana.

### Alternativas si el tutor prefiere otra cosa

1. **Detección de idioma del contenido** para alimentar el filtro de E.1 H7 CA.2, que hoy es un requisito escondido sin implementación obvia.
2. **Recomendación de cuentas** en el onboarding de E.1 H14 CA.3, basada en los intereses seleccionados.
3. **Resumen de hilos largos** de conversación en E.2 H4.

## Riesgos

Registro vivo. Se revisa cada lunes en el planning, no una vez por mes.

| # | Riesgo | Prob. | Impacto | Mitigación | Cuándo se decide |
|---|---|---|---|---|---|
| R1 | Cobertura del 85% en el frontend mobile es costosa y se posterga | Alta | Alto | **Gate escalonado**: backend desde S3, mobile y backoffice desde S5. Entre S3 y S5 los repos de cliente reportan cobertura sin bloquear, y el número se mira en la review del lunes. Se testean hooks, servicios y lógica de estado antes que componentes visuales. | S3 y S5 |
| R2 | Push en iOS requiere cuenta de Apple Developer paga | Media | Alto | Decidir en S2 si se demuestra solo en Android. Si es así, comunicarlo al tutor por escrito antes de S8. | S2 |
| R3 | Envío de emails limitado por sandbox del proveedor | Media | Medio | Verificar dominio en S1. Tener plan B con un segundo proveedor. El registro de S2 depende de esto. | S1 |
| R4 | Costo de EKS supera el presupuesto | Alta | Muy alto | El control plane (73 USD/mes) no se puede pausar y es el 77% de la config mínima; una config razonable ronda 166 USD/mes. La palanca real es destruir y recrear el cluster entre sprints con Terraform (12-15 min), que baja el promedio a unos 9 USD/mes. Cuentas de plan pago desde S1, con budget y alertas (`T-61`, `T-23`). | S1 |
| R5 | Mantener dos stacks backend duplica la infraestructura de calidad | Alta | Medio | Limitar a exactamente dos lenguajes. Plantillas de servicio compartidas. Workflows de CI parametrizados. | S1 |
| R6 | Consistencia de contadores entre servicios | Media | Alto | Mantener follows y posts en el mismo servicio para poder usar transacciones locales. Documentado como ADR. | S1 |
| R7 | Un integrante se atrasa y bloquea a los demás | Media | Alto | Historias flex identificadas. Techo del 40% y piso del 15% de los puntos del sprint por persona, verificado cada lunes. Pair programming en las historias de 5 puntos. | Semanal |
| R8 | Alcance de 155 puntos resulta inalcanzable | Media | Alto | Umbral de recorte definido: menos de 60 puntos aceptados al 28 de septiembre dispara revisión formal en el checkpoint del 19 de octubre. | 28 sept |
| R9 | El tutor rechaza criterios de aceptación al final | Baja | Alto | Aceptación incremental: cada lunes se demuestra lo de la semana, no se acumula para la entrega. | Semanal |
| R10 | Deriva entre lo documentado y lo implementado | Alta | Medio | Documentación en el repositorio, actualizada en el mismo PR que el código. Parte de la Definition of Done. | Continuo |
| R11 | **El despliegue en EKS se corre y arrastra la entrega intermedia del 28 de septiembre** | Media | Muy alto | El spike arranca en S4, el 7 de septiembre, sin esperar a la clase del 21. Plan B: desplegar en ECS con Fargate, que no exige aprender Kubernetes, aceptando que se pierde el alineamiento con el temario. La decisión se toma el 20 de septiembre, no después. | S5 |
| R12 | **Al grupo 3 le toca la fecha temprana de entrega y el plan estaba hecho para la tardía** | Media | Alto | Se planifica siempre contra la fecha temprana, 28 de septiembre y 30 de noviembre. Preguntar al tutor en S1. | S1 |
| R13 | **Un integrante llega a noviembre sin acumular sus 15 puntos optativos** | Media | Alto | Tabla de acumulación de optativas por integrante, revisada en los tres hitos de control. El Bloque 1 es el más expuesto porque sus optativas dependen del modelo de post. Si al 26 de octubre alguien está por debajo de 6 puntos optativos aceptados, se le reasigna una historia de otro integrante. | 26 oct |
| R14 | **Se llega al 7 de diciembre con deuda y el recuperatorio exige una funcionalidad extra** | Baja | Alto | S13 y S14 no llevan puntos nuevos. Cualquier historia que se corra a esas semanas se recorta en vez de correrse. | S12 |
| R15 | **La cuenta de AWS del free plan se cierra a los 6 meses o al agotar los 200 USD de crédito**, lo que ocurra primero, y el cuatrimestre dura más | Alta | Muy alto | Abrir cuentas con plan pago, una por integrante (800 USD en total), rotando quién hostea, con la infraestructura en código (`T-61`). | S1 |
| R16 | El techo de 100 operaciones/seg de MongoDB Atlas M0 hace que las pruebas de carga de S6 y S12 contra `notifications-api` choquen contra el free tier, no contra el sistema | Media | Medio | Decidir antes de S6 si se acota el alcance de esa prueba o se corre contra una instancia local. | S6 |

## Decisiones abiertas

Cada una necesita dueño y fecha de resolución. Se cargan como issues con la label `decision` en `udesa-x-platform` en S1, y ninguna puede quedar abierta más allá del sprint en el que bloquea una historia.

### Ambigüedades del enunciado que hay que consensuar con el tutor

| # | Tema | Detalle |
|---|---|---|
| D1 | Umbral de reportes | E.3 H5 CA.2 dice "más de 5" y CA.4 dice "si se cumple la condición". Definir si el umbral es 5 o 6. |
| D2 | Políticas de lockout | E.1 H2 bloquea a los 5 intentos por 15 minutos, E.1 H13 a los 3 por 15, E.5 H2 a los 3 por 30. Confirmar que son tres políticas distintas y documentar por qué. |
| D3 | Eliminación de cuenta | E.1 H4 dice "permanentemente" pero CA.1 exige soft-delete. Se implementa soft-delete y se documenta que "permanente" significa irreversible para el usuario. |
| D4 | Integridad de follows al eliminar cuenta | E.1 H4 CA.1 exige integridad referencial y CA.2 exige eliminar relaciones de seguimiento. Definir si los follows se borran físicamente o se marcan. |
| D5 | Roles de administrador | La consigna menciona SuperAdmin, administrador y Moderador. Unificar a dos roles: `SUPER_ADMIN` y `MODERATOR`. |
| D6 | Formato del handle | E.1 H1 CA.3 dice que empieza con `@` y tiene entre 4 y 15 caracteres. Definir si el `@` se almacena o es solo presentación, y si cuenta en el largo. |
| D7 | Aprobación de solicitudes de seguimiento | E.3 H1 CA.2 crea solicitudes pendientes pero ninguna historia describe la pantalla para aprobarlas o rechazarlas. Se implementa como parte de E.3 H1 bajo el criterio de "elementos implícitos". |
| D8 | Preferencia de presencia | E.3 H7 CA.3 exige poder ocultar el estado en línea, pero E.1 H7 no enumera esa preferencia. Se agrega al modelo de preferencias. |
| D9 | Puntos de la funcionalidad de IA | La consigna no le asigna puntos. Confirmar que no se descuenta del alcance optativo. |

### Decisiones técnicas del equipo

| # | Tema | Propuesta |
|---|---|---|
| D10 | Almacenamiento de contraseñas | Hashing con Argon2id. La consigna dice "encriptada" pero cifrado reversible sería un defecto de seguridad. |
| D11 | Paginación | Keyset pagination por `(created_at, id)` en todos los listados. El offset se rompe con inserciones concurrentes. |
| D12 | Estrategia de feed | Fan-out on read sobre proyección de follows, con posibilidad de materializar timelines si la prueba de carga lo exige. Empezar por el camino simple. |
| D13 | Composición del feed | Definir si incluye posts propios. E.2 H5 CA.1 ya confirma que incluye retweets de los seguidos. |
| D14 | "Tiempo real" en likes y métricas | E.2 H6 CA.2 y E.5 H3 CA.1 dicen "tiempo real". Se interpreta como actualización optimista en el cliente más refresco, no WebSockets. Documentar. |
| D15 | Imágenes que exceden el límite | E.2 H7 CA.2 fija 1 MB por imagen. Definir si el cliente comprime antes de subir o si el backend rechaza. |
| D16 | Idioma del contenido | E.1 H7 CA.2 exige filtrar el feed por idioma, lo que implica detectar el idioma de cada post. Se resuelve con una librería de detección o como parte de la funcionalidad de IA. Es un requisito escondido y costoso. |
| D17 | Alertas de servicio caído | E.5 H11 CA.4 exige email a todos los admins si un servicio cae. Definir debounce para evitar tormenta de correos. |
| D18 | Zona horaria | Todo en UTC en backend, conversión a local en el cliente. |
| D19 | Retención de datos | E.1 H12 exige política de privacidad. Definir qué dice sobre borrado real y cuánto se conserva tras el soft-delete. |
| D20 | Presupuesto de AWS | Queda abierto quién paga: el control plane no escala a cero (73 USD/mes fijos), una config razonable ronda 166 USD/mes, y la palanca real es destruir y recrear el cluster entre sprints (~9 USD/mes apagado). Definir en S1: cuentas con plan pago, una por integrante, y confirmar con el docente si AWS Academy Learner Lab sirve. |
| D21 | Plan B si EKS se complica | Definir el 20 de septiembre, no después: ECS con Fargate cumple el requisito de contenedores y despliegue productivo sin exigir Kubernetes, a costa de perder el alineamiento con las clases de Cloud Computing. Además es cuatro veces más barato: entre 34 y 44 USD/mes contra 147 de EKS. **App Runner ya no es opción**, está cerrado a clientes nuevos. |
| D22 | Sincronización de contratos copiados | El tutor indicó copiar los esquemas en vez de empaquetarlos. Definir el script de sincronización y el test de contrato que detecta divergencia. |
| D23 | Autenticación: JWT con denylist vs. token opaco | Ambas hacen round-trip a Redis en cada request, así que el argumento clásico a favor de JWT se cae. Decide el equipo. |
| D24 | Subida de media: stream vs. presigned URL | Stream cumple E1-H8 CA.7 y CA.3 al pie de la letra; presigned URL con validación posterior es mejor práctica pero incumple esos criterios como están redactados. Ver `T-31`. |
| D25 | Acceso del tutor a Grafana Cloud con 3 asientos | El free tier son 3 usuarios y el equipo más el tutor son 5. Opciones: dashboards públicos, asientos rotativos, o Honeycomb como complemento. |
| D26 | UUIDv7 como PK de posts | PostgreSQL 18 lo trae nativo (`uuidv7()`). Decidir antes de la primera migración, después sale más caro. |

### Decisiones ya cerradas por el tutor (2026-08-19)

Se registran como ADR en `udesa-x-platform/docs/adr/` a medida que se toman, numeradas en ese orden, y no se reabren:

| # | Decisión | Resolución |
|---|---|---|
| ADR-001 | Estructura de repositorios | **Un repositorio por servicio.** Respondido por el tutor el 19-08: cada uno con sus tests y coverage, su pipeline de CI, sus scripts, su Docker y compose de desarrollo, y sus manifiestos. |
| ADR-002 | Contratos de eventos | **Copiados entre repositorios**, no publicados como librería. Recomendación del tutor el 19-08, para no pelear con empaquetado y versionado. |
| ADR-003 | Visibilidad de los repositorios | **Públicos.** Es lo que habilita ramas protegidas, secrets de organización y Actions sin cuota en el plan gratuito. |
| ADR-004 | Alta de issues en el Project | **Un workflow por repositorio** con `actions/add-to-project`. El incorporado de GitHub acepta un solo repo. |

La plataforma de despliegue y el proveedor de nube **no tienen ADR todavía**. Se deciden con la clase de Cloud Computing cursada, dentro de la ventana de `D21`: registrarlas hoy sería dar por cerrado algo que el equipo no puede justificar.

## Proceso ágil

La consigna exige "adopción de metodologías ágiles". Se evalúa el proceso, no solo el producto, así que hay que dejar evidencia.

### Marco

Scrum adaptado con **sprints de una semana**, alineados uno a uno con las clases de los lunes. No hay Product Owner externo: el rol lo cumple el tutor en la reunión semanal.

El sprint semanal no es una preferencia estética, es la consecuencia de cómo funciona la cursada. La reunión de los lunes revisa lo trabajado la semana anterior y define lo de la siguiente. Un sprint de dos semanas haría que uno de cada dos lunes no tuviera nada que demostrar, que es exactamente la señal que un tutor lee como grupo que no avanza.

### Ceremonias

| Ceremonia | Cuándo | Duración | Evidencia |
|---|---|---|---|
| Review con el tutor | Lunes, en clase | 30 min | Demo de lo cerrado la semana anterior, sobre el entorno desplegado |
| Retrospectiva corta | Lunes, después de la review | 15 min | Tres líneas en `docs/retros/SXX.md`: qué salió bien, qué no, qué acción concreta y con qué dueño |
| Planning | Lunes, después de la retro | 45 min | Issues movidas a `Ready` con estimación, dueño y sprint. Verificación del techo y el piso de carga en la vista `Por integrante` |
| Daily asincrónico | Diario, escrito | - | Mensaje en el canal: hecho, próximo, bloqueos |
| Refinamiento | Jueves | 30 min | Las historias del sprint siguiente cumplen la Definition of Ready antes del lunes |

La retro semanal de 15 minutos parece poco, y lo es a propósito: una retro larga cada dos semanas se cancela cuando hay presión, una corta todas las semanas sobrevive. Las actas en el repositorio no son burocracia, son la evidencia de que el proceso existió, y el tutor las va a pedir.

El refinamiento del jueves existe para que el planning del lunes no se vaya en discutir qué significa una historia. Si una historia llega al lunes sin cumplir la Definition of Ready, no entra al sprint.

### Cierre de sprint

Un sprint cierra el domingo. El lunes por la mañana, antes de la clase, el facilitador registra en el issue del sprint:

- Puntos planificados y puntos aceptados.
- Puntos por integrante.
- Historias que se corren al sprint siguiente, con el motivo.
- Estado del pipeline y de la cobertura.

Sin ese registro, la regla de recorte de la sección de capacidad no se puede aplicar, porque nadie sabe cuántos sprints consecutivos se viene incumpliendo.

### Roles rotativos

Los cuatro roles de la sección "Participación pareja" rotan una posición cada lunes. En cuatro semanas todos pasaron por los cuatro. La rotación es fija y se publica al inicio del semestre, para que nadie tenga que negociarla cada semana.

El **Escriba** de la semana suma una responsabilidad: mantener `AGENTS.md` y las skills al día. Si una regla aparece en una revisión, se escribe ese mismo día. Sin dueño explícito, esos archivos envejecen en tres semanas y dejan de servir.

### Cómo se trabaja con el agente

La consigna exige que cada estudiante sea capaz de explicar el funcionamiento y justificar las decisiones de diseño de lo que entregó. Un agente que programa más rápido de lo que el equipo entiende hace perder esa condición sin que se note hasta la defensa, cuando ya no hay margen para corregirlo.

Esto no es una recomendación: es parte del proceso desde S1, con issues propias y con lugar en la Definition of Done.

**`AGENTS.md` en cada repositorio.** Corto, tipo índice: mapa del repo, reglas del equipo y qué checks correr. El bloque común se sincroniza desde `udesa-x-platform`; el bloque propio lo escribe quien crea el repo. Ahí viven las guidelines del tutor, así que el agente las tiene siempre en contexto y no hay que recordárselas.

**Tres pasos, siempre en este orden.** Planear: se parte de la historia y su issue, el agente arma un plan y una persona lo corrige antes de que se escriba código. Ejecutar y verificar: se corre el plan y se corren los checks del repo. Mergear: PR con la explicación, revisión de otra persona, merge.

**Skills versionadas en el repositorio, no en la máquina de cada uno.** Viven en `.agents/skills/` y se sincronizan a los seis repos. Así los cuatro usan el mismo procedimiento y la mejora que hace uno la heredan los otros tres.

| Skill | Cuándo se usa |
|---|---|
| `explicar-implementacion` | Antes de cada merge. Produce qué cambió, por qué, ventajas y desventajas, y mejoras posibles, explicado como a alguien que recién aprende. También sirve para preparar la defensa de una historia. |
| `revisar-pr` | Al revisar un PR. Chequea criterios de aceptación cubiertos, tests con su identificador, cobertura, seguridad y reglas del repo. Produce el informe; **no aprueba**: la aprobación la da una persona. |

**Regla del equipo: nadie sube algo que no puede explicar.** El PR sin la sección de explicación no se revisa. No es una formalidad de proceso: es el único mecanismo que detecta a tiempo que alguien está mergeando código que no entiende.

**El agente no commitea, no pushea y no abre ni mergea PRs.** Puede escribir el código, correr los checks y redactar el mensaje de commit y el cuerpo del PR; ejecutar esas cuatro acciones es siempre de una persona, desde su cuenta. Es lo que hace que la autoría del historial signifique algo: el tutor puede pedir el `git log` de cualquier semana y lo que figura ahí es lo que cada uno se comprometió a defender. La regla completa, con lo que sí puede hacer, está en [`CONVENCIONES.md`](./CONVENCIONES.md).

**Nivel del código: junior que está aprendiendo.** La regla concreta, escrita en `AGENTS.md`, es que no se introducen dependencias, patrones ni abstracciones que no estén ya en el repositorio. Si hace falta, se abre un ADR y lo decide una persona. Es lo que impide que el código corra más rápido que el entendimiento del equipo, que es el modo silencioso de fallar la defensa.

### Política de ramas y revisión

Las reglas completas están en [`CONVENCIONES.md`](./CONVENCIONES.md). Lo esencial:

- Rama base `main`, protegida: sin push directo, CI verde obligatorio, al menos una aprobación.
- Funcionalidad: `feature-<nombre>`. Fix sin funcionalidad: `fix-<nombre>`. Es la convención del tutor.
- Toda rama tiene su issue asociada, en el mismo repositorio.
- Un PR por historia, o por criterio de aceptación si la historia es grande.
- Descripción del PR en español, con la plantilla del repo. La sección "Explicación de la implementación" es obligatoria: **sin ella el PR no se revisa.**
- Commits en formato Conventional Commits.
- Ningún integrante aprueba su propio PR. El revisor primario de la semana es el primer revisor de todo.
- **Ningún PR queda abierto de un lunes al siguiente.** Si no se puede cerrar, se parte.

## Gestión en GitHub

Las reglas de labels, ramas, milestones y PRs están en [`CONVENCIONES.md`](./CONVENCIONES.md). La configuración del tablero, con sus campos y vistas, en [`CATALOGO-ISSUES.md`](./CATALOGO-ISSUES.md). Acá va solo lo que este plan necesita del tablero.

**Las issues viven en el repositorio donde vive su código.** Lo pidió el tutor: toda rama lleva su issue asociada, y el milestone semanal se cierra con el tag del repo que efectivamente se tocó. En `udesa-x-platform` quedan solo las transversales: infraestructura, documentación y decisiones.

**Dos vistas sostienen las reglas de este plan.** Si dejan de reflejar la realidad, las reglas quedan sin forma de verificarse:

- `Por Integrante` verifica el techo del 40% y el piso del 15% de cada sprint. Se mira cada lunes en el planning.
- `Alcance Optativo` verifica los 15 puntos optativos por persona que exige la consigna. Se mira en los tres hitos de control: 28 de septiembre, 26 de octubre y 16 de noviembre.

**Sin columna de bloqueados.** Una issue bloqueada pierde su estado real si se la mueve a una columna aparte. Se usa la label `blocked` con un comentario que enlaza al bloqueante.

### Límite de trabajo en curso

Una issue activa por integrante en `In Progress`. Antes de tomar una nueva, hay que empujar las que están en `In Review`. Revisar el PR de otro tiene prioridad sobre empezar código propio.

Con sprints de una semana el límite es más duro de lo que parece: si el lunes alguien toma dos historias, el domingo tiene dos a medias y el lunes siguiente no hay nada que demostrar.

## Plantilla de issue de historia

```markdown
# [E1-H1] Registro de Usuarios

## Historia

COMO usuario nuevo
QUIERO registrarme con mis datos personales y validar mi cuenta mediante un token de correo
PARA asegurar la autenticidad de mi perfil y acceder de forma segura al sistema

## Criterios de aceptación

- [ ] CA.1 Un usuario no debe poder entrar al sistema si su cuenta no fue validada por el token enviado al email.
      Test: `auth-service/test/registro.spec.ts::E1-H1.CA1`
- [ ] CA.2 ...
      Test: ...

## Metadata

- Épica: E.1 Usuarios
- Tipo: Obligatoria
- Puntos: 3
- Sprint: S2
- Área: Mobile + Backend
- Responsable primario:
- Revisor:

## Dependencias

- Bloquea:
- Bloqueado por:

## Fuera de alcance

Qué NO incluye esta historia, para evitar discusiones en la revisión.

## Evidencia

- Pull Request:
- Tests que cubren cada CA:
- Verificado en staging:
- Captura o video:
```

## Trazabilidad de criterios de aceptación

Cada criterio de aceptación debe estar cubierto por al menos un test automatizado cuyo nombre referencie su identificador, con el formato `E1-H1.CA3`.

Esto tiene dos consecuencias prácticas. Primero, la defensa ante el tutor se vuelve mecánica: se ejecuta la suite filtrando por identificador y se muestra el criterio verificado. Segundo, obliga a que cada criterio sea verificable; si no se puede escribir el test, el criterio está mal entendido y hay que consultarlo antes de programar.

Los 56 conjuntos de criterios suman aproximadamente 220 criterios individuales. Ese es el verdadero tamaño del sistema de tests, y es la razón por la que el gate de cobertura tiene que estar activo desde la semana 1.

## Definition of Ready

Una issue solo puede pasar a `Ready` cuando:

- Los criterios de aceptación están escritos y son verificables.
- Las dependencias están identificadas y resueltas o planificadas.
- El diseño de UI existe, aunque sea un boceto, si la historia toca pantallas.
- El contrato de API está definido si la historia cruza servicios.
- Está estimada en puntos.
- Tiene responsable primario y revisor asignados.
- No hay decisiones abiertas que la bloqueen.

## Definition of Done

Una issue solo puede pasar a `Done` cuando:

- Todos los criterios de aceptación están verificados, cada uno con su test referenciado.
- Hay tests unitarios y la cobertura del servicio se mantiene por encima del 85%.
- Hay tests de integración si la historia cruza componentes o toca persistencia.
- El PR incluye la sección "Explicación de la implementación" completa, y el dueño de la historia puede defender cada decisión sin ayuda.
- Otro integrante revisó y aprobó el código. La skill `revisar-pr` produce el informe; la aprobación la da la persona.
- El pipeline de CI está verde.
- La funcionalidad fue validada en staging, no solo en local.
- Se revisaron los aspectos de seguridad aplicables del checklist OWASP.
- La documentación se actualizó en el mismo PR.
- La evidencia está vinculada en la issue.
- No quedan defectos críticos abiertos asociados.

## Objetivos de nivel de servicio

Sin números concretos, "prueba de estrés ejecutada" no demuestra nada. Estos son los objetivos contra los que se corre la prueba de carga, medidos en staging con volumen sembrado.

### Volumen de datos sembrado

| Entidad | Cantidad |
|---|---:|
| Usuarios | 10.000 |
| Relaciones de seguimiento | 500.000 |
| Posts | 200.000 |
| Interacciones (likes, retweets, respuestas) | 1.000.000 |
| Notificaciones | 300.000 |

### Objetivos de latencia y error

| Flujo | Concurrencia | p95 | Tasa de error |
|---|---:|---:|---:|
| Login | 100 usuarios | < 400 ms | < 0,5% |
| Carga del feed (primera página) | 200 usuarios | < 500 ms | < 1% |
| Feed, páginas siguientes | 200 usuarios | < 300 ms | < 1% |
| Crear post sin imagen | 100 usuarios | < 400 ms | < 1% |
| Búsqueda de posts | 100 usuarios | < 800 ms | < 1% |
| Perfil de usuario | 200 usuarios | < 400 ms | < 1% |

La prueba de carga se corre dos veces: una línea base en S6, con el sistema recién desplegado en AWS, y la final en S12, que es el avance que la cátedra espera el 16 de noviembre. Comparar ambas es lo que demuestra que se hizo ingeniería y no solo una medición al azar.

## Carga por bloque

El detalle historia por historia, con tipo, puntos, sprint y bloque, está en [`CATALOGO-ISSUES.md`](./CATALOGO-ISSUES.md). Acá va el agregado, que es lo que se usa para verificar el equilibrio.

### Carga total por bloque

| Bloque | Obligatorias | Optativas | Total |
|---|---:|---:|---:|
| Bloque 1 | 23 | 19 | 42 |
| Bloque 2 | 17 | 18 | 35 |
| Bloque 3 | 20 | 18 | 38 |
| Bloque 4 | 22 | 18 | 40 |
| **Total** | **82** | **73** | **155** |

El Bloque 2 tiene 5 a 7 puntos menos que el resto, y es deliberado: lleva la navegación y la sesión de la app mobile en S2, que no dan puntos y son el andamiaje sobre el que trabajan los otros tres, y lidera el seed y la prueba de carga final en S12. Si en la práctica esa carga resulta menor de lo previsto, la historia que se le reasigna primero es E.2 H10, Búsqueda, del Bloque 4.

## Issues técnicos transversales

Las 68 issues técnicas `T-00` a `T-67` están catalogadas en [`CATALOGO-ISSUES.md`](./CATALOGO-ISSUES.md), con su título y el sprint en que caen. No otorgan puntos de historia, pero son condición de aprobación: cubren los requisitos no funcionales de la consigna.

En qué sprint entra cada una figura en las tablas de la sección "Sprints" de este documento, que es donde se comprometen.

## Dependencias principales

```text
S1  Tablero y skeleton backend
 -> S2  Backoffice dockerizado y registro
   -> S3  Testing, CI y administradores
     -> S4  Grafo social y E2E backoffice
       -> S5  Posts, feed y E2E mobile
         -> S6  Despliegue productivo          [entrega intermedia, 28 sept]
           -> S7  Interacciones y media
             -> S8  Búsqueda, notificaciones e IA
               -> S9  Cierre de obligatorias   [26 oct]
                 -> S10 Observabilidad e IA
                   -> S11 Escalabilidad y optativas
                     -> S12 Carga y documentación
                       -> S13 Endurecimiento    [entrega final, 30 nov]
                         -> S14 Correcciones
                           -> S15 Recuperatorio
```

Dependencias funcionales que condicionan el orden:

- La autenticación es dependencia de todas las historias de usuario, por eso va en S2 y S3.
- **El grafo de seguidores es dependencia del feed, del perfil, de las notificaciones, de las listas y de las invitaciones.** Por eso E.3 H1 va en S4 y no después del feed.
- Las preferencias de privacidad son dependencia del feed, del perfil y del seguimiento.
- El modelo de post es dependencia de respuestas, retweets, likes, búsqueda, hashtags y citas. Es también la razón por la que las optativas del Bloque 1 no pueden empezar antes de S8.
- El almacenamiento de media se implementa para la foto de perfil en S6 y se reutiliza para las imágenes de posts en S7.
- Las denuncias son dependencia del backoffice, de la auditoría y de la funcionalidad de IA.
- La cola asíncrona es dependencia de los emails, las notificaciones y el triage de IA. Se levanta en S4, en cuanto existe `notifications-api` y hay dos microservicios que comunicar, que es lo que la consigna pide. En S2 el email de verificación va sincrónico detrás de una interfaz.
- Silenciar usuario es dependencia de la notificación de mención, porque E.4 H4 CA.2 exige no notificar menciones de usuarios silenciados. Las dos van en S10, en ese orden.
- La observabilidad es dependencia del healthcheck, las métricas, el estado de microservicios y el release.
- CI debe ejecutarse en todos los Pull Requests desde S1, y con gate de cobertura desde S3.
- La aprobación del tutor es dependencia de la funcionalidad de IA y de las decisiones abiertas de alcance.

Dependencias de calendario, que son las que no se negocian:

- El cluster de EKS tiene que estar sirviendo tráfico el 27 de septiembre o la entrega intermedia se cae.
- Las 30 historias obligatorias tienen que estar aceptadas el 26 de octubre.
- El build mobile tiene que estar en manos del tutor antes del 30 de noviembre, y una distribución de Expo puede demorar días en aprobarse.

## Primer paso operativo

Esto es lo que hay que ejecutar entre el 19 y el 23 de agosto para llegar al lunes 24 con el atraso saldado. El orden importa: los puntos 1 a 4 son bloqueantes para el resto del equipo.

1. Crear `udesa-x-platform` y subir `CONSIGNA.md`, `PLANIFICACION.md`, `ARQUITECTURA.md` y `CONVENCIONES.md`.
2. Crear `udesa-x-notifications-api`. Los otros cinco repos ya existen.
3. Poner `AGENTS.md`, `.editorconfig`, las dos skills, `copilot-instructions.md` y la plantilla de PR en los seis repos, y dejar andando `sync-comunes.sh`.
4. Crear las labels `feature`, `tech debt`, `spike` y `bug` en los seis repos, más las complementarias del equipo.
5. Crear los milestones `S1` y `S2` en los repos que tienen trabajo esas semanas. Los siguientes se crean sprint a sprint: un milestone vacío y vencido resta más de lo que aporta.
6. Configurar el Project de la organización: los campos `Sprint` y `Story Points`, y las vistas `Sprint Actual`, `Por Integrante`, `Alcance Optativo`, `Sin Clasificar`, `Roadmap` y `My items`, tomando issues de los seis repos.
7. Cargar las issues de las historias de **S2** en el repositorio que le corresponde a cada una, con los criterios de aceptación textuales de la consigna, puntos, dueño y sprint. Las historias de S3 en adelante se cargan en el planning de su sprint.
8. Cargar las issues técnicas de **S1 y S2** en el repo que corresponda, y en `udesa-x-platform` las decisiones abiertas cuya fecha límite cae antes de S3, con la label `decision`, dueño y fecha. Las de S1 que ya están resueltas entran cerradas, con el commit que las resolvió en el cuerpo.
9. Verificar en la vista `Alcance Optativo` que cada integrante suma entre 18 y 19 puntos optativos.
10. Verificar en la vista `Por Integrante`, filtrando sprint por sprint, que nadie supera el 40% de los puntos de ninguna semana entre S3 y S12, y que quien quede por debajo del 15% tiene su issue técnica anotada.
11. Registrar los ADR en `udesa-x-platform/docs/adr/`.
12. Levantar `users-api` con `/healthcheck`, Dockerfile, compose de desarrollo y CI en verde.

**Inventario del semestre: 157 issues.** 56 de historias, más 101 transversales: 68 técnicas `T-00` a `T-67`, 7 de IA y 26 decisiones `D1` a `D26`, catalogadas en `CATALOGO-ISSUES.md`.

Es el alcance a cubrir, no una carga inicial. Cada issue se crea en el planning de su sprint, en el repositorio donde vive su código. Solo van en `udesa-x-platform` las que no pertenecen a ningún servicio: documentación, decisiones e infraestructura compartida.

Y tres preguntas al tutor que no pueden esperar al 24 de agosto, porque las respuestas cambian el plan:

- ¿Qué fecha de entrega intermedia y final le toca al grupo 3? Hasta que responda se trabaja contra el 28 de septiembre y el 30 de noviembre.
- ¿Hay créditos de AWS para la cursada, o el cluster lo paga el equipo? La respuesta define si se va a EKS o al plan B de ECS con Fargate.
- ¿Se acepta demostrar push solo en Android? Si la respuesta es no, hay que presupuestar la cuenta de Apple Developer antes de S8.

