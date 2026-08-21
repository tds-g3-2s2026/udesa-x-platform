---
name: revisar-pr
description: Revisa un Pull Request contra el checklist del equipo (criterios de aceptación cubiertos, tests nombrados, cobertura, seguridad OWASP, reglas del repo). Usala SIEMPRE que te pidan revisar, mirar o aprobar un PR, cuando alguien pregunte "está listo para mergear", "podés revisar esto", "qué le falta a este PR", o cuando toque ser revisor primario de la semana. No aprueba nada por sí sola: produce el informe que la persona usa para decidir.
---

# Revisar Pull Request

Esta skill produce un informe de revisión. **No aprueba el PR.** La aprobación en GitHub la
da una persona, que es quien se hace responsable de lo que entra a `main`.

Eso no es una formalidad: si el agente aprobara, nadie del equipo estaría obligado a leer el
código, y la consigna exige que cada estudiante pueda explicar y justificar lo que entregó.

## Entrada

1. El diff completo (`git diff main...HEAD`).
2. La issue asociada, con sus criterios de aceptación.
3. El `AGENTS.md` del repositorio.
4. La sección "Explicación de la implementación" de la descripción del PR.

**Si esa sección no está o está vacía, frená acá.** El informe es una sola línea: el PR no
se revisa hasta que el autor la complete. Es regla del equipo y no tiene excepciones.

## Qué revisar

Recorré estos seis bloques en orden. Los primeros son los que más frecuentemente fallan.

### 1. Criterios de aceptación

Por cada CA de la issue, buscá qué parte del diff lo cubre y qué test lo verifica.

Los tests tienen que llevar el identificador del criterio en el nombre, con el formato
`E1-H1.CA3`. Sin eso, la defensa ante el tutor deja de ser mecánica y hay que ir a buscar a
mano qué test corresponde a qué criterio.

Marcá explícitamente los CA sin cobertura. Es el hallazgo más común y el más caro: un CA sin
implementar aparece recién cuando el tutor rechaza la historia entera.

### 2. Tests

- ¿Los tests verifican algo, o solo ejecutan código? Un test sin `assert` sube la cobertura
  y no prueba nada. Buscá específicamente esto.
- ¿Están cubiertos los caminos de error, no solo el feliz?
- Si la historia toca persistencia o cruza componentes, ¿hay test de integración?

### 3. Cobertura

¿El PR mantiene el repo por encima del umbral vigente? El umbral y su fecha de activación
están en el `AGENTS.md` de cada repo, porque no arrancan todos juntos.

Si la cobertura bajó, decí qué archivos la bajaron. "Bajó al 83%" no le sirve a nadie.

### 4. Seguridad

Revisá solo lo que aplica al diff. No pegues el OWASP Top 10 entero en cada informe.

- **Autorización**: ¿el endpoint verifica que el usuario puede hacer esto, o alcanza con
  estar logueado? Verificación de propiedad en las acciones sobre recursos propios.
- **Entrada**: ¿se valida el esquema? ¿se sanitiza el texto libre que se va a renderizar?
- **Filtración**: ¿el mensaje de error revela si un usuario existe? ¿vuelve algún stack
  trace al cliente?
- **Secretos**: ¿hay algo hardcodeado que debería estar en configuración?
- **Consultas**: ¿todo pasa por el ORM con parámetros, o hay SQL armado con strings?

### 5. Reglas del repositorio

Contra el `AGENTS.md`:

- ¿El código está en la capa que le corresponde según el mapa del repo?
- ¿Aparece alguna dependencia nueva? Toda dependencia nueva necesita ADR. Sin excepción.
- ¿Aparece un patrón o abstracción que no existía en el repo? Misma regla.
- ¿La rama sigue `feature-<nombre>` o `fix-<nombre>`?
- ¿El PR enlaza su issue?

### 6. Comprensibilidad

Este bloque es propio de este proyecto y es el que se saltea más fácil.

Preguntate si alguien del equipo que no escribió esto puede entenderlo leyendo el diff y la
explicación. Si la respuesta es no, es un hallazgo, aunque el código sea correcto.

Señales concretas: abstracciones que solo tienen un uso, capas de indirección sin motivo
declarado, código más general de lo que la historia pide, uso de una función del lenguaje
que no aparece en ningún otro lado del repo.

Nada de eso es un error técnico. Todo eso hace que el equipo pierda el hilo de su propio
código, que es el modo silencioso de fallar la defensa.

## Formato del informe

```markdown
## Revisión de PR #<n> — <título>

**Veredicto:** listo para aprobar | cambios necesarios | falta la explicación

### Bloqueantes
<!-- Sin esto no se mergea. Si no hay, poné "ninguno". -->

### A corregir
<!-- Hay que arreglarlo, no bloquea la conversación. -->

### Sugerencias
<!-- Mejoras opcionales. Que quede claro que son opcionales. -->

### Cobertura de criterios de aceptación

| CA | Cubierto | Test |
|---|---|---|
| CA.1 | sí | `test_registro.py::E1-H1.CA1` |
| CA.2 | no | — |
```

## Cómo escribir los hallazgos

Cada hallazgo lleva el archivo, la línea y **por qué importa**. "Falta validación" no le
sirve a quien lo tiene que arreglar; "falta validar que `bio` no exceda 160 caracteres en
`schemas.py:31`, lo pide el CA.1 de E1-H6" sí.

Separá lo que está mal de lo que es preferencia tuya. Un informe que mezcla las dos cosas
enseña al equipo a ignorar los informes.

Si el PR está bien, decilo en una línea y no inventes hallazgos para justificar la revisión.
