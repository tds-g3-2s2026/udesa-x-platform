# udesa-x-platform

Repositorio central de gestión, arquitectura, documentación e infraestructura compartida para **UdeSA-X** (Taller de Desarrollo de Software - Grupo 3, 2S2026).

## Documentación principal

Toda la documentación base del proyecto está centralizada en [`docs/`](./docs/):

- [`docs/CONSIGNA.md`](./docs/CONSIGNA.md): Transcripción depurada de la consigna oficial, requisitos funcionales/no funcionales, épicas e historias de usuario con criterios de aceptación.
- [`docs/ARQUITECTURA.md`](./docs/ARQUITECTURA.md): Arquitectura de referencia del sistema, mapa de servicios, stack tecnológico, comunicaciones, persistencia, observabilidad y seguridad (OWASP Top 10:2025).
- [`docs/PLANIFICACION.md`](./docs/PLANIFICACION.md): Plan de trabajo del semestre dividido en 15 sprints semanales, reparto de historias por integrante, gestión en GitHub Projects y análisis de riesgos.
- [`docs/CONVENCIONES.md`](./docs/CONVENCIONES.md): Reglas de trabajo del equipo y guidelines del tutor: repositorios, ramas, issues, labels, milestones, PRs y sincronización entre repos. Es la fuente del bloque común de los `AGENTS.md`.
- [`docs/CATALOGO-ISSUES.md`](./docs/CATALOGO-ISSUES.md): Inventario de las issues del semestre con sus identificadores `T-XX`, `AI-XX` y `DXX`, y estado del tablero. Es lo que da sentido a las referencias `T-XX` de la planificación.

Además, [`AGENTS.md`](./AGENTS.md) es el punto de entrada para trabajar en este repo, con o sin agente: mapa, reglas del equipo y checks.

## Estructura del repositorio

```text
udesa-x-platform/
├── AGENTS.md                  # Mapa, reglas y checks; fuente del bloque común
├── .editorconfig              # Fuente, se sincroniza a todos los repos
├── .agents/
│   └── skills/                # Skills del equipo, versionadas y sincronizadas
├── docs/
│   ├── CONSIGNA.md            # Requisitos y alcance oficial
│   ├── PLANIFICACION.md       # Sprints, roles, reparto y riesgos
│   ├── ARQUITECTURA.md        # Diseño de referencia y mapa técnico
│   ├── CONVENCIONES.md        # Reglas de trabajo del equipo
│   ├── CATALOGO-ISSUES.md     # Inventario de issues del semestre
│   ├── adr/                   # Decisiones de arquitectura, una por archivo
│   ├── actas/                 # Minutas de reuniones de seguimiento
│   └── retros/                # Retrospectivas semanales
├── compose/                   # Docker Compose integrado para ambiente local completo
├── k8s/                       # Namespace, cuotas, límites e Ingress; los aplica el docente
├── templates/
│   └── repo-servicio/         # Plantilla de repositorio de servicio
├── scripts/                   # sync-contracts.sh y sync-comunes.sh
└── .github/
    ├── workflows/             # Reusable workflows para CI/CD de todos los repos
    ├── copilot-instructions.md  # Fuente, se sincroniza a todos los repos
    └── PULL_REQUEST_TEMPLATE.md # Fuente, se sincroniza a todos los repos
```

## Mapa de repositorios de la organización

La solución se estructura en seis repositorios bajo la organización `tds-g3-2s2026`, todos públicos (ver [ADR-003](./docs/adr/ADR-003-repositorios-publicos.md)):

| Repositorio | Descripción | Stack principal |
|---|---|---|
| `udesa-x-platform` | Gestión central, docs, infra compartida, CI/CD reusable | Kubernetes (manifiestos planos), GitHub Actions |
| `udesa-x-mobile` | Aplicación mobile para usuarios finales | React Native + Expo, TanStack Query, Zustand |
| `udesa-x-backoffice` | Panel web de administración y moderación | React 19 + Vite 8 + Mantine |
| `udesa-x-users-api` | Identidad, autenticación, perfiles, administradores y avatares | FastAPI + Python 3.13, PostgreSQL 18, Redis, S3 |
| `udesa-x-posts-api` | Contenido, grafo social, feed cronológico, búsqueda e imágenes de post | FastAPI + Python 3.13, PostgreSQL 18, Redis, S3 |
| `udesa-x-notifications-api` | Notificaciones push (FCM), historial in-app, emails y triage IA | NestJS 11 + TypeScript, MongoDB Atlas |

