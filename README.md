# StudentOverflow

**StudentOverflow** es una plataforma web donde los estudiantes pueden hacer preguntas académicas y recibir respuestas de otros usuarios. Inspirado en StackOverflow, este sitio busca fomentar el aprendizaje colaborativo.

---

## Tecnologías utilizadas

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Jinja2
- Tailwind CSS (para estilos)

---

## Funcionalidades implementadas

- Registro e inicio de sesión de usuarios.
- Publicar preguntas.
- Ver lista de preguntas.
- Ver detalles de una pregunta y sus respuestas.
- Responder preguntas (cualquier usuario autenticado puede responder).
- Gestión básica de usuarios y preguntas.
- Votos (estructura básica para respuestas, puede extenderse).

---

## Estructura del proyecto

- `/app` - Código fuente de la aplicación Flask.
  - `models.py` - Definición de los modelos (User, Question, Answer, Tag, Vote).
  - `__init__.py`
  - `routes.py` - Rutas principales de la aplicación.
  - `auth.py` - Maneja el inicio de sesión, registro y autenticación.
  - `templates/` - Plantillas HTML con Jinja2.
  - `static/` - Assets estáticos (CSS, JS, imágenes).

- `README.md` - Este archivo.
- `requirements.txt` - Dependencias Python.
- `run.py` - Script para iniciar el proyecto.
- `.venv/` (no incluido en el repositorio) - Entorno virtual que contiene variables de entorno y keys sensibles.

---

## Instalación y configuración

1. Clona el repositorio:

```bash
git clone https://github.com/tuusuario/studentoverflow.git
cd studentoverflow

```

2. Crea y activa un entorno virtual (recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# o
.venv\Scripts\activate     # Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecuta la aplicación:
```bash
flask run.py
```

La app correrá en http://127.0.0.1:5000/.

---

Autor
Desarrollado por AngelMancilla