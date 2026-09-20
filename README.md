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
| Deployment, Service, ConfigMap, Secret y Job de migración de cada servicio | El futuro pipeline de CD, dentro del namespace del grupo |

Los valores de cuota, el grupo de ALB y el host salen de la clase 6, Cloud Computing I del
14 de septiembre, la misma que cierra el [ADR-008](./docs/adr/ADR-008-plataforma-de-despliegue.md).
Los fija la cátedra: no son decisiones del equipo y no se cambian por cuenta propia.

La cuota del equipo es de `2` CPU y `2Gi` de memoria en requests, `4` CPU y `4Gi`
en limits, hasta `8` pods, `10` Services, `10` ConfigMaps y `10` Secrets.
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
`/api/admin` van a `users-api`, y `/api/users` a `posts-api`. La razón es el ciclo de cambio:
este archivo lo aplica el docente a mano, así que agregar un backend nuevo tiene que ser un
cambio en el gateway que despliega CI, y no una revisión más de este manifiesto. Además evita
mantener la misma tabla de ruteo en dos lugares.

La contrapartida es que `api-gateway` queda en el camino crítico: si su Deployment no está
arriba, todo `/api` responde 503. Tiene que desplegarse antes o junto con el primer apply del
Ingress.

El puerto `80` es una decisión del equipo para todos los Services, no un valor impuesto
por la cátedra. Sus manifiestos deben declarar `spec.ports[].port: 80`.
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
| PostgreSQL | Validación de CA y hostname con el driver real. Estas APIs usan SQLAlchemy + asyncpg (`ssl=verify-full`, no el parámetro libpq `sslmode`), con la CA de RDS disponible para el driver; comprobarlo contra la instancia asignada. No usar `require` como sustituto de validación del servidor |
| Redis con encryption in transit | esquema `rediss://` |
| RabbitMQ, si queda fuera del cluster | esquema `amqps://` |

Se fija cuando se creen las bases, en la issue
[#46](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/46).

### GitHub Secrets para el despliegue

Cargar los valores en **Settings > Secrets and variables > Actions** de cada repositorio
que ejecute el despliegue, o como secrets de organización con acceso a esos repositorios.
Documentar un valor acá no lo crea en GitHub. No alcanza con cargarlo solo en la
plataforma si el workflow corre desde un repositorio de servicio.

| Secret | Qué contiene y para qué se usa | De dónde sale |
|---|---|---|
| `AWS_ROLE_ARN` | ARN completo del rol IAM que asume GitHub Actions para desplegar. No es un usuario IAM ni una clave de acceso. | Lo entrega la cátedra; se consulta en IAM > Roles > rol de CI > ARN. El acceso a EKS de ese rol está acotado a `tds-group-3`. |
| `AWS_REGION` | Región donde opera el despliegue: `us-east-2`. | La fija la cátedra y está registrada en ADR-008. |
| `EKS_CLUSTER_NAME` | Nombre del cluster que usa el pipeline al preparar kubeconfig: `tds-cluster`. | Lo entrega la cátedra; se confirma en EKS > Clusters y en ADR-008. |
| `S3_BUCKET` | Nombre del bucket asignado para los archivos del sistema, sin `s3://` ni una URL. | Lo entrega la cátedra; se consulta en S3 > Buckets. No se deduce del nombre del namespace. |
| `ECR_URI_PREFIX` | Prefijo de URI para las imágenes privadas. Tiene la forma `<account-id>.dkr.ecr.us-east-2.amazonaws.com`, más el prefijo de repositorio si la cátedra asigna uno; sin `https://` ni tag de imagen. | Pedir el prefijo exacto a la cátedra y contrastarlo con la URI de los repositorios asignados en ECR > Private registry > Repositories. Respetar también el separador entre ese prefijo y el nombre del servicio. |

El pipeline construirá **`ECR_IMAGE`**, la referencia completa del repositorio asignado
con tag inmutable por commit o digest, a partir de los datos reales de ECR. Los tres
Deployment usan únicamente `${ECR_IMAGE}` como marcador. Kubernetes no lo expande:
el futuro CD debe sustituirlo y rechazar valores vacíos o marcadores sin resolver antes
de aplicar. El ARN del rol, el bucket, el Account ID y la URI real se piden a la cátedra.

Las claves personales de AWS no se usan como credenciales del pipeline.
Nunca commitear credenciales, tokens ni `k8s/secret.yaml` con valores reales:
ese archivo debe estar en `.gitignore` de cada repositorio.
Solo se versionan plantillas de secretos sin valores reales.

### Orden del primer despliegue y de las actualizaciones

**Estas PRs no implementan CD ni publican imágenes.** El workflow actual valida código e
imágenes localmente en el runner; hacer merge no modifica EKS. El futuro CD debe:

1. Partir de un commit validado, construir la imagen y publicarla en ECR con referencia
   inmutable. Usar OIDC para asumir el rol de CI, no claves personales. Confirmar por
   separado los permisos de push del pipeline, pull del cluster y edición del namespace.
2. Esperar el namespace/cuotas de la cátedra y las bases accesibles. Aplicar ConfigMap y
   Secret real antes de los workloads, nunca `secret.template.yaml` ni un `apply -f k8s/`
   que pueda sobrescribir secretos con plantillas vacías. El gateway no necesita Secret.
3. Ejecutar `alembic upgrade head` de cada API con la misma imagen de la versión, como
   Job de ejecución única, y esperar su éxito antes del rollout. Crear el primer
   superadmin de users con su comando idempotente y credenciales de bootstrap separadas.
   Reservar cuota para los Jobs y retirar los terminados después de conservar sus logs.
4. Aplicar los Services y Deployments con la imagen resuelta. Esperar
   `kubectl rollout status deployment/<servicio> -n tds-group-3` con timeout; si falla,
   detener el pipeline, no anunciar éxito ni hacer rollback de base automáticamente.
5. Tener el gateway y las APIs listos antes de habilitar el Ingress con el docente.
   Comprobar login y una operación autenticada de posts por HTTPS desde el host público.

Users firma con una clave privada Ed25519 estable; posts recibe su pública correspondiente.
Ambos validan `JWT_ISSUER=users-api`. No hay descubrimiento JWKS ni rotación automática.
Agregar la validación de issuer invalida tokens antiguos que no tengan ese claim: los
usuarios deben iniciar sesión otra vez. Una rotación de clave también requiere coordinar
ambos servicios; no generar una clave nueva en cada deploy.

Los valores de `envFrom` se leen al crear el contenedor. Cambiar Secret o ConfigMap no
actualiza los pods existentes: el CD debe reemplazarlos también en cambios solo de
configuración. Una migración debe ser compatible con la versión anterior durante el
rolling update. Volver a una imagen anterior **no** revierte el esquema de la base.
No usar `alembic stamp` para adoptar una base existente sin verificar su esquema.

Pendientes externos: bases y TLS real ([#46](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/46)),
identidades/acceso ([#47](https://github.com/tds-g3-2s2026/udesa-x-platform/issues/47)),
ECR y workflow de CD (`T-14`, S6). Los clientes deben usar
`https://tds-group-3.tds-linar.udesa.edu.ar/api` como base, sin `/v1`, también para posts;
los defaults locales antiguos no son configuración de producción. Si el backoffice se
sirve desde otro origen, configurar `CORS_ALLOWED_ORIGINS` en users con ese origen real.
No se inventan esos valores ni se promete una validación en AWS antes de disponer de ellos.

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
