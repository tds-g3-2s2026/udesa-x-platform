# Guía funcional de UdeSA-X

Qué puede hacer un usuario en la app y un administrador en el backoffice, historia por historia,
y qué pantalla cubre cada criterio de aceptación. Los criterios completos están en
[`CONSIGNA.md`](./CONSIGNA.md). Cómo está construido cada servicio está en
[`ARQUITECTURA.md`](./ARQUITECTURA.md).

## Cómo cargar una historia

Cada historia la carga o la revisa quien la hizo, porque es quien la puede explicar:

1. Completá una fila por criterio, mirando la pantalla real y no lo que decía la issue.
2. En "Pantalla", poné cómo se llega: `Perfil > Editar perfil`. Si el criterio no tiene pantalla,
   poné `Sin pantalla (backend)` y contá qué nota el usuario.
3. En "Qué ve el usuario", usá los textos que aparecen en la app y evitá los nombres de código.
4. Si algo no cumple el criterio o se resolvió distinto, decilo en esa fila.
5. Agregá arriba de la tabla una frase que diga qué permite la historia, y cambiá el estado en
   la tabla de seguimiento.

Si tu historia está en estado Borrador, ya tiene el texto armado a partir del código: revisalo,
corregí lo que haga falta y pasala a Cargada.

## Seguimiento

- **Cargada:** ya está en esta guía.
- **Borrador:** es de S2 a S9, está armada a partir del código y falta que la revise su dueño.
- **Se carga en S13:** es de S10 a S12.
- **Fuera de alcance:** optativa que el plan dejó afuera (`PLANIFICACION.md`).
- **Sin issue:** optativa del catálogo que todavía no tiene issue ni dueño.

