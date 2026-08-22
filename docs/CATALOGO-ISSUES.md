# Catalogo de issues — UdeSA-X (Grupo 3, 2S2026)

Enumeracion completa de las issues a cargar en el tablero Kanban de la organizacion `tds-g3-2s2026`, derivada de `docs/CONSIGNA.md` y `docs/PLANIFICACION.md`.

**Total: 157 issues.**


## 1. Resumen

| Grupo | Cantidad | Puntos |
|---|---:|---:|
| Historias de usuario | 56 | 173 |
| Issues tecnicos (`T-XX`) | 68 | — |
| Issues de IA (`AI-XX`) | 7 | — |
| Decisiones abiertas (`DXX`) | 26 | — |
| **Total** | **157** | **173** |

### Desglose de historias

| Tipo | Historias | Puntos |
|---|---:|---:|
| Obligatorias | 30 | 82 |
| Optativas comprometidas | 23 | 73 |
| Optativas fuera de alcance | 3 | 18 |
| **Total** | **56** | **173** |

- Comprometido (obligatorias + optativas comprometidas): **155 puntos en 53 historias**.
- Minimo exigido por la consigna: 82 obligatorios + 60 optativos = **142 puntos**.
- Criterios de aceptacion individuales a testear: **216**.

## 2. Estado del tablero

El tablero de la organización ya está configurado. Las reglas de labels, ramas y milestones
son las de `CONVENCIONES.md`; acá queda registrado solo lo propio del Project.

**Campos propios**

| Campo | Tipo | Uso |
|---|---|---|
| `Sprint` | Iteration | Semanal desde el 2026-08-17. Habilita el roadmap y el filtro `sprint:@current` |
| `Story Points` | Number | Puntos de la consigna. Es lo que suman las vistas por integrante y de alcance optativo |

`Status` usa las opciones de la plantilla: `Backlog`, `Ready`, `In progress`, `In review`, `Done`.

**Vistas**

| Vista | Filtro | Para qué |
|---|---|---|
| `Sprint Actual` | `sprint:@current` | La review de los lunes |
| `Por Integrante` | `sprint:@current`, agrupada por asignado | Control de techo del 40% y piso del 15% |
| `Alcance Optativo` | `label:"scope:optional"` | Verificar los 15 puntos optativos por integrante |
| `Sin Clasificar` | `no:sprint` | Bandeja de entrada: lo que llegó y falta triagear |
| `Roadmap` | — | Línea de tiempo sobre el campo `Sprint` |
| `My items` | `assignee:@me` | Lo propio |

**Alta automática.** Cada repo tiene `.github/workflows/add-to-project.yml`, que suma al
tablero toda issue nueva con `actions/add-to-project` y el secret de organización
`ADD_TO_PROJECT_PAT`. El workflow incorporado de GitHub no sirve acá: acepta un solo
repositorio y son seis.

**Milestones.** Se crean sprint a sprint, solo en los repos con trabajo esa semana. Las fechas
de los quince sprints están en la tabla de sprints de `PLANIFICACION.md`.


## 3. Historias de usuario (56 issues)

Tipo: `O` obligatoria · `S` optativa comprometida · `B` optativa fuera de alcance.


### E.1 Usuarios — 14 historias, 36 puntos

