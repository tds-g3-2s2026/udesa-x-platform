# ADR-026: `expo-speech-recognition` y `expo-speech` para la voz en la app

**Fecha:** 2026-11-19 · **Estado:** aceptada · **Decide:** el equipo

## Contexto

`AI-05` (`udesa-x-mobile#76`) es el lado de la app del asistente por voz: el usuario mantiene
apretado un botón, dice lo que quiere, y la app le pregunta a `assistant-api` qué hacer y lee la
respuesta en voz alta. El ADR-023 fijó que la voz se pasa a texto en el teléfono y que al modelo
nunca le llega audio. La app no tiene ninguna librería de voz, y la regla de simplicidad de su
`AGENTS.md` pide un ADR aprobado antes de sumar una.

## Decisión

**Voz a texto con `expo-speech-recognition`**, en la versión `3.1.3`, la que su autor publica
para el SDK 54 de Expo. Usa el reconocedor del sistema: `SFSpeechRecognizer` en iOS y
`SpeechRecognizer` en Android. Se configura en `es-AR`, sin escucha continua ni palabra de
activación: escucha mientras el botón está apretado. Lo que sale del reconocedor es texto, y es
lo único que la app manda a `assistant-api`.

**Texto a voz con `expo-speech`**, la librería del SDK de Expo (`~14.0.8` en el SDK 54), para
leer la oración de `finish`.

Los permisos de micrófono y de reconocimiento de voz se declaran con el config plugin de
`expo-speech-recognition` en `app.json`, con su explicación en español.

## Alternativas descartadas

- **Mandar el audio y transcribirlo del lado del servidor**, con Amazon Transcribe o Whisper.
  Contradice el ADR-023: el audio saldría del teléfono hacia la infraestructura del grupo. Suma
  costo y demora, y la cátedra solo habilitó Bedrock con Claude Haiku 5.5.
- **`@react-native-voice/voice`.** Hace lo mismo con el reconocedor del sistema, pero su última
  versión es de mayo de 2022.
- **Whisper dentro de la app.** El modelo pesa cientos de MB y la transcripción en el teléfono
  tarda segundos.

## Consecuencias

- **Es un módulo nativo:** no corre en Expo Go. Hacen falta una APK de desarrollo nueva para
  programar y una de `preview` nueva para probar contra producción.
- **Se prueba en Android.** Un build propio en iPhone exige una cuenta paga de Apple Developer,
  que el equipo no tiene. Los teléfonos de prueba son Android.
- **El audio no pasa por UdeSA-X, pero puede salir del teléfono.** Según el dispositivo, el
  reconocedor de Android o el de iOS procesa el audio en los servidores de Google o de Apple.
  Se documenta en `AI-07`, junto con los demás límites del asistente.
- Desde el SDK 56, `expo-speech-recognition` numera sus versiones igual que Expo. Actualizar el
  SDK obliga a subirla en el mismo PR.