| Historia | Tipo | Puntos | Sprint | Dueño | Estado |
|---|---|---:|---|---|---|
| E1-H1. Registro de Usuarios | Obligatoria | 3 | S2 | @tommycass | Borrador |
| E1-H2. Inicio de Sesión | Obligatoria | 3 | S2 | @tommycass | Borrador |
| E1-H3. Cierre de Sesión | Obligatoria | 1 | S2 | @FedeTrejo | Cargada |
| E1-H4. Eliminación de Cuenta | Obligatoria | 3 | S9 | @FedeTrejo | Cargada |
| E1-H5. Olvidé Mi Contraseña | Obligatoria | 3 | S3 | @FedeTrejo | Cargada |
| E1-H6. Editar mi perfil | Obligatoria | 2 | S3 | @FedeTrejo | Cargada |
| E1-H7. Preferencias | Optativa | 2 | S4 | @FedeTrejo | Cargada |
| E1-H8. Foto de Perfil | Optativa | 3 | S10 | @FedeTrejo | Se carga en S13 |
| E1-H9. Social Login | Optativa | 5 | - | - | Fuera de alcance |
| E1-H10. Tema de la Aplicación | Optativa | 1 | S4 | @FedeTrejo | Cargada |
| E1-H11. Enviar Feedback o Reportar Error | Optativa | 3 | S11 | @FedeTrejo | Se carga en S13 |
| E1-H12. Aceptación de Términos y Política de Privacidad | Obligatoria | 1 | S2 | @FedeTrejo | Cargada |
| E1-H13. Cambiar Contraseña | Optativa | 3 | S3 | @FedeTrejo | Cargada |
| E1-H14. Onboarding Inicial | Optativa | 3 | S12 | @FedeTrejo | Se carga en S13 |
| E2-H1. Crear Post | Obligatoria | 3 | S6 | @FedeTrejo | Cargada |
| E2-H2. Feed Principal | Obligatoria | 3 | S6 | @FedeTrejo | Cargada |
| E2-H3. Eliminar Post | Obligatoria | 2 | S8 | @varbelaiz | Borrador |
| E2-H4. Responder a un Post | Obligatoria | 2 | S8 | @FedeTrejo | Cargada |
| E2-H5. Retweet / Repost | Obligatoria | 2 | S8 | @varbelaiz | Borrador |
| E2-H6. Like a un Post | Obligatoria | 2 | S8 | @FedeTrejo | Cargada |
| E2-H7. Post con Imagen | Obligatoria | 5 | S9 | @FedeTrejo | Cargada |
| E2-H8. Hashtags | Optativa | 3 | S11 | @varbelaiz | Se carga en S13 |
| E2-H9. Menciones a Usuarios | Optativa | 3 | S12 | @jleonalderete | Se carga en S13 |
| E2-H10. Búsqueda de Posts y Usuarios | Obligatoria | 5 | S10 | @varbelaiz | Se carga en S13 |
| E2-H11. Trending Topics | Optativa | 3 | S12 | @varbelaiz | Se carga en S13 |
| E2-H12. Guardar Posts | Optativa | 3 | S12 | @varbelaiz | Se carga en S13 |
| E2-H13. Citar Post | Optativa | 5 | - | - | Sin issue |
| E2-H14. Visualización de Perfil de Usuario | Obligatoria | 3 | S9 | @tommycass | Borrador |
| E2-H15. Post con Video | Optativa | 5 | - | - | Fuera de alcance |
| E3-H1. Seguir a un Usuario | Obligatoria | 5 | S5 | @tommycass | Borrador |
| E3-H2. Dejar de Seguir a un Usuario | Obligatoria | 2 | S5 | @tommycass | Borrador |
| E3-H3. Listado de Seguidores y Seguidos | Obligatoria | 3 | S5 | @FedeTrejo | Cargada |
| E3-H4. Bloquear Usuario | Obligatoria | 2 | S6 | @tommycass | Borrador |
| E3-H5. Denunciar Usuario | Obligatoria | 2 | S6 | @jleonalderete | Borrador |
| E3-H6. Mensajes Directos | Optativa | 8 | - | - | Fuera de alcance |
| E3-H7. Usuarios en Línea | Optativa | 3 | - | - | Sin issue |
| E3-H8. Listas Personalizadas | Optativa | 3 | S12 | @tommycass | Se carga en S13 |
| E3-H9. Invitar Usuarios Externos | Optativa | 2 | S11 | @varbelaiz | Se carga en S13 |
| E3-H10. Silenciar Usuario | Optativa | 5 | S10 | @tommycass | Se carga en S13 |
| E4-H1. Recibir notificaciones de nuevo seguidor | Obligatoria | 2 | S10 | @jleonalderete | Se carga en S13 |
| E4-H2. Notificación de interacción | Obligatoria | 2 | S11 | @jleonalderete | Se carga en S13 |
| E4-H3. Centro de Notificaciones In-App | Obligatoria | 3 | S10 | @FedeTrejo | Se carga en S13 |
| E4-H4. Notificación de mención | Optativa | 5 | S12 | @jleonalderete | Se carga en S13 |
| E4-H5. Configurar Preferencias de Notificación | Optativa | 3 | S11 | @jleonalderete | Se carga en S13 |
| E5-H1. Creación de Administradores | Obligatoria | 5 | S4 | @jleonalderete | Borrador |
| E5-H2. Inicio de Sesión como Administrador | Obligatoria | 2 | S3 | @jleonalderete | Borrador |
| E5-H3. Visualización de Métricas | Optativa | 5 | S11 | @jleonalderete | Se carga en S13 |
| E5-H4. Buscador y Detalles de Usuarios | Obligatoria | 3 | S9 | @tommycass | Borrador |
| E5-H5. Bloqueo de Usuarios por Admin | Obligatoria | 2 | S9 | @tommycass | Borrador |
| E5-H6. Logs de Auditoría | Obligatoria | 3 | S10 | @varbelaiz | Se carga en S13 |
| E5-H7. Gestión de Denuncias | Obligatoria | 3 | S9 | @tommycass | Borrador |
| E5-H8. Exportar Datos | Optativa | 2 | S11 | @tommycass | Se carga en S13 |
| E5-H9. Registro de Última Conexión | Optativa | 2 | S11 | @tommycass | Se carga en S13 |
| E5-H10. Borrado Forzado de Contenido | Optativa | 3 | S12 | @tommycass | Se carga en S13 |
| E5-H11. Estado de los Microservicios | Optativa | 5 | S7 | @varbelaiz | Borrador |
| E5-H12. Gestión de Feedback/Reportes | Optativa | 3 | S12 | @FedeTrejo | Se carga en S13 |

## Mapa de pantallas

**App mobile.** Sin sesión están el inicio de sesión, el registro en tres pasos, la verificación del
correo, la recuperación de contraseña, y los textos de Términos y Privacidad. Con sesión, la barra
inferior tiene cuatro pestañas:

