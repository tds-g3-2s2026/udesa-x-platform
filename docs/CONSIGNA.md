# UdeSA-X

Transcripción depurada de `UdeSA-X.pdf`. Se corrigieron errores de formato propios de la extracción del PDF, pero se conservaron los requisitos y criterios de aceptación originales. Cuando exista una ambigüedad de alcance, la decisión debe comunicarse y consensuarse con el team leader o tutor.

## Introducción

En esta oportunidad vamos a desarrollar una aplicación mobile UdeSA-X, una red social tipo microblogging inspirada en X, ex Twitter, que permite a los estudiantes de la Universidad publicar mensajes cortos, interactuar con publicaciones de otros usuarios y mantenerse informados en tiempo real.

Adicionalmente, se requiere una segunda aplicación web que funcione como backoffice, destinada exclusivamente para administradores. Su objetivo será monitorear el funcionamiento de la aplicación principal, detectar posibles fallas, identificar anomalías y garantizar la correcta operación del sistema.

Para llevar adelante el desarrollo, el team leader definió un conjunto de requisitos funcionales y no funcionales que debemos considerar desde el inicio del proyecto.

Las historias de usuario constituyen la base del alcance del sistema: a partir de ellas se desprenden las épicas, funcionalidades y casos de uso que deben implementarse. No obstante, se asume que el equipo cuenta con el criterio técnico y el sentido común necesarios para tomar decisiones de diseño e incorporar aquellos elementos que resulten evidentes o implícitos, aun cuando no estén explicitados de manera literal.

Cualquier decisión relevante, supuesto asumido o cambio respecto del alcance original deberá ser debidamente comunicado y consensuado con el team leader antes de su implementación.

## Requisitos

- La aplicación principal deberá ser exclusivamente mobile y estará orientada a los usuarios finales.
- El backoffice deberá implementarse como una aplicación web, de uso exclusivo para administradores.
- La solución deberá diseñarse bajo una arquitectura orientada a microservicios, garantizando desacoplamiento, escalabilidad y mantenibilidad.
- La aplicación debe contar con persistencia y el uso de, al menos, dos tipos de bases de datos.
- El backend no puede ser desarrollado en una única tecnología. Por ejemplo, no puede estar todo desarrollado en Python.
- La aplicación deberá estar desplegada en un entorno productivo en la nube.
- Cada microservicio deberá estar contenedorizado con Docker, asegurando portabilidad y consistencia entre ambientes.
- Se deberán proteger los datos de los usuarios, cumpliendo con buenas prácticas de seguridad y tomando como referencia los lineamientos del OWASP Top 10.
- El desarrollo deberá seguir un enfoque iterativo e incremental. Se espera la adopción de metodologías ágiles y herramientas adecuadas para la planificación, seguimiento y gestión del trabajo.
- El equipo será responsable tanto de la documentación técnica y funcional como de asegurar la calidad y mantenibilidad del código.
- Se deberán implementar distintos niveles de testing para garantizar la robustez del sistema, incluyendo pruebas unitarias, de integración y pruebas de estrés con carga de datos en volumen, a fin de validar todos los flujos críticos de la aplicación.
- Todos los servicios backend deberán incluir tests de integración, validando la correcta interacción entre componentes y dependencias externas.
- Cada microservicio, incluyendo el frontend, deberá contar con una cobertura mínima del 85% de tests unitarios. Estos tests deberán ejecutarse automáticamente como parte del pipeline de Integración Continua (CI).
- Se deberá implementar un pipeline de Continuous Deployment (CD) utilizando GitHub Actions, automatizando el proceso de build, test y despliegue.
- La aplicación deberá contar con capacidades de observabilidad y monitoreo, permitiendo recolectar métricas, logs y trazas para detectar incidentes y analizar el comportamiento del sistema. Se debe asegurar que el tutor del grupo pueda acceder a la plataforma utilizada por el equipo.
- Al menos uno de los microservicios deberá implementar un mecanismo de Rate Limiting, con el objetivo de controlar el tráfico y proteger el sistema ante abusos o picos de carga.
- Se deberá implementar al menos una cola para comunicar dos microservicios de forma asincrónica.
- La aplicación y el backoffice deberán ofrecer una buena experiencia de usuario mediante diseños claros e intuitivos. La usabilidad, la navegabilidad y la consistencia visual son componentes esenciales del entregable.

## Inteligencia Artificial

A partir de la segunda mitad del semestre, el proyecto evolucionará con la incorporación de Historias de Usuario enfocadas en la integración de Inteligencia Artificial. Estas propuestas surgirán de la colaboración entre alumnos y tutores durante las reuniones semanales.

Cada grupo deberá implementar, al menos, una funcionalidad que integre IA, y deberá ser acordada con el tutor.

## Condición de aprobación

- Cumplir con todos los requisitos mencionados anteriormente.
- Realizar el total de las historias de usuario obligatorias, incluyendo todos sus criterios de aceptación.
- Implementar un total de 15 puntos de historias optativas por cada integrante del grupo, incluyendo todos sus criterios de aceptación.
- Proponer e implementar, al menos, una funcionalidad que utilice Inteligencia Artificial.

## Contrato moral

La realización de este proyecto se basa en el compromiso mutuo de honestidad académica. Se espera que cada estudiante sea el autor genuino de sus producciones, utilizando los recursos tecnológicos y las IAs de manera ética, como apoyo para la investigación y el enriquecimiento del contenido, y nunca como sustituto del esfuerzo intelectual propio.

Cada estudiante deberá ser responsable de la funcionalidad desarrollada y deberá ser capaz de explicar su funcionamiento y justificar las decisiones de diseño tomadas.

## Nota sobre las épicas

Las épicas tienen únicamente el objetivo de hacer más sencillo el seguimiento del enunciado y no tienen por qué ser vistas como parte del diseño del proyecto o de los microservicios.

# Épicas

Las historias se diferencian en obligatorias y optativas.

## E.1 Usuarios

### E1-H1. Registro de Usuarios - Obligatoria - 3 puntos

**COMO** usuario nuevo **QUIERO** registrarme con mis datos personales y validar mi cuenta mediante un token de correo electrónico **PARA** asegurar la autenticidad de mi perfil y acceder de forma segura al sistema.

#### Criterios de aceptación

