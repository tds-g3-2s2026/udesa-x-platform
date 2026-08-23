# ADR-001: Un repositorio por servicio

**Fecha:** 2026-08-19 · **Estado:** aceptada · **Decide:** el equipo, confirmado por el tutor

## Contexto

La consigna exige una arquitectura de microservicios pero no dice dónde vive el código. Las
dos opciones eran un monorepo con los servicios en carpetas, o un repositorio por servicio.
En ambos casos el runtime es el mismo: cada servicio con su contenedor, su base y su
despliegue independiente.

El equipo se inclinaba por consolidar: los contratos de eventos se comparten entre servicios
y así no se duplican, y se evitaba mantener siete pipelines de CI/CD y siete réplicas de la
documentación general.

Como la elección podía afectar cómo se evalúa el requisito de microservicios, se le preguntó
al tutor si la separación en repositorios forma parte de la evaluación o si era indistinta y
se podía decidir por criterio técnico.

## Decisión

Un repositorio por servicio.

Respuesta del tutor, 2026-08-19: se espera tener repositorios separados. Cada servicio en su
repositorio, con sus tests y coverage, sus pipelines de CI y scripts asociados, su Docker y
composes para desarrollo, y sus manifiestos de Kubernetes.

## Consecuencias

- Seis repositorios, cada uno con su CI y su gate de cobertura del 85%.
- Los archivos comunes se duplican. Se mitiga con `sync-comunes.sh`, que los propaga desde
  `udesa-x-platform`, y con reusable workflows de GitHub para el CI.
- Las issues viven en el repositorio de su código, no centralizadas, y el milestone semanal
  coincide con el tag del repo que efectivamente se tocó.
- El costo operativo de cualquier cambio transversal se multiplica por seis. Es el precio de
  que la separación entre servicios sea explícita y verificable.