| Pestaña | Qué tiene |
|---|---|
| Inicio | El feed y el acceso para escribir un post nuevo |
| Buscar | Búsqueda de posts y de usuarios |
| Notificaciones | El centro de notificaciones |
| Perfil | Los datos de la cuenta, y los accesos a Editar perfil, Cambiar contraseña, Eliminar cuenta, Configuración, Seguidores, Siguiendo, Solicitudes pendientes, Tema oscuro y Cerrar Sesión |

**Backoffice web.**

| Ruta | Qué tiene |
|---|---|
| `/login` y `/change-password` | Inicio de sesión del administrador y cambio de contraseña |
| `/` | Métricas |
| `/health` | Estado de los servicios |
| `/moderation` | Bandeja de denuncias |
| `/users`, `/users/search` y `/users/:id` | Administradores, búsqueda de cuentas y detalle de una cuenta |
| `/audit` | Registro de auditoría |

## App: cuenta y perfil

### E1-H1. Registro de Usuarios

Obligatoria · 3 puntos · S2 · Dueño: @tommycass

Permite crear una cuenta en tres pasos y validarla con un link que llega por correo.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Inicio de sesión | Hasta tocar el link del correo no se puede entrar: aparece el aviso "Cuenta sin verificar". |
| CA.2 | Registro > ¿Cuál es tu correo? | Un correo mal escrito muestra "Ingresá un correo electrónico válido". Uno ya usado, "El email o el nombre de usuario ya están en uso". |
| CA.3 | Registro > Elegí tu usuario | El usuario empieza con `@` y lleva de 4 a 15 letras, números o guiones bajos. Si ya existe, muestra el mismo aviso de arriba. |
| CA.4 | Registro > Creá tu contraseña | Pide al menos 8 caracteres, una mayúscula y un número. Se guarda encriptada con Argon2. |
| CA.5 | Registro | Cada paso avisa si el campo quedó vacío. La API también lo rechaza. |
| CA.6 | Revisá tu correo; Inicio de sesión | El link dura 24 horas. Se puede pedir otro con "Reenviar link", o con "Reenviar el link" desde el aviso del inicio de sesión. |
| CA.7 | Sin pantalla (backend) | `Alumno@udesa.edu.ar` y `alumno@udesa.edu.ar` cuentan como el mismo correo. |

### E1-H2. Inicio de Sesión

Obligatoria · 3 puntos · S2 · Dueño: @tommycass

Permite entrar con usuario o email y contraseña.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Inicio de sesión | Al entrar, la app recibe un token que dura 15 minutos y otro que lo renueva durante 7 días, así la sesión sigue abierta. |
| CA.2 | Inicio de sesión | Con 5 contraseñas mal seguidas, avisa "La cuenta quedó bloqueada temporalmente por 15 minutos". |
| CA.3 | Inicio de sesión | Si falla el usuario o la contraseña, el mensaje es siempre "Credenciales inválidas". |
| CA.4 | Inicio de sesión | Con la contraseña correcta y la cuenta sin validar, aparece "Cuenta sin verificar" y ofrece "Reenviar el link". |
| CA.5 | Inicio de sesión | Una cuenta bloqueada o eliminada ve "Cuenta suspendida". |

### E1-H3. Cierre de Sesión

Obligatoria · 1 punto · S2 · Dueño: @FedeTrejo

Permite cerrar la sesión en el dispositivo y que el token deje de servir.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Perfil > Cerrar Sesión | La sesión se cierra también en el backend: ese token ya no sirve para hacer pedidos. |
| CA.2 | Perfil > Cerrar Sesión | La app borra los tokens y los datos de la sesión guardados en el dispositivo, y vuelve al inicio de sesión. |

### E1-H4. Eliminación de Cuenta

Obligatoria · 3 puntos · S9 · Dueño: @FedeTrejo

Permite borrar la cuenta para siempre, confirmando con la contraseña.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Inicio de sesión | La cuenta eliminada ya no puede volver a entrar. |
| CA.2 | Perfil > Seguidores / Siguiendo | La cuenta eliminada desaparece de las listas de seguidores y seguidos de los demás. |
| CA.3 | Perfil > Eliminar cuenta | Pide la "Contraseña actual" y confirma con el aviso "¿Eliminar la cuenta definitivamente?". |
| CA.4 | Inicio, perfiles | Los posts de esa cuenta dejan de aparecer para los demás. |
| CA.5 | Detalle de post | Las respuestas y retweets de esa cuenta siguen en el hilo, pero el autor aparece como `[Usuario eliminado]` y no abre ningún perfil. |

