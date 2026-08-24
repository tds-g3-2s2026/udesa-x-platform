# Instrucciones de Copilot

Este archivo configura cómo GitHub Copilot genera texto en este repositorio. Se sincroniza
desde `udesa-x-platform` hacia todos los repos del proyecto.

## Idioma

La frontera es el archivo de código: **si lo lee un intérprete o un compilador, va en inglés;
si lo lee una persona fuera del código, va en español.**

En **inglés**, todo lo que vive dentro de un archivo de código: nombres de variables,
funciones, clases, tablas y columnas, más los comentarios y los docstrings. También los
nombres de los archivos y carpetas de código: `user_service.py`, `src/`, `tests/unit/`. No
mezclar los dos idiomas dentro de un identificador: `getUserById` está bien, `obtenerUserById`
no.

En **español rioplatense**, todo lo que se escribe para el equipo o el tutor: descripciones de
Pull Request, mensajes de commit, resúmenes de cambios, comentarios de revisión y
documentación. El español en los PR es un requisito del tutor.

## Descripción de Pull Request

El repositorio tiene una plantilla en `.github/PULL_REQUEST_TEMPLATE.md`. **Respetá sus
secciones y no inventes otras.** La estructura es:

```markdown
# Qué cambió

Una o dos oraciones sobre el cambio, en español.

# Por qué

Qué problema resuelve o qué criterio de aceptación cubre.

# Cómo probarlo

Pasos concretos para verificar el cambio.

---

# Explicación de la implementación

**Qué cambió**

Los cambios reales, en lenguaje llano, con archivos y funciones concretas.

**Por qué**

Por qué así y no de otra forma. Anclado en un criterio de aceptación, una regla del
`AGENTS.md` o un ADR.

**Ventajas y desventajas**

Qué gana esta solución y qué cuesta. Toda decisión tiene un costo: nombralo.

**Mejoras posibles**

Qué quedó afuera a propósito y qué se haría con más tiempo.

---

# Checklist

<!-- El de la plantilla, sin modificar. -->

# Issue

Closes #<número>
```

**La sección "Explicación de la implementación" no es opcional: sin ella el PR no se
revisa.** La produce la skill `explicar-implementacion` de `.agents/skills/`, y después la
revisa y la firma una persona. Nunca la omitas ni la resumas en una línea.

No generes descripciones de una sola línea del tipo "Update service.py". Si el cambio toca
varios archivos, explicá el cambio como unidad, no archivo por archivo.

## Commits

Formato Conventional Commits, con el tipo y el scope en inglés y la descripción en español:

```
feat(users): agregar validacion de handle unico
fix(posts): corregir contador de retweets al deshacer
test(users): cubrir CA.4 de E1-H1
docs(platform): actualizar mapa de servicios
```

Tipos válidos: `feat`, `fix`, `test`, `docs`, `chore`, `refactor`, `ci`.

## Qué no hacer

No propongas dependencias nuevas ni patrones que no estén ya en el repositorio. Si algo
parece necesitarlo, decilo en la descripción del PR para que el equipo lo discuta, pero no
lo agregues.
