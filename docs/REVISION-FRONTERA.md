# Revisión de frontera del stack

Contraste de cada pieza de `ARQUITECTURA.md` contra el estado real del ecosistema al 2026-08-19. Todo lo que sigue está verificado contra fuentes primarias en esa fecha, no contra memoria.

El criterio de la revisión no es "usar lo más nuevo". Es: dónde el documento apuesta a algo que hoy está muerto, deprecado o mal calibrado, y dónde hay una mejora que se paga sola porque no suma piezas para operar. Cada punto trae el costo de adoptarlo, porque el presupuesto real del proyecto son cuatro personas y quince semanas.

Cada ítem lleva una etiqueta:

- **Corregir**: el documento afirma algo que hoy es falso o apuesta a una pieza sin futuro. No es opcional.
- **Endurecer**: mejora concreta de robustez o seguridad con costo cercano a cero.
- **Opción**: hay dos caminos defendibles y la decisión es del equipo. Va con recomendación, no con imposición.
- **Sin cambio**: el documento ya eligió bien. Se registra para que nadie vuelva a discutirlo en S1.

## Resumen: qué cambiaría y qué no

La conclusión general es que el documento envejeció bien. La arquitectura (cuatro servicios, dos lenguajes, cola entre ellos, bases fuera del cluster, outbox) no tiene nada que corregir: es la misma decisión que tomaría hoy alguien que empieza de cero. Lo que envejeció son piezas puntuales del stack y una tabla de seguridad.

Hay seis correcciones que no son negociables porque el documento apuesta a algo que dejó de existir o nunca fue cierto:

1. **El NGINX Ingress Controller está archivado desde marzo de 2026** y no va a recibir un solo parche de seguridad más. Es la corrección más grave y la que más trabajo cuesta.
2. La tabla de OWASP mapea contra el Top 10 de 2021, y desde enero de 2026 rige el de 2025.
3. Detox está abandonado y no funciona con la arquitectura actual de React Native.
4. El free tier de Grafana Cloud son 3 usuarios, y el equipo más el tutor son 5.
5. Copiar las plantillas de CI entre siete repos es trabajo que GitHub Actions ya resuelve.
6. El CD no menciona OIDC, lo que implica claves de larga vida de AWS en siete repos.

Y hay dos números del presupuesto que están mal en el documento y afectan decisiones de calendario: **el free tier de 12 meses de AWS ya no existe** desde julio de 2025, y el costo real del cluster es bastante más alto que los 150 USD mensuales estimados.

## 1. Correcciones que no son negociables

### 1.1 El controller de ingress elegido está archivado - **Corregir**

Es el hallazgo más grave de toda la revisión. El documento elige NGINX Ingress Controller en tres lugares distintos (vista general, tabla de Kubernetes, rate limiting por IP). **El repositorio `kubernetes/ingress-nginx` está archivado desde el 24 de marzo de 2026.** Última release: `controller-v1.15.1`, del 19 de marzo de 2026.

Cita textual del README del repositorio archivado:

> "Best-effort maintenance will continue until March 2026. Afterward, there will be no further releases, no bugfixes, and no updates to resolve any security vulnerabilities that may be discovered."

Y más explícito todavía:

> "If you are not already using ingress-nginx, you should not be deploying it as it is not being developed. Instead you should identify a Gateway API implementation and use it."

Lo que hace peligrosa esta pieza es que **no se rompe**. Las imágenes y los charts siguen descargables, el cluster va a funcionar perfecto durante los quince sprints, y nunca más va a recibir un parche de seguridad. El ritmo de CVEs antes del cierre era de seis en cuatro meses, incluyendo CVE-2026-4342 (CVSS 8.8, ejecución remota de código con exposición de Secrets), y el antecedente grande fue IngressNightmare (CVE-2025-1974, CVSS 9.8). Desplegar hoy un controller que jamás se va a parchear es una decisión difícil de defender en un trabajo que dedica una sección entera a OWASP.

El motivo del retiro fue burnout de mantenedores, según el anuncio: "only one or two people doing development work, on their own time, after work hours and on weekends". El sucesor propuesto, InGate, **también está archivado** (`[EOL] InGate`, último push el 30 de junio de 2026). AWS ya lo advierte por su cuenta en las release notes de EKS 1.35, aclarando que ninguna alternativa es un reemplazo directo.

Aclaración para no exagerar el alcance: **la API `Ingress` de Kubernetes no está deprecada**, sigue siendo GA aunque congelada en features. Lo que murió es este controller en particular.