- CA.1: Un usuario no debe poder entrar al sistema si su cuenta no fue validada por el token enviado al email.
- CA.2: El sistema debe validar que el formato del email sea correcto y no debe permitir correos duplicados.
- CA.3: El nombre de usuario, handle, debe ser único, comenzar con `@` y contener entre 4 y 15 caracteres, usando solamente letras, números y guiones bajos.
- CA.4: La contraseña debe tener al menos 8 caracteres, una mayúscula y un número, y guardarse encriptada.
- CA.5: El sistema debe validar que no se envíen campos obligatorios vacíos o nulos desde el cliente.
- CA.6: El token o link de validación enviado al correo debe tener un tiempo de expiración, por ejemplo, 24 horas. Si expira, el usuario debe poder solicitar un reenvío desde la pantalla de login.
- CA.7: La validación de unicidad del email debe ser case-insensitive. Por ejemplo, `Alumno@udesa.edu.ar` debe considerarse igual que `alumno@udesa.edu.ar`.

### E1-H2. Inicio de Sesión - Obligatoria - 3 puntos

**COMO** usuario registrado **QUIERO** ingresar mis credenciales, nombre de usuario o email y contraseña, **PARA** acceder a mi cuenta personal y utilizar las funcionalidades del sistema.

#### Criterios de aceptación

- CA.1: El sistema debe proveer un token JWT con un tiempo de expiración definido al iniciar sesión correctamente.
- CA.2: Si el usuario falla la contraseña 5 veces consecutivas, la cuenta debe bloquearse temporalmente por 15 minutos.
- CA.3: Si el usuario o la contraseña son incorrectos, el mensaje de error debe ser genérico, por ejemplo, `Credenciales inválidas`, para evitar enumeración de usuarios.
- CA.4: Si el usuario ingresa credenciales correctas pero su cuenta no está validada, el sistema debe denegar el acceso y mostrar un mensaje invitándolo a revisar su casilla de correo.
- CA.5: El sistema debe impedir el login y mostrar un mensaje de `Cuenta suspendida` si el usuario fue bloqueado por un administrador o si eliminó su cuenta mediante soft-delete.

### E1-H3. Cierre de Sesión - Obligatoria - 1 punto

**COMO** usuario registrado **QUIERO** cerrar mi sesión y que el token de acceso sea invalidado **PARA** garantizar que nadie más use la app desde mi dispositivo.

#### Criterios de aceptación

- CA.1: El token de sesión activo debe ser revocado en el backend.
- CA.2: En la app mobile se deben borrar de forma segura los datos relacionados a la sesión local y el JWT del usuario.

### E1-H4. Eliminación de Cuenta - Obligatoria - 3 puntos

**COMO** usuario registrado **QUIERO** poder eliminar mi cuenta permanentemente **PARA** que se borre toda mi información, incluyendo perfil, publicaciones, seguidores e historial de actividad.

#### Criterios de aceptación

- CA.1: Se debe implementar un soft-delete en la base de datos manteniendo la integridad referencial, pero el usuario no debe poder volver a loguearse.
- CA.2: Todas las relaciones de seguimiento del usuario eliminado deben eliminarse automáticamente y desaparecer de las listas de sus seguidores y seguidos.
- CA.3: Para confirmar la eliminación definitiva, la app mobile debe requerir que el usuario reingrese su contraseña actual.
- CA.4: Todos los posts del usuario eliminado deben dejar de mostrarse en el feed y timeline de los demás usuarios de forma inmediata.
- CA.5: Las respuestas y retweets del usuario eliminado deben mostrar un estado `[Usuario eliminado]` para no romper los hilos de conversación existentes.

### E1-H5. Olvidé Mi Contraseña - Obligatoria - 3 puntos

**COMO** usuario registrado **QUIERO** solicitar el restablecimiento de mi contraseña ingresando mi email o nombre de usuario **PARA** recuperar el acceso a mi cuenta en caso de olvido.

#### Criterios de aceptación

- CA.1: El usuario debe recibir un link con una duración máxima de 10 minutos.
- CA.2: Si el link expira, la interfaz debe mostrar un error claro y dar la opción de enviar uno nuevo.
- CA.3: Al ingresar la nueva contraseña, esta debe validarse mediante confirmación doble y cumplir con las mismas políticas de seguridad de E1-H1.
- CA.4: Al solicitar el restablecimiento, el mensaje devuelto debe ser siempre genérico, sin revelar si la cuenta realmente está registrada, para evitar ataques de enumeración de usuarios.
- CA.5: El link debe ser de un solo uso. Una vez utilizado con éxito para cambiar la contraseña, debe ser invalidado.
- CA.6: La nueva contraseña ingresada por el usuario no debe ser igual a su contraseña actual.
- CA.7: Al cambiar la contraseña con éxito, el sistema debe revocar automáticamente todos los tokens de sesión JWT activos y forzar un nuevo inicio de sesión.
- CA.8: Se debe limitar la cantidad de veces que se puede pedir un token de recuperación para un mismo correo.

### E1-H6. Editar mi perfil - Obligatoria - 2 puntos

**COMO** usuario registrado **QUIERO** editar los campos de datos de mi perfil **PARA** mantener mi información actualizada.

#### Criterios de aceptación

- CA.1: El sistema debe validar que los campos de texto no superen los caracteres máximos permitidos, por ejemplo, una biografía de 160 caracteres como máximo.
- CA.2: No se puede cambiar el email.
- CA.3: El usuario debe poder establecer una biografía y un Display Name, nombre visible.
- CA.4: El backend debe sanitizar estrictamente los campos de texto eliminando o escapando etiquetas HTML y scripts para prevenir ataques de inyección.
- CA.5: El nombre de usuario es obligatorio y no puede quedar vacío ni contener únicamente espacios en blanco.
- CA.6: Al guardar los cambios exitosamente, la aplicación mobile debe actualizar el estado global y reflejar inmediatamente los nuevos datos en la pantalla.

### E1-H7. Preferencias - Optativa - 2 puntos

**COMO** usuario registrado **QUIERO** configurar mis preferencias **PARA** que la aplicación se adapte a mis necesidades de privacidad y personalización.

#### Criterios de aceptación

