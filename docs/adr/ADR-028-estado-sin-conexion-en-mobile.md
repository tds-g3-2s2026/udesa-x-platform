# ADR-028: `@react-native-community/netinfo` para el estado sin conexión en mobile

**Fecha:** 2026-11-26 · **Estado:** propuesta · **Decide:** el equipo

## Contexto

`T-57` (`udesa-x-mobile#104`) pide que la app sepa cuándo no hay conexión. Hoy no lo sabe: sin
red, cada pantalla cae a su estado de error, y publicar o dar like falla después del timeout con
un mensaje genérico. La app no tiene ninguna librería que informe el estado de la red, y la regla
de simplicidad de su `AGENTS.md` pide un ADR aprobado antes de sumar una.

Dos datos del código pesan en la decisión. React Query ya está en la app, pero solo lo usan
búsqueda, notificaciones y tendencias: el feed y el perfil piden sus datos con `useState` y axios.
Y los tres clientes axios comparten los interceptores de `attachAuthInterceptors`.

## Decisión

**`@react-native-community/netinfo`**, en la versión `11.4.1`, la que `expo install` fija para el
SDK 54. Sus cambios alimentan a `onlineManager` de React Query, que queda como el único lugar
donde la app sabe si hay conexión: el aviso, las pantallas y la guarda de escrituras lo leen.
Cuenta como sin conexión `isConnected === false` o `isInternetReachable === false`, así que un
Wi-Fi sin salida a internet también cuenta. Mientras NetInfo no midió (`null`) se asume que hay
red, para no abrir la app con un aviso falso.

Con eso:

- El layout raíz muestra un aviso "Sin conexión" en todas las pantallas.
- Las consultas de React Query se pausan y se reanudan solas. El feed conserva lo que ya cargó y
  se recarga al volver la red.
- **Las escrituras sin red se bloquean con un aviso, no se encolan.** Un interceptor de request en
  `attachAuthInterceptors` rechaza todo lo que no sea `GET` o `HEAD` antes de que salga del
  teléfono. Las llamadas a `/auth` quedan afuera: login y registro ya fallan con su mensaje de
  conexión, y un refresco rechazado ahí cerraría la sesión.

## Alternativas descartadas

- **Encolar las escrituras y mandarlas al volver la red.** Es bastante más trabajo (guardar la
  cola, reintentar, mostrar lo pendiente) y puede mandar algo que el usuario ya no quiere, como un
  like que deshizo o un post que perdió sentido. Nadie lo pidió.
- **`expo-network`.** Es la librería del SDK de Expo y también informa si hay red y si se llega a
  internet. No hay una diferencia técnica que pese para este uso: se elige NetInfo porque lo pide
  `T-57`. Si el equipo prefiere quedarse dentro del SDK de Expo, como en el ADR-026, el cambio se
  limita a `watchConnection`.
- **Chequear la red en cada pantalla antes de escribir.** Repite el chequeo en cada acción y una
  acción nueva puede olvidarlo. En el interceptor, una regla cubre los tres clientes.
- **Migrar el feed y el perfil a React Query** para que también se pausen solos. Toca dos
  pantallas, sus tests y los hooks de likes y borrado que comparten cinco pantallas. Queda fuera
  de `T-57`.

## Consecuencias

- **Es un módulo nativo:** hace falta una APK de desarrollo nueva.
- **Las acciones que escriben no esperan el timeout:** fallan al instante con "Sin conexión.
  Probá de nuevo cuando vuelva la red.".
- **Los perfiles no se conservan sin red.** Abrir uno muestra su error de carga. La caché tampoco
  se guarda en el teléfono: abrir la app sin red empieza vacía.
- **Un refresco que falla por la red sigue cerrando la sesión**, como antes de este cambio. La
  guarda no lo provoca, porque `/auth` queda afuera, pero tampoco lo resuelve: va en un issue
  aparte.
