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
| `udesa-x-platform` | Gestión central, docs, infra compartida, CI/CD reusable | Kustomize, Terraform, GitHub Actions |
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