| ID | Titulo | Tipo | Pts | Sprint | Bloque | CAs | Labels |
|---|---|:--:|---:|---|---|---:|---|
| `E1-H1` | Registro de Usuarios | O | 3 | S2 | B2 | 7 | `epic:e1-users` `feature` `scope:mandatory` |
| `E1-H2` | Inicio de Sesión | O | 3 | S2 | B4 | 5 | `epic:e1-users` `feature` `scope:mandatory` |
| `E1-H3` | Cierre de Sesión | O | 1 | S2 | B3 | 2 | `epic:e1-users` `feature` `scope:mandatory` |
| `E1-H4` | Eliminación de Cuenta | O | 3 | S8 | B2 | 5 | `epic:e1-users` `feature` `scope:mandatory` |
| `E1-H5` | Olvidé Mi Contraseña | O | 3 | S3 | B3 | 8 | `epic:e1-users` `feature` `scope:mandatory` |
| `E1-H6` | Editar mi perfil | O | 2 | S3 | B1 | 6 | `epic:e1-users` `feature` `scope:mandatory` |
| `E1-H7` | Preferencias | S | 2 | S4 | B2 | 5 | `epic:e1-users` `feature` `scope:optional` |
| `E1-H8` | Foto de Perfil | S | 3 | S6 | B2 | 7 | `epic:e1-users` `feature` `scope:optional` |
| `E1-H9` | Social Login | B | 5 | Backlog | — | 4 | `epic:e1-users` `feature` `scope:backlog` |
| `E1-H10` | Tema de la Aplicación | S | 1 | S4 | B2 | 2 | `epic:e1-users` `feature` `scope:optional` |
| `E1-H11` | Enviar Feedback o Reportar Error | S | 3 | S10 | B2 | 5 | `epic:e1-users` `feature` `scope:optional` |
| `E1-H12` | Aceptación de Términos y Política de Privacidad | O | 1 | S2 | B1 | 2 | `epic:e1-users` `feature` `scope:mandatory` |
| `E1-H13` | Cambiar Contraseña | S | 3 | S3 | B2 | 5 | `epic:e1-users` `feature` `scope:optional` |
| `E1-H14` | Onboarding Inicial | S | 3 | S7 | B2 | 3 | `epic:e1-users` `feature` `scope:optional` |

### E.2 Publicaciones — 15 historias, 49 puntos

| ID | Titulo | Tipo | Pts | Sprint | Bloque | CAs | Labels |
|---|---|:--:|---:|---|---|---:|---|
| `E2-H1` | Crear Post | O | 3 | S5 | B1 | 5 | `epic:e2-posts` `feature` `scope:mandatory` |
| `E2-H2` | Feed Principal | O | 3 | S5 | B2 | 5 | `epic:e2-posts` `feature` `scope:mandatory` |
| `E2-H3` | Eliminar Post | O | 2 | S5 | B4 | 4 | `epic:e2-posts` `feature` `scope:mandatory` |
| `E2-H4` | Responder a un Post | O | 2 | S7 | B2 | 4 | `epic:e2-posts` `feature` `scope:mandatory` |
| `E2-H5` | Retweet / Repost | O | 2 | S7 | B4 | 4 | `epic:e2-posts` `feature` `scope:mandatory` |
| `E2-H6` | Like a un Post | O | 2 | S7 | B3 | 3 | `epic:e2-posts` `feature` `scope:mandatory` |
| `E2-H7` | Post con Imagen | O | 5 | S7 | B1 | 5 | `epic:e2-posts` `feature` `scope:mandatory` |
| `E2-H8` | Hashtags | S | 3 | S8 | B1 | 5 | `epic:e2-posts` `feature` `scope:optional` |
| `E2-H9` | Menciones a Usuarios | S | 3 | S8 | B1 | 3 | `epic:e2-posts` `feature` `scope:optional` |
| `E2-H10` | Búsqueda de Posts y Usuarios | O | 5 | S8 | B4 | 5 | `epic:e2-posts` `feature` `scope:mandatory` |
| `E2-H11` | Trending Topics | S | 3 | S11 | B1 | 3 | `epic:e2-posts` `feature` `scope:optional` |
| `E2-H12` | Guardar Posts | S | 3 | S11 | B2 | 3 | `epic:e2-posts` `feature` `scope:optional` |
| `E2-H13` | Citar Post | S | 5 | S12 | B1 | 4 | `epic:e2-posts` `feature` `scope:optional` |
| `E2-H14` | Visualización de Perfil de Usuario | O | 3 | S5 | B3 | 4 | `epic:e2-posts` `feature` `scope:mandatory` |
| `E2-H15` | Post con Video | B | 5 | Backlog | — | 5 | `epic:e2-posts` `feature` `scope:backlog` |

### E.3 Interacciones Sociales — 10 historias, 35 puntos