### E1-H5. Olvidé Mi Contraseña

Obligatoria · 3 puntos · S3 · Dueño: @FedeTrejo

Permite recuperar el acceso sin saber la contraseña, con un código que llega por correo. La consigna habla de un link: en la app el correo trae un código que se pega en la pantalla.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Inicio de sesión > ¿Olvidaste tu contraseña? | Se ingresa "Usuario o Email" y llega un código por correo, válido por 10 minutos. |
| CA.2 | Restablecer contraseña | Con un código vencido avisa que los códigos duran 10 minutos y ofrece "Pedir un código nuevo". |
| CA.3 | Restablecer contraseña | Pide "Contraseña nueva" y "Repetí la contraseña", con las mismas reglas que el registro. |
| CA.4 | ¿Olvidaste tu contraseña? | Siempre muestra "Revisá tu correo", exista o no la cuenta. |
| CA.5 | Restablecer contraseña | Un código ya usado se rechaza igual que uno vencido. |
| CA.6 | Restablecer contraseña | Rechaza una contraseña igual a la actual. |
| CA.7 | Restablecer contraseña | Al terminar se cierran todas las sesiones y la app lleva a "Iniciar Sesión". |
| CA.8 | ¿Olvidaste tu contraseña? | Con más de 3 pedidos en 60 minutos para el mismo usuario o email, avisa que hay que esperar. |

### E1-H6. Editar mi perfil

Obligatoria · 2 puntos · S3 · Dueño: @FedeTrejo

Permite cambiar el nombre visible y la biografía.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Perfil > Editar perfil | La biografía llega hasta 160 caracteres y el nombre visible hasta 50. |
| CA.2 | Perfil > Editar perfil | El email no aparece como campo editable. Si alguien lo manda directo a la API, se rechaza. |
| CA.3 | Perfil > Editar perfil | Campos "Nombre visible" y "Biografía". |
| CA.4 | Sin pantalla (backend) | Las etiquetas HTML y los scripts se limpian antes de guardar. |
| CA.5 | Perfil > Editar perfil | El nombre visible no puede quedar vacío ni tener solo espacios. |
| CA.6 | Perfil | Al guardar, los datos nuevos se ven enseguida, sin recargar. |

### E1-H7. Preferencias

Optativa · 2 puntos · S4 · Dueño: @FedeTrejo

Permite elegir quién ve el perfil y el idioma del feed.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Perfil > Configuración | Sección "Visibilidad del perfil", con "Público" y "Protegido". |
| CA.2 | Perfil > Configuración | Sección "Idioma del feed", con "Español", "Inglés" y "Todos". Por ahora solo se guarda: el feed todavía no filtra por idioma (`T-35`). |
| CA.3 | Sin pantalla (backend) | Un valor fuera de los permitidos o con mal formato se rechaza. |
| CA.4 | Sin pantalla (backend) | Solo se aceptan los valores exactos de cada preferencia, también por API directa. |
| CA.5 | Registro | Una cuenta nueva arranca como pública y con todos los idiomas, sin elegir nada. |

### E1-H8. Foto de Perfil

Optativa · 3 puntos · S10 · Dueño: @FedeTrejo

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |
| CA.4 |  |  |
| CA.5 |  |  |
| CA.6 |  |  |
| CA.7 |  |  |

### E1-H10. Tema de la Aplicación

Optativa · 1 punto · S4 · Dueño: @FedeTrejo

Permite alternar entre tema claro y oscuro.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Perfil > Tema oscuro | La elección se guarda solo en el dispositivo y no viaja a la API. |
| CA.2 | Perfil > Tema oscuro | Los colores cambian al instante, sin reiniciar la app. |

### E1-H11. Enviar Feedback o Reportar Error

Optativa · 3 puntos · S11 · Dueño: @FedeTrejo

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |
| CA.4 |  |  |
| CA.5 |  |  |

### E1-H12. Aceptación de Términos y Política de Privacidad

Obligatoria · 1 punto · S2 · Dueño: @FedeTrejo

