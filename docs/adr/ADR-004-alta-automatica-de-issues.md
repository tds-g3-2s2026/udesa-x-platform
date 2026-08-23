# ADR-004: Alta automática de issues en el Project

**Fecha:** 2026-08-21 · **Estado:** aceptada · **Decide:** Tomás Castro

## Contexto

Las issues viven en el repositorio de su código, en seis repositorios, y el seguimiento es
un único Project de organización. Si sumarlas al tablero es manual, el tablero se
desactualiza y deja de servir para la review de los lunes.

El workflow incorporado de GitHub, "Auto-add to project", acepta **un solo repositorio** por
proyecto: el selector es de opción única. No cubre el caso.

## Decisión

Cada repositorio lleva `.github/workflows/add-to-project.yml` con `actions/add-to-project@v2`,
disparado por `issues: [opened, reopened]`.

La autenticación usa el secret de organización `ADD_TO_PROJECT_PAT`, un token clásico con los
scopes `project` y `public_repo`. El `GITHUB_TOKEN` que Actions provee por defecto no sirve:
no puede escribir en Projects v2 de organización.

## Consecuencias

- Toda issue nueva aparece en el tablero sin intervención, sin campos cargados. La vista
  `Sin Clasificar` (`no:sprint`) es la bandeja de entrada donde se triagea en el planning.
- El PAT vence y hay que renovarlo. Está cargado como secret de organización, así que se
  actualiza en un solo lugar. Fecha de vencimiento: enero de 2027, elegida para no caer
  dentro del semestre.
- El token depende de una cuenta personal. Si esa cuenta pierde acceso a la organización, el
  alta automática deja de funcionar en los seis repos a la vez.