| ID | Titulo | Tipo | Pts | Sprint | Bloque | CAs | Labels |
|---|---|:--:|---:|---|---|---:|---|
| `E3-H1` | Seguir a un Usuario | O | 5 | S4 | B3 | 5 | `epic:e3-social` `feature` `scope:mandatory` |
| `E3-H2` | Dejar de Seguir a un Usuario | O | 2 | S4 | B4 | 3 | `epic:e3-social` `feature` `scope:mandatory` |
| `E3-H3` | Listado de Seguidores y Seguidos | O | 3 | S4 | B1 | 3 | `epic:e3-social` `feature` `scope:mandatory` |
| `E3-H4` | Bloquear Usuario | O | 2 | S6 | B3 | 5 | `epic:e3-social` `feature` `scope:mandatory` |
| `E3-H5` | Denunciar Usuario | O | 2 | S6 | B1 | 4 | `epic:e3-social` `feature` `scope:mandatory` |
| `E3-H6` | Mensajes Directos | B | 8 | Backlog | — | 4 | `epic:e3-social` `feature` `scope:backlog` |
| `E3-H7` | Usuarios en Línea | S | 3 | S11 | B3 | 3 | `epic:e3-social` `feature` `scope:optional` |
| `E3-H8` | Listas Personalizadas | S | 3 | S12 | B3 | 4 | `epic:e3-social` `feature` `scope:optional` |
| `E3-H9` | Invitar Usuarios Externos | S | 2 | S7 | B3 | 3 | `epic:e3-social` `feature` `scope:optional` |
| `E3-H10` | Silenciar Usuario | S | 5 | S10 | B3 | 5 | `epic:e3-social` `feature` `scope:optional` |

### E.4 Notificaciones — 5 historias, 15 puntos

| ID | Titulo | Tipo | Pts | Sprint | Bloque | CAs | Labels |
|---|---|:--:|---:|---|---|---:|---|
| `E4-H1` | Recibir notificaciones de nuevo seguidor | O | 2 | S8 | B3 | 4 | `epic:e4-notif` `feature` `scope:mandatory` |
| `E4-H2` | Notificación de interacción | O | 2 | S8 | B3 | 2 | `epic:e4-notif` `feature` `scope:mandatory` |
| `E4-H3` | Centro de Notificaciones In-App | O | 3 | S8 | B2 | 5 | `epic:e4-notif` `feature` `scope:mandatory` |
| `E4-H4` | Notificación de mención | S | 5 | S10 | B1 | 3 | `epic:e4-notif` `feature` `scope:optional` |
| `E4-H5` | Configurar Preferencias de Notificación | S | 3 | S9 | B3 | 2 | `epic:e4-notif` `feature` `scope:optional` |

### E.5 Administradores / Backoffice Web — 12 historias, 38 puntos

| ID | Titulo | Tipo | Pts | Sprint | Bloque | CAs | Labels |
|---|---|:--:|---:|---|---|---:|---|
| `E5-H1` | Creación de Administradores | O | 5 | S3 | B4 | 4 | `epic:e5-backoffice` `feature` `scope:mandatory` |
| `E5-H2` | Inicio de Sesión como Administrador | O | 2 | S3 | B1 | 3 | `epic:e5-backoffice` `feature` `scope:mandatory` |
| `E5-H3` | Visualización de Métricas | S | 5 | S10 | B4 | 2 | `epic:e5-backoffice` `feature` `scope:optional` |
| `E5-H4` | Buscador y Detalles de Usuarios | O | 3 | S9 | B4 | 3 | `epic:e5-backoffice` `feature` `scope:mandatory` |
| `E5-H5` | Bloqueo de Usuarios por Admin | O | 2 | S9 | B1 | 2 | `epic:e5-backoffice` `feature` `scope:mandatory` |
| `E5-H6` | Logs de Auditoría | O | 3 | S9 | B2 | 3 | `epic:e5-backoffice` `feature` `scope:mandatory` |
| `E5-H7` | Gestión de Denuncias | O | 3 | S9 | B1 | 3 | `epic:e5-backoffice` `feature` `scope:mandatory` |
| `E5-H8` | Exportar Datos | S | 2 | S7 | B4 | 2 | `epic:e5-backoffice` `feature` `scope:optional` |
| `E5-H9` | Registro de Última Conexión | S | 2 | S6 | B3 | 2 | `epic:e5-backoffice` `feature` `scope:optional` |
| `E5-H10` | Borrado Forzado de Contenido | S | 3 | S12 | B4 | 2 | `epic:e5-backoffice` `feature` `scope:optional` |
| `E5-H11` | Estado de los Microservicios | S | 5 | S6 | B4 | 4 | `epic:e5-backoffice` `feature` `scope:optional` |
| `E5-H12` | Gestión de Feedback/Reportes | S | 3 | S11 | B4 | 3 | `epic:e5-backoffice` `feature` `scope:optional` |