Pide aceptar los Términos y la Política de Privacidad antes de crear la cuenta.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Registro, paso de la contraseña | Checkbox con enlaces a Términos y a Privacidad. Sin marcarlo, el botón queda deshabilitado. |
| CA.2 | Sin pantalla (backend) | La cuenta guarda que aceptó y cuándo. |

### E1-H13. Cambiar Contraseña

Optativa · 3 puntos · S3 · Dueño: @FedeTrejo

Permite cambiar la contraseña con la sesión iniciada, sabiendo la actual.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Perfil > Cambiar contraseña | Campos "Contraseña actual", "Contraseña nueva" y "Repetí la contraseña nueva". |
| CA.2 | Perfil > Cambiar contraseña | Rechaza una contraseña que no cumple las reglas del registro o que es igual a la anterior. |
| CA.3 | Inicio de sesión | Al cambiarla se cierran todas las sesiones, también la actual, y la app vuelve al inicio de sesión. |
| CA.4 | Perfil > Cambiar contraseña | Marca el error si la contraseña actual está mal. Con 3 errores seguidos, se bloquea por 15 minutos. |
| CA.5 | Correo | Llega un aviso de que la contraseña fue modificada. |

### E1-H14. Onboarding Inicial

Optativa · 3 puntos · S12 · Dueño: @FedeTrejo

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |

## App: publicaciones

### E2-H1. Crear Post

Obligatoria · 3 puntos · S6 · Dueño: @FedeTrejo

Permite publicar un mensaje corto.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Inicio > ¿Qué está pasando? | El contador muestra `n/280` y no deja publicar si se pasa. |
| CA.2 | Nuevo post | No deja publicar un texto vacío o con solo espacios, salvo que el post lleve imágenes. |
| CA.3 | Sin pantalla (backend) | Las etiquetas HTML y los scripts se limpian antes de guardar. |
| CA.4 | Inicio | El post nuevo aparece con su autor, su fecha y los contadores en 0. |
| CA.5 | Nuevo post | Con más de 30 posts en una hora, muestra un error y no publica. |

### E2-H2. Feed Principal

Obligatoria · 3 puntos · S6 · Dueño: @FedeTrejo

Muestra lo que publican las cuentas que seguís, de lo más nuevo a lo más viejo.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Inicio | Los posts van del más reciente al más antiguo. |
| CA.2 | Inicio | Al llegar al final carga la página siguiente, de a 20. |
| CA.3 | Inicio | Cada post muestra avatar, nombre, handle, contenido, tiempo relativo y contadores de likes, retweets y respuestas. |
| CA.4 | Inicio | Sin posts, muestra "Todavía no hay publicaciones" y una lista de "Cuentas para seguir". |
| CA.5 | Sin pantalla (backend) | La API no devuelve posts de una cuenta protegida a quien no la sigue. |

### E2-H3. Eliminar Post

Obligatoria · 2 puntos · S8 · Dueño: @varbelaiz

Permite borrar un post propio.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Inicio, detalle de post | El botón aparece en los posts propios. Si otra cuenta lo pide por API, se rechaza con "Solo el autor puede eliminar la publicación.". |
| CA.2 | Inicio, detalle de post | Antes de borrar pregunta "¿Eliminar publicación?" y aclara que no se puede deshacer. |
| CA.3 | Inicio | Los retweets de ese post se borran y desaparecen de los feeds. |
| CA.4 | Detalle de post | Las respuestas siguen ahí y el post original muestra `[Post eliminado]`. |

### E2-H4. Responder a un Post

Obligatoria · 2 puntos · S8 · Dueño: @FedeTrejo

Permite responder un post y leer la conversación.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Detalle de post | La respuesta queda debajo del post original, formando el hilo. |
| CA.2 | Detalle de post > Nueva respuesta | Tiene los mismos límites que un post: no vacía y hasta 280 caracteres. |
| CA.3 | Nueva respuesta | Si no se puede responder, muestra "No podés responder a esta publicación.", sin decir que hay un bloqueo. |
| CA.4 | Detalle de post | La sección "Respuestas" las ordena por fecha y carga de a 20. |

### E2-H5. Retweet / Repost

Obligatoria · 2 puntos · S8 · Dueño: @varbelaiz