Dos decisiones del 2026-08-20 explican este mapa y están justificadas en [`ARQUITECTURA.md`](./docs/ARQUITECTURA.md):

- **Python es el stack principal del backend** (A25). `users-api` y `posts-api` van en FastAPI, y `notifications-api` es el único servicio en TypeScript. La consigna exige más de una tecnología, no fija el peso de cada una.
- **No hay `media-api`** (A26). La subida de archivos vive en el servicio dueño del dato, con el módulo de streaming escrito una vez en `users-api` y copiado a `posts-api`.

## Archivos comunes

Estos archivos tienen su fuente acá y se sincronizan al resto de los repos con [`scripts/sync-comunes.sh`](./scripts/sync-comunes.sh). No se editan en la copia local: se editan acá y se propagan.

| Archivo | Destino |
|---|---|
| `.editorconfig` | todos los repos |
| `.github/copilot-instructions.md` | todos los repos |
| `.github/PULL_REQUEST_TEMPLATE.md` | todos los repos |
| `.agents/skills/` | todos los repos |
| bloque común de `AGENTS.md` | todos los repos |
| `docs/eventos/*.json` → `contracts/events/` | repos de servicio, vía `sync-contracts.sh` |

## Despliegue en el cluster de la cátedra

Según el [ADR-008](./docs/adr/ADR-008-plataforma-de-despliegue.md), usamos el cluster
`tds-cluster`, región `us-east-2`, y únicamente el namespace `tds-group-3`.
Los manifiestos son planos, sin Kustomize ni overlays.

| Recurso | Quién lo aplica |
|---|---|
| [`k8s/namespace.yaml`](./k8s/namespace.yaml): Namespace, ResourceQuota y LimitRange | El docente, después de revisar y aprobar el PR |
| [`k8s/ingress.yaml`](./k8s/ingress.yaml): entrada HTTP del sistema | El docente, después de revisar y aprobar el PR |
| [`k8s/networkpolicy.yaml`](./k8s/networkpolicy.yaml): los pods del namespace solo aceptan tráfico entre ellos | El docente, después de revisar y aprobar el PR |
| Deployment, Service, ConfigMap, Secret y Job de migración de cada servicio | [`deploy.yml`](./.github/workflows/deploy.yml), en cada push a `main` del servicio |
| [`k8s/redis.yaml`](./k8s/redis.yaml): Deployment y Service del Redis compartido | [`deploy-redis.yml`](./.github/workflows/deploy-redis.yml), cuando cambia el manifiesto o a mano desde Actions |

Los valores de cuota, el grupo de ALB y el host salen de la clase 6, Cloud Computing I del
14 de septiembre, la misma que cierra el [ADR-008](./docs/adr/ADR-008-plataforma-de-despliegue.md).
Los fija la cátedra: no son decisiones del equipo y no se cambian por cuenta propia.

La cuota del equipo es de `2` CPU y `2Gi` de memoria en requests, `4` CPU y `4Gi`
en limits, hasta `8` pods, `4` Services, `4` ConfigMaps y `4` Secrets.
**Uno de los cuatro ConfigMaps ya está ocupado** por `kube-root-ca.crt`, que Kubernetes
crea solo en cada namespace: quedan tres, uno por servicio con código.
Por contenedor, el mínimo es `100m` / `128Mi` y el máximo `500m` / `512Mi`.
Los valores predeterminados son request `100m` / `128Mi` y limit `500m` / `512Mi`.
Igualmente, cada Deployment debe declarar sus requests y limits explícitamente.

