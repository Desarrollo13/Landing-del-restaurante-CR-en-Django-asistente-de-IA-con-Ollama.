# Landing CR — Restaurante

Landing page para el restaurante **CR**, construida con **Django** (plantillas del lado del servidor) y un **asistente de IA local** mediante **Ollama**. Incluye carta por categorías, galería, testimonios, formulario de reservas con API JSON y un chatbot que recomienda platos según necesidades alimentarias.

Todo el contenido y el código están en español.

## Características

- Landing responsive (móvil, tablet y escritorio) con navegación fija, menú hamburguesa y animaciones al hacer scroll.
- Carta dinámica en pestañas por categoría, con precio, descripción e información saludable.
- Galería de imágenes adaptable y uniforme.
- Testimonios de clientes.
- Formulario de reservas con validación en cliente y servidor.
- Asistente de IA con respuestas en **streaming**, usando únicamente la carta real (no inventa platos).
- Panel de administración de Django para gestionar todo el contenido.
- Comando de datos de demostración idempotente.
- Configuración lista para desplegar en Render (variables de entorno, WhiteNoise, gunicorn y PostgreSQL).

## Stack tecnológico

| Capa | Tecnología |
| --- | --- |
| Backend | Python 3.10.5 · Django 5.2.18 |
| Base de datos | SQLite en local · PostgreSQL en producción (`DATABASE_URL`) |
| IA | Ollama (`qwen2.5:3b`) con API de chat en streaming |
| Estáticos | WhiteNoise + `collectstatic` en producción |
| Servidor | `runserver` en local · gunicorn en Render |
| Frontend | Plantillas Django, CSS y JavaScript vanilla |

## Estructura del proyecto

```
ladingpage/
├─ backend/
│  ├─ restaurant/      # configuración: settings, urls, WSGI/ASGI y middleware CORS
│  ├─ nucleo/          # página de inicio + comando cargar_demo
│  ├─ platos/          # Categoría y Plato (+ datos saludables y alérgenos)
│  ├─ reservas/        # modelo Reserva + API de creación
│  ├─ galeria/         # ImagenGaleria
│  ├─ testimonios/     # Testimonio
│  ├─ asistente/       # API de chat con Ollama (streaming NDJSON)
│  ├─ templates/       # base.html, index.html y partials/
│  ├─ static/          # css/style.css y js/main.js
│  ├─ media/           # imágenes subidas desde el admin (NO versionadas)
│  └─ db.sqlite3       # base de datos local (NO versionada)
├─ venv/               # entorno virtual (NO versionado)
├─ requirements.txt    # dependencias de Python
├─ build.sh            # build para Render (instalar, collectstatic, migrate)
├─ render.yaml         # Blueprint de despliegue en Render
└─ .env.example        # plantilla de variables de entorno (sin secretos)
```

> `.gitignore` excluye `db.sqlite3`, `media/`, `staticfiles/`, `venv/` y los `.env` (solo se versiona `.env.example`).

## Requisitos previos

