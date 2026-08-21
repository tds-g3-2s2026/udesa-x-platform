# Instrucciones de Copilot

Este archivo configura cómo GitHub Copilot genera texto en este repositorio. Se sincroniza
desde `udesa-x-platform` hacia todos los repos del proyecto.

## Idioma

Escribí **siempre en español rioplatense** las descripciones de Pull Request, los resúmenes
de cambios y los comentarios de revisión. Es un requisito del tutor.

El código va en inglés: nombres de variables, funciones, clases, tablas y columnas. No
mezclar los dos idiomas dentro de un identificador. `getUserById` está bien, `obtenerUserById`
no.

Los comentarios dentro del código van en español, porque explican el porqué y los lee el equipo.

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