- CA.1: El usuario debe poder configurar la visibilidad de su perfil: `Público`, donde cualquiera ve sus posts, o `Protegido`, donde sólo seguidores aprobados pueden verlos.
- CA.2: El usuario debe poder elegir el idioma preferido para el contenido del feed, por ejemplo, Español, Inglés o Todos.
- CA.3: El backend debe rechazar cualquier intento de guardar configuraciones con valores fuera de los permitidos o con formatos inválidos.
- CA.4: El backend sólo debe aceptar los valores exactos definidos para cada preferencia. Los valores no válidos enviados directamente mediante la API deben ser rechazados.
- CA.5: Al crearse una cuenta nueva durante el registro, el sistema debe asignar automáticamente preferencias por defecto.

### E1-H8. Foto de Perfil - Optativa - 3 puntos

**COMO** usuario registrado **QUIERO** subir y actualizar una foto de perfil y una imagen de portada **PARA** personalizar mi cuenta y que otros usuarios puedan reconocerme visualmente.

#### Criterios de aceptación

- CA.1: El sistema sólo debe aceptar formatos válidos de imagen, JPG y PNG.
- CA.2: La imagen de perfil no debe superar los 5 MB y la de portada no debe superar los 10 MB.
- CA.3: El backend debe validar el contenido real del archivo inspeccionando el MIME type o magic numbers, y no confiar únicamente en la extensión.
- CA.4: Al actualizar la foto de perfil o portada, el backend debe eliminar el archivo anterior del storage.
- CA.5: Si el usuario es nuevo, no subió ninguna foto o decide eliminar la actual, el sistema debe proveer y renderizar un avatar por defecto, tanto en la vista de perfil como en los posts.
- CA.6: El usuario debe contar con un botón explícito de `Eliminar foto actual`, que debe ejecutar la eliminación y devolver el perfil al estado de avatar por defecto.
- CA.7: El backend debe procesar la subida mediante streams directamente hacia el storage. El archivo completo no debe cargarse en la memoria del servidor.

### E1-H9. Social Login - Optativa - 5 puntos

**COMO** usuario nuevo o registrado **QUIERO** iniciar sesión utilizando mi cuenta de Google o Apple **PARA** acceder más rápido sin tener que recordar una nueva contraseña.

#### Criterios de aceptación

- CA.1: Si el email de Google o Apple no existe, se debe crear la cuenta y autocompletar el nombre.
- CA.2: Si el email ya existe, se debe vincular el método de inicio de sesión a la cuenta existente.
- CA.3: La validación final del inicio de sesión debe hacerse siempre en el backend. El servidor debe recibir el ID Token emitido por Google o Apple desde la app mobile y verificar su firma y validez con los servidores del proveedor antes de emitir el JWT propio.
- CA.4: Si una cuenta fue creada exclusivamente mediante Social Login y el usuario intenta usar Olvidé mi Contraseña o loguearse con email y contraseña estándar, el sistema debe indicar que la cuenta está vinculada a un proveedor social.

### E1-H10. Tema de la Aplicación - Optativa - 1 punto

**COMO** usuario registrado **QUIERO** poder alternar entre un tema Claro y un tema Oscuro **PARA** que la interfaz sea más cómoda según la iluminación del entorno.

#### Criterios de aceptación

- CA.1: Esta preferencia debe guardarse únicamente de forma local en el dispositivo.
- CA.2: La aplicación debe cambiar los colores de fondo y texto de forma inmediata al seleccionar la opción, sin reiniciar la app.

### E1-H11. Enviar Feedback o Reportar Error - Optativa - 3 puntos

**COMO** usuario registrado **QUIERO** un formulario simple dentro de Configuración para enviar comentarios o reportar un bug **PARA** ayudar a mejorar la aplicación si algo falla.

#### Criterios de aceptación

- CA.1: El formulario debe incluir un campo de texto libre de 500 caracteres como máximo.
- CA.2: El envío debe generar un registro y enviar un email a la cuenta de soporte del equipo.
- CA.3: La aplicación mobile debe adjuntar automáticamente y de forma oculta la metadata del dispositivo: sistema operativo, versión de la app e ID del usuario.
- CA.4: El endpoint debe estar protegido por un Rate Limit estricto, por ejemplo, máximo 2 envíos por usuario por hora.
- CA.5: Frontend y backend no deben permitir formularios cuyo texto esté vacío o contenga únicamente espacios en blanco.

### E1-H12. Aceptación de Términos y Política de Privacidad - Obligatoria - 1 punto

**COMO** usuario nuevo **QUIERO** leer y aceptar los Términos y Condiciones y la Política de Privacidad antes de registrarme **PARA** saber legalmente cómo se utilizarán y almacenarán mis datos personales y publicaciones.

#### Criterios de aceptación

- CA.1: El formulario de registro debe incluir un checkbox obligatorio con enlaces a textos estáticos de Términos y Privacidad. Si no está marcado, el botón de registro debe estar deshabilitado.
- CA.2: El backend debe guardar un registro, con booleano y timestamp, indicando cuándo el usuario aceptó estas políticas.

### E1-H13. Cambiar Contraseña - Optativa - 3 puntos

**COMO** usuario registrado y logueado **QUIERO** poder cambiar mi contraseña desde la pantalla de configuración ingresando mi clave actual **PARA** mantener mi cuenta segura de forma proactiva sin usar el flujo de recuperación por email.

#### Criterios de aceptación

- CA.1: El formulario debe solicitar Contraseña actual, Nueva contraseña y Confirmar nueva contraseña.
- CA.2: El backend debe validar que la nueva contraseña cumpla con los requisitos de seguridad de E1-H1 y no sea igual a la anterior.
- CA.3: Al cambiar la contraseña exitosamente, el sistema debe invalidar o revocar todos los JWT activos, incluyendo la sesión actual, y redirigir la app mobile a Inicio de Sesión.
- CA.4: El backend debe validar que la Contraseña actual sea correcta. Si el usuario falla 3 veces consecutivas, la cuenta debe bloquearse temporalmente por 15 minutos, reutilizando la lógica de E1-H2.
- CA.5: El sistema debe enviar un correo automático notificando que la contraseña fue modificada.

### E1-H14. Onboarding Inicial - Optativa - 3 puntos

**COMO** usuario que acaba de registrarse **QUIERO** ver pantallas explicativas sobre cómo funciona la aplicación y seleccionar mis intereses iniciales **PARA** personalizar mi experiencia desde el primer momento y seguir cuentas relevantes.

#### Criterios de aceptación