## 4. Issues tecnicos transversales (68 issues)

No otorgan puntos de historia, pero son condicion de aprobacion: cubren los 17 requisitos
no funcionales de la consigna.


### Fundaciones y plataforma — 29 issues

| ID | Titulo | Sprint |
|---|---|---|
| `T-00` | Configurar el Project y cargar las issues del sprint en curso y el siguiente | S1 |
| `T-01` | Crear `udesa-x-platform`, registrar los ADR y validar la arquitectura | S1 |
| `T-02` | Definir límites, responsables y contratos de cada servicio | S1 |
| `T-03` | Poner la estructura estándar en `notifications-api` | S4 |
| `T-04` | Provisionar PostgreSQL y MongoDB gestionados, fuera del cluster | S2 |
| `T-05` | Plantilla de repositorio de servicio: Dockerfile, tests, scripts, k8s, reusable workflows desde `udesa-x-platform` | S1 |
| `T-06` | `docker-compose.dev.yml` en cada repo de servicio | S1 |
| `T-07` | `docker-compose.full.yml` en platform, con imágenes publicadas | S2 |
| `T-08` | Endpoint `/healthcheck` y probes de Kubernetes estandarizados | S1 |
| `T-09` | Provisionar el cluster de EKS | S5 |
| `T-10` | Gateway API con NGINX Gateway Fabric: TLS, routing y rate limiting por IP | S5 |
| `T-11` | Manifiestos base con Kustomize y overlays de staging y producción | S5 |
| `T-12` | SOPS con age y gestión de configuración por entorno | S5 |
| `T-14` | Workflow de CD: build, push, `kubectl apply`, rollback automático y OIDC hacia AWS | S5 |
| `T-15` | Registry de imágenes y política de etiquetado por SHA | S2 |
| `T-16` | Script de sincronización de contratos y test de divergencia | S4 |
| `T-17` | Ramas protegidas, convención de commits y plantilla de PR en los seis repos | S1 |
| `T-19` | Diseño base y sistema de componentes de mobile y backoffice | S3 |
| `T-20` | Walking skeleton desplegado y accesible en el cluster | S6 |
| `T-22` | Definir entornos: desarrollo, staging, producción | S2 |
| `T-23` | Presupuesto del cluster y alertas de gasto | S1 |
| `T-24` | Formato estandarizado de respuesta de error (RFC 7807) | S1 |
| `T-25` | Versionado de API y política de cambios | S1 |
| `T-61` | Cuentas de AWS con plan pago, budget con alertas, y confirmar con el docente si AWS Academy Learner Lab sirve | S1 |
| `T-63` | `AGENTS.md` base y por repositorio | S1 |
| `T-64` | Skills `explicar-implementacion` y `revisar-pr` | S1 |
| `T-65` | `.editorconfig`, linters y formatters en los seis repos | S1 |
| `T-66` | Instrucciones de Copilot y plantilla de PR en español | S1 |
| `T-67` | Script de sincronización de comunes y convención de tags | S1 |

### Backend, comunicacion y seguridad — 13 issues