- Python 3.10 o superior.
- [Ollama](https://ollama.com) instalado y con el modelo descargado:

  ```
  ollama pull qwen2.5:3b
  ```

## Instalación y ejecución local

1. Clona el repositorio y entra en la carpeta.
2. Crea y activa el entorno virtual:

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```powershell
   pip install -r requirements.txt
   ```

4. Aplica las migraciones y carga los datos de demostración:

   ```powershell
   cd backend
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py cargar_demo
   ```

5. Arranca Ollama (en otra terminal) y Django:

   ```powershell
   ollama serve
   ```

   ```powershell
   cd backend
   ..\venv\Scripts\activate
   python manage.py runserver
   ```

6. Abre `http://127.0.0.1:8000/`. El admin está en `http://127.0.0.1:8000/admin/`.

> Usa siempre el **venv**. En este equipo `py` es Python 3.14 y `python` es 3.12 (sin Django); el venv tiene Python 3.10.5 + Django 5.2.18.

## Variables de entorno

Se leen en `backend/restaurant/settings.py` y tienen valores por defecto para desarrollo local.

| Variable | Por defecto | Descripción |
| --- | --- | --- |
| `SECRET_KEY` | clave insegura de desarrollo | Clave secreta de Django (en producción usa una larga y aleatoria) |
| `DEBUG` | `True` | Ponla en `False` en producción |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Lista separada por comas; `RENDER_EXTERNAL_HOSTNAME` se añade sola |
| `CORS_ALLOWED_ORIGINS` | `*` | Orígenes permitidos para consumir la API desde el navegador |
| `CSRF_TRUSTED_ORIGINS` | localhost | Orígenes de confianza para CSRF; el dominio de Render se añade solo |
| `DATABASE_URL` | SQLite local | URL de PostgreSQL en producción |
| `OLLAMA_URL` | `http://127.0.0.1:11434/api/chat` | Endpoint de chat de Ollama |
| `OLLAMA_MODEL` | `qwen2.5:3b` | Modelo a usar |
| `OLLAMA_AUTH_USER` | vacío | Usuario si el túnel usa autenticación básica |
| `OLLAMA_AUTH_PASS` | vacío | Contraseña si el túnel usa autenticación básica |
| `SECURE_SSL_REDIRECT` | `True` con `DEBUG=False` | Redirección a HTTPS |
| `SECURE_HSTS_SECONDS` | `31536000` con `DEBUG=False` | Duración de HSTS |
| `ADMIN_USERNAME` | vacío | Usuario del superusuario creado por `crear_admin` |
| `ADMIN_EMAIL` | vacío | Correo del superusuario |
| `ADMIN_PASSWORD` | vacío | Contraseña del superusuario |
| `CARGAR_DEMO` | `0` | `1` para cargar datos demo durante el build |

Copia `.env.example` como `.env` si quieres configurar el desarrollo local. **No subas nunca el `.env` al repositorio.**

## Modelos de datos

| App | Modelo | Campos principales |
| --- | --- | --- |
| `platos` | `Categoria` | nombre, descripción, orden, activa |
| `platos` | `Plato` | categoría, nombre, descripción, precio, imagen/URL, destacado, disponible, calorías, vegetariano, vegano, sin gluten, alérgenos, etiquetas, orden |
| `reservas` | `Reserva` | nombre, correo, teléfono, fecha, hora, comensales, mensaje, estado (pendiente/confirmada/cancelada) |
| `galeria` | `ImagenGaleria` | título, imagen/URL, orden, activa |
| `testimonios` | `Testimonio` | nombre, cargo, texto, foto/URL, activo, orden |

Las imágenes se pueden subir como archivo (`media/`) o indicar una URL externa. La propiedad `imagen_src` / `foto_src` prioriza el archivo subido.

## Endpoints

| Método | URL | Descripción |
| --- | --- | --- |
| GET | `/` | Página de inicio |
| GET | `/api/salud/` | Estado del servicio de reservas |
| POST | `/api/reservas/` | Crear una reserva |
| POST | `/api/asistente/` | Chat con IA (respuesta en streaming NDJSON) |
| GET | `/api/asistente/salud/` | Estado del asistente + modelo activo |
| GET | `/admin/` | Panel de administración de Django |

### Crear una reserva

```http
POST /api/reservas/
Content-Type: application/json

{
  "nombre": "Ana Pérez",
  "correo": "ana@example.com",
  "telefono": "+34 600 000 000",
  "fecha": "2026-11-20",
  "hora": "20:30",
  "comensales": 4,
  "mensaje": "Mesa junto a la ventana"
}
```

Respuesta `201`:

```json
{
  "ok": true,
  "mensaje": "Reserva recibida correctamente.",
  "reserva": {
    "id": 1,
    "nombre": "Ana Pérez",
    "fecha": "2026-11-20",
    "hora": "20:30",
    "comensales": 4,
    "estado": "pendiente"
  }
}
```

Validaciones: nombre de al menos 2 caracteres, correo válido, fecha obligatoria y no pasada, entre 1 y 20 comensales. Si hay errores devuelve `400` con el objeto `errores`.

### Chat con el asistente

```http
POST /api/asistente/
Content-Type: application/json

{
  "mensaje": "¿Tienen algo vegano y sin gluten?",
  "historial": [
    {"role": "user", "content": "Hola"},
    {"role": "assistant", "content": "¡Hola! ¿Qué buscas?"}
  ]
}
```

La respuesta es `application/x-ndjson`, una línea JSON por evento:

```
{"delta": "Tenemos "}
{"delta": "la ensalada de temporada..."}
{"done": true}
```

En caso de error se emite `{"error": "..."}`. El frontend lee el stream con `fetch` + `ReadableStream` y va pintando los fragmentos.

## Asistente de IA

- Flujo: navegador → Django → Ollama → respuesta en streaming. El navegador nunca llama a Ollama directamente.
- El contexto se construye con los platos **disponibles** de la base de datos (nombre, categoría, precio, descripción, calorías, vegano/vegetariano, sin gluten, alérgenos y etiquetas).
- Se envían como máximo los últimos 8 mensajes del historial y se limitan los textos a 2000 caracteres.
- Temperatura `0.4`, timeout de 180 segundos.
- Límite de **20 consultas por minuto por IP** (caché de Django).
- Reglas del prompt: responder en español, en 2 a 4 frases, recomendar de 1 a 3 platos y no inventar información.

### Exponer Ollama por túnel (para desplegar en Render)

Render no puede ver tu `127.0.0.1`, así que hay que publicar Ollama con ngrok o Cloudflare Tunnel mientras tu PC esté encendida.

Con ngrok:

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

## Administración

En `/admin/` se pueden gestionar:

- **Categorías y platos**: precios, imágenes, disponibilidad, orden y datos saludables.
- **Reservas**: estado, fecha y datos de contacto.
- **Galería**: imágenes, orden y visibilidad.
- **Testimonios**: texto, foto, orden y visibilidad.

## Datos de demostración

```powershell
python manage.py cargar_demo
```

Carga 3 categorías, 4 platos (con datos saludables), 5 imágenes de galería y 3 testimonios. Es idempotente: se puede ejecutar varias veces sin duplicar registros.

La base de datos no se versiona. En una instalación nueva:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py cargar_demo
```

## Pruebas

```powershell
cd backend
..\venv\Scripts\python.exe manage.py check
..\venv\Scripts\python.exe manage.py test
```

Actualmente no hay tests automatizados; `check` valida la configuración del proyecto.

## Despliegue en Render

El repo incluye `requirements.txt`, `build.sh` y `render.yaml` (Blueprint).

1. Sube el repo a GitHub.
2. En Render: **New → Blueprint** y elige el repo.
3. Rellena las variables marcadas con `sync: false`:
   - `OLLAMA_URL`, `OLLAMA_AUTH_USER` y `OLLAMA_AUTH_PASS` con los datos de tu túnel.
   - `ADMIN_USERNAME`, `ADMIN_EMAIL` y `ADMIN_PASSWORD` para el superusuario.
4. `build.sh` instala dependencias, ejecuta `collectstatic`, `migrate` y crea el superusuario con `crear_admin` en cada despliegue (y carga datos demo si `CARGAR_DEMO=1`).
5. Espera a que termine el deploy y entra en `https://TU-APP.onrender.com/admin/` con esas credenciales.

> El plan gratuito de Render **no tiene Shell ni SSH** ni discos persistentes. Por eso el superusuario y los datos demo se crean desde `build.sh` vía variables de entorno. Si cambias `ADMIN_PASSWORD`, el próximo deploy actualiza la contraseña.

Notas de producción:

- Con `DEBUG=False` se activan redirección a HTTPS, HSTS y cookies seguras.
- Los estáticos se sirven con WhiteNoise; no hace falta un CDN.
- El plan gratuito de PostgreSQL en Render **caduca a los 30 días**; exporta los datos o usa otro proveedor.
- El disco de Render es efímero: las imágenes subidas al admin no se conservan entre despliegues. Para producción conviene usar URLs externas o almacenamiento de objetos (S3, Cloudinary, etc.).
- El web service gratuito se duerme tras 15 minutos sin tráfico; la primera petición tarda ~1 minuto en despertarlo.

## Seguridad

- `db.sqlite3`, `media/`, `venv/`, `staticfiles/` y `.env` están fuera del repositorio.
- `SECRET_KEY` y credenciales se inyectan por variables de entorno en producción.
- El túnel de Ollama debe usar autenticación básica.
- La API de reservas y el chat son `csrf_exempt` porque se consumen como API JSON; el formulario valida los datos en el servidor.
- El límite de peticiones del asistente reduce el abuso del endpoint.

## Estado del proyecto

- [x] Landing en Django (templates + estáticos) y responsive
- [x] Apps en español: nucleo, platos, reservas, galeria, testimonios
- [x] Admin para gestionar platos, galería, testimonios y reservas
- [x] Carta en pestañas por categoría
- [x] Galería uniforme y adaptativa
- [x] Asistente IA con Ollama integrado (escritorio y móvil verificados)
- [x] Configuración de producción (env vars, WhiteNoise, gunicorn, `render.yaml`)

## Próximos pasos

- [ ] Que el asistente recuerde la reserva recién hecha (fecha, comensales) al recomendar.
- [ ] Subir a `qwen2.5:7b` para mejor español si el equipo lo soporta.
- [ ] Añadir tests automatizados para la API de reservas y el asistente.
- [ ] Desplegar: subir el repo a GitHub y crear el Blueprint en Render.