- CA.1: El usuario debe visualizar un carrusel explicativo con las funcionalidades principales antes de acceder al feed por primera vez.
- CA.2: El sistema debe presentar categorías de interés, por ejemplo Deportes, Tecnología, Política o Música, para seleccionar al menos 3.
- CA.3: El onboarding debe sugerir al menos 5 cuentas populares para seguir y el usuario debe poder seleccionar cuáles seguir con un solo tap.

## E.2 Publicaciones

### E2-H1. Crear Post - Obligatoria - 3 puntos

**COMO** usuario del sistema **QUIERO** escribir y publicar un mensaje corto, post o tweet, **PARA** compartir mis pensamientos con la comunidad.

#### Criterios de aceptación

- CA.1: El texto del post no debe superar los 280 caracteres.
- CA.2: El sistema debe validar que el texto no esté vacío ni contenga únicamente espacios en blanco.
- CA.3: El backend debe sanitizar el contenido eliminando o escapando etiquetas HTML y scripts para prevenir XSS.
- CA.4: El post debe almacenarse con ID del autor, contenido, timestamp de creación y contadores de likes, retweets y respuestas inicializados en 0.
- CA.5: Para evitar spam, un usuario no puede publicar más de 30 posts por hora.

### E2-H2. Feed Principal - Obligatoria - 3 puntos

**COMO** usuario del sistema **QUIERO** visualizar un feed con las publicaciones de los usuarios que sigo, ordenadas cronológicamente **PARA** mantenerme informado de la actividad de mi red.

#### Criterios de aceptación

- CA.1: El feed debe mostrar los posts ordenados del más reciente al más antiguo.
- CA.2: El feed debe implementar scroll infinito, cargando posts en páginas de 20 elementos.
- CA.3: Cada post debe incluir avatar y nombre del autor, handle, contenido, timestamp relativo y contadores de likes, retweets y respuestas.
- CA.4: Si el feed está vacío, debe mostrar un Empty State amigable con sugerencias de cuentas populares.
- CA.5: El sistema debe impedir que un usuario consulte por API los posts de una cuenta protegida a la que no sigue.

### E2-H3. Eliminar Post - Obligatoria - 2 puntos

**COMO** usuario del sistema **QUIERO** eliminar un post que publiqué **PARA** remover contenido que ya no deseo que sea público.

#### Criterios de aceptación

- CA.1: Sólo el autor del post debe poder eliminarlo.
- CA.2: El sistema debe pedir una confirmación antes de eliminarlo.
- CA.3: Al eliminarse un post, los retweets asociados deben invalidarse automáticamente y desaparecer de los feeds.
- CA.4: Si el post tenía respuestas, las respuestas deben mantenerse y el post original debe mostrarse como `[Post eliminado]`.

### E2-H4. Responder a un Post - Obligatoria - 2 puntos

**COMO** usuario del sistema **QUIERO** responder a un post de otro usuario **PARA** participar en conversaciones y debates.

#### Criterios de aceptación

- CA.1: La respuesta debe vincularse al post original formando un hilo visible.
- CA.2: Las respuestas deben cumplir las mismas validaciones que un post regular.
- CA.3: No se puede responder a un post de un usuario que tiene bloqueado al emisor. El backend debe devolver un mensaje genérico.
- CA.4: Las respuestas deben mostrarse debajo del post ordenadas cronológicamente y paginadas de a 20.

### E2-H5. Retweet / Repost - Obligatoria - 2 puntos

**COMO** usuario del sistema **QUIERO** compartir un post de otro usuario en mi propio perfil **PARA** amplificar contenido para mis seguidores.

#### Criterios de aceptación

- CA.1: El retweet debe aparecer en el feed de los seguidores indicando `Retweeteado por @usuario`.
- CA.2: Un usuario no puede retweetear el mismo post más de una vez. Si ya lo hizo, debe poder deshacerlo.
- CA.3: Al deshacer un retweet, la publicación debe desaparecer del perfil y decrementar el contador del post original.
- CA.4: No se puede retweetear un post de una cuenta protegida si no se la sigue.

### E2-H6. Like a un Post - Obligatoria - 2 puntos

**COMO** usuario del sistema **QUIERO** dar Me gusta a un post **PARA** expresar que me gustó el contenido.

#### Criterios de aceptación

- CA.1: Un usuario sólo puede dar un Me gusta por post. Al presionar nuevamente debe quitarlo.
- CA.2: El contador de likes debe actualizarse en tiempo real en la interfaz.
- CA.3: El backend debe garantizar que no existan likes duplicados para el mismo usuario y post, manteniendo idempotencia.

### E2-H7. Post con Imagen - Obligatoria - 5 puntos

**COMO** usuario del sistema **QUIERO** adjuntar una imagen a mi post **PARA** enriquecerlo con contenido visual.

#### Criterios de aceptación

- CA.1: Se aceptan hasta 4 imágenes por post en formatos JPG y PNG.
- CA.2: Cada imagen no debe superar 1 MB.
- CA.3: El backend debe validar el contenido real del archivo mediante MIME type o magic numbers.
- CA.4: Las imágenes deben renderizarse en un layout adaptativo: una imagen ocupa todo el ancho, dos se dividen en mitades y tres o cuatro forman una grilla 2x2.
- CA.5: Al tocar una imagen, debe abrirse un visor a pantalla completa con zoom y navegación entre las imágenes del post.

### E2-H8. Hashtags - Optativa - 3 puntos

**COMO** usuario del sistema **QUIERO** incluir hashtags en mis posts **PARA** categorizar mi contenido y hacerlo descubrible.

#### Criterios de aceptación

- CA.1: El sistema debe detectar palabras precedidas por `#` y almacenarlas como entidades asociadas al post.
- CA.2: Los hashtags deben renderizarse con estilo visual diferenciado y ser clickeables.
- CA.3: Al tocar un hashtag, el usuario debe ser redirigido a una búsqueda con todos los posts que lo contienen.
- CA.4: Un post no puede contener más de 10 hashtags. Si se excede, el backend debe rechazar la publicación.
- CA.5: Los hashtags deben ser case-insensitive.

### E2-H9. Menciones a Usuarios - Optativa - 3 puntos

**COMO** usuario del sistema **QUIERO** mencionar usuarios en mis posts usando su handle **PARA** referirlos directamente y notificarlos.

#### Criterios de aceptación

