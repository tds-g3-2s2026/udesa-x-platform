"""Synthetic campus topics and compatible publication text."""

TOPICS = (
    (
        "estudio",
        "¿Cómo organizan el repaso de {subject}?",
        "Me sirve practicar {subject} por tema.",
    ),
    (
        "programación",
        "Hoy avancé con {subject}. ¿Algún consejo?",
        "Para {subject}, probaría casos pequeños.",
    ),
    ("deportes", "¿Quién se suma a {subject} esta semana?", "Me sumo a {subject} el viernes."),
    (
        "libros",
        "¿Qué recomiendan para empezar con {subject}?",
        "Para {subject}, buscaría una introducción.",
    ),
    (
        "proyectos",
        "Estamos preparando {subject} para la clase.",
        "Podemos revisar {subject} en grupo.",
    ),
    (
        "campus",
        "¿Nos juntamos para {subject} después de clase?",
        "Me sumo para {subject} después de las seis.",
    ),
)
SUBJECTS = (
    ("álgebra", "estadística", "criptografía"),
    ("tests de integración", "consultas SQL", "estructuras de datos"),
    ("fútbol", "tenis", "básquet"),
    ("ciencia ficción", "historia argentina", "literatura latinoamericana"),
    ("una presentación", "el prototipo", "la entrega final"),
    ("estudiar en la biblioteca", "tomar un café", "organizar el taller"),
)

POST_SUFFIXES = ("", " ¿Qué les parece?", " Compartan sus experiencias.")
REPLY_SUFFIXES = ("", " Después les cuento cómo salió.", " Lo podemos conversar en clase.")
LONG_POST_PADDING = " Estoy reuniendo ideas para compartir en el próximo encuentro."
DISPLAY_NAME = "Estudiante {number}"
BIO = "Me interesa {topic}."


def generate_post_text(rng, topic, subject, index):
    text = TOPICS[topic][1].format(subject=subject) + rng.choice(POST_SUFFIXES)
    if index % 10 == 0:
        text = (text + LONG_POST_PADDING * 6)[:280]
    return text


def generate_reply_text(rng, topic, subject):
    return TOPICS[topic][2].format(subject=subject) + rng.choice(REPLY_SUFFIXES)