**La cuota es de ocho pods, no seis.** Un escenario futuro con `users-api`, `posts-api`,
`api-gateway`, `notifications-api`, RabbitMQ y Redis tendría seis pods con una réplica
cada uno; no significa que esos seis componentes ya estén desplegados. El séptimo y octavo
entran si alcanzan las demás cuotas; el noveno es rechazado.

Los tres Deployment HTTP usan `maxSurge: 1` y `maxUnavailable: 0`: conservan el pod anterior
hasta que el nuevo esté listo. Reservar capacidad para el pod adicional y los Jobs de
migración activos, incluyendo CPU y memoria. Ejecutar los despliegues de forma secuencial
si comparten ese margen; la exclusión de GitHub Actions de un repo no serializa otros repos.
Un pod todavía terminando también puede consumir cuota. Sin margen, el rollout puede
quedar trabado: no aumentar automáticamente `maxUnavailable` a costa de interrumpir el servicio.
Una réplica con rolling update no es alta disponibilidad. Ocho contenedores con límites
de `500m` / `512Mi` agotan los `4` CPU / `4Gi` de limits.

El Ingress comparte el ALB mediante `group.name: tds-shared`, usa `group.order: "203"`
y solo recibe tráfico para `tds-group-3.tds-linar.udesa.edu.ar`.
No cambiar el grupo compartido ni agregar reglas sin host: eso puede crear otro ALB
o interferir con otros equipos. Los cambios de DNS se coordinan con el docente.

| Path (`Prefix`, sin reescritura) | Service | Puerto del Service |
|---|---|---|
| `/api` | `api-gateway` | `80` |

**El Ingress tiene una sola regla y apunta a `api-gateway`.** Ese servicio reparte
internamente por prefijo (`udesa-x-api-gateway`, `src/routing.ts`): `/api/auth`, `/api/me` y
`/api/admin` van a `users-api`; `/api/users`, `/api/follow-requests`, `/api/posts`, `/api/feed`,
`/api/blocks` y `/api/reports` van a `posts-api`.
La razón es el ciclo de cambio:
este archivo lo aplica el docente a mano, así que agregar un backend nuevo tiene que ser un
cambio en el gateway que despliega CI, y no una revisión más de este manifiesto. Además evita
mantener la misma tabla de ruteo en dos lugares.

La contrapartida es que `api-gateway` queda en el camino crítico: si su Deployment no está
arriba, todo `/api` responde 503. Tiene que desplegarse antes o junto con el primer apply del
Ingress.

El puerto `80` es una decisión del equipo para todos los Services HTTP, no un valor impuesto
por la cátedra. Sus manifiestos deben declarar `spec.ports[].port: 80`. La excepción es
Redis, que no habla HTTP y queda en `6379`, el puerto que fija el `REDIS_URL` del ADR-009.
El Service apunta al puerto nombrado `http`, declarado como `containerPort: 8000` en el
Deployment. Ese número coincide con Uvicorn/Bun y el `EXPOSE` del Dockerfile; no tiene
por qué ser el puerto `80` del Service.
El Ingress usa la clase `alb`, targets por IP y `/healthcheck`, que el gateway expone sin
dependencias propias, para comprobar la salud del target group.
Las annotations de alcance de grupo (`scheme`, `listen-ports`, `certificate-arn`, subnets)
no se declaran acá a propósito: son del ALB compartido y las fija la cátedra. Declararlas
con un valor distinto al del resto del grupo rompe la reconciliación para todos los equipos.