- CA.1: El sistema debe detectar palabras precedidas por `@` y renderizarlas como links al perfil mencionado.
- CA.2: Si el handle no existe, debe renderizarse como texto plano sin link.
- CA.3: El usuario mencionado debe recibir una notificación in-app y push si tiene notificaciones habilitadas.

### E2-H10. Búsqueda de Posts y Usuarios - Obligatoria - 5 puntos

**COMO** usuario del sistema **QUIERO** buscar posts por texto, hashtags o buscar usuarios por nombre o handle **PARA** descubrir contenido y cuentas relevantes.

#### Criterios de aceptación

- CA.1: La búsqueda debe soportar coincidencias parciales y ser case-insensitive.
- CA.2: Los resultados deben separarse en dos tabs: Posts y Usuarios.
- CA.3: Los resultados de posts deben mostrar un snippet con el término buscado resaltado.
- CA.4: Los resultados deben implementar paginación con scroll infinito, 20 resultados por página.
- CA.5: Los posts de cuentas protegidas no deben aparecer para usuarios que no siguen esas cuentas.

### E2-H11. Trending Topics - Optativa - 3 puntos

**COMO** usuario del sistema **QUIERO** ver los hashtags más utilizados en las últimas horas **PARA** estar al tanto de los temas populares.

#### Criterios de aceptación

- CA.1: Se deben calcular basándose en la cantidad de posts con un hashtag en las últimas 24 horas.
- CA.2: Se deben mostrar los 10 hashtags más populares junto con la cantidad de posts asociados.
- CA.3: Deben actualizarse periódicamente, cada 15 minutos como mínimo.

### E2-H12. Guardar Posts - Optativa - 3 puntos

**COMO** usuario del sistema **QUIERO** guardar posts en una lista de favoritos privada **PARA** releerlos más tarde sin buscarlos nuevamente.

#### Criterios de aceptación

- CA.1: El usuario debe poder guardar y quitar posts con un solo tap.
- CA.2: La lista debe ser completamente privada.
- CA.3: La lista debe ordenarse por fecha de guardado, de más reciente a más antigua, con paginación.

### E2-H13. Citar Post - Optativa - 5 puntos

**COMO** usuario del sistema **QUIERO** compartir un post agregándole mi propio comentario **PARA** añadir contexto u opinión.

#### Criterios de aceptación

- CA.1: El Quote Tweet debe mostrar el post original embebido dentro del nuevo post.
- CA.2: El comentario debe cumplir las validaciones de un post regular y el límite de 280 caracteres.
- CA.3: El post citado debe incrementar un contador de citas visible.
- CA.4: Si el post original es eliminado, el Quote Tweet debe seguir existiendo mostrando `[Post original eliminado]`.

### E2-H14. Visualización de Perfil de Usuario - Obligatoria - 3 puntos

**COMO** usuario del sistema **QUIERO** entrar al perfil de otro usuario para ver su biografía, foto e historial de publicaciones **PARA** conocer su actividad y decidir si quiero seguirlo.

#### Criterios de aceptación

- CA.1: El perfil debe mostrar foto de perfil, foto de portada, Display Name, handle, biografía, fecha de registro, cantidad de seguidores y seguidos.
- CA.2: Debe mostrar un tab con los posts del usuario, incluidos retweets, ordenados cronológicamente y paginados.
- CA.3: Si la cuenta es protegida y el usuario no la sigue, los posts no deben mostrarse y debe aparecer un mensaje indicando que la cuenta es privada.
- CA.4: El endpoint sólo debe devolver los últimos 20 posts por página.

### E2-H15. Post con Video - Optativa - 5 puntos

**COMO** usuario del sistema **QUIERO** adjuntar un video a mi post **PARA** enriquecer mi publicación con contenido visual.

#### Criterios de aceptación

- CA.1: El video no debe superar los 140 segundos.
- CA.2: El video no debe superar los 512 MB.
- CA.3: El backend sólo debe permitir formato MP4.
- CA.4: Sólo se puede adjuntar un video por post.
- CA.5: El backend no permite fotos y videos dentro de un mismo post.

## E.3 Interacciones Sociales

### E3-H1. Seguir a un Usuario - Obligatoria - 5 puntos

**COMO** usuario del sistema **QUIERO** seguir a otro usuario **PARA** que sus publicaciones aparezcan en mi feed y estar al tanto de su actividad.

#### Criterios de aceptación

- CA.1: Si la cuenta destino es pública, la relación se establece inmediatamente.
- CA.2: Si la cuenta destino es protegida, la solicitud queda Pendiente hasta que el dueño la apruebe.
- CA.3: El sistema debe impedir seguirse a uno mismo.
- CA.4: El backend debe actualizar los contadores de seguidores y seguidos de forma consistente y atómica.
- CA.5: Un usuario no puede enviar más de 50 solicitudes de seguimiento por hora.

### E3-H2. Dejar de Seguir a un Usuario - Obligatoria - 2 puntos

**COMO** usuario del sistema **QUIERO** dejar de seguir a un usuario **PARA** que sus publicaciones dejen de aparecer en mi feed.

#### Criterios de aceptación

- CA.1: La acción debe ser inmediata y no requiere confirmación.
- CA.2: El cambio debe reflejarse inmediatamente en los contadores.
- CA.3: Los posts del usuario dejado de seguir deben desaparecer del feed en la siguiente carga o refresh.

### E3-H3. Listado de Seguidores y Seguidos - Obligatoria - 3 puntos

**COMO** usuario del sistema **QUIERO** ver la lista de mis seguidores y de las cuentas que sigo **PARA** administrar mi red de contactos.

#### Criterios de aceptación

- CA.1: Ambas listas deben mostrar foto de perfil, Display Name, handle y botón Seguir o Siguiendo.
- CA.2: Las listas deben implementar scroll infinito si superan los 20 usuarios.
- CA.3: Si el usuario no tiene seguidores o no sigue a nadie, debe mostrarse un Empty State amigable.

### E3-H4. Bloquear Usuario - Obligatoria - 2 puntos

**COMO** usuario del sistema **QUIERO** bloquear a otro usuario **PARA** que no pueda ver mis posts, seguirme, enviarme mensajes ni interactuar conmigo.

#### Criterios de aceptación

