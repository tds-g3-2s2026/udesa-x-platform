# udesa-x-platform

Repositorio central de gestión, arquitectura, documentación e infraestructura compartida para **UdeSA-X** (Taller de Desarrollo de Software - Grupo 3, 2S2026).

## Documentación principal

Toda la documentación base del proyecto está centralizada en [`docs/`](./docs/):

- [`docs/CONSIGNA.md`](./docs/CONSIGNA.md): Transcripción depurada de la consigna oficial, requisitos funcionales/no funcionales, épicas e historias de usuario con criterios de aceptación.
- [`docs/ARQUITECTURA.md`](./docs/ARQUITECTURA.md): Arquitectura de referencia del sistema, mapa de servicios, stack tecnológico, comunicaciones, persistencia, observabilidad y seguridad (OWASP Top 10:2025).
- [`docs/PLANIFICACION.md`](./docs/PLANIFICACION.md): Plan de trabajo del semestre dividido en 15 sprints semanales, reparto de historias por integrante, gestión en GitHub Projects y análisis de riesgos.
- [`docs/REVISION-FRONTERA.md`](./docs/REVISION-FRONTERA.md): Auditoría del stack tecnológico contra fuentes primarias (2026-08-19), costos de infraestructura y justificación de decisiones técnicas.

## Estructura del repositorio

```text
udesa-x-platform/
├── docs/
│   ├── CONSIGNA.md            # Requisitos y alcance oficial
│   ├── PLANIFICACION.md       # Sprints, roles, reparto y riesgos
│   ├── ARQUITECTURA.md        # Diseño de referencia y mapa técnico
│   ├── REVISION-FRONTERA.md   # Auditoría de versiones y decisiones
│   ├── adr/                   # Architecture Decision Records
│   ├── eventos/               # Esquemas JSON Schema fuente de eventos
│   ├── actas/                 # Minutas de reuniones de seguimiento
│   └── retros/                # Retrospectivas semanales
├── k8s/                       # Manifiestos de Kubernetes compartidos y Gateway API
├── terraform/                 # Definición de infraestructura como código (EKS, RDS, etc.)
├── compose/                   # Docker Compose integrado para ambiente local completo
├── scripts/                   # Scripts de utilidad (ej. sync-contracts.sh)
└── .github/
    └── workflows/             # Reusable workflows para CI/CD de todos los repos
```

## Mapa de repositorios de la organización

La solución se estructura en siete repositorios bajo la organización `tds-g3-2s2026`:

| Repositorio | Descripción | Stack principal |
|---|---|---|
| `udesa-x-platform` | Gestión central, docs, infra compartida, CI/CD reusable | Kustomize, Terraform, GitHub Actions |
| `udesa-x-mobile` | Aplicación mobile para usuarios finales | React Native + Expo, TanStack Query, Zustand |
| `udesa-x-backoffice` | Panel web de administración y moderación | React 19 + Vite 8 + Mantine |
| `udesa-x-users-api` | Identidad, autenticación, perfiles y administradores | NestJS 11 + TypeScript, PostgreSQL 18, Valkey |
| `udesa-x-posts-api` | Contenido, grafo social, feed cronológico y búsqueda | FastAPI + Python 3.13, PostgreSQL 18, Valkey |
| `udesa-x-notifications-api` | Notificaciones push (FCM), historial in-app y triage IA | NestJS 11 + TypeScript, MongoDB Atlas |
| `udesa-x-media-api` | Ingesta por streaming y almacenamiento de imágenes | NestJS 11 + TypeScript, Amazon S3, Sharp |