Anuncios: [retiro, 11/11/2025](https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/) y [declaración del Steering Committee, 29/01/2026](https://kubernetes.io/blog/2026/01/29/ingress-nginx-statement/).

**Qué poner en su lugar**: ver la sección 7.1. La respuesta corta es NGINX Gateway Fabric sobre Gateway API, que conserva el motor NGINX y la forma de trabajar, y cuesta reescribir los manifiestos de routing una vez.

### 1.2 La tabla de OWASP mapea contra el Top 10 de 2021 - **Corregir**

El OWASP Top 10:2025 se anunció en noviembre de 2025 y quedó final en enero de 2026. Es la versión vigente. Los cambios que rompen la tabla actual del documento:

| 2021 (lo que dice el doc) | 2025 (lo que rige) |
| --- | --- |
| A01 Control de acceso roto | A01 Broken Access Control, ahora **absorbe SSRF** |
| A02 Fallas criptográficas | Bajó a A04 |
| A03 Inyección | Bajó a A05 |
| A04 Diseño inseguro | Bajó a A06 |
| A05 Configuración incorrecta | **Subió a A02** |
| A06 Componentes vulnerables | Se expandió a **A03 Software Supply Chain Failures** |
| A10 SSRF | **Desapareció**, se fusionó en A01 |
| - | **A10 Mishandling of Exceptional Conditions**, categoría nueva |

La fila A10 del documento ("Ninguna URL provista por el usuario se consume desde el servidor") ya no corresponde a A10 y hay que moverla a A01. Falta cubrir la categoría A10 nueva, que es manejo de errores y condiciones excepcionales: fallar de forma segura, no filtrar stack traces al cliente, definir el comportamiento ante timeout de una dependencia. Buena parte de eso ya está en el documento disperso (timeouts, comportamiento ante fallo del destino, el fallback del triage de IA); solo hay que nombrarlo.

A03 conviene resaltarlo porque el proyecto ya tiene la mitad hecha: Dependabot, escaneo de imágenes, imágenes por SHA. Sumar SBOM y attestations de build lo cierra casi sin trabajo.

Referencia: [OWASP Top 10:2025](https://owasp.org/Top10/2025/). ASVS va por la 5.0 (mayo de 2025); alcanza con usar el nivel L1 como checklist antes de las entregas. Mobile Top 10 sigue siendo la edición 2024.

### 1.3 Detox está abandonado - **Corregir**

El documento dice "Detox o Maestro". Hoy es Maestro y no hay alternativa:

- Detox lleva más de dos meses sin un solo commit, y tiene un bug abierto que rompe la sincronización con la New Architecture de React Native, que desde el SDK 55 de Expo es el único modo que existe. Su propia guía de CI está marcada como desactualizada y la documentación de Expo ya ni lo menciona.
- Maestro (CLI 2.8.0) publica cada tres o cuatro semanas, con commits hasta el 18 de agosto de 2026. No exige instrumentar la app: testea el binario por accesibilidad con flujos declarativos en YAML, mientras Detox obliga a tocar Podfile y build.gradle.

Costo de adoptar: cero, es la decisión por defecto al escribir el primer test de E2E en S13.

### 1.4 Grafana Cloud free no alcanza para el equipo más el tutor - **Corregir**

El documento eligió Grafana Cloud citando textualmente que "su capa gratuita permite invitar usuarios, y la consigna exige que el tutor acceda a la plataforma". El free tier son **3 usuarios**. El equipo son cuatro personas más el tutor: cinco.

El resto del free tier es generoso y no es el problema: 14 días de retención, 10.000 series activas, 50 GB de logs, 50 GB de trazas, 50 GB de perfiles y 500 VUh de k6 por mes, que además cubre las pruebas de carga de S6 y S12 sin cuenta aparte.

Opciones, de menor a mayor costo:

1. **Dashboards públicos o snapshots para el tutor.** No consume asiento. Es la salida más barata y probablemente suficiente: el tutor necesita ver, no administrar.
2. **Tres asientos rotativos** entre las cuatro personas. Funciona pero es fricción semanal.
3. **Honeycomb como complemento** para trazas: 20 millones de eventos por mes, 60 días de retención y usuarios ilimitados. Suma una herramienta más, que es exactamente lo que se quiere evitar.

Recomendación: opción 1, y verificar en S2 que el tutor efectivamente puede entrar sin login. Si la cátedra exige que el tutor tenga cuenta propia con acceso completo, se cae a la opción 3.

Descartadas: Better Stack retiene 3 días, Axiom da 2 usuarios, New Relic da 1 usuario full, Datadog free no tiene logs ni APM. Autohospedar el stack LGTM en el cluster consume varios GB de RAM que compiten con las apps y suma upgrades y backups a mantener.

### 1.5 Copiar las plantillas de CI entre siete repos es innecesario - **Corregir**

El documento dice que los workflows viven en `udesa-x-platform/.github/workflow-templates/` y se copian "igual que los contratos". La analogía con los contratos no se sostiene: copiar los contratos fue una indicación explícita del tutor para no pelear con empaquetado. Nadie pidió copiar los workflows, y GitHub Actions ya resuelve esto de fábrica.

Con **reusable workflows**, el pipeline vive una sola vez en el repo de plataforma y cada repo de servicio queda con tres líneas:

```yaml
jobs:
  ci:
    uses: tds-g3-2s2026/udesa-x-platform/.github/workflows/ci-node.yml@main
    secrets: inherit
```

Funciona en el plan gratuito. Elimina la clase entera de bug "el CI de un repo quedó atrás y nadie se dio cuenta", que con siete repos y quince semanas es cuestión de tiempo.

Aclaración importante: los *required workflows* a nivel organización (forzar un workflow sin archivo en el repo) sí exigen GitHub Enterprise Cloud. No hacen falta: alcanza con branch protection por repo, disponible en el plan gratuito, exigiendo que el check pase antes de mergear.

Si los siete repos son públicos, Actions es gratis e ilimitado y desaparece cualquier presión de cuota. En repos privados son 2.000 minutos por mes para toda la organización, que con siete repos y CI en cada PR se consume rápido.

### 1.6 El CD no menciona OIDC hacia AWS - **Corregir**

El pipeline hace `kubectl apply` contra EKS, lo que implica credenciales de AWS. Tal como está escrito, eso significa una access key de larga vida guardada en los secrets de GitHub, en siete repos.

OIDC elimina la credencial permanente: se configura el proveedor y un rol de IAM una vez en la cuenta de AWS, y cada workflow pide un token efímero con `permissions: id-token: write`. Es media hora de trabajo, una sola vez, y cierra el riesgo más obvio de la cadena de despliegue.

Dato posterior a mayo de 2026: desde el 23 de abril de 2026 los repos nuevos usan *immutable subject claims* (ID numérico de owner y repo en el claim `sub`), así que renombrar un repo ya no rompe la trust policy.

## 2. Backend TypeScript: users, notifications, media

Veredicto general: **el stack elegido es correcto y no hay que cambiarlo.** NestJS sobre TypeScript sigue siendo la opción de madurez, y ninguna alternativa justifica el costo de migrar para un equipo de cuatro. Los ajustes son incrementales.

| Pieza | Estado hoy | Acción |
| --- | --- | --- |
| Runtime | Node 24 es Active LTS hasta abril de 2028. Node 22 pasó a maintenance | **Fijar Node 24** en Dockerfiles y CI |
| Framework | NestJS v11, activo. v12 en roadmap para Q3 2026 con ESM y Standard Schema | Sin cambio |
| Adaptador HTTP | Fastify contra Express | **Opción**: Fastify en los servicios nuevos |
| ORM | Prisma 7 eliminó el motor Rust, cliente TypeScript puro | **Fijar Prisma 7** |
| Tests | NestJS v11 ya trae Vitest en lugar de Jest | **Vitest**, no Jest |
| Compilador | TypeScript 7, reescrito en Go, 8-12x más rápido | Adoptar cuando esté GA |
| Validación | Zod v4 conforme a Standard Schema | **Opción**, ver abajo |

**Prisma 7 - Endurecer.** El cambio es relevante para este proyecto en particular: el cliente pasó de 14 MB con binario nativo de Rust a 1.6 MB de TypeScript puro, con hasta 3.4x más velocidad en queries grandes. Desaparece la clase de problema "el binario de Prisma no corre en esta imagen base", que es justo la que aparece al armar Dockerfiles multi-stage con imágenes slim o distroless. Prisma Migrate sigue siendo la mejor herramienta de migraciones del ecosistema Node, que es lo que importa con cuatro personas tocando el mismo esquema.

Drizzle es la alternativa legítima: más rápido en overhead crudo y ya superó a Prisma en adopción de proyectos nuevos. El motivo para no elegirlo acá es que drizzle-kit es notablemente menos maduro que Prisma Migrate en detección de drift y rollback.

**Fastify como adaptador - Opción.** Da alrededor de 50% más de throughput HTTP puro que Express, aunque con una base de datos de por medio la diferencia se diluye en I/O. El caveat real es compatibilidad de middleware. Recomendación: arrancar `notifications-api` y `media-api` directamente con Fastify, que son repos nuevos, y dejar `users-api` como esté si ya tiene código sobre Express.

**Validación - Opción.** El documento no fija herramienta. Lo natural en NestJS es class-validator con el ValidationPipe, y sigue siendo la integración más directa. Zod v4 ya cerró la brecha de performance que lo descartaba y es el camino al que va NestJS v12 con Standard Schema. Recomendación pragmática: class-validator en los DTOs de entrada HTTP, y Zod para configuración de entorno y validación de eventos, que es donde class-validator no encaja.

Para los esquemas de eventos que viajan por RabbitMQ, JSON Schema Draft 2020-12 con Ajv sigue siendo el estándar, y es lo que hace posible el test de contrato que el documento ya planteó.

**Cliente de RabbitMQ.** `amqplib` es el estándar histórico y la opción de máxima madurez, pero obliga a escribir a mano la reconexión y la resuscripción. `rabbitmq-client` (v5, cero dependencias, TypeScript nativo) da eso de fábrica. Con quince sprints, la segunda ahorra tiempo real; con criterio de madurez estricta, la primera. Cualquiera de las dos es defendible.

**Imágenes Docker.** Multi-stage con `node:24-slim` en runtime. Distroless baja la superficie de ataque pero deja el contenedor sin shell, y depurar un pod colgado en EKS sin shell es doloroso para quien recién aprende Kubernetes. Recomendación: arrancar con slim y evaluar distroless recién en los sprints finales, cuando el pipeline ya sea aburrido.

**Descartados y por qué**: Bun y Deno (adopción minoritaria, sin ventaja real en pods de larga vida), Hono (no da DI ni estructura, y con cuatro personas rotando la estructura opinionada de Nest vale más que los req/s), Encore.ts (autoprovisiona infraestructura, que choca de frente con "ya estamos en EKS").

## 3. Backend Python: posts

Veredicto: **FastAPI sigue siendo la elección correcta.** No hay razón para migrar. Las correcciones son de tooling y de configuración de runtime.

| Pieza | Recomendación | Nota |
| --- | --- | --- |
| Python | 3.13 estándar | **No** usar 3.14 free-threaded |
| Framework | FastAPI | Sin cambio |
| Servidor | Uvicorn, 1 worker por pod | Escalar con réplicas, no con `--workers` |
| Dependencias | uv | Estándar de facto, lockfile commiteable |
| Lint y formato | Ruff | Reemplaza black, flake8, isort y pylint |
| Tipos | mypy en CI, ty en el editor | ty pasó a beta en agosto de 2026 |
| ORM | SQLAlchemy 2.x async con asyncpg | **No** SQLModel |
| Migraciones | Alembic | Sin cambio |

**Free-threading: no - Corregir preventivamente.** Python 3.14 pasó free-threading de experimental a soportado y bajó el overhead single-thread de 40% a 5-10%, así que es tentador. No conviene: pydantic-core tuvo segfaults en builds free-threaded hasta PyO3 0.23, la disponibilidad de wheels `cp314t` para el ecosistema (asyncpg, uvloop) todavía se rastrea activamente, y un servicio web es I/O-bound, así que asyncio ya resuelve el problema que free-threading vendría a resolver. No hay nada que ganar y hay un runtime que depurar.

**Un worker por pod - Endurecer.** Es la corrección de configuración más importante de esta sección, y el documento no la menciona. En Kubernetes corresponde un proceso por contenedor: así el HPA, los probes y el scheduler controlan la unidad real de escala. Con `--workers N` adentro del pod, un worker colgado no lo ve nadie: el pod sigue respondiendo el probe y Kubernetes cree que está sano. Configuración concreta: `uvicorn --workers 1 --loop uvloop --http httptools`, `terminationGracePeriodSeconds` mayor al request más largo, y un hook `preStop` con un sleep corto para drenar conexiones antes del SIGTERM.

**SQLAlchemy 2.x async, no SQLModel.** SQLModel es una capa fina sobre SQLAlchemy que ahorra boilerplate en CRUDs simples, pero para contadores atómicos, outbox transaccional y queries de grafo se termina bajando al Core igual, con una indirección de más.

**Pooling: sin proxy.** El pool nativo vía `create_async_engine` (pool_size 20, max_overflow 10, pool_pre_ping, pool_recycle 1800) alcanza sobrado. RDS Proxy y PgBouncer suman un componente más a monitorear sin resolver un problema que este proyecto todavía no tiene. Agregarlo solo si se ve agotamiento de conexiones medido.

**Búsqueda: `pg_trgm` y `tsvector` alcanzan - Sin cambio.** La guía práctica por volumen es clara: por debajo de 500.000 filas Postgres nativo alcanza sin extensión adicional, y entre 500.000 y 2 millones alcanza sumando `pg_trgm` con caché, que es exactamente lo que el documento ya planteó. Elasticsearch se justifica arriba de 2 millones de filas o cuando la búsqueda es el producto. Vale registrar `pg_search` de ParadeDB (ranking BM25 embebido en Postgres) como la opción a mirar si el ranking de `tsvector` se queda corto, porque mejora el motor sin sumar un servicio.

**Nota sobre Postgres 18 y búsqueda**: el FTS ahora respeta el collation provider del cluster en vez de forzar libc. Hay que reindexar los índices de texto después de un upgrade mayor, cosa de no descubrirlo en la demo.

## 4. Clientes: mobile y backoffice

### Mobile

| Pieza | Estado | Acción |
| --- | --- | --- |
| Expo SDK | 57, con React Native 0.86 y React 19.2 | Fijar y no perseguir cada SDK |
| New Architecture | Ya no es opcional: el opt-out se removió en RN 0.82 y el código legacy se borró en SDK 55 | Sin decisión que tomar |
| Expo Router | Versionado alineado al SDK (`57.x`), desacoplado de React Navigation | Sin cambio |
| Estado de servidor | TanStack Query v5 (5.101.x), sin v6 a la vista | Sin cambio |
| Estado global | Zustand 5 | Sin cambio |
| Tokens | expo-secure-store | Sin cambio |
| E2E | Maestro | **Corregir**: no Detox |
| Tests unitarios | React Native Testing Library **14** | **Corregir**: arrancar en 14, no en 13 |

**RNTL 14 - Corregir.** La versión 14 (junio de 2026) es un major con ruptura fuerte: todas las APIs core pasaron a ser asíncronas (`render`, `renderHook`, `fireEvent` devuelven Promise). Arrancar en 14 desde el primer test cuesta lo mismo que arrancar en 13; migrar a mitad del cuatrimestre obliga a reescribir cada test. Como el gate de cobertura arranca en S3, esta decisión hay que tomarla antes de escribir el primer test, no después.

**Persistencia offline - Opción.** Si se quiere caché offline en mobile, el patrón es `persistQueryClient` sobre MMKV, no sobre AsyncStorage. Con la salvedad de que MMKV va para caché y preferencias, nunca para tokens: no está respaldado por hardware. Los tokens siguen en expo-secure-store.

**Distribución.** EAS Build free da 15 builds de Android y 15 de iOS por mes, con cola de baja prioridad. Para iOS igual hace falta la cuenta de Apple Developer paga y registrar el UDID del tutor. Para las demos semanales conviene priorizar Android, que instala el APK directo. Esto confirma lo que el documento ya anticipaba en A15.

### Backoffice web

| Pieza | Estado | Acción |
| --- | --- | --- |
| Vite | 8, con Rolldown ya por defecto | Arrancar en 8 |
| React | 19.2 | Sin cambio |
| React Compiler | Estable 1.0 desde octubre de 2025 | **Endurecer**: activarlo desde S1 |
| Router | TanStack Router | **Opción** sobre React Router |
| UI | Mantine | **Opción** sobre shadcn |
| Tablas | TanStack Table | Sin cambio |
| Gráficos | Recharts | Sin cambio |
| Tests | Vitest 4.1.x | No saltar a Vitest 5, está en RC |

**React Compiler - Endurecer.** Estable desde hace diez meses sin patches, en producción en Meta. Para un equipo que está aprendiendo React, elimina toda una clase de bug: `useMemo` y `useCallback` mal puestos. Activarlo en el sprint 1 junto con las reglas nuevas de `eslint-plugin-react-hooks`.

**Mantine sobre shadcn - Opción.** Con shadcn hay que ensamblar a mano react-hook-form, Zod y Recharts; Mantine trae formularios y gráficos en el mismo monorepo con versionado en lockstep. Para un backoffice de tablas, formularios y gráficos con quince semanas, el pegamento entre librerías es justamente lo que consume sprints. shadcn da más control de diseño, que este proyecto no necesita. Dato para quien elija shadcn igual: desde julio de 2026 su default pasó de Radix a Base UI.

**React Router v8 salió en junio de 2026** y es ESM-only, elimina `react-router-dom` como paquete separado y exige Node 22.22+. Cualquier tutorial anterior a esa fecha tiene imports que ya no existen. TanStack Router evita ese ruido y da type-safety de rutas y search params sin generación de código.

**Playwright Component Testing: no usar.** Los paquetes experimentales viejos se deprecaron el 5 de agosto de 2026 y se borraron del repo dos días después. El modelo nuevo tiene menos de un mes de vida y su propia documentación admite que la API está tomando forma. Los componentes se cubren con Vitest y Testing Library; Playwright queda para E2E web si sobra tiempo.

### El hueco que el documento deja abierto: contratos HTTP

El documento resuelve muy bien los contratos de eventos (copiados, con test de contrato contra la fuente) y no dice nada de los contratos REST entre los cuatro servicios y los dos clientes. Ese es el contrato que se rompe más seguido, porque cambia en cada sprint.

**Opción**: generar los clientes desde el OpenAPI que NestJS y FastAPI ya exponen. La herramienta con mejor salud de proyecto hoy es **Orval**: genera tipos, cliente y hooks de TanStack Query de una pasada, acepta una URL remota como entrada y no depende del compiler API de TypeScript. Cada repo cliente corre su propio script contra el `openapi.json` del backend y commitea lo generado, de modo que un cambio de contrato aparece como diff en el PR. Es el mismo espíritu que la decisión A3 del tutor: nada que publicar, la divergencia se ve en la review.

Advertencia: `openapi-typescript`, que sería la elección obvia, lleva seis meses sin release y se rompe con TypeScript 7 por depender del compiler API. No arrancar por ahí.

## 5. Datos y mensajería

Veredicto: **la arquitectura de datos no tiene nada que corregir.** Postgres más Mongo más Redis, bases fuera del cluster, un dueño por esquema, RabbitMQ con outbox. Todo eso se sostiene. Lo que sigue son mejoras baratas y dos advertencias de calendario.

### Verificado al 2026-08-19

| Pieza | Versión | Fuente |
| --- | --- | --- |
| PostgreSQL | 18.6 (13/08/2026) | postgresql.org |
| PostgreSQL en RDS | 18.4 disponible | docs de AWS |
| RabbitMQ | 4.2.10 (17/08/2026) | rabbitmq.com |
| Valkey | 9.1.1 (21/07/2026), BSD | valkey.io |
| Redis | 8.8, tri-licencia con AGPLv3 desde 8.0 | redis.io |
| sharp | 0.35.3 | registry de npm |

### Cambios recomendados

**UUIDv7 como PK de posts - Opción, recomendada.** PostgreSQL 18 trae `uuidv7()` como función nativa. Contra UUIDv4 evita el bloat del índice B-tree porque el prefijo temporal mantiene los inserts append-mostly; contra bigserial evita exponer volumen y IDs adivinables en un feed público; y permite generar el ID en la aplicación antes del insert, que es útil para el outbox. ULID queda descartado: hace lo mismo, no es estándar IETF y no tiene función nativa. El documento hoy no fija criterio de PK, y es más barato fijarlo antes de la primera migración que después.

**Colas quorum explícitas - Endurecer.** Las classic mirrored queues fueron removidas en RabbitMQ 4.0. Si nadie declara el tipo, se terminan usando colas sin replicación. Declarar `x-queue-type: quorum` y la DLQ con `x-dead-letter-exchange` en la declaración. El documento ya contempla el dashboard de dead letter queue, así que la DLQ hay que declararla igual.

Para el cluster: un solo nodo con volumen persistente alcanza para demostrar el requisito. Tres nodos con quorum queues solo si se quiere mostrar HA real.

**`SKIP LOCKED` y `pg_notify` en el outbox - Endurecer.** El publicador debe usar `SELECT ... FOR UPDATE SKIP LOCKED` para que dos réplicas no tomen el mismo evento. Y un trigger con `pg_notify` después del insert despierta al publicador al instante, dejando el polling periódico como red de seguridad. Baja la latencia a casi cero sin agregar CDC ni Debezium, que exigirían Kafka Connect en el cluster.

**Idempotencia del consumidor - Endurecer.** El documento dice que el consumidor "deduplica por id de evento" sin decir cómo. El patrón concreto: tabla con el id del evento como PK, y el insert en la tabla de dedup dentro de la misma transacción que el efecto de negocio. Así el at-least-once del broker se vuelve exactly-once desde la perspectiva del negocio, sin librerías.

**Valkey en lugar de Redis - Opción, recomendada.** Mismo protocolo, cero cambios de código. Licencia BSD sin discusión posible, contra la tri-licencia de Redis 8 que incluye AGPL. Y en ElastiCache es alrededor de 20% más barato en nodos y hasta 33% en serverless, que importa con este presupuesto.

**Migraciones - Endurecer.** El documento dice "migraciones versionadas y ejecutadas como Job antes del rollout" y nada más. Tres agregados que evitan incidentes:

1. `pg_advisory_lock` sostenido durante la migración, para que dos rollouts en carrera no migren a la vez.
2. Expand y contract en deploys separados: primero lo aditivo, el `DROP` o el `NOT NULL` en un deploy posterior. Nunca juntos.
3. Rollback forward-only. Las down-migrations casi nunca se prueban y fallan justo cuando se las necesita.

Sobre unificar Prisma Migrate y Alembic en una sola herramienta (Flyway o Atlas): **no vale la pena.** Obligaría a escribir todas las migraciones en SQL plano y perder la autogeneración desde el esquema de Prisma y desde los modelos de SQLAlchemy. Dos toolchains nativas cuestan menos que una toolchain común que nadie autogenera. Queda registrado como opción evaluada y descartada.

### Advertencias con impacto en el calendario

**Atlas M0 tiene un techo de 100 operaciones por segundo.** También 0.5 GB de almacenamiento, 500 conexiones y auto-pausa a los 30 días sin actividad. Las pruebas de carga de S6 y S12 contra `notifications-api` van a chocar contra el free tier, no contra el sistema. Hay que decidir antes de S6 si se acota el alcance de esa prueba de carga o si se prueba `notifications-api` contra una instancia local. Y capear el pool de conexiones bien por debajo de 500.

**El conflicto de `media-api`.** El documento exige subida por stream sin cargar en memoria (E1-H8 CA.7) y validación por magic numbers (E1-H8 CA.3). Ambas obligan a que los bytes pasen por el servicio. La práctica recomendada hoy es presigned PUT directo del cliente a S3, que evita proxear bytes y ahorra cómputo y ancho de banda. Pero entonces el servidor nunca ve el archivo y ninguno de los dos criterios se cumple como están redactados.

Tres caminos:

1. **Mantener el diseño actual.** Cumple los criterios de aceptación al pie de la letra. Es lo que el documento ya planteó y Node hace bien. Costo: el servicio proxea todos los bytes.
2. **Presigned PUT con validación posterior.** El objeto entra en cuarentena, un evento de S3 dispara la validación de magic numbers y la generación de miniaturas, y recién ahí se marca como válido. Más robusto y más barato, pero cambia la semántica de las historias y hay que renegociarlas.
3. **Híbrido**: presigned para adjuntos de post, stream por el servicio para avatar y portada, que son los que tienen validación más estricta.

Recomendación: opción 1 para la entrega intermedia, porque cumplir la consigna literal vale más que optimizar, y evaluar la 2 en S13 si sobra tiempo. Lo importante es que la decisión sea consciente y quede en un ADR.

**Media.** `sharp` sigue siendo la referencia en Node. AVIF ya tiene 94.67% de soporte en navegadores y comprime entre 20% y 30% mejor que WebP, así que conviene generar las miniaturas en AVIF. S3 Express One Zone es para cargas de altísima tasa de requests: no aplica, S3 Standard.

**CloudFront**: el free tier vigente es un plan permanente de 100 GB de transferencia y 1 millón de requests por mes. No es el viejo esquema de 1 TB. Alcanza de sobra para el proyecto, pero conviene saber el número real antes de presupuestar.

**pgmq no está en la lista de extensiones soportadas de RDS.** Queda descartado, y de todos modos reemplazar RabbitMQ por una cola dentro de Postgres entraría en conflicto con el requisito de la consigna de tener una cola entre dos microservicios.

### Sobre el broker: RabbitMQ sigue siendo correcto

NATS JetStream es operativamente más simple: un binario en Go, footprint chico, clientes maduros en Node y Python. Si el requisito fuera solo técnico, sería la recomendación. Pero la consigna pide demostrar la cola, y el management plugin de RabbitMQ da un dashboard web con exchanges, colas y mensajes en vivo que NATS no iguala sin herramientas de terceros. La decisión A9 se sostiene, ahora con un motivo más preciso que "simplicidad operativa".

Descartados: MSK Serverless (sin free tier, cobra por hora de cluster), SQS y EventBridge (gestionados y con free tier generoso, pero viven fuera del cluster y son más difíciles de defender como cola entre microservicios), Redpanda (sin ventaja sobre lo que ya hay).

## 6. Observabilidad, CI y seguridad

### OpenTelemetry

Traces y métricas están estables en los SDK de Node y Python. **Logs sigue experimental** en el SDK de JS: hay que fijar la versión exacta o va a romper en un `npm update`. Profiling entró en alfa en marzo de 2026; ignorarlo.

La auto-instrumentación funciona bien sin tocar código en los dos lenguajes: en Node con `@opentelemetry/auto-instrumentations-node` configurado por variables de entorno, en Python con `opentelemetry-instrument uvicorn main:app`. Cubre HTTP, Postgres, Redis y Mongo. Los spans de negocio hay que agregarlos a mano, pero eso es opcional.

**Collector: modo gateway (Deployment con una o dos réplicas), no DaemonSet ni sidecar.** El DaemonSet es para telemetría por nodo y el sidecar es para Fargate, donde no hay DaemonSet posible. El gateway centraliza batching, reintentos y muestreo, y permite cambiar de backend sin tocar las apps. El diagrama del documento ya lo dibuja así, solo falta que el manifiesto lo diga.

**OTLP sobre HTTP con protobuf**, no gRPC: evita configurar HTTP/2 fino en el ingress y a este volumen la diferencia de throughput es irrelevante.

**Muestreo**: arrancar sin muestreo. Con 50 GB de trazas en el free tier sobra. Si una prueba de carga dispara el volumen, bajar a `parentbased_traceidratio` en 0.2.

**Logging**: pino en Node (con `nestjs-pino`) y structlog en Python. Los dos emiten JSON listo para Loki e inyectan el `trace_id`. Detalle que hace perder una tarde: en Python hay que inicializar OpenTelemetry **antes** que structlog, o el processor no encuentra el span activo.

### Cobertura

El gate de 85% es requisito de la cátedra y no se discute. Lo que sí conviene decidir es cómo evitar que se cumpla con tests vacíos, porque el porcentaje de líneas no mide si el test verifica algo.

En Node, Vitest con el provider `v8` ya viene integrado: no hace falta c8 ni nyc. En Python, `pytest-cov` con `--cov-fail-under=85` hace fallar el job solo.

**Opción barata contra los tests de mentira**: correr mutation testing (Stryker en TypeScript, mutmut en Python) sobre los módulos críticos (autenticación, autorización, contadores) una vez por sprint o antes de cada entrega, nunca como gate de PR porque es lento. Es la única medida que detecta un test sin asserts.

Codecov es gratis e ilimitado para repos públicos y da comentarios de diff-coverage en el PR; en privados el plan gratis topea en 250 uploads por mes, que con siete repos hay que vigilar.

### Cadena de suministro, ordenado por valor sobre esfuerzo

1. **Secret scanning con push protection** de GitHub: gratis, cero configuración, bloquea el push antes de que el secreto entre al repo. Complementar con gitleaks en pre-commit.
2. **Dependabot**: el documento ya lo tiene. Renovate es más configurable pero esa flexibilidad no aporta nada acá.
3. **Trivy**: un solo binario cubre imágenes, manifiestos de Kubernetes y Terraform, o sea los cuatro servicios más el repo de plataforma. Nota de seguridad concreta: la action `aquasecurity/trivy-action` fue comprometida en un ataque de cadena de suministro el 19 de marzo de 2026. **Pinnear todas las actions por SHA de commit, no por tag.** Eso vale para las siete, no solo para Trivy, y es literalmente A03 del Top 10 nuevo aplicado al propio pipeline.
4. **SAST**: CodeQL es gratis e ilimitado solo en repos públicos. Si los repos son privados, Semgrep gratis cubre hasta 10 contribuyentes y 50 repos, que sobra.
5. **SBOM y attestations**: syft más `actions/attest-build-provenance`. Llega a SLSA nivel 2 casi sin trabajo, y con reusable workflows a nivel 3. Menor prioridad, pero cierra A03 de forma demostrable.

### Pruebas de carga

k6 sigue siendo la opción y el motor es open source. El free tier de Grafana Cloud incluye 500 VUh por mes, así que no hace falta cuenta aparte. Los thresholds van en el script (`http_req_duration: ['p(95)<500']`), y si fallan k6 devuelve exit code distinto de cero y el job falla solo: eso convierte los SLO del documento en algo verificable en CI y no en una promesa.

Recomendación operativa: un smoke liviano en cada PR y la prueba pesada en un job nocturno o manual, para no quemar minutos de Actions.

### Autenticación: una opción a decidir

El documento usa JWT de 15 minutos con revocación por `jti` en Redis. Funciona y está bien pensado. Pero vale plantear la alternativa, porque el argumento clásico a favor de JWT se cae en este diseño:

| | JWT con denylist (lo del doc) | Token opaco con sesión en Redis |
| --- | --- | --- |
| Round-trip a Redis | En cada request, para chequear la denylist | En cada request, para leer la sesión |
| Revocación | Por `jti` con TTL | Borrar la key, instantánea |
| Superficie de ataque | Parsers de JWT, confusión de algoritmo, `alg:none` | Ninguna, es un identificador opaco |
| Manejo de claves | Rotación de la clave de firma | No aplica |

El punto es que el JWT se elige normalmente para evitar el round-trip al almacén de sesiones, y este diseño hace el round-trip igual para consultar la denylist. Sin ese beneficio, el token opaco es estrictamente más simple.

Contraargumento honesto: JWT es lo que la materia probablemente espera ver, y `posts-api` podría validar el token sin llamar a `users-api`, lo que evita acoplamiento entre servicios. Con Redis compartido entre ambos, eso se cumple igual con tokens opacos.

Recomendación: es decisión del equipo, ambas son defendibles. Si se queda con JWT, tres endurecimientos que sí son obligatorios:

- Nunca aceptar `alg:none` y preferir algoritmo asimétrico (EdDSA o ES256) sobre HS256 compartido, para evitar confusión de algoritmo.
- Guardar en la denylist el hash SHA-256 del token, nunca el token crudo.
- **Rotación de refresh tokens con detección de reuso**: si aparece un refresh token ya usado, se asume comprometido y se revoca la familia entera de sesiones del usuario. El documento tiene refresh de 7 días sin mencionar rotación, y esto es el estándar actual.

**Argon2id**: sigue siendo la primera recomendación de OWASP. Parámetros mínimos concretos, que el documento no fija: `m=19456` (19 MiB), `t=2`, `p=1`. Sin esos números, "Argon2id" no dice nada: se puede configurar tan débil como para no servir.

## 7. Infraestructura y despliegue

Es la sección con más cambios, porque es donde el ecosistema se movió más y donde está el dinero.

### 7.1 El reemplazo del ingress - **Corregir**

Con ingress-nginx archivado (ver 1.1), la recomendación oficial de Kubernetes es migrar a una implementación de Gateway API. Gateway API va por **v1.6.1** (16 de julio de 2026), con GatewayClass, Gateway, HTTPRoute, GRPCRoute y TLSRoute en GA, y TCPRoute y UDPRoute graduados a Standard en la v1.6.0.

**Recomendación: NGINX Gateway Fabric v2.6.7**, conforme a Gateway API v1.6.1 y ya GA. Es de las implementaciones más al día, y conserva el motor NGINX, así que el conocimiento del equipo sobre configuración de NGINX no se tira. Traefik y Cilium también están en v1.6.1; Envoy Gateway va un escalón atrás.

Qué se conserva y qué se pierde respecto de lo que el documento planeaba:

| | ingress-nginx (lo del doc) | NGINX Gateway Fabric |
| --- | --- | --- |
| TLS con cert-manager | Anotación en el Ingress | Igual de simple, se anota el Gateway |
| Routing por path | `spec.rules.http.paths` | `HTTPRoute` con matchers, más expresivo |
| Rate limiting por IP | Anotación `limit-rps` | CRD `RateLimitPolicy` en `v1alpha1` |

**TLS y routing no pierden nada.** cert-manager tiene soporte maduro de Gateway API (detalle: el flag `enableGatewayAPI` quedó deprecado a favor de `gatewayAPI.enabled`).

**El rate limiting sí pierde en dos frentes, y conviene saberlo antes de elegir.** Primero, Gateway API no estandarizó rate limiting: cada implementación usa su propia CRD, así que cambiar de NGINX Gateway Fabric a Envoy Gateway después obliga a reescribir esa parte. Segundo, la `RateLimitPolicy` está en `v1alpha1` y puede romper entre minors, así que hay que fijar la versión del chart. Lo que **no** se pierde: sigue funcionando con NGINX open source, sin NGINX Plus, sin Redis y sin costo.

**Un matiz que conviene documentar y que suma en la defensa**: el rate limit del ingress es local a cada pod de NGINX. Con tres réplicas, el límite efectivo se triplica. Correr una sola réplica para la demo y explicar por qué demuestra que se entendió el problema. La alternativa realmente distribuida es Envoy Gateway con `BackendTrafficPolicy` en modo global, que exige Redis más el servicio de rate limit de Envoy: más piezas de las que este proyecto necesita.

### 7.2 Los números reales de EKS - **Corregir**

El documento estima "alrededor de 150 USD mensuales" y advierte del control plane. La estimación es del orden correcto, pero incompleta. Costos verificados contra la Price List API y las páginas de precios, en us-east-1:

| Configuración | USD/mes | Desglose |
| --- | --- | --- |
| Mínima (2× t4g.small spot, sin NAT, sin balanceador) | **94,36** | Control plane 73,00 + nodos 10,66 + EBS 3,20 + IPv4 7,30 + ECR 0,20 |
| Razonable (2× t4g.medium on-demand, 1 ALB, sin NAT) | **165,93** | Control plane 73,00 + nodos 49,06 + EBS 4,80 + ALB 16,43 + LCU 5,84 + IPv4 14,60 + resto 2,20 |
| Razonable con NAT gateway | **195,13** | |
| Razonable con VPC endpoints | **231,63** | |

Proyección de agosto a diciembre, cuatro meses y medio: entre 425 y 878 USD según la configuración.

**El dato que ordena todas las decisiones: en la configuración mínima, el control plane es el 77% del costo.** Sin él, el resto serían 21,36 USD. No hay forma de pausarlo: un cluster con el nodegroup en cero cuesta 73,00 USD exactos y nada más.

**Palancas, ordenadas por impacto real:**

1. **Destruir y recrear el cluster entre sprints: hasta -165 USD/mes.** Con `make up` y `make down` sobre Terraform, recrear tarda de 12 a 15 minutos. Prendido 40 horas al mes en lugar de 730, la configuración razonable baja a unos 9 USD mensuales. Es, por lejos, la palanca más grande. Tiene una consecuencia de diseño que aparece más abajo, en secretos.
2. **Nodegroup a cero entre demos: -49 USD/mes.** Un managed node group acepta `minSize=0` y `desiredSize=0`.
3. **Un solo ALB compartido en lugar de uno por servicio: -71 USD/mes.** Las primeras 10 reglas de routing no cuentan para LCU, así que con cuatro u ocho paths quedan en cero por esa dimensión.
4. **Spot: -57% en cómputo.** Interrupción estimada: t4g.small entre 5% y 10%, t4g.medium entre 15% y 20%, t3.medium arriba del 20%.
5. **Nodos en subredes públicas sin NAT: -29,20 USD netos.** Con security groups cerrados y acceso por SSM, no por SSH.
6. **Graviton sobre x86: -19,2%.** Las imágenes tienen que ser arm64.

Dos cosas que el documento no contempla y que conviene saber: **los VPC endpoints son la peor opción, no una alternativa al NAT** (cinco interface endpoints en dos zonas cuestan 73,00 USD y encima dejan sin salida a internet), y **sa-east-1 sale entre 35% y 45% más caro** que us-east-1 en cómputo y transferencia, mientras el control plane cuesta lo mismo. Ir a us-east-1.

### 7.3 Dos trampas que hay que desactivar el día uno - **Endurecer**

**Los clusters de EKS se crean con `upgradePolicy=EXTENDED` por defecto.** Si el cluster queda en una versión que entró en soporte extendido, AWS no bloquea nada: empieza a cobrar seis veces más por el control plane. Se desactiva con `aws eks update-cluster-config --upgrade-policy supportType=STANDARD`. Además conviene evitar Kubernetes 1.34, cuyo soporte estándar termina el 2 de diciembre de 2026, justo sobre el cierre del cuatrimestre.

**El free tier de 12 meses de AWS dejó de existir el 15 de julio de 2025.** Las cuentas nuevas entran a un "Free Plan" con 100 USD de crédito al abrir más hasta 100 USD por completar actividades, y **la cuenta se cierra sola a los 6 meses o al agotar los créditos, lo que ocurra primero**. Ya no existe el free tier específico de RDS, ElastiCache, S3 ni Amazon MQ para cuentas nuevas: todo se consume contra esos 200 USD.

Consecuencias prácticas:

- **Abrir las cuentas con plan pago.** Cobran los mismos 200 USD de crédito, y la cuenta no se cierra a los 6 meses. Un cuatrimestre dura más que eso.
- **Cuatro personas con una cuenta cada una son 800 USD.** Los términos prohíben que una misma persona abra varias cuentas, no que cuatro personas distintas abran una cada una. Rotar quién hostea, con la infraestructura en código.
- **Si la cuenta se une a una AWS Organization, los créditos expiran de inmediato.**
- Si alguien tiene una cuenta abierta antes del 15 de julio de 2025 y todavía dentro de su ventana de 12 meses, conserva el free tier viejo. Vale preguntar.
- **El GitHub Student Pack no incluye créditos de AWS.** Sí da 100 USD de Azure y 50 de MongoDB Atlas.
- **AWS Cloud Credit for Research tiene un ciclo de revisión de 90 a 120 días.** Aplicar hoy significa respuesta en diciembre. No llega.

**Advertencia sobre AWS Academy Learner Lab**, si la cátedra lo ofrece: tiene límite de tiempo por sesión, apaga o borra recursos al cerrarla, y restringe IAM a un rol fijo mientras EKS necesita crear roles. Un cluster que tiene que vivir meses no encaja en ese modelo. Hay que confirmarlo con el docente **antes** de basar el proyecto ahí, no en S2. Esto agranda el alcance de `T-23`.

### 7.4 Auto Mode: probablemente sí, con los números a la vista - **Opción**

EKS Auto Mode cobra un recargo por instancia que se puede determinar: **12% sobre el precio de la instancia** para las familias t3 y t4g. Con dos nodos chicos son 14 o 15 USD por mes. A cambio gestiona el escalado (trae Karpenter embebido), el controller de balanceo y el enforcement de network policies, sin instalar ni configurar nada.

Dos detalles que cambian el cálculo:

- **El fee es un monto fijo por tipo de instancia y no baja con Spot.** Sobre Spot el recargo efectivo se duplica: para t3.large es 24,4% real, no 12%.
- **Auto Mode no admite instancias nano, micro ni small.** El piso es t3.medium o t4g.medium. Un t4g.small es imposible en Auto Mode, aunque sí funciona en un managed node group clásico.

Recomendación: pagar los 14 USD. Con la entrega del 28 de septiembre encima, no pelearse con la configuración del load balancer controller y del autoescalado vale más que el ahorro. Compatibilidad relevante: **NGINX Gateway Fabric detrás de un `Service type: LoadBalancer` (NLB) funciona bien en Auto Mode.** Lo que no funciona es Gateway API nativa contra ALB, porque el controller gestionado todavía no la soporta.

**No arrancar nada en EKS Fargate.** No tiene EOL anunciado, pero AWS publicó una guía de migración que dice que Auto Mode es el camino recomendado, y Kubernetes 1.35 deprecó cgroup v1 mientras las release notes de EKS aclaran que Fargate sigue usándolo. Además no soporta ARM, ni DaemonSets, ni Spot.

### 7.5 El plan B es cuatro veces más barato de lo que parece

El documento plantea ECS con Fargate como plan B y fija la decisión para el 20 de septiembre. Los números del mismo workload (5 tasks de 0,5 vCPU y 1 GB):

| | EKS 2× t4g.medium | Fargate ARM | Fargate Spot ARM |
| --- | --- | --- | --- |
| Control plane | 73,00 | 0,00 | 0,00 |
| Cómputo | 49,06 | 72,09 | 22,55 |
| EBS | 3,20 | incluido | incluido |
| Con 1 ALB | **147,26** | **94,09** | **44,55** |

El control plane solo (73,00) cuesta más que todo el cómputo de Fargate ARM del workload (72,09). El descuento de Fargate Spot es del 68,72% verificado.

Esto no cambia la decisión, porque el alineamiento con las clases de Cloud Computing y la entrega en EKS lo impone el cronograma. Pero conviene tenerlo escrito para la reunión del 20 de septiembre: si EKS no llega, el plan B además ahorra tres cuartas partes del presupuesto. Configuración recomendada si se activa: `FARGATE_SPOT weight=4, FARGATE weight=1, base=1` para garantizar una task on-demand siempre viva, `stopTimeout: 120` (el default de 30 segundos pierde mensajes en vuelo) y **nunca Spot para RabbitMQ**.

**Corrección al abanico de alternativas**: App Runner **está cerrado a clientes nuevos**. Texto de AWS: "we decided to close AWS App Runner to new customers... we do not plan to introduce new features". Con cuentas nuevas no se puede crear un servicio. Su reemplazo es ECS Express Mode, que provisiona Fargate más ALB con TLS y autoescalado en una llamada, sin cargo adicional, y comparte el ALB entre servicios.

### 7.6 Secretos: Sealed Secrets choca con la palanca de ahorro - **Corregir**

El documento elige Sealed Secrets. El proyecto está sano (v0.39.0, del 18 de agosto de 2026), así que el problema no es abandono. El problema es de encaje: **la clave privada vive solo dentro del cluster**, y la palanca de ahorro más grande de la sección 7.2 es destruir y recrear el cluster entre sprints. Cada recreación deja todos los SealedSecrets del repositorio irrecuperables.

Detalle que hace perder una tarde a quien siga un tutorial viejo: el repositorio se mudó de `bitnami-labs/sealed-secrets` a `bitnami/sealed-secrets` el 15 de junio de 2026 y la URL vieja del repo de Helm devuelve 404. La alarma general sobre el catálogo de imágenes de Bitnami no lo afecta: la imagen del controller sigue pública.

| | SOPS + age | Sealed Secrets | External Secrets + Parameter Store |
| --- | --- | --- | --- |
| Costo | 0 | 0 | 0 con Parameter Store Standard |
| Pods en el cluster | **0** | 1 | 3 (~96 MiB) |
| Sobrevive a recrear el cluster | **sí** | **no**, salvo backup manual de la clave | **sí** |
| Secretos en Git | cifrados | cifrados | **ninguno** |
| Setup | una tarde | una tarde | cerca de un sprint |

**Recomendación: SOPS con age, desencriptando en GitHub Actions.** Cero pods en un cluster apretado, cero costo, y encaja con el `kubectl apply` desde Actions que el documento ya planeó. Si más adelante se suma Flux, la desencriptación de SOPS es nativa, así que el trabajo se mueve del pipeline al cluster en lugar de tirarse. Evitar `ksops`: requiere flags alpha de Kustomize que Argo CD deshabilita por defecto.

El tradeoff honesto: los secretos quedan cifrados en Git y la clave age es un secret de Actions; si se compromete, hay que rotar todo a mano. External Secrets con Parameter Store es mejor (nada sensible en Git, ni siquiera cifrado) y sale 0 USD, pero cuesta cerca de un sprint de configuración. Es la migración a hacer si sobra tiempo, y con Pod Identity el setup es una sola llamada.

Si igual se elige Sealed Secrets: **hacer backup de la master key desde el primer día**.

### 7.7 El resto de las decisiones de plataforma

**Kustomize sobre Helm - Sin cambio.** Cuatro microservicios con overlays de staging y producción es literalmente el caso de diseño de Kustomize. Usar el binario standalone (v5.8.1), no el embebido en kubectl, que va atrasado. Helm solo para instalar RabbitMQ desde un chart de terceros. Dato con fecha: **Helm 3 tiene EOL fechado**, features hasta el 9 de septiembre de 2026 y seguridad hasta el 10 de febrero de 2027. Helm 4 salió en noviembre de 2025.

**`kubectl apply` desde Actions - Sin cambio, con una nota.** Arrancar así con OIDC es correcto. Si más adelante quieren GitOps, la elección para un cluster chico es **Flux** (2 pods, 128 MiB) y no Argo CD (7 pods, cerca de 1 GiB, y sus manifiestos upstream no declaran `resources:`, así que todos sus pods quedan BestEffort y son los primeros en ser desalojados). Ojo con `aws-actions/configure-aws-credentials`: la v6.0.0 es breaking.

**KEDA - Opción, muy recomendada.** Es la mejor relación demostración/esfuerzo de todo el proyecto. El documento demuestra escalabilidad con HPA por CPU; KEDA escala `notifications-api` por profundidad de la cola de RabbitMQ, que es la métrica que de verdad importa, y con `minReplicaCount: 0` permite mostrar cero pods, publicar mensajes y verlos aparecer. Eso el HPA por CPU no lo puede hacer nunca. Es `helm install` y un `ScaledObject`. Dos advertencias que ahorran horas: **nunca definir un HPA propio sobre el mismo Deployment que un ScaledObject** (KEDA genera el suyo), y el vhost de RabbitMQ hay que URL-encodearlo (`/` es `%2F`).

**Karpenter y Cluster Autoscaler: ninguno de los dos.** Con dos nodos chicos cuestan uno o dos sprints de IAM, tags de subredes y NodePools sin aportar a lo que se va a defender, que es el escalado de pods. Con Auto Mode, Karpenter ya viene embebido sin configurar.

**EKS Pod Identity sobre IRSA - Endurecer.** Es lo que AWS recomienda hoy: sin proveedor OIDC, sin anotar el ServiceAccount, trust policy de una línea, y el mismo rol se reutiliza entre clusters, que importa si se destruye y recrea el cluster seguido. No funciona en Fargate ni Windows, y no se puede combinar con IRSA en el mismo ServiceAccount.

**GHCR sobre ECR - Sin cambio.** El documento eligió GHCR para no atar el CI a AWS, y el argumento se sostiene: el almacenamiento y el ancho de banda del registry de GitHub son gratis. ECR tiene mejor latencia y egreso gratis dentro de la misma región, pero con cuatro imágenes el costo sería de unos 0,30 USD mensuales: la decisión es por fricción, no por plata. Detalle operativo: GHCR requiere un PAT classic con `read:packages`, los fine-grained no están soportados.

**NetworkPolicies - Endurecer con una advertencia.** El documento las menciona en A05. Funcionan nativamente con el VPC CNI, pero **requieren el addon `vpc-cni` v1.21.0 o superior**, y conviene verificar que el enforcement esté habilitado en la configuración del addon: si no lo está, la API acepta las policies y no hacen nada, que es la peor forma de fallar. Limitaciones a documentar: solo nodos Linux EC2, solo una familia de IP a la vez, y los pods sin `ownerReferences` no tienen enforcement confiable. Auto Mode trae el enforcement de fábrica.

**Pod Security Admission restricted - Endurecer, con expectativas realistas.** Rompe cosas, pero de forma predecible. `readOnlyRootFilesystem` es lo que más rompe: casi todo escribe en `/tmp` (montar un `emptyDir`), NGINX necesita `/var/cache/nginx` y RabbitMQ su directorio de datos. Estrategia realista: `restricted` en el namespace de los cuatro microservicios y `baseline` en el de RabbitMQ.

Dos trampas concretas: **`enforce` solo evalúa Pods, no Deployments**, así que un Deployment inválido se crea sin error y sus pods fallan en silencio (por eso hay que poner los tres labels, `enforce`, `warn` y `audit`, no solo el primero). Y **seccomp no es `RuntimeDefault` por defecto**: el default sigue siendo `Unconfined` salvo que el kubelet lo cambie, así que hay que declararlo explícito en cada pod.

**Logs del control plane**: activar solo `api` y `authenticator`, con retención de 7 días. El default de CloudWatch es "never expire", y los 5 GB always-free alcanzan si no se activa `audit`. **No activar Container Insights**: cuesta entre 2 y 13 USD mensuales con dos nodos, y el `kube-prometheus-stack` dentro del cluster sale 0 y queda mejor en la demo.

### 7.8 Stack de infraestructura recomendado

EKS 1.36 con `upgradePolicy=STANDARD`, Auto Mode, 2 nodos t4g.medium en Spot, en subredes públicas sin NAT con security groups cerrados y acceso por SSM. NGINX Gateway Fabric sobre Gateway API v1.6.1 con cert-manager, detrás de un NLB. Imágenes arm64. Kustomize con `kubectl apply` desde Actions con OIDC. SOPS con age. RabbitMQ dentro del cluster con volumen EBS. RDS db.t4g.micro, Valkey dentro del cluster, Atlas M0. metrics-server con HPA, más KEDA para la cola. Región us-east-1.

Costo estimado: entre 85 y 137 USD mensuales corriendo continuo, o cerca de 9 USD si se apaga entre sprints.

**Para la semana del 28 de septiembre: pasar el nodegroup a on-demand el lunes anterior y dejarlo prendido hasta la entrega.** Una interrupción de Spot durante la defensa no vale los 28 USD que ahorra.

## 8. Qué no cambiaría

Vale registrarlo para que nadie reabra estas discusiones en S1:

- **Cuatro servicios con esos límites.** Identidad junto con perfil, y grafo junto con contenido y feed, están bien justificados en el documento y siguen siendo la respuesta correcta. Separarlos generaría sagas distribuidas para lo que hoy es una transacción.
- **Dos lenguajes, no tres.** Cumple el requisito con el mínimo costo de contexto.
- **Bases fuera del cluster.** Operar Postgres con estado en Kubernetes es una materia aparte.
- **RabbitMQ sobre Kafka**, ahora con un motivo más preciso: el management plugin da un dashboard con exchanges, colas y mensajes en vivo que hace demostrable el requisito. NATS JetStream es operativamente más simple, y si el requisito fuera solo técnico sería la recomendación.
- **Patrón outbox.** Es la decisión más madura del documento.
- **Contratos de eventos copiados con test de contrato.** La indicación del tutor es razonable y la mitigación propuesta cubre el riesgo real.
- **PostgreSQL para búsqueda, sin Elasticsearch.**
- **El triage de IA como consumidor dentro de `notifications-api`**, con la IA que nunca sanciona.

## 9. Orden sugerido para decidir

Por fecha límite real, no por importancia:

| Cuándo | Qué | Por qué esa fecha |
| --- | --- | --- |
| Esta semana | Cuentas de AWS con plan pago, budget con alertas, y consultar al docente por AWS Academy | Si Learner Lab no sirve, cambia todo el plan de infraestructura |
| Antes de S1 | Reemplazo del ingress: NGINX Gateway Fabric | Afecta los manifiestos de los cuatro servicios |
| Antes de S1 | UUIDv7 como PK | Después de la primera migración cuesta mucho más |
| Antes de S1 | Reusable workflows en lugar de plantillas copiadas | Cuanto más tarde, más divergencia hay que reconciliar |
| Antes de S2 | Verificar el acceso del tutor a Grafana Cloud | El documento apoya un requisito de la consigna en esto |
| Antes de S3 | RNTL 14 y Maestro; decisión sobre JWT u opaco | El gate de cobertura arranca en S3 y fija los tests |
| Antes de S6 | Alcance de la prueba de carga contra Atlas M0 | El free tier topea en 100 ops/seg |
| Antes del 20/09 | Confirmar el plan B con los números de Fargate | Es la fecha que el documento ya fijó |

## Fuentes

Todo lo verificable de este documento se contrastó contra fuentes primarias el 2026-08-19: blogs y documentación oficial de Kubernetes, AWS, PostgreSQL, RabbitMQ, Prisma, Expo, OWASP y GitHub, más el registro de npm y la Price List API de AWS.

Quedaron **sin confirmar** y no deberían citarse como dato duro en la entrega: si EKS está habilitado dentro del free account plan, el presupuesto real del AWS Academy Learner Lab, el precio por vCPU-hora de GKE Autopilot, y el nivel exacto de SLSA que alcanzan las attestations nativas de GitHub Actions.