| ID | Titulo | Sprint |
|---|---|---|
| `T-18` | Threat model y primera revisión OWASP Top 10 | S7 |
| `T-26` | Rate limiting por usuario reutilizable | S3 |
| `T-27` | Cola asíncrona con contratos de eventos versionados | S4 |
| `T-28` | Patrón outbox para publicación confiable de eventos | S4 |
| `T-29` | RBAC de SuperAdmin y Moderador | S3 |
| `T-30` | Paginación por cursor como estándar transversal | S4 |
| `T-31` | Servicio de media: streams, validación por magic numbers (decidir stream vs. presigned URL, ver D24) | S6 |
| `T-32` | Política de soft-delete y retención documentada | S7 |
| `T-33` | FCM: registro, actualización y depuración de device tokens | S8 |
| `T-34` | Deep linking en la app mobile | S8 |
| `T-35` | Detección de idioma del contenido para el filtro de feed | S11 |
| `T-60` | NetworkPolicies entre pods y segunda revisión OWASP | S13 |
| `T-62` | Pinnear GitHub Actions por SHA, SBOM con syft y attestations de build | S13 |

### Calidad y operacion — 18 issues

| ID | Titulo | Sprint |
|---|---|---|
| `T-13` | CI vía reusable workflow desde `udesa-x-platform`, con gate de cobertura del 85% | S1 |
| `T-21` | Observabilidad mínima: logs estructurados y dashboard | S6 |
| `T-36` | Cobertura mínima del 85% por servicio, verificada en CI | S3 |
| `T-37` | Tests de integración de todos los servicios backend | S3 |
| `T-38` | Suite E2E de los flujos críticos | S8 |
| `T-39` | Seed de datos y generador de volumen para pruebas de carga | S6 |
| `T-40` | Prueba de carga: línea base sobre el feed | S6 |
| `T-41` | Prueba de carga final contra los SLOs | S12 |
| `T-42` | Métricas, logs y trazas distribuidas | S10 |
| `T-43` | Acceso del tutor a la plataforma de observabilidad | S6 |
| `T-44` | Alertas y notificación de incidentes | S10 |
| `T-45` | Distribución del build mobile al tutor | S13 |
| `T-46` | Runbook de despliegue, rollback y recuperación | S13 |
| `T-47` | Backup y restore de las bases de datos | S13 |
| `T-48` | Revisión de UX, accesibilidad y consistencia visual | S13 |
| `T-49` | Documentación técnica y funcional | S11 |
| `T-50` | Diagramas C4 del sistema | S4 |
| `T-59` | HorizontalPodAutoscaler por servicio, más KEDA escalando `notifications-api` por profundidad de cola con `minReplicaCount: 0` | S11 |

### Producto minimo implicito — 8 issues

| ID | Titulo | Sprint |
|---|---|---|
| `T-51` | Navegación principal y estructura de tabs de la app | S2 |
| `T-52` | Splash, sesión persistente y refresco de token | S2 |
| `T-53` | Manejo de estados de carga, vacío y error en todas las pantallas | S5 |
| `T-54` | Pull to refresh en el feed | S5 |
| `T-55` | Pantalla de detalle de post e hilo de conversación | S7 |
| `T-56` | Pantalla de solicitudes de seguimiento pendientes | S4 |
| `T-57` | Manejo de estado sin conexión | S13 |
| `T-58` | Textos estáticos de Términos y Política de Privacidad | S2 |

## 5. Issues de Inteligencia Artificial (7 issues)

Cubren la condicion de aprobacion "al menos una funcionalidad que utilice IA".
Propuesta del plan: triage asistido de denuncias en el backoffice.

| ID | Titulo | Sprint |
|---|---|---|
| `AI-01` | Proponer y acordar la funcionalidad de IA con el tutor | S7 |
| `AI-02` | Definir datos enviados, privacidad, proveedor y modelo | S8 |
| `AI-03` | Spike técnico: prompt, salida estructurada, costo medido | S8 |
| `AI-04` | Implementar el triage asistido de denuncias | S10 |
| `AI-05` | Integrar la sugerencia en la bandeja del backoffice | S10 |
| `AI-06` | Tests de casos válidos, errores, timeout y baja confianza | S10 |
| `AI-07` | Documentar intervención humana, límites y sesgos | S13 |

## 6. Decisiones abiertas (26 issues)