Permite compartir un post con quienes te siguen, y deshacerlo.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Inicio | El post aparece en el feed de los seguidores con la leyenda "Retweeteado por @usuario". |
| CA.2 | Inicio, detalle de post | El botón pasa de "Retweetear" a "Deshacer retweet", así que no se puede repetir. |
| CA.3 | Perfil de un usuario | Al deshacerlo, sale del perfil y el contador del post original baja. |
| CA.4 | Sin pantalla (backend) | Un post de una cuenta protegida que no seguís responde igual que uno que no existe. |

### E2-H6. Like a un Post

Obligatoria · 2 puntos · S8 · Dueño: @FedeTrejo

Permite marcar con Me gusta un post y quitarlo.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Inicio, detalle de post | El corazón se pinta al tocarlo y vuelve a su estado al tocarlo otra vez. |
| CA.2 | Inicio, detalle de post | El contador cambia al instante en el dispositivo de quien toca, y vuelve atrás si el pedido falla. |
| CA.3 | Sin pantalla (backend) | Repetir el pedido no crea un segundo like. |

### E2-H7. Post con Imagen

Obligatoria · 5 puntos · S9 · Dueño: @FedeTrejo

Permite sumar imágenes a un post nuevo. Las respuestas no llevan imágenes.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Nuevo post > Imágenes | Se eligen de la galería hasta 4, en JPG o PNG. El botón muestra `n/4`. |
| CA.2 | Nuevo post > Imágenes | Una imagen de más de 1 MB no se agrega, y aparece el aviso "Algunas imágenes no se agregaron". |
| CA.3 | Sin pantalla (backend) | Se mira el contenido real del archivo: no alcanza con que la extensión sea la correcta. |
| CA.4 | Inicio, detalle de post | Una imagen ocupa todo el ancho, dos van en mitades, y tres o cuatro forman una grilla de 2x2. |
| CA.5 | Inicio, detalle de post | Al tocar una imagen se abre a pantalla completa, con zoom y paso entre las imágenes del post. |

### E2-H8. Hashtags

Optativa · 3 puntos · S11 · Dueño: @varbelaiz

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |
| CA.4 |  |  |
| CA.5 |  |  |

### E2-H9. Menciones a Usuarios

Optativa · 3 puntos · S12 · Dueño: @jleonalderete

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |

### E2-H10. Búsqueda de Posts y Usuarios

Obligatoria · 5 puntos · S10 · Dueño: @varbelaiz

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |
| CA.4 |  |  |
| CA.5 |  |  |

### E2-H11. Trending Topics

Optativa · 3 puntos · S12 · Dueño: @varbelaiz

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |

### E2-H12. Guardar Posts

Optativa · 3 puntos · S12 · Dueño: @varbelaiz

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |

### E2-H14. Visualización de Perfil de Usuario

Obligatoria · 3 puntos · S9 · Dueño: @tommycass

Muestra el perfil de otra cuenta y sus publicaciones.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Perfil de un usuario | Muestra foto de perfil, portada, nombre visible, handle, biografía, "Se unió en" y los contadores de Siguiendo y Seguidores. |
| CA.2 | Perfil de un usuario | La sección "Publicaciones" trae sus posts y retweets, por fecha y con scroll infinito. |
| CA.3 | Perfil de un usuario | Si es protegida y no la seguís, ves su encabezado y el aviso "Esta cuenta es privada", sin posts. |
| CA.4 | Sin pantalla (backend) | La API devuelve de a 20 posts por página. |

## App: interacciones sociales

### E3-H1. Seguir a un Usuario

Obligatoria · 5 puntos · S5 · Dueño: @tommycass

Permite seguir a otra cuenta, con aprobación del dueño si es protegida.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Perfil de un usuario, listas de cuentas | El botón "Seguir" pasa a "Siguiendo" de inmediato. |
| CA.2 | Perfil de un usuario; Perfil > Solicitudes pendientes | El botón muestra "Solicitado". El dueño de la cuenta decide con "Aprobar" o "Rechazar". |
| CA.3 | Sin pantalla (backend) | Si se intenta por API, responde "No podés seguirte a vos mismo". |
| CA.4 | Sin pantalla (backend) | Los contadores de las dos cuentas se actualizan junto con la relación. |
| CA.5 | Botón Seguir | Pasado el límite, avisa "Alcanzaste el límite de 50 por hora. Probá más tarde.". |

### E3-H2. Dejar de Seguir a un Usuario

Obligatoria · 2 puntos · S5 · Dueño: @tommycass

