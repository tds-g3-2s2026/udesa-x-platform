# ADR-022: Autoaprobación de fixes y chores que no toman decisiones

**Fecha:** 2026-10-27 · **Estado:** aceptada · **Decide:** el equipo, con el visto bueno del tutor
en la reunión del 2026-10-27

## Contexto

Desde el 2026-08-21 `main` exige en todos los repos una aprobación de otra persona, también a
los admins. La regla es la misma para un PR que agrega una pantalla entera y para uno que sube
la versión del `pyproject.toml`.

De los 218 PRs mergeados desde el 2026-09-01, 66 son ramas `fix-` o `chore-` de 100 líneas o
menos. La mediana de espera de esos PRs es media hora, pero 10 esperaron más de cuatro horas.
La espera no es lo más caro: lo más caro es que aprobar se vuelva un trámite. Si la mitad de lo
que se aprueba no necesitaba mirarse, la aprobación pierde peso en los PRs que sí.

El tutor aprobó que esos PRs se mergeen sin revisión y pidió que el equipo acuerde cuáles
entran. El prefijo de la rama no alcanza para decidirlo. Cuatro ejemplos de este semestre:

- `fix-postgres-en-rds` (`udesa-x-platform#112`) movió las bases de producción de Neon a RDS.
  Es el ADR-021.
- `chore-contratos-eventos` (`udesa-x-platform#99`) fijó la forma de todos los eventos. Es el
  ADR-017.
- Las ramas `chore-adr-*` son ADRs: son decisiones por definición.
- `chore-networkpolicy` (`udesa-x-api-gateway#8`) cambió quién puede hablarle al gateway.

Hace falta un criterio que mire qué hace el cambio, no cómo se llama la rama.

## Decisión

**Un PR de una rama `fix-` o `chore-` se mergea sin aprobación si las cuatro preguntas de abajo
dan "no". Si alguna da "sí", o si hay duda, va con revisión como siempre.** Los PRs de
`feature-` siempre van con revisión.

1. **¿Cierra una historia o cambia lo que pide un criterio de aceptación?** Lo que se entrega
   como historia lo revisa otra persona: lo pide la Definition of Done y es lo que se defiende
   ante el tutor. Un fix que hace que algo vuelva a cumplir su criterio sí entra, porque no
   decide nada nuevo: vuelve a lo que ya estaba acordado. Si para arreglarlo hay que elegir
   cómo debería comportarse, eso ya es una decisión.
2. **¿Toma una decisión que el resto del equipo tiene que conocer?** Las señales:
   - pide un ADR o cambia uno;
   - suma o saca una dependencia, o la cambia de versión mayor;
   - cambia un contrato entre piezas: eventos, rutas internas entre servicios, rutas del
     gateway, o respuestas que consumen `mobile` o `backoffice`;
   - cambia algo que comparten todos los repos: los archivos comunes, el bloque común de
     `AGENTS.md` o los workflows reusables de `platform`.

   No cuentan las copias que hacen `sync-comunes.sh` o `sync-contracts.sh` sin tocar nada a
   mano, ni repetir en otro repo un cambio que ya se revisó en uno: la decisión se revisó en el
   PR original.

3. **¿Hace falta algo más que un `git revert` para deshacerlo?** Entran acá:
   - migraciones de base, que una vez desplegadas no se deshacen con un revert;
   - borrado o transformación de datos;
   - seguridad: autenticación, permisos, tokens, secretos, TLS o NetworkPolicy. Si sale mal, el
     daño puede pasar antes del revert;
   - los controles del CI: bajar el umbral de cobertura, saltear tests o sacar un check
     requerido.
4. **¿Tiene más de 200 líneas escritas a mano?** No cuentan los lockfiles ni las copias que
   generan los scripts. El tamaño no es una decisión, pero un chore grande suele esconder una,
   y en un cambio grande se justifica que lo lea otra persona.

**Lo que no cambia.** El PR autoaprobado sigue teniendo su issue, el CI en verde y la
descripción de siempre (ver `CONVENCIONES.md`), más una frase que diga por qué entra. Lleva la
etiqueta `autoaprobado` y lo mergea su autor. El agente sigue sin mergear: la decisión de que
un PR entra la toma la persona que lo firma.

**Revisión posterior.** En la review del lunes, el revisor primario mira los PRs con
`autoaprobado` de la semana, en todos los repos:

```text
org:tds-g3-2s2026 is:pr is:merged label:autoaprobado merged:>=AAAA-MM-DD
```

Si alguno no debería haber entrado, se corrige con un PR revisado y se anota en el acta. Si el
error vino de una pregunta poco clara, se ajusta con un ADR nuevo que reemplace a este.

**Cómo se aplica en GitHub.** La protección de rama clásica no permite que la aprobación sea
opcional para algunos PRs. Cada repo pasa a tener dos rulesets sobre `main`:

| Ruleset         | Reglas                                                                              | Quién lo saltea                                     |
| --------------- | ----------------------------------------------------------------------------------- | --------------------------------------------------- |
| `main-ci`       | PR obligatorio, los checks de CI que hoy exige cada repo, sin force push ni borrado | Nadie                                               |
| `main-revision` | Una aprobación                                                                      | Los integrantes (rol admin), solo al mergear un PR  |

Para autoaprobar, el autor mergea con la opción de saltear las reglas. Solo se saltea
`main-revision`: el CI se sigue exigiendo. Cada bypass queda registrado en "Rule insights" del
repo, con quién lo hizo y en qué PR.

## Alternativas descartadas

- **Autoaprobar por prefijo de rama.** Es automático, pero los ejemplos del contexto muestran
  que el prefijo no dice si hay una decisión adentro.
- **Que un workflow apruebe los PRs que tengan la etiqueta.** GitHub deja que Actions apruebe
  PRs solo si un admin de la organización lo habilita, y avisa que es un riesgo de seguridad.
  Además pone a una automatización a aprobar, que es justo lo que `CONVENCIONES.md` le saca al
  agente. La etiqueta igual la pone una persona, así que no gana control.
- **Bajar a cero las aprobaciones requeridas.** Es lo más simple, pero revisar deja de ser lo
  normal y pasa a ser algo que hay que pedir. Con el bypass, lo normal sigue siendo la revisión
  y saltearla queda registrado.
- **Seguir aprobando todo, más rápido.** Es lo que ya pasa con los PRs chicos: la aprobación
  existe, pero no dice si alguien leyó el cambio.

## Consecuencias

- Los PRs chicos de mantenimiento no esperan a nadie. Conviene separar lo mecánico de lo que
  decide: la parte mecánica entra sola y la revisión se concentra en la otra.
- La aprobación obligatoria pasa de ser un bloqueo a ser una regla del equipo con registro.
  Técnicamente, cualquiera del equipo podría mergear un `feature-` salteando la revisión. Lo
  detecta la revisión del lunes, que mira los PRs mergeados así.
- El autor de un PR autoaprobado responde solo por lo que mergea, igual que ya responde por lo
  que firma.
- Los dos rulesets y la etiqueta `autoaprobado` se configuraron en todos los repos el
  2026-10-27, mientras el tutor revisaba este ADR. Si pide cambios, se ajustan los rulesets; si
  no se acepta, se vuelve a la protección clásica, que se recrea en minutos.
- Actualiza `CONVENCIONES.md` (protección de `main` y Pull Requests) y la política de revisión
  y la Definition of Done de `PLANIFICACION.md`.