- CA.1: El usuario bloqueado no recibe notificación del bloqueo.
- CA.2: El usuario que bloquea debe tener una sección para ver la lista de bloqueados y desbloquearlos.
- CA.3: Al bloquear, se deben eliminar automáticamente las relaciones de seguimiento en cualquier dirección.
- CA.4: El usuario bloqueado no debe poder ver el perfil del bloqueador. El backend debe devolver 404 ante acceso directo.
- CA.5: Los posts del bloqueador deben dejar de mostrarse en el feed y en los resultados de búsqueda del bloqueado, y viceversa.

### E3-H5. Denunciar Usuario - Obligatoria - 2 puntos

**COMO** usuario del sistema **QUIERO** poder reportar a un usuario o publicación por comportamiento indebido **PARA** mantener la seguridad y calidad de la comunidad.

#### Criterios de aceptación

- CA.1: Se debe poder elegir un motivo, por ejemplo Spam, Acoso, Contenido inapropiado o Suplantación de identidad, y enviar el reporte al backoffice.
- CA.2: Si un usuario recibe más de 5 reportes de cuentas distintas, su cuenta pasa temporalmente a estado En revisión.
- CA.3: No se puede reportar a la misma persona más de una vez en un lapso de 24 horas desde el mismo usuario.
- CA.4: Si se cumple la condición de reportes y la cuenta pasa a En revisión, el backend debe revocar inmediatamente todos los JWT activos del usuario.

### E3-H6. Mensajes Directos - Optativa - 8 puntos

**COMO** usuario del sistema **QUIERO** acceder a una sección de mensajería directa **PARA** conversar en privado con otros usuarios.

#### Criterios de aceptación

- CA.1: Sólo se pueden enviar mensajes si ambos usuarios se siguen mutuamente o si el receptor permite DMs de cualquiera.
- CA.2: Los mensajes deben guardarse en la base de datos para conservar el historial.
- CA.3: Si el receptor no está conectado, el backend debe guardar el mensaje y enviarlo como notificación push.
- CA.4: Al abrir un chat se deben cargar sólo los últimos 50 mensajes, con paginación hacia el historial anterior.

### E3-H7. Usuarios en Línea - Optativa - 3 puntos

**COMO** usuario del sistema **QUIERO** ver quiénes de las personas que sigo están conectadas **PARA** saber quién está activo en la plataforma.

#### Criterios de aceptación

- CA.1: Un usuario se considera en línea si interactuó con la app en los últimos 5 minutos.
- CA.2: Debe mostrarse un indicador visual en la foto de perfil del listado de DMs.
- CA.3: El usuario debe poder desactivar su indicador de presencia desde preferencias para aparecer siempre como desconectado.

### E3-H8. Listas Personalizadas - Optativa - 3 puntos

**COMO** usuario del sistema **QUIERO** crear listas personalizadas de usuarios **PARA** organizar un feed alternativo con publicaciones sólo de esos usuarios.

#### Criterios de aceptación

- CA.1: Un usuario puede pertenecer a más de una lista.
- CA.2: El usuario debe poder acceder a un feed filtrado exclusivamente por los miembros de una lista.
- CA.3: Si el usuario deja de seguir o bloquea a alguien de una lista, el backend debe quitarlo automáticamente.
- CA.4: Si se elimina una lista, los posts de esos usuarios deben seguir apareciendo en el feed principal.

### E3-H9. Invitar Usuarios Externos - Optativa - 2 puntos

**COMO** usuario del sistema **QUIERO** enviar una invitación por email o link a externos **PARA** que se sumen a la plataforma.

#### Criterios de aceptación

- CA.1: El link generado debe incluir un parámetro de referido para asociar al usuario nuevo con quien lo invitó.
- CA.2: Si el invitado se registra mediante el link, se debe generar automáticamente una relación de seguimiento hacia quien lo invitó.
- CA.3: Un usuario no puede generar más de 10 links de invitación únicos por día.

### E3-H10. Silenciar Usuario - Optativa - 5 puntos

**COMO** usuario del sistema **QUIERO** silenciar a un usuario sin dejar de seguirlo **PARA** que sus posts no aparezcan en mi feed principal sin romper la relación de seguimiento.

#### Criterios de aceptación

- CA.1: El usuario silenciado no recibe notificación de que fue silenciado.
- CA.2: Sus posts deben ocultarse del feed principal, pero seguir accesibles desde su perfil.
- CA.3: El usuario debe tener una sección para ver la lista de silenciados y desilenciarlos.
- CA.4: Se deben dejar de enviar notificaciones push sobre actividad del usuario silenciado.
- CA.5: Los retweets del usuario silenciado también deben ocultarse del feed.

## E.4 Notificaciones

### E4-H1. Recibir notificaciones de nuevo seguidor - Obligatoria - 2 puntos

**COMO** usuario del sistema **QUIERO** recibir una notificación push cuando alguien me empiece a seguir **PARA** saber quién se interesa en mi contenido.

#### Criterios de aceptación

- CA.1: El servicio de notificaciones debe usar FCM para entregar notificaciones push.
- CA.2: Al tocar la notificación, la app debe abrirse directamente en el perfil del nuevo seguidor.
- CA.3: El backend debe almacenar y actualizar el Device Token de FCM cada vez que el usuario inicia sesión.
- CA.4: Si Firebase informa que un token no es válido, el backend debe eliminarlo de la base de datos.

### E4-H2. Notificación de interacción - Obligatoria - 2 puntos

**COMO** usuario del sistema **QUIERO** recibir una notificación cuando alguien da Like, Retweet, Respuesta o Cita a uno de mis posts **PARA** estar al tanto de la actividad sobre mi contenido.

#### Criterios de aceptación

- CA.1: El mensaje debe incluir el tipo de interacción y el nombre de usuario que la realizó.
- CA.2: Al tocar la notificación push con la app cerrada o en segundo plano, se debe abrir la app y redirigir al post correspondiente.

### E4-H3. Centro de Notificaciones In-App - Obligatoria - 3 puntos

**COMO** usuario del sistema **QUIERO** tener un panel interno con el historial de notificaciones **PARA** revisar alertas descartadas en el celular.

#### Criterios de aceptación

- CA.1: Las notificaciones no leídas deben tener un indicador visual distinto.
- CA.2: El usuario debe poder marcar todas como leídas con un botón.
- CA.3: El backend debe devolver un máximo de 20 notificaciones por página, ordenadas de más reciente a más antigua.
- CA.4: El usuario debe poder borrar una notificación mediante swipe o un ícono de tacho.
- CA.5: La notificación debe eliminarse lógicamente en la base de datos.