Se cargan con `decision` en S1. Ninguna puede quedar abierta mas alla del sprint
en el que bloquea una historia.


### Ambiguedades del enunciado — consensuar con el tutor (`needs-tutor`)

| ID | Tema |
|---|---|
| `D1` | Umbral de reportes |
| `D2` | Políticas de lockout |
| `D3` | Eliminación de cuenta |
| `D4` | Integridad de follows al eliminar cuenta |
| `D5` | Roles de administrador |
| `D6` | Formato del handle |
| `D7` | Aprobación de solicitudes de seguimiento |
| `D8` | Preferencia de presencia |
| `D9` | Puntos de la funcionalidad de IA |

### Decisiones tecnicas del equipo

| ID | Tema |
|---|---|
| `D10` | Almacenamiento de contraseñas |
| `D11` | Paginación |
| `D12` | Estrategia de feed |
| `D13` | Composición del feed |
| `D14` | "Tiempo real" en likes y métricas |
| `D15` | Imágenes que exceden el límite |
| `D16` | Idioma del contenido |
| `D17` | Alertas de servicio caído |
| `D18` | Zona horaria |
| `D19` | Retención de datos |
| `D20` | Presupuesto de AWS |
| `D21` | Plan B si EKS se complica |
| `D22` | Sincronización de contratos copiados |
| `D23` | Autenticación: JWT con denylist vs. token opaco |
| `D24` | Subida de media: stream vs. presigned URL |
| `D25` | Acceso del tutor a Grafana Cloud con 3 asientos |
| `D26` | UUIDv7 como PK de posts |

## 7. Distribucion por sprint

| Sprint | Historias | Pts | Tecnicos | IA | Decisiones | Total issues |
|---|---:|---:|---:|---:|---:|---:|
| `S1` | 0 | 0 | 12 | 0 | 26 | 38 |
| `S2` | 4 | 8 | 7 | 0 | 0 | 11 |
| `S3` | 5 | 15 | 5 | 0 | 0 | 10 |
| `S4` | 5 | 13 | 7 | 0 | 0 | 12 |
| `S5` | 4 | 11 | 7 | 0 | 0 | 11 |
| `S6` | 5 | 14 | 6 | 0 | 0 | 11 |
| `S7` | 7 | 18 | 3 | 1 | 0 | 11 |
| `S8` | 7 | 21 | 3 | 2 | 0 | 12 |
| `S9` | 5 | 14 | 0 | 0 | 0 | 5 |
| `S10` | 4 | 18 | 2 | 3 | 0 | 9 |
| `S11` | 4 | 12 | 3 | 0 | 0 | 7 |
| `S12` | 3 | 11 | 1 | 0 | 0 | 4 |
| `S13` | 0 | 0 | 7 | 1 | 0 | 8 |
| `S14` | 0 | 0 | 0 | 0 | 0 | 0 |
| `S15` | 0 | 0 | 0 | 0 | 0 | 0 |
| `Backlog` | 3 | 18 | 0 | 0 | 0 | 3 |
| **Total** | **56** | **173** | **68** | **7** | **26** | **157** |

> S1 concentra 38 issues porque incluye las 26 decisiones abiertas y las 12 fundaciones
> de plataforma. Son issues de definicion y configuracion, no de desarrollo.


## 8. Como cargar

Cada issue tiene su cuerpo listo en `cuerpos/<ID>.md`, con titulo, labels y metadata en
comentarios HTML en las primeras lineas (no se renderizan al pegarlos en GitHub).

Orden sugerido, de mayor a menor desbloqueo:

1. Milestones `S1` a `S15` con sus due dates.
2. Labels y campos del Project.
3. Las 26 decisiones (`DXX`): son las que bloquean historias.
4. Los 12 tecnicos de S1: son los que desbloquean a los otros integrantes.
5. Las 56 historias, que es el alcance que el tutor va a revisar.
6. El resto de tecnicos y los de IA.

`issues.csv` tiene la misma informacion en formato tabular, separado por `;` y en UTF-8
con BOM, para abrirlo directo en Excel.
