# ADR-018: Librerías para imágenes en publicaciones

**Fecha:** 2026-10-23 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

`E2-H7` pide adjuntar hasta cuatro imágenes JPG o PNG a un post, de 1 MB como máximo, validadas
por su contenido real (`CA.1` a `CA.3`), mostradas en una grilla adaptativa y abiertas en un
visor a pantalla completa con zoom y navegación entre las imágenes del post (`CA.4` y `CA.5`).

Ninguna de las dos partes tiene hoy con qué hacerlo. `mobile` no trae selector de imágenes ni
visor, y `posts-api` no trae cliente de S3 ni lector de formularios multipart. La regla de
simplicidad de los `AGENTS.md` pide un ADR aprobado antes de sumar una librería.

## Decisión

**En `mobile`: `expo-image-picker` para elegir las imágenes y `@nandorojo/galeria` para
verlas. En `posts-api`: `aioboto3` y `python-multipart`.**

- **Selector: `expo-image-picker`**, en la versión que `expo install` fija para el SDK 54
  (`~17.0.11`). Es la librería oficial de Expo para esto. Se llama con `quality: 1`, porque
  cualquier otro valor vuelve a codificar el archivo sin que el usuario lo pida, y la regla de
  1 MB está pensada para avisar, no para comprimir (`D15`, opción B). Su plugin de configuración
  agrega por defecto el permiso `RECORD_AUDIO` en Android; la app lo bloquea junto con
  `CAMERA`, porque solo se elige de la galería.
- **Visor: `@nandorojo/galeria` 3.1.0.** Trae pellizco y doble toque para el zoom, deslizar para
  cerrar y varias imágenes en un mismo visor, que es lo que pide `CA.5`. Envuelve las imágenes
  que ya dibuja la grilla y abre el visor en la que se tocó, así que no hace falta un
  componente de visor propio. Es nativa (Swift y Kotlin) y exige la Nueva Arquitectura, que el
  proyecto ya tiene activa (`newArchEnabled`).
- **Backend: `aioboto3` 15.5.0 y `python-multipart` 0.0.32.** Ya figuran en el stack de
  `ARQUITECTURA.md`: `aioboto3` es el cliente asíncrono de S3 (sube, borra y firma las URLs de
  lectura) y `python-multipart` lee el cuerpo multipart. `posts-api` no usa `UploadFile` de
  FastAPI, que recibe cada archivo completo antes de que corra el endpoint: alimenta el parser
  de `python-multipart` chunk a chunk desde `request.stream()` y corta en el byte que pasa 1 MB
  (1.048.576 bytes) o la quinta imagen. Cada imagen se guarda en un archivo temporal
  (`SpooledTemporaryFile`, en memoria hasta 256 KB), así no se retiene el archivo entero en
  memoria. Este módulo es el que reutiliza `E1-H8`.

## Alternativas descartadas

- **`react-native-image-viewing`.** JavaScript puro y sin dependencias nativas, pero la última
  versión publicada es de mayo de 2022.
- **`react-native-awesome-gallery`.** Pide `react-native-reanimated` y
  `react-native-gesture-handler`, que el proyecto no tiene instalados: sumaría dos módulos
  nativos más solo para el visor.
- **Un visor escrito a mano.** No suma dependencias, pero el zoom con pellizco en Android
  requiere código de gestos propio que no se puede probar sin un dispositivo, y `CA.5` lo exige.
- **`boto3` síncrono.** Bloquearía el event loop de FastAPI en cada subida o firma, o habría
  que mandarlo a un thread pool a mano. `aioboto3` es el mismo SDK con interfaz asíncrona.
- **`UploadFile` / `Form` de FastAPI.** Es el camino más corto, pero corta por tamaño después
  de recibir todo el cuerpo, lo que contradice "corta al pasar 1 MB" y el stream de `E1-H8`.

## Consecuencias

- Las dos librerías de `mobile` son nativas: hace falta una APK nueva para probar cualquier cosa
  de esta historia, y `@nandorojo/galeria` no funciona en Expo Go, solo en la APK de desarrollo o
  la de `preview` que ya se generan con EAS.
- En Jest el visor se reemplaza por un doble en `jest.setup.ts`: los tests verifican qué
  imágenes recibe el visor y en qué orden, no el zoom ni los gestos, que son de la librería.
- `@nandorojo/galeria` depende de un solo mantenedor. Si se abandona, el reemplazo se limita a
  `PostImageGrid`, el único componente que la importa.
- Galeria exige iOS 16.4 o superior. La entrega es una APK de Android, así que no afecta hoy.
- El plugin de `expo-image-picker` cambia el manifiesto de Android: solo surte efecto con una
  APK nueva.
- `aioboto3` fija `botocore` y `wrapt<2`: en `posts-api`, `wrapt` baja de 2.5.0 a 1.17.3. Trae
  además `aiohttp` como dependencia transitiva.
- Las URLs de lectura son firmadas (SigV4), directas a S3 y vencen en 1 hora
  (`IMAGE_URL_EXPIRY_SECONDS`). Salen contra el host regional del bucket
  (`<bucket>.s3.<región>.amazonaws.com`): el host global redirige con un 307 cuando el bucket
  no está en `us-east-1`. El bucket es privado y las credenciales las resuelve el SDK
  (variables de entorno o rol del pod); no son settings del servicio.
- La subida y la lectura se probaron contra un bucket real (`tds-group-3-media`, `us-east-2`).
  Para que funcione en el cluster, el pod necesita credenciales de acceso al bucket y el
  ConfigMap necesita `S3_BUCKET` y `S3_REGION`. Sin `S3_BUCKET` el servicio arranca igual y
  publicar con imágenes responde 503.