### E4-H4. Notificación de mención - Optativa - 5 puntos

**COMO** usuario del sistema **QUIERO** recibir una alerta push cuando otro usuario me mencione usando mi handle **PARA** ver el contexto y responder rápidamente.

#### Criterios de aceptación

- CA.1: La notificación debe incluir un preview del texto del post de hasta 100 caracteres.
- CA.2: Si el usuario mencionado tiene silenciado al autor, la notificación no debe enviarse.
- CA.3: No se debe volver a notificar por menciones del mismo autor en el mismo hilo.

### E4-H5. Configurar Preferencias de Notificación - Optativa - 3 puntos

**COMO** usuario del sistema **QUIERO** configurar qué tipos de notificaciones quiero recibir **PARA** evitar notificaciones que no me interesan.

#### Criterios de aceptación

- CA.1: Debe existir un toggle individual para Likes, Retweets, Respuestas, Menciones, Nuevos seguidores y Mensajes directos.
- CA.2: Se debe consultar obligatoriamente la tabla de preferencias antes de enviar el push.

## E.5 Administradores, Backoffice Web

### E5-H1. Creación de Administradores - Obligatoria - 5 puntos

**COMO** administrador principal, SuperAdmin, **QUIERO** poder crear credenciales para el backoffice **PARA** delegar tareas de soporte y moderación.

#### Criterios de aceptación

- CA.1: Las contraseñas de administradores deben crearse desde el panel, pero el nuevo administrador debe ser forzado a cambiarla en su primer login.
- CA.2: Debe existir control de roles SuperAdmin y Moderador. El Moderador no puede crear otros administradores.
- CA.3: La contraseña temporal debe expirar en 24 horas. Si el nuevo administrador no inicia sesión en ese lapso, el SuperAdmin debe generar una nueva.
- CA.4: El sistema debe validar que el correo pertenezca a un dominio autorizado si se define una restricción institucional.

### E5-H2. Inicio de Sesión como Administrador - Obligatoria - 2 puntos

**COMO** administrador del sistema **QUIERO** iniciar sesión en el portal web del backoffice con email y contraseña **PARA** acceder a herramientas de gestión y moderación.

#### Criterios de aceptación

- CA.1: El JWT debe contener el rol del usuario para que el frontend muestre u oculte pantallas según permisos.
- CA.2: Un usuario regular de la app mobile no debe poder iniciar sesión en el backoffice. El backend debe devolver 403 Forbidden.
- CA.3: El login del backoffice debe bloquearse por 30 minutos tras 3 intentos fallidos consecutivos.

### E5-H3. Visualización de Métricas - Optativa - 5 puntos

**COMO** administrador del sistema **QUIERO** visualizar un dashboard con métricas clave **PARA** monitorear la salud y crecimiento de la plataforma.

#### Criterios de aceptación

- CA.1: El dashboard debe actualizarse en tiempo real o permitir refresco manual.
- CA.2: Debe mostrar un gráfico de barras o líneas con los registros de la última semana.

### E5-H4. Buscador y Detalles de Usuarios - Obligatoria - 3 puntos

**COMO** administrador del sistema **QUIERO** buscar usuarios por email o handle y ver el detalle de su perfil **PARA** dar soporte o auditar cuentas.

#### Criterios de aceptación

- CA.1: El detalle debe mostrar estado, fecha de registro, cantidad de seguidores y cantidad de posts.
- CA.2: La búsqueda debe soportar coincidencias parciales.
- CA.3: Debe implementar paginación.

### E5-H5. Bloqueo de Usuarios por Admin - Obligatoria - 2 puntos

**COMO** administrador del sistema **QUIERO** cambiar el estado de un usuario a Bloqueado **PARA** sancionar a quienes incumplan los términos.

#### Criterios de aceptación

- CA.1: El administrador debe ingresar obligatoriamente un motivo antes de ejecutar el bloqueo.
- CA.2: El usuario bloqueado debe perder el acceso mediante invalidación inmediata del token.

### E5-H6. Logs de Auditoría - Obligatoria - 3 puntos

**COMO** administrador del sistema **QUIERO** ver un registro de las acciones de otros administradores **PARA** tener control y trazabilidad.

#### Criterios de aceptación

- CA.1: Se debe registrar email del administrador, acción, entidad afectada y timestamp.
- CA.2: Los logs deben ser de sólo lectura y ningún administrador debe poder borrarlos.
- CA.3: Los registros deben mostrarse paginados y ordenados por fecha descendente.

### E5-H7. Gestión de Denuncias - Obligatoria - 3 puntos

**COMO** administrador del sistema **QUIERO** visualizar una lista de denuncias **PARA** revisar los casos y tomar acciones disciplinarias.

#### Criterios de aceptación

- CA.1: La lista debe ordenar reportes por severidad, según la cantidad de reportes recibidos por el mismo usuario.
- CA.2: El administrador debe tener acciones rápidas para Descartar denuncia o Suspender cuenta.
- CA.3: Debe existir una acción Resolver o Cerrar caso que cambie el estado a Resuelta y quite el reporte de la vista de pendientes.

### E5-H8. Exportar Datos - Optativa - 2 puntos

**COMO** administrador del sistema **QUIERO** descargar usuarios filtrados en formato CSV **PARA** hacer análisis en Excel u otras herramientas.

#### Criterios de aceptación

- CA.1: El CSV debe contener ID, Handle, Email, Estado y Fecha de Registro.
- CA.2: La funcionalidad debe estar restringida al rol SuperAdmin. Un Moderador debe recibir 403 Forbidden.

### E5-H9. Registro de Última Conexión - Optativa - 2 puntos

**COMO** administrador del sistema **QUIERO** ver la fecha y hora de la última conexión **PARA** identificar cuentas inactivas, abandonadas o bots.

#### Criterios de aceptación

- CA.1: Cada login exitoso debe actualizar `fecha_ultimo_login`.
- CA.2: Este dato debe mostrarse como columna obligatoria en el buscador de usuarios del panel.

### E5-H10. Borrado Forzado de Contenido - Optativa - 3 puntos

