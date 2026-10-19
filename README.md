# Landing CR — Restaurante

Landing page para el restaurante **CR**, construida con **Django** (plantillas) y un **asistente de IA local** vía **Ollama**. Todo el contenido y el código están en español.

## Estructura

```
ladingpage/
├─ backend/
│  ├─ restaurant/      # configuración del proyecto (settings, urls, middleware CORS)
│  ├─ nucleo/          # página de inicio + comando cargar_demo
│  ├─ platos/          # Categoría y Plato (+ datos saludables)
│  ├─ reservas/        # modelo Reserva + API
│  ├─ galeria/         # ImagenGaleria
│  ├─ testimonios/     # Testimonio
│  ├─ asistente/       # API de chat con Ollama (streaming)
│  ├─ templates/       # base.html, index.html y partials/
│  ├─ static/          # css/style.css, js/main.js
│  ├─ media/           # imágenes subidas (NO versionadas)
│  └─ db.sqlite3       # base de datos local (NO versionada)
└─ venv/               # entorno virtual (NO versionado)
```

> `.gitignore` excluye `db.sqlite3`, `media/`, `staticfiles/`, `venv/` y los `.env` (solo se versiona `.env.example`, sin secretos).

## Cómo ejecutar

1. Ollama en marcha en `http://127.0.0.1:11434` con el modelo `qwen2.5:3b`.
2. Django:

```
cd C:\xampp\htdocs\ladingpage\backend
..\venv\Scripts\activate
pip install -r ..\requirements.txt
python manage.py runserver
```

3. Abrir `http://127.0.0.1:8000/`

> Usa siempre el **venv** (`..\venv\Scripts\python.exe`). En este equipo `py` = Python 3.14 y `python` = 3.12 (sin Django); el venv tiene Python 3.10.5 + Django 5.2.18.

## Endpoints

| Método | URL | Descripción |
| --- | --- | --- |
| GET | `/` | Página de inicio |
| GET | `/api/salud/` | Estado del servicio de reservas |
| POST | `/api/reservas/` | Crear reserva |
| POST | `/api/asistente/` | Chat con IA (respuesta en streaming NDJSON) |
| GET | `/api/asistente/salud/` | Estado del asistente + modelo activo |
| GET | `/admin/` | Panel de administración (django) |

## Asistente de IA

Configuración por variables de entorno (con valores por defecto para local) en `backend/restaurant/settings.py`:

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `OLLAMA_URL` | `http://127.0.0.1:11434/api/chat` | URL del endpoint de chat de Ollama |
| `OLLAMA_MODEL` | `qwen2.5:3b` | Modelo a usar |
| `OLLAMA_AUTH_USER` | vacío | Usuario si el túnel usa autenticación básica |
| `OLLAMA_AUTH_PASS` | vacío | Contraseña si el túnel usa autenticación básica |

- El flujo es: navegador → Django → Ollama → respuesta en streaming. El navegador nunca llama a Ollama directamente.
- Límite: 20 consultas/minuto por IP.
- Cambiar de modelo: `ollama pull qwen2.5:7b` y ajustar `OLLAMA_MODEL`.

### Exponer Ollama por túnel (para desplegar en Render)

Render no puede ver tu `127.0.0.1`, así que hay que publicar Ollama con ngrok o Cloudflare Tunnel mientras tu PC esté encendida.

Con ngrok (ya instalado en este equipo):

```powershell
# 1. Ollama debe estar corriendo
ollama serve

# 2. En otra terminal, publicar Ollama con usuario y contraseña
ngrok http 11434 --basic-auth "cr:una-clave-larga"
```

ngrok muestra una URL tipo `https://xxxx-xx-xx.ngrok-free.app`. En Render (o en tu `.env` local) configura:

```
OLLAMA_URL=https://xxxx-xx-xx.ngrok-free.app/api/chat
OLLAMA_MODEL=qwen2.5:3b
OLLAMA_AUTH_USER=cr
OLLAMA_AUTH_PASS=una-clave-larga
```

- La URL gratuita de ngrok **cambia cada vez que reinicias el túnel**: actualiza `OLLAMA_URL` en Render cada vez.
- Sin `--basic-auth` el endpoint queda público y cualquiera podría usar tu Ollama.
- Alternativa sin cuenta: `cloudflared tunnel --url http://localhost:11434` (URL `trycloudflare.com`, también cambia y no tiene autenticación).
- Si tu PC se apaga o duerme, el asistente deja de responder; el resto de la landing sigue funcionando.

## Despliegue en Render

El repo incluye `requirements.txt`, `build.sh` y `render.yaml` (blueprint) para desplegar en [Render](https://render.com).

1. Sube el repo a GitHub.
2. En Render: **New → Blueprint** y elige el repo (`render.yaml` ya lo define).
3. Rellena las variables marcadas con `sync: false` en el panel de Render: `OLLAMA_URL`, `OLLAMA_AUTH_USER`, `OLLAMA_AUTH_PASS` con los datos de tu túnel.
4. En cada despliegue, `build.sh` instala dependencias, ejecuta `collectstatic` y `migrate`.

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `SECRET_KEY` | (insegura de desarrollo) | Generada por Render; en local usa el valor por defecto |
| `DEBUG` | `True` | Ponla en `False` en producción |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Lista separada por comas; `RENDER_EXTERNAL_HOSTNAME` se añade sola |
| `CORS_ALLOWED_ORIGINS` | `*` | Orígenes permitidos para la API |
| `CSRF_TRUSTED_ORIGINS` | localhost | Añade el dominio de Render automáticamente |
| `DATABASE_URL` | SQLite local | Render la enlaza a su PostgreSQL |

- Con `DEBUG=False` se activan redirección a HTTPS, HSTS y cookies seguras.
- El plan gratuito de PostgreSQL en Render **caduca a los 30 días**; exporta los datos o cambia a otro proveedor de base de datos si lo necesitas.
- Los estáticos se sirven con WhiteNoise (`collectstatic`); no hace falta un CDN.

## Datos demo

```
python manage.py cargar_demo
```

Carga 3 categorías, 4 platos (con datos saludables), imágenes de galería y testimonios. Es idempotente.

La base de datos no se versiona. En una instalación nueva crea el superusuario:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py cargar_demo
```

En Render puedes ejecutar `createsuperuser` desde la **Shell** del servicio tras el primer despliegue.

## Estado actual

- [x] Landing en Django (templates + estáticos) y responsive
- [x] Apps en español: nucleo, platos, reservas, galeria, testimonios
- [x] Admin para gestionar platos, galería, testimonios y reservas
- [x] Carta en pestañas por categoría
- [x] Galería uniforme y adaptativa
- [x] Asistente IA con Ollama integrado (escritorio y móvil verificados)
- [x] Configuración de producción (env vars, WhiteNoise, gunicorn, `render.yaml`)

## Próximos pasos sugeridos

- [ ] Que el asistente recuerde la reserva recién hecha (fecha, comensales) al recomendar.
- [ ] Subir a `qwen2.5:7b` para mejor español si el equipo lo soporta.
- [ ] Desplegar: subir el repo a GitHub y crear el Blueprint en Render.
