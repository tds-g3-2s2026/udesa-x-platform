# Búsqueda literal y estado de servidor en mobile

Estado: acordada para implementación; entrega en borrador para revisión del equipo.

## Decisión

La búsqueda conserva el significado literal del texto y usa `ILIKE` con índices GIN de `pg_trgm`. Se escapan los comodines antes de construir el patrón parametrizado. El mínimo de tres caracteres limita consultas poco selectivas; no garantiza que todo término pueda aprovechar trigramas. Las migraciones crean índices en cada base y conservan la extensión al revertirlos.

Los resultados se ordenan por creación e id descendentes y se paginan con cursor. Los filtros de permisos se aplican antes de completar veinte resultados. La búsqueda de cuentas pertenece a identidad y la de publicaciones a contenido; el grafo social conserva su dueño.

Mobile adopta TanStack Query v5 sobre Axios para las búsquedas. Cada consulta pertenece a una cuenta, una pestaña y un texto. La caché vive en memoria, se cancela y limpia al terminar la sesión y se revalida al recuperar foco. El resto de los flujos mantiene su gestión actual de estado.

## Consecuencias

Los índices agregan almacenamiento y costo de escritura. La consulta de bloqueos introduce una dependencia HTTP: se reutiliza la conexión, con timeout y un reintento acotado, y una falla responde como servicio no disponible. No se incorpora búsqueda lingüística, tolerancia a errores ni un motor adicional.

Inicializar un perfil social ausente usa la visibilidad actual de identidad y no modifica perfiles existentes. La sincronización general de cambios posteriores de privacidad queda fuera de esta entrega.