La integración requiere desplegar conjuntamente las versiones alineadas:
[users-api#42](https://github.com/tds-g3-2s2026/udesa-x-users-api/pull/42),
[posts-api#37](https://github.com/tds-g3-2s2026/udesa-x-posts-api/pull/37) y los manifiestos del
[gateway#2](https://github.com/tds-g3-2s2026/udesa-x-api-gateway/issues/2). El gateway conserva
`/api` y la query: los backends deben montar sus rutas bajo ese prefijo. Sus URLs internas
son `http://users-api` y `http://posts-api`, sin `/api` ni `:8000`.

Las APIs usan `/livez` para liveness sin consultar dependencias y `/healthcheck` para
readiness con PostgreSQL y Redis. Una caída de la base retira el pod del tráfico, sin
reiniciarlo por liveness. Las sondas consultan el pod directamente y no necesitan una
regla pública en el Ingress. El healthcheck del gateway no demuestra la salud de las APIs.

### Aislamiento de red

Dos NetworkPolicy, sugeridas por la cátedra. [`k8s/networkpolicy.yaml`](./k8s/networkpolicy.yaml)
deja que los pods del namespace solo reciban tráfico de otros pods del mismo namespace. La de
`udesa-x-api-gateway` le abre además el gateway al ALB, desde sus dos subredes: `10.100.0.0/20`
y `10.100.16.0/20`, las que llevan la etiqueta `kubernetes.io/role/elb` en la VPC del cluster.
Funciona porque el ingress usa `target-type: ip`: el ALB le habla directo al pod, y el origen
que ve el gateway es la IP del ALB.

**Hoy no filtran nada.** El agente de red del cluster, `aws-eks-nodeagent` dentro del
DaemonSet `aws-node`, corre con `--enable-network-policy=false`: el objeto se crea pero nadie lo
aplica. Habilitarlo es una decisión de la cátedra sobre el cluster entero.

Cuando se habilite, verificar que `users-api` y `posts-api` sigan en `Ready`. Las sondas las
hace el kubelet desde la IP del nodo, que no es un pod del namespace; si quedan bloqueadas, los
pods se reinician en bucle sin que el error mencione la NetworkPolicy.

### Cifrado en tránsito

El TLS del sistema se termina en el ALB compartido, con el certificado de ACM que administra
la cátedra. Por eso el Ingress no declara `certificate-arn` ni `listen-ports`.

Del ALB hacia adentro el tráfico va en HTTP plano por decisión operativa; no hay mTLS.
Un mesh o cert-manager necesita componentes de alcance de cluster que administra la
cátedra, pero no es la única manera de implementar TLS: también podría terminarlo cada
aplicación con certificados provisionados. Eso queda fuera de este despliegue.

No asumir cifrado entre nodos por el solo hecho de usar Nitro: AWS lo ofrece para
[tipos de instancia y trayectos específicos](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/data-protection.html#encryption-transit).
Hay que confirmar los nodos y la topología reales con la cátedra; esa protección tampoco
equivale a TLS entre aplicaciones ni a autenticación mutua.

**Las conexiones que salen del cluster sí van cifradas y eso es responsabilidad del equipo.**
Las bases persistentes son gestionadas y viven fuera del cluster, así que cada servicio tiene
que exigir TLS en su URL de conexión, no solo permitirlo:

| Destino | Qué usar |
|---|---|
| PostgreSQL | Validación de CA y hostname con el driver real. Estas APIs usan SQLAlchemy + asyncpg, así que va `?ssl=verify-full` en la URL y no el parámetro libpq `sslmode`, que asyncpg no acepta y hace fallar la conexión. No usar `require` como sustituto de validación del servidor. asyncpg no mira el almacén del sistema: hace falta además `PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt`, que ya está en el ConfigMap de cada servicio |
| Redis | Va dentro del cluster, no sale del namespace: `redis://`. Si alguna vez pasa a ser gestionado, `rediss://` |
| RabbitMQ, si queda fuera del cluster | esquema `amqps://` |

### Bases de datos gestionadas

Decidido en el [ADR-009](./docs/adr/ADR-009-bases-gestionadas-y-migraciones.md), issue
[#46](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/46). **Proveedor: Neon**, capa
gratuita, sin tarjeta, PostgreSQL 18 y TLS obligatorio. Un proyecto por servicio, región
`aws-us-east-2`, la del cluster.

| Qué | Dónde vive | Quién lo consume | Dónde está la URL |
|---|---|---|---|
| Proyecto `users-api` (`mute-hat-57607938`), base `users` | Neon, `aws-us-east-2` | `users-api` | Secret `DATABASE_URL` del repo `udesa-x-users-api` |
| Proyecto `posts-api` (`floral-haze-34260608`), base `posts` | Neon, `aws-us-east-2` | `posts-api` | Secret `DATABASE_URL` del repo `udesa-x-posts-api` |
| Redis compartido | Pod del namespace `tds-group-3`, manifiesto `k8s/redis.yaml` de este repo | `users-api` con `/0`, `posts-api` con `/1` | Secret `REDIS_URL` de cada repo de servicio |

Estado al 2026-09-20: los dos proyectos existen con PostgreSQL 18.6, su `0001` aplicada y los
cuatro secrets cargados. El manifiesto del Redis está en `k8s/redis.yaml` y lo aplica
`deploy-redis.yml`.

Ninguna URL se escribe en un archivo del repositorio: van como GitHub Secret del repositorio
que las usa, y `k8s/secret.yaml` sigue en `.gitignore`. La URL que da la consola de Neon se
carga **corrigiendo los parámetros**: `postgresql+asyncpg://<rol>:<clave>@<host>/<base>?ssl=verify-full`,
con el endpoint directo y no el `-pooler`, que es PgBouncer en modo transacción y choca con el
caché de prepared statements de asyncpg.

El Redis compartido lo aplica el CD de este repositorio, no una persona: el permiso del equipo
sobre el cluster es de solo lectura. Un reinicio de ese pod pierde la denylist de JWT y los
contadores de rate limit, que es el precio aceptado de que no tenga volumen.

Detalles del manifiesto que conviene saber explicar:

- **Estrategia `Recreate`, no `RollingUpdate`.** Durante un rollout convivirían dos Redis
  independientes detrás del mismo Service, y una revocación escrita en el viejo no existiría
  en el nuevo. El corte dura lo que tarda en arrancar el pod y, además, no consume el margen
  de cuota que reservan los `maxSurge` de las APIs.
- **`maxmemory 192mb` con `noeviction`.** El límite de memoria del contenedor es `256Mi`:
  Redis rechaza escrituras antes de que el kernel mate el pod y se pierda todo junto. No se
  expulsan claves porque expulsar una revocación volvería válido, sin aviso, un token revocado.
- **Sin `--protected-mode`.** La imagen oficial lo apaga sola cuando arranca sin archivo de
  configuración, que es lo que permite que las APIs se conecten desde otros pods.

**Desde la primera migración aplicada contra Neon, el esquema solo cambia con Alembic.** La
`0001` de cada servicio queda congelada: nada de editarla ni de `alembic stamp` contra una base
con datos.

### GitHub Secrets para el despliegue

Los valores viven como **secrets de organización** con visibilidad para todos los
repositorios, y no en este archivo: los repositorios son públicos y el Account ID quedaría
a la vista en cualquier log de Actions. Acá se documenta qué es cada uno y de dónde salió,
no su contenido. Documentar un valor acá tampoco lo crea en GitHub.

Los recursos los creó el equipo en la Parte 1 de la guía de despliegue
([#60](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/60)), todos en `us-east-2` y
con el prefijo `tds-group-3`. La infraestructura compartida es de la cátedra y no se toca:
cluster, VPC, ALB, certificados y zona DNS.

| Secret | Qué contiene y para qué se usa | De dónde sale |
|---|---|---|
| `AWS_ROLE_ARN` | ARN del rol `GitHubActions-tds-group-3-Deploy`, que GitHub Actions asume por OIDC. No es un usuario IAM ni una clave de acceso: no hay ninguna credencial de largo plazo. | Rol propio del grupo. Confía en `token.actions.githubusercontent.com` con `aud` igual a `sts.amazonaws.com` y `sub` acotado a `repo:tds-g3-2s2026@315118458/*`, lleva la permissions boundary `tds-group-boundary`, y su acceso al cluster sale de un Access Entry con `AmazonEKSEditPolicy` de alcance `tds-group-3`. |
| `AWS_REGION` | Región donde opera el despliegue: `us-east-2`. | La fija la cátedra y está registrada en ADR-008. |
| `EKS_CLUSTER_NAME` | Nombre del cluster que usa el pipeline al preparar kubeconfig: `tds-cluster`. | Cluster compartido de la cátedra; se confirma en EKS > Clusters y en ADR-008. |
| `S3_BUCKET` | Nombre del bucket de los archivos del backoffice, sin `s3://` ni una URL. | Bucket propio del grupo, con los cuatro bloqueos de acceso público activos: quien lo sirve es CloudFront por OAC, no el bucket. |
| `CLOUDFRONT_DISTRIBUTION_ID` | ID de la distribución `tds-group-3-frontend`, que usa el deploy del backoffice para invalidar la caché después de publicar. | Distribución propia del grupo, creada en la Parte 4 de la guía. La policy `tds-group-3-deploy-policy` permite invalidar solo esa distribución. |
| `ECR_URI_PREFIX` | Prefijo de URI de las imágenes, con la forma `<account-id>.dkr.ecr.us-east-2.amazonaws.com/tds-group-3`; sin `https://` ni tag. **Ya incluye el prefijo del grupo**, así que la referencia se arma como `${ECR_URI_PREFIX}/<servicio>:<tag>` y no repite `tds-group-3`. | Tres repositorios propios del grupo, uno por servicio con código: `tds-group-3/api-gateway`, `tds-group-3/users-api` y `tds-group-3/posts-api`, los tres con tags mutables. |

El pipeline arma **`ECR_IMAGE`** como `${ECR_URI_PREFIX}/<servicio>@sha256:<digest>`: la
imagen se publica con el commit como tag, pero se despliega por digest, que es lo que la
hace inmutable aunque los repositorios de ECR acepten retaggear. Los tres Deployment usan
únicamente `${ECR_IMAGE}` como marcador. Kubernetes no lo expande: el pipeline lo sustituye
y corta el despliegue si queda cualquier otro `${...}` sin resolver.

**El `sub` lleva el ID de la organización.** Los repositorios de `tds-g3-2s2026` emiten el
token con el formato de sujeto inmutable de GitHub: `repo:tds-g3-2s2026@315118458/<repo>@<id>:...`.
Una condición con el nombre solo, `repo:tds-g3-2s2026/*`, no coincide y AWS rechaza el
`AssumeRoleWithWebIdentity`. El ID además es más seguro que el nombre: si la organización se
borrara, quien creara otra con el mismo nombre no heredaría el acceso al rol.

**Un solo dominio para todo.** `tds-group-3.tds-linar.udesa.edu.ar` apunta, con un registro A
con Alias en Route 53, a la distribución de CloudFront. La distribución manda `/api/*` al ALB,
sin caché y reenviando todos los headers (el ALB elige el namespace por el `Host`), y el resto
al bucket, que solo ella puede leer a través de su OAC. El backoffice y la API comparten
origen, así que no hace falta CORS.

Las claves personales de AWS no se usan como credenciales del pipeline.
Nunca commitear credenciales, tokens ni `k8s/secret.yaml` con valores reales:
ese archivo debe estar en `.gitignore` de cada repositorio.
Solo se versionan plantillas de secretos sin valores reales.

### Despliegue continuo

Cada servicio llama a [`deploy.yml`](./.github/workflows/deploy.yml) desde su `ci.yml`, con
`needs: ci` y solo en push a `main`: un PR nunca despliega y un commit que no pasó el CI
tampoco. El job que llama tiene que declarar `permissions: id-token: write`, sin eso no hay
token de OIDC.

| Servicio | `secretos` | `migracion` |
|---|---|---|
| `users-api` | `DATABASE_URL REDIS_URL JWT_PRIVATE_KEY` | `alembic upgrade head` |
| `posts-api` | `DATABASE_URL REDIS_URL JWT_PUBLIC_KEY` | `alembic upgrade head` |
| `api-gateway` | ninguno | ninguna |

Qué hace, en orden:

1. Verifica que estén los secrets de organización, los secrets listados en `secretos`, los
   manifiestos y el marcador `${ECR_IMAGE}`. Si falta algo, falla nombrando qué falta.
2. Asume `AWS_ROLE_ARN` por OIDC, construye la imagen y la publica en ECR.
3. Se conecta al cluster y comprueba que el namespace tenga su ResourceQuota y que el rol
   pueda crear lo que va a aplicar.
4. Aplica `k8s/configmap.yaml` y arma `<servicio>-secret` con los GitHub Secrets listados,
   con server-side apply para que los valores no queden copiados en una annotation. Nunca
   aplica `secret.template.yaml`, `namespace.yaml` ni `ingress.yaml`.
5. Si hay `migracion`, la corre como Job con la misma imagen y espera que termine bien. Si
   falla, corta ahí y los pods anteriores siguen sirviendo. Los logs quedan en el run y el
   Job se retira solo a la hora.
6. Si el servicio tiene `k8s/networkpolicy.yaml`, la aplica. Es el caso del gateway, que tiene
   que aceptar el tráfico del ALB. Después aplica `k8s/service.yaml` y el Deployment con la
   imagen resuelta y espera el rollout. Si no converge, muestra el diagnóstico, hace
   `kubectl rollout undo` y falla. En el primer despliegue no hay versión anterior: solo falla.

El pod template lleva la annotation `udesa-x/config-hash`, calculada sobre el ConfigMap y los
valores del Secret: un cambio solo de configuración también reemplaza los pods. El rollback
vuelve atrás los pods, no el ConfigMap, el Secret, la NetworkPolicy ni el esquema de la base.
Borrar `k8s/networkpolicy.yaml` de un servicio no la borra del cluster: hay que hacerlo con
`kubectl delete`.

Un despliegue por servicio a la vez, sin cancelar el que ya está tocando el cluster. Repos
distintos sí corren en paralelo: si se mergea en los tres a la vez, las migraciones y los
pods extra del `maxSurge` comparten la cuota.

Lo que el pipeline no hace y queda para el primer despliegue:

- Crear el primer superadmin de users, con su comando idempotente y credenciales de
  bootstrap separadas.
- Aplicar el Ingress, que es del docente. El gateway y las APIs tienen que estar listos
  antes, y después se comprueba login y una operación autenticada de posts por HTTPS desde
  el host público.

Users firma con una clave privada Ed25519 estable; posts recibe su pública correspondiente.
Ambos validan `JWT_ISSUER=users-api`. No hay descubrimiento JWKS ni rotación automática.
Agregar la validación de issuer invalida tokens antiguos que no tengan ese claim: los
usuarios deben iniciar sesión otra vez. Una rotación de clave también requiere coordinar
ambos servicios; no generar una clave nueva en cada deploy. El par de producción se generó
el 2026-09-27 y existe solo como GitHub Secret: `JWT_PRIVATE_KEY` en `udesa-x-users-api` y
`JWT_PUBLIC_KEY` en `udesa-x-posts-api`.

Los valores de `envFrom` se leen al crear el contenedor. Cambiar Secret o ConfigMap no
actualiza los pods existentes: por eso el pipeline pone el hash de la configuración en el pod
template, y un cambio solo de configuración también los reemplaza. Una migración debe ser
compatible con la versión anterior durante el rolling update. Volver a una imagen anterior
**no** revierte el esquema de la base.
No usar `alembic stamp` para adoptar una base existente sin verificar su esquema.

Pendientes externos: bases y TLS real ([#46](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/46))
e identidades/acceso ([#47](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/47)). Los clientes deben usar
`https://tds-group-3.tds-linar.udesa.edu.ar/api` como base, sin `/v1`, también para posts;
los defaults locales antiguos no son configuración de producción. Si el backoffice se
sirve desde otro origen, configurar `CORS_ALLOWED_ORIGINS` en users con ese origen real.
No se inventan esos valores ni se promete una validación en AWS antes de disponer de ellos.

### Cómo verificar qué está desplegado

Cada push a `main` de un servicio lo vuelve a desplegar, así que la versión que corre no se
anota acá: se consulta. Con el acceso personal descrito abajo:

```bash
kubectl --context tds-group-3 -n tds-group-3 get pods,deploy,svc,ingress -o wide
```

Los pods tienen que estar `Running` y `1/1`. El `/healthcheck` de las APIs no se expone por el
Ingress: es su readiness probe, así que `1/1` significa que responde bien con PostgreSQL y Redis.

La columna de imágenes muestra el digest de cada servicio. Para saber a qué commit corresponde,
buscar ese digest en el log del job `deploy` del run de CI en `main`: la imagen se publica con el
commit como tag y se despliega por digest.

El ruteo se prueba por el host público y sin token:

```bash
curl -i https://tds-group-3.tds-linar.udesa.edu.ar/api/me    # 401 de users-api
curl -i https://tds-group-3.tds-linar.udesa.edu.ar/api/feed  # 401 de posts-api
curl -i https://tds-group-3.tds-linar.udesa.edu.ar/api/nada  # 404 del gateway
```

Un `404 no route configured` en un prefijo que debería existir significa que falta en la tabla
del gateway. Un `503` en todo `/api` significa que el gateway no está listo.

### Acceso personal de cada integrante

Cada integrante necesita **su propio usuario IAM**, claves de acceso y MFA habilitado,
entregados o autorizados por la cátedra. No se comparten usuarios, claves ni dispositivos
MFA. El nombre del perfil local puede ser el mismo en las tres máquinas; eso no significa
que usen la misma identidad.

Instalar una versión actual de AWS CLI v2 que incluya `aws configure mfa-login` y
`kubectl` compatible con la versión del cluster. La cátedra también debe habilitar el
acceso de la identidad personal al cluster y el permiso para describirlo.

1. Configurar el perfil personal. Ingresar las claves propias cuando el CLI las pida,
   región `us-east-2` y formato de salida `json`:

   ```bash
   aws configure --profile tds-group-3
   ```

2. Obtener una sesión temporal con MFA. Reemplazar `<MFA_DEVICE_ARN>` por el ARN del
   dispositivo propio, visible en IAM > Users > usuario propio > Security credentials:

   ```bash
   aws configure set mfa_serial '<MFA_DEVICE_ARN>' --profile tds-group-3
   aws configure mfa-login --profile tds-group-3 --update-profile tds-group-3-mfa
   aws sts get-caller-identity --profile tds-group-3-mfa --region us-east-2
   ```

   El CLI pide el código MFA y guarda credenciales temporales en el perfil
   `tds-group-3-mfa`, sin reemplazar las claves del perfil base.
   Habilitar MFA en la consola y ejecutar solo `aws configure` no alcanza:
   hay que obtener la sesión temporal. Al vencer, repetir `mfa-login`.
   Este flujo usa MFA de códigos de un solo uso, no passkeys; ver la
   [documentación de AWS](https://docs.aws.amazon.com/cli/latest/reference/configure/mfa-login.html).

3. Configurar kubeconfig usando explícitamente el perfil con MFA:

   ```bash
   aws eks update-kubeconfig \
     --profile tds-group-3-mfa \
     --region us-east-2 \
     --name tds-cluster \
     --alias tds-group-3
   ```

   El comando actualiza el kubeconfig local y selecciona ese contexto.
   El perfil queda referenciado para que `kubectl` obtenga los tokens de EKS.
   No usar el rol de CI para acceder desde una máquina personal.

4. Verificar la lectura, siempre con el contexto y namespace del grupo explícitos:

   ```bash
   kubectl --context tds-group-3 -n tds-group-3 get pods,services,ingresses
   kubectl --context tds-group-3 -n tds-group-3 describe resourcequota
   kubectl --context tds-group-3 -n tds-group-3 describe limitrange
   ```

   No consultar ni modificar namespaces ajenos.

**El acceso personal es de solo lectura. Un `kubectl apply` devuelve `Forbidden`:
es lo esperado, no un error que haya que resolver ampliando permisos.**
Para comprobarlo sin persistir cambios, desde la raíz de la plataforma:

```bash
kubectl --context tds-group-3 -n tds-group-3 apply --server-side --dry-run=server -f k8s/ingress.yaml
```

El dry-run del servidor verifica la autorización de escritura y debe ser rechazado.
Si se acepta, avisar al docente; no probar un apply real.
Si falla una lectura por credenciales vencidas, renovar MFA; si persiste un error de
autorización o de conectividad, consultar al docente. La comprobación real de acceso
de los tres integrantes se sigue en [la issue #47](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/47).