Permite dejar de seguir a una cuenta.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Botón Siguiendo | Al tocarlo deja de seguir al instante, sin pedir confirmación. |
| CA.2 | Perfil de un usuario | El contador de seguidores cambia enseguida. |
| CA.3 | Inicio | Sus posts ya no aparecen la próxima vez que se carga el feed. |

### E3-H3. Listado de Seguidores y Seguidos

Obligatoria · 3 puntos · S5 · Dueño: @FedeTrejo

Muestra quién te sigue y a quién seguís.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Perfil > Seguidores / Siguiendo | Cada fila muestra nombre visible, handle y botón Seguir o Siguiendo. La foto de perfil falta: la fila usa un ícono genérico, aunque la API ya la devuelve. |
| CA.2 | Perfil > Seguidores / Siguiendo | Al llegar al final carga la página siguiente, de a 20. |
| CA.3 | Perfil > Seguidores / Siguiendo | Sin cuentas, muestra "Todavía no te sigue nadie" o "Todavía no seguís a nadie", según la pestaña. |

### E3-H4. Bloquear Usuario

Obligatoria · 2 puntos · S6 · Dueño: @tommycass

Permite cortar todo contacto con una cuenta. Hoy se bloquea desde las listas de seguidores y seguidos, no desde el perfil.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Sin pantalla (backend) | La cuenta bloqueada no recibe ningún aviso. |
| CA.2 | Perfil > Configuración > Cuentas bloqueadas | Lista las cuentas bloqueadas, con el botón "Desbloquear". |
| CA.3 | Perfil > Seguidores / Siguiendo | El aviso "¿Bloquear a ...?" explica que se eliminan los seguimientos entre las dos cuentas, y la fila sale de la lista. |
| CA.4 | Perfil de un usuario | Quien fue bloqueado no puede abrir el perfil: la API responde 404, como si no existiera. |
| CA.5 | Inicio, Buscar | Los posts de cada una dejan de aparecerle a la otra en el feed y en la búsqueda. |

### E3-H5. Denunciar Usuario

Obligatoria · 2 puntos · S6 · Dueño: @jleonalderete

Permite denunciar una cuenta o un post, y lleva a revisión a las cuentas muy denunciadas.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Post, perfil de un usuario, listas > Denunciar | Se elige Spam, Acoso, Contenido inapropiado o Suplantación de identidad. Al enviar, muestra "Denuncia enviada", y el caso llega al backoffice. |
| CA.2 | Sin pantalla (backend) | Con denuncias de 6 cuentas distintas, la cuenta pasa a En revisión. |
| CA.3 | Denunciar | Repetir antes de 24 horas muestra "Ya denunciaste esta cuenta en las últimas 24 horas". |
| CA.4 | Sin pantalla (backend) | Al pasar a En revisión se cierran todas las sesiones de esa cuenta. |

### E3-H8. Listas Personalizadas

Optativa · 3 puntos · S12 · Dueño: @tommycass

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |
| CA.4 |  |  |

### E3-H9. Invitar Usuarios Externos

Optativa · 2 puntos · S11 · Dueño: @varbelaiz

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |

### E3-H10. Silenciar Usuario

Optativa · 5 puntos · S10 · Dueño: @tommycass

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |
| CA.4 |  |  |
| CA.5 |  |  |

## App: notificaciones

### E4-H1. Recibir notificaciones de nuevo seguidor

Obligatoria · 2 puntos · S10 · Dueño: @jleonalderete

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |
| CA.4 |  |  |

### E4-H2. Notificación de interacción

Obligatoria · 2 puntos · S11 · Dueño: @jleonalderete

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |

### E4-H3. Centro de Notificaciones In-App

Obligatoria · 3 puntos · S10 · Dueño: @FedeTrejo

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |
| CA.4 |  |  |
| CA.5 |  |  |

### E4-H4. Notificación de mención

Optativa · 5 puntos · S12 · Dueño: @jleonalderete

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |

### E4-H5. Configurar Preferencias de Notificación

Optativa · 3 puntos · S11 · Dueño: @jleonalderete

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |

## Backoffice: administración

### E5-H1. Creación de Administradores

Obligatoria · 5 puntos · S4 · Dueño: @jleonalderete

