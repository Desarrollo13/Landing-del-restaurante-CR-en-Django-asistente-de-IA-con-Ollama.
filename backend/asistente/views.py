import base64
import json
import urllib.error
import urllib.request

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from platos.models import Plato

LIMITE_POR_MINUTO = 20


def _carta_texto():
    """Construye el contexto de la carta para el modelo."""
    lineas = []
    platos = Plato.objects.filter(disponible=True).select_related("categoria")
    for plato in platos:
        partes = [f"{plato.nombre} ({plato.categoria.nombre}) - {plato.precio} EUR"]
        if plato.descripcion:
            partes.append(plato.descripcion)
        datos = []
        if plato.calorias:
            datos.append(f"{plato.calorias} kcal")
        if plato.es_vegano:
            datos.append("vegano")
        elif plato.es_vegetariano:
            datos.append("vegetariano")
        if plato.sin_gluten:
            datos.append("sin gluten")
        if plato.alergenos:
            datos.append(f"alérgenos: {plato.alergenos}")
        if plato.etiquetas:
            datos.append(plato.etiquetas)
        if datos:
            partes.append("[" + ", ".join(datos) + "]")
        lineas.append("- " + ". ".join(partes))
    return "\n".join(lineas) or "(carta vacía)"


def _instrucciones(carta):
    return (
        "Eres 'CR Asistente', el ayudante virtual del restaurante CR. "
        "Ayudas a los clientes a elegir platos, sobre todo según sus necesidades "
        "(algo saludable, ligero, vegetariano, vegano, sin gluten, alergias, etc.).\n"
        "Reglas:\n"
        "- Usa ÚNICAMENTE la información de la carta que aparece abajo. No inventes platos, "
        "precios ni datos nutricionales.\n"
        "- Si no tienes la información necesaria, dilo con naturalidad y sugiere preguntar al personal.\n"
        "- Responde en español, cercano y claro, en 2 a 4 frases. Puedes recomendar de 1 a 3 platos concretos.\n"
        "- No pidas datos personales.\n\n"
        "CARTA:\n" + carta
    )


def _cabeceras_ollama():
    cabeceras = {"Content-Type": "application/json", "User-Agent": "CR-Asistente/1.0"}
    usuario = settings.OLLAMA_AUTH_USER
    clave = settings.OLLAMA_AUTH_PASS
    if usuario and clave:
        credenciales = base64.b64encode(f"{usuario}:{clave}".encode("utf-8")).decode("ascii")
        cabeceras["Authorization"] = f"Basic {credenciales}"
    return cabeceras


def _demasiadas_peticiones(ip):
    clave = f"asistente_limite_{ip}"
    actual = cache.get(clave, 0)
    if actual >= LIMITE_POR_MINUTO:
        return True
    cache.set(clave, actual + 1, timeout=60)
    return False


@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    ip = request.META.get("REMOTE_ADDR", "anon")
    if _demasiadas_peticiones(ip):
        return JsonResponse(
            {"error": "Demasiadas consultas seguidas. Espera un momento, por favor."},
            status=429,
        )

    try:
        datos = json.loads(request.body.decode("utf-8") or "{}")
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON no válido."}, status=400)

    mensaje = str(datos.get("mensaje") or "").strip()
    if not mensaje:
        return JsonResponse({"error": "Falta el mensaje."}, status=400)

    historial = datos.get("historial")
    if not isinstance(historial, list):
        historial = []
    historial = [
        m
        for m in historial
        if isinstance(m, dict) and m.get("role") in {"user", "assistant"} and m.get("content")
    ][-8:]

    mensajes = [{"role": "system", "content": _instrucciones(_carta_texto())}]
    mensajes += [{"role": m["role"], "content": str(m["content"])[:2000]} for m in historial]
    mensajes.append({"role": "user", "content": mensaje[:2000]})

    payload = json.dumps(
        {
            "model": settings.OLLAMA_MODEL,
            "messages": mensajes,
            "stream": True,
            "options": {"temperature": 0.4},
        }
    ).encode("utf-8")

    def eventos():
        peticion = urllib.request.Request(
            settings.OLLAMA_URL,
            data=payload,
            headers=_cabeceras_ollama(),
        )
        try:
            with urllib.request.urlopen(peticion, timeout=180) as respuesta:
                for linea in respuesta:
                    linea = linea.strip()
                    if not linea:
                        continue
                    try:
                        trozo = json.loads(linea)
                    except ValueError:
                        continue
                    contenido = trozo.get("message", {}).get("content", "")
                    if contenido:
                        yield json.dumps({"delta": contenido}) + "\n"
                    if trozo.get("done"):
                        break
        except urllib.error.URLError:
            yield json.dumps(
                {"error": "No se pudo conectar con el asistente. ¿Está Ollama en marcha?"}
            ) + "\n"
        except Exception:
            yield json.dumps({"error": "Ocurrió un error al generar la respuesta."}) + "\n"
        yield json.dumps({"done": True}) + "\n"

    respuesta = StreamingHttpResponse(eventos(), content_type="application/x-ndjson")
    respuesta["X-Accel-Buffering"] = "no"
    respuesta["Cache-Control"] = "no-cache"
    return respuesta


@require_http_methods(["GET"])
def salud(request):
    return JsonResponse({"estado": "ok", "servicio": "asistente", "modelo": settings.OLLAMA_MODEL})
