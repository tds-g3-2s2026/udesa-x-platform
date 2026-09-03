# ADR-006: Inversión de dependencias en los servicios backend

**Fecha:** 2026-09-03 · **Estado:** aceptada · **Decide:** el equipo, a pedido del tutor

## Contexto

En la reunión del 31 de agosto el tutor pidió organizar la distribución del proyecto
empezando por `users-api`, con el backend estructurado en carpetas, y agregó una condición
concreta: **cada archivo y servicio se tiene que poder mover de un lado a otro sin importar la
tecnología**. Dejó `tds-udesa/clase-testing-fullstack` como referencia.

El primer intento reorganizó el código por feature (`udesa-x-users-api#17`). Eso resolvió la
parte visible: el servicio pasó de tener todos los módulos planos en una carpeta a tener
`features/`, `core/` y `adapters/`.

Pero organizar carpetas no desacopla nada. Después de esa reorganización, `features/auth/service.py`
seguía abriendo con `from sqlalchemy import or_, select` y trabajando con `AsyncSession` directo.
La regla "no puede haber dos cuentas con el mismo email" estaba escrita en el idioma de
SQLAlchemy, así que mover esos datos a otro motor obligaba a reescribir el servicio y no solo
la capa de datos.

En el repositorio de referencia, `app/services/dogs.py` no importa SQLAlchemy en ninguna línea:
recibe un `DogRepository`, que es una clase abstracta declarada junto al negocio, y la
implementación concreta vive aparte en `infrastructure/database/`.

La diferencia importa para este proyecto y no solo en abstracto: la consigna exige al menos dos
tipos de base de datos, y `posts-api` va a usar MongoDB. Sin esta separación, cada servicio
queda casado con su motor desde el primer día.

## Decisión

Los servicios backend dependen de interfaces, nunca de una tecnología concreta.

**El agrupamiento por feature se conserva.** Esta decisión es sobre hacia dónde apuntan las
dependencias, no sobre cómo se agrupan los archivos.

| Capa | Qué contiene | Qué puede importar |
|---|---|---|
| `features/<x>/` | Reglas de negocio, casos de uso, y las interfaces que necesitan | `core/`, nunca `infrastructure/` |
| `core/` | Configuración, errores, seguridad, y las interfaces transversales | Nada de `features/` ni de `infrastructure/`, salvo `deps.py` |
| `infrastructure/` | Las implementaciones, agrupadas por tecnología | Lo que necesite |

Cuatro reglas:

1. **La interfaz vive del lado del negocio.** Un `UserRepository` se declara en
   `features/auth/`, no en `infrastructure/`. El negocio dicta el contrato y la tecnología se
   adapta, no al revés.
2. **El modelo de dominio se separa del de persistencia.** Dataclasses con las reglas en
   `features/<x>/domain.py`; tablas del ORM en `infrastructure/database/`. Cada repositorio
   traduce entre los dos.
3. **`core/deps.py` es el único módulo que conoce las implementaciones.** Es la costura:
   cambiar de motor o de proveedor es escribir una clase y tocar ese archivo.
4. **Los repositorios no confirman la transacción.** La unidad de trabajo es el request, no la
   operación individual: se abre y se cierra en `core/db.session_scope`. Es una diferencia
   deliberada con el repositorio de la cátedra, que hace `commit` adentro del repositorio. Un
   registro son tres operaciones —crear la cuenta, crear el token y mandar el correo— y tienen
   que quedar todas o ninguna.

**Excepción:** el healthcheck le habla a PostgreSQL y a Redis directamente. Su trabajo es
verificar que la infraestructura real responde; una interfaz en el medio lo vaciaría de
sentido.

La forma queda implementada en `udesa-x-users-api` y es la que tienen que seguir `posts-api` y
`notifications-api` cuando arranquen.

## Consecuencias

- **Los servicios se testean sin infraestructura.** En `users-api` eso significó 33 tests
  nuevos que corren en dos segundos sin Docker y prueban cosas que un test de integración no
  ve: que un login bloqueado corta sin llegar a consultar la base, que un login exitoso
  resetea el contador de intentos.
- **`posts-api` puede usar MongoDB sin que su lógica de negocio se entere.** Es lo que hace
  viable el requisito de dos motores de base sin duplicar reglas.
- **Más archivos.** En `users-api`, `src/` pasó de 20 a 26 módulos para el mismo comportamiento.
- **Indirección.** Para seguir qué hace una llamada hay que saltar de la interfaz a la
  implementación. Un archivo más de lectura, siempre.
- **El mapeo entre fila y objeto de dominio se escribe a mano.** Agregar una columna obliga a
  tocar tres lugares: la tabla, la dataclass y la función que traduce.
- **La regla depende de la revisión.** Hoy nada impide que alguien vuelva a importar SQLAlchemy
  dentro de una feature: está escrito en el `AGENTS.md` de cada repo y se controla al revisar.
  Un test que falle ante ese import queda pendiente.

Las tres primeras desventajas son el precio conocido del patrón. Se acepta porque hay reglas de
negocio que vale la pena probar aisladas, porque van a convivir dos motores de base y porque el
proveedor de correo todavía no está elegido. En un servicio sin reglas y con una sola base no
se justificaría, y no hay que aplicarlo por costumbre.