Permite al superadministrador crear otros administradores.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Administradores > Crear administrador; Elegí tu contraseña | El alta muestra una "Contraseña temporal" para copiar. En el primer ingreso, el panel obliga a cambiarla. |
| CA.2 | Crear administrador | El rol es Moderador o Superadministrador. Un moderador no ve Administradores, y el backend se lo niega. |
| CA.3 | Administradores | Vencida la temporal aparece "Temporal vencida", y el botón "Regenerar" crea otra. |
| CA.4 | Crear administrador | Si se configura un dominio, rechaza los correos de otro. Los manifiestos no definen ninguno hoy, así que no restringe. |

### E5-H2. Inicio de Sesión como Administrador

Obligatoria · 2 puntos · S3 · Dueño: @jleonalderete

Permite entrar al backoffice con email y contraseña.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Menú lateral | El token lleva el rol, y el menú muestra Administradores solo al superadministrador. |
| CA.2 | Inicio de sesión | Una cuenta de la app recibe un 403 y el mensaje "Esta cuenta no tiene acceso al backoffice". |
| CA.3 | Inicio de sesión | Con 3 intentos fallidos seguidos, se bloquea por 30 minutos. |

### E5-H3. Visualización de Métricas

Optativa · 5 puntos · S11 · Dueño: @jleonalderete

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |

### E5-H4. Buscador y Detalles de Usuarios

Obligatoria · 3 puntos · S9 · Dueño: @tommycass

Permite buscar cuentas de la app y ver su detalle.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Usuarios > detalle | Muestra estado, "Se registró el", y los contadores de Seguidores y Posts. |
| CA.2 | Usuarios | El campo "Email o handle" busca por una parte del texto, desde 3 caracteres. |
| CA.3 | Usuarios | Los resultados se recorren con "Anterior" y "Siguiente". |

### E5-H5. Bloqueo de Usuarios por Admin

Obligatoria · 2 puntos · S9 · Dueño: @tommycass

Permite bloquear una cuenta que incumple los términos.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Usuarios > detalle > Bloquear | No se puede confirmar sin escribir un motivo. El motivo queda visible en el detalle. |
| CA.2 | Usuarios > detalle > Bloquear | La cuenta pierde el acceso al instante y se cierran todas sus sesiones. |

### E5-H6. Logs de Auditoría

Obligatoria · 3 puntos · S10 · Dueño: @varbelaiz

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |

### E5-H7. Gestión de Denuncias

Obligatoria · 3 puntos · S9 · Dueño: @tommycass

Permite revisar las denuncias y resolver cada caso.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Moderation Queue | Primero aparecen las cuentas denunciadas por más personas distintas. |
| CA.2 | Moderation Queue | Cada caso tiene "Descartar denuncia" y "Suspender cuenta", que pide un motivo y bloquea la cuenta. |
| CA.3 | Moderation Queue | "Resolver" cierra el caso y lo saca de los pendientes. |

### E5-H8. Exportar Datos

Optativa · 2 puntos · S11 · Dueño: @tommycass

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |

### E5-H9. Registro de Última Conexión

Optativa · 2 puntos · S11 · Dueño: @tommycass

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |

### E5-H10. Borrado Forzado de Contenido

Optativa · 3 puntos · S12 · Dueño: @tommycass

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |

### E5-H11. Estado de los Microservicios

Optativa · 5 puntos · S7 · Dueño: @varbelaiz

Muestra si los servicios están en línea. Lista `users-api`, `posts-api` y `api-gateway`: `notifications-api` todavía no está.

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 | Service Health | Consulta `/api/health/<servicio>` en el gateway, que le pide el `/healthcheck` a cada servicio, porque ese no es público. Se actualiza cada 30 segundos. |
| CA.2 | Service Health | Una etiqueta verde dice "En línea" y una roja, "Caído". |
| CA.3 | Service Health | Si tarda más de 5 segundos, corta el pedido y marca "Caído", sin trabar la pantalla. |
| CA.4 | Correo | Grafana Cloud vigila esos mismos endpoints y avisa por correo a una lista fija (ADR-012). Se configura fuera del código, así que esta fila no se pudo comprobar acá. |

### E5-H12. Gestión de Feedback/Reportes

Optativa · 3 puntos · S12 · Dueño: @FedeTrejo

| Criterio | Pantalla | Qué ve el usuario |
|---|---|---|
| CA.1 |  |  |
| CA.2 |  |  |
| CA.3 |  |  |
