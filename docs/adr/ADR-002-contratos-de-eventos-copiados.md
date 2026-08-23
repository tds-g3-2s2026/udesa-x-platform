# ADR-002: Contratos de eventos copiados entre repositorios

**Fecha:** 2026-08-19 · **Estado:** aceptada · **Decide:** el equipo, confirmado por el tutor

## Contexto

Con un repositorio por servicio ([ADR-001](./ADR-001-un-repositorio-por-servicio.md)), los
esquemas de los eventos que viajan por la cola los necesitan tanto el que publica como el que
consume. Las opciones eran publicarlos como librería versionada o copiarlos.

## Decisión

Se copian. Los esquemas fuente viven en `udesa-x-platform/docs/eventos/` y se propagan a
`contracts/events/` de cada repositorio de servicio.

Consultado el 2026-08-19, el tutor respondió que ante contratos con schemas idénticos se puede
copiarlos o armar librerías propias, y recomendó para este TP copiarlos, para no tener que
pelearse con empaquetados.

## Consecuencias

- No hay que resolver publicación de paquetes, versionado semántico ni un registry privado.
- Aparece el riesgo de divergencia: dos servicios con copias distintas del mismo esquema
  fallan en runtime, no en compilación. Se mitiga con el script de sincronización y un test
  que compara las copias contra la fuente (`T-16`).
- Cambiar un esquema pasa a ser un cambio coordinado en varios repositorios.
