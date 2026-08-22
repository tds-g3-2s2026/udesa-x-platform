# ADR-003: Repositorios públicos

**Fecha:** 2026-08-21 · **Estado:** aceptada · **Decide:** Tomás Castro

## Contexto

La organización está en el plan gratuito de GitHub. Con repositorios privados, ese plan no
habilita:

- Ramas protegidas ni rulesets. La API responde `403: Upgrade to GitHub Pro or make this
  repository public`. Sin esto, cualquiera puede pushear a `main` y la guideline del tutor
  de "toda rama sale de un PR aprobado" queda como acuerdo verbal, no como regla aplicada.
- Secrets de organización. Habría que cargar el mismo secret seis veces y rotarlo seis veces.
- Minutos de Actions ilimitados. En privado son 2.000 por mes para toda la organización,
  que con seis repos y CI en cada PR se consume rápido.

Alternativas evaluadas: pagar GitHub Team (4 USD por persona por mes) o gestionar el
programa de GitHub Education, que no llegaba para la review del 24 de agosto.

## Decisión

Los seis repositorios pasan a públicos.

La consigna no exige que sean privados. Antes del cambio se revisó el historial completo en
busca de credenciales y no había ninguna.

## Consecuencias

- Quedan habilitadas las ramas protegidas, los secrets de organización y Actions sin cuota.
- El código es visible para cualquiera, incluidos otros grupos de la cursada. Se comunica al
  tutor en la reunión del 24 de agosto por el contrato moral de honestidad académica.
- Ningún secreto puede entrar al repositorio, ni siquiera temporalmente: un commit que se
  revierte sigue estando en el historial y el historial ahora es público.