**COMO** administrador del sistema **QUIERO** borrar contenido de un post o la biografía de un usuario desde el panel web **PARA** eliminar rápidamente textos que incumplan las normas sin bloquear toda la cuenta.

#### Criterios de aceptación

- CA.1: Debe existir una acción llamada `Limpiar Contenido` al visualizar el detalle de un usuario o post.
- CA.2: Al ejecutar la acción, se deben sobrescribir inmediatamente los campos correspondientes con valores vacíos o con el placeholder `[Contenido eliminado por moderación]`.

### E5-H11. Estado de los Microservicios - Optativa - 5 puntos

**COMO** administrador del sistema **QUIERO** visualizar el estado En línea o Caído de cada microservicio **PARA** detectar fallas técnicas rápidamente.

#### Criterios de aceptación

- CA.1: El backoffice debe consumir el endpoint `/healthcheck` de cada microservicio.
- CA.2: Debe mostrar un indicador visual: verde para OK y rojo para Caído.
- CA.3: Si el endpoint tarda más de 5 segundos, el backoffice debe abortar la petición y marcar el servicio como Caído sin quedar bloqueado.
- CA.4: Si un servicio se cae, todos los administradores deben recibir una alerta por email.

### E5-H12. Gestión de Feedback/Reportes - Optativa - 3 puntos

**COMO** administrador del sistema **QUIERO** visualizar una bandeja con feedback y reportes de errores enviados desde la app mobile **PARA** identificar problemas técnicos y mejorar la plataforma.

#### Criterios de aceptación

- CA.1: La lista debe mostrar texto, ID o nombre de usuario, metadata del dispositivo y fecha de envío.
- CA.2: El administrador debe poder marcar mensajes como Leídos o Resueltos para quitarlos de la bandeja principal.
- CA.3: Si el usuario que envió el feedback es eliminado o bloqueado, el reporte debe conservarse en el backoffice.

# Puntos de historias de usuario

| Historia | Tipo | Puntos |
|---|---|---:|
| E.1 H1. Registro de Usuarios | Obligatoria | 3 |
| E.1 H2. Inicio de Sesión | Obligatoria | 3 |
| E.1 H3. Cierre de Sesión | Obligatoria | 1 |
| E.1 H4. Eliminación de Cuenta | Obligatoria | 3 |
| E.1 H5. Olvidé Mi Contraseña | Obligatoria | 3 |
| E.1 H6. Editar mi perfil | Obligatoria | 2 |
| E.1 H7. Preferencias | Optativa | 2 |
| E.1 H8. Foto de Perfil | Optativa | 3 |
| E.1 H9. Social Login | Optativa | 5 |
| E.1 H10. Tema de la Aplicación | Optativa | 1 |
| E.1 H11. Enviar Feedback o Reportar Error | Optativa | 3 |
| E.1 H12. Aceptación de Términos y Política de Privacidad | Obligatoria | 1 |
| E.1 H13. Cambiar Contraseña | Optativa | 3 |
| E.1 H14. Onboarding Inicial | Optativa | 3 |
| **Subtotal E.1** |  | **36** |
| E.2 H1. Crear Post | Obligatoria | 3 |
| E.2 H2. Feed Principal | Obligatoria | 3 |
| E.2 H3. Eliminar Post | Obligatoria | 2 |
| E.2 H4. Responder a un Post | Obligatoria | 2 |
| E.2 H5. Retweet / Repost | Obligatoria | 2 |
| E.2 H6. Like a un Post | Obligatoria | 2 |
| E.2 H7. Post con Imagen | Obligatoria | 5 |
| E.2 H8. Hashtags | Optativa | 3 |
| E.2 H9. Menciones a Usuarios | Optativa | 3 |
| E.2 H10. Búsqueda de Posts y Usuarios | Obligatoria | 5 |
| E.2 H11. Trending Topics | Optativa | 3 |
| E.2 H12. Guardar Posts | Optativa | 3 |
| E.2 H13. Citar Post | Optativa | 5 |
| E.2 H14. Visualización de Perfil de Usuario | Obligatoria | 3 |
| E.2 H15. Post con Video | Optativa | 5 |
| **Subtotal E.2** |  | **49** |
| E.3 H1. Seguir a un Usuario | Obligatoria | 5 |
| E.3 H2. Dejar de Seguir a un Usuario | Obligatoria | 2 |
| E.3 H3. Listado de Seguidores y Seguidos | Obligatoria | 3 |
| E.3 H4. Bloquear Usuario | Obligatoria | 2 |
| E.3 H5. Denunciar Usuario | Obligatoria | 2 |
| E.3 H6. Mensajes Directos | Optativa | 8 |
| E.3 H7. Usuarios en línea | Optativa | 3 |
| E.3 H8. Listas Personalizadas | Optativa | 3 |
| E.3 H9. Invitar Usuarios Externos | Optativa | 2 |
| E.3 H10. Silenciar Usuario | Optativa | 5 |
| **Subtotal E.3** |  | **35** |
| E.4 H1. Recibir notificaciones de nuevo seguidor | Obligatoria | 2 |
| E.4 H2. Notificación de interacción | Obligatoria | 2 |
| E.4 H3. Centro de Notificaciones In-App | Obligatoria | 3 |
| E.4 H4. Notificación de mención | Optativa | 5 |
| E.4 H5. Configurar Preferencias de Notificación | Optativa | 3 |
| **Subtotal E.4** |  | **15** |
| E.5 H1. Creación de Administradores | Obligatoria | 5 |
| E.5 H2. Inicio de sesión como Administrador | Obligatoria | 2 |
| E.5 H3. Visualización de Métricas | Optativa | 5 |
| E.5 H4. Buscador y Detalles de Usuarios | Obligatoria | 3 |
| E.5 H5. Bloqueo de Usuarios por Admin | Obligatoria | 2 |
| E.5 H6. Logs de Auditoría | Obligatoria | 3 |
| E.5 H7. Gestión de Denuncias | Obligatoria | 3 |
| E.5 H8. Exportar Datos | Optativa | 2 |
| E.5 H9. Registro de Última Conexión | Optativa | 2 |
| E.5 H10. Borrado Forzado de Contenido | Optativa | 3 |
| E.5 H11. Estado de los Microservicios | Optativa | 5 |
| E.5 H12. Gestión de Feedback/Reportes | Optativa | 3 |
| **Subtotal E.5** |  | **38** |
| **TOTAL** |  | **173** |
