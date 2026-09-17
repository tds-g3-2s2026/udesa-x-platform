# ADR-008: Plataforma de despliegue sobre el cluster de la cátedra

**Fecha:** 2026-09-14 · **Estado:** aceptada · **Decide:** la cátedra, el equipo se adapta

**Cierra la decisión abierta `D21`** y **reemplaza las decisiones `A17` y `A18`** del registro
de `ARQUITECTURA.md`.

## Contexto

Hasta hoy el despliegue no tenía ADR a propósito. `PLANIFICACION.md` lo dejaba anotado: *"la
plataforma de despliegue y el proveedor de nube se deciden con la clase de Cloud Computing
cursada, dentro de la ventana de `D21`: registrarlas hoy sería dar por cerrado algo que el
equipo no puede justificar"*. En paralelo quedaban abiertas `A16`, el presupuesto de AWS, y
`D21`, el plan B con ECS si EKS se complicaba.

La clase de Cloud Computing I del 14 de septiembre fijó las condiciones, y no son las que el
equipo había supuesto:

- **El cluster ya existe y lo provisiona la cátedra**: `tds-cluster`, región `us-east-2`.
- **Cada grupo recibe un namespace propio**, `tds-group-3`, con cuota y límites.
- **Los integrantes tienen permiso de solo lectura sobre el cluster.** Un `kubectl apply`
  desde una máquina del equipo responde `Forbidden`, y eso es el comportamiento esperado.
- **El role de CI puede editar únicamente su namespace**, vía EKS Access Entry con
  `AmazonEKSEditPolicy` acotada.
- **`namespace.yaml` e `ingress.yaml` los revisa y aplica el docente**, por pull request.

Sobre ese reparto de permisos, dos decisiones previas dejaron de ser posibles.

**`A17` elegía Gateway API con NGINX Gateway Fabric**, porque `ingress-nginx` está archivado
desde marzo de 2026. El razonamiento sigue siendo correcto, pero **es inaplicable**: instalar
un gateway controller exige recursos de alcance de cluster, CRDs, un `GatewayClass` y un
Deployment fuera del namespace propio. Nada de eso entra dentro de los permisos del grupo. No
es que convenga otra cosa: no hay forma de hacerlo.

**`A18` elegía SOPS con age** para los secretos. El modelo de la cátedra resuelve lo mismo por
otro camino: una plantilla versionada sin valores, el secreto real fuera del repositorio, y los
valores inyectados desde GitHub Secrets por el pipeline. Sumar SOPS encima no agrega
confidencialidad, agrega una pieza que nadie pidió.

## Decisión

El despliegue va sobre el cluster de la cátedra, con la estructura que la cátedra pide.

**Un solo `ingress.yaml`** para todo el sistema, con la API `Ingress` de Kubernetes. La API no
está deprecada; lo que está archivado es el controller `ingress-nginx`, y qué controller corre
en el cluster es una decisión de la cátedra, no del equipo.

**Manifiestos planos por repositorio**, en una carpeta `k8s/`:

```text
k8s/
├── deployment.yaml
├── service.yaml
├── configmap.yaml
└── secret.template.yaml
```

Sin Kustomize ni overlays por ahora. Hay un solo entorno y un solo namespace: una capa de
composición para un único destino es complejidad sin contrapartida.

**`namespace.yaml` e `ingress.yaml` viven en `udesa-x-platform`**, porque son del sistema y no
de un servicio, y son los dos archivos que aplica el docente.

**Los secretos** se versionan solo como plantilla. `k8s/secret.yaml`, el archivo con valores
reales, va en `.gitignore` de cada repositorio. Los valores llegan desde GitHub Secrets.

**`containerPort` del Deployment, `targetPort` del Service y el puerto que escucha la
aplicación son el mismo número**, y se verifica contra el `EXPOSE` del Dockerfile de cada
servicio.

**Todos los endpoints de todos los servicios van bajo el prefijo `/api`.** Con un único
`Ingress` para el sistema entero, el ruteo es por path, y sin prefijo no hay forma de decidir
a qué servicio mandar una petición: `users-api` y `posts-api` publican rutas de primer nivel
que se pisan. Con el prefijo, la regla queda sin ambigüedad:

| Path | Servicio |
|---|---|
| `/api/auth/*`, `/api/me/*`, `/api/admin/*` | `users-api` |
| `/api/users/*` | `posts-api` |

Es el prefijo tal cual lo pidió la cátedra, sin número de versión. Agregarlo sería una decisión
propia que nadie pidió, y cambiarlo más adelante es cambiar un prefijo.

**El `healthcheck` queda fuera de `/api`.** Las sondas de Kubernetes pegan directo contra el
pod, no pasan por el ingress, así que no necesita ser ruteable desde afuera. **Conviene
confirmarlo con el tutor**: si esperan que también esté bajo el prefijo, es mover una línea.

**Este cambio rompe a los clientes y por eso va primero.** `udesa-x-mobile` ya apunta a
`/api/v1`, que no coincide con nada de lo que los servicios publican hoy, y `udesa-x-backoffice`
apunta a la raíz. Los dos se corrigen en el mismo movimiento, que es lo que la issue
`udesa-x-mobile#11` venía arrastrando.

**Quién aplica qué:**

| Recurso | Lo aplica |
|---|---|
| `namespace.yaml`, `ingress.yaml` | El docente, después de aprobar el PR |
| `configmap`, `secret`, `deployment`, `service` | El pipeline de CI |
| Cualquier cosa desde una máquina del equipo | Nadie: el permiso es de solo lectura |

## Consecuencias

**Sobre las tareas técnicas:**

| Tarea | Qué pasa |
|---|---|
| `T-09` provisionar el cluster de EKS | Se cierra: la provisiona la cátedra |
| `T-10` Gateway API con NGINX Gateway Fabric | Se reemplaza por el `ingress.yaml` que aprueba el docente |
| `T-11` manifiestos con Kustomize y overlays | Se simplifica a manifiestos planos |
| `T-12` SOPS con age | Se corre, reemplazada por plantilla más GitHub Secrets |
| `T-14` workflow de CD | Pasa a S6: la clase que lo cubre es el 21 de septiembre |
| Prefijo `/api` | Nuevo, sale de esta decisión. Toca los dos servicios y los dos clientes |

**El rate limiting no se pierde.** `ARQUITECTURA.md` lo repartía entre el gateway, por IP, y
los servicios, por usuario. La mitad del gateway deja de ser del equipo, pero el requisito de
la consigna, *"rate limiting en al menos un microservicio"*, ya está cumplido y desplegado:
`users-api` limita los intentos de login y `posts-api` los seguimientos por hora. Lo que se
pierde es la primera línea de defensa por IP, y conviene decirlo antes de que lo pregunten.

**`A16`, el presupuesto de AWS, deja de ser un problema del equipo.** No hay que decidir si el
cluster se destruye entre sprints ni quién lo paga.

**`D21`, el plan B con ECS, se descarta.** Existía por si EKS se complicaba por costo o por
tiempo de provisión. Las dos razones desaparecen cuando el cluster viene dado.

**Lo que el equipo no controla, no lo puede arreglar.** Si el ingress se cae o el controller
cambia de versión, la respuesta es avisar al docente. Ese es el costo de no ser dueños de la
entrada, y es aceptable: el objetivo de la materia es desplegar el sistema, no operar un
cluster.
