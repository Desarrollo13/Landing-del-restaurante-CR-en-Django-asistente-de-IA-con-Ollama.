import json
from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Reserva


def _parse_json(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (ValueError, UnicodeDecodeError):
        return None


def _limpiar_comensales(valor):
    if valor is None:
        return None
    texto = str(valor).strip().replace("+", "")
    if not texto.isdigit():
        return None
    numero = int(texto)
    return numero if 1 <= numero <= 20 else None


def _limpiar_fecha(valor):
    if not valor:
        return None
    try:
        return datetime.strptime(str(valor), "%Y-%m-%d").date()
    except ValueError:
        return None


def _limpiar_hora(valor):
    if not valor:
        return None
    try:
        return datetime.strptime(str(valor), "%H:%M").time()
    except ValueError:
        return None


@require_http_methods(["GET"])
def salud(request):
    return JsonResponse({"estado": "ok", "servicio": "api-reservas"})


@csrf_exempt
@require_http_methods(["POST"])
def crear_reserva(request):
    datos = _parse_json(request)
    if datos is None:
        return JsonResponse({"ok": False, "errores": {"detalle": "JSON no válido."}}, status=400)

    errores = {}

    nombre = str(datos.get("nombre") or "").strip()
    if len(nombre) < 2:
        errores["nombre"] = "Introduce un nombre válido."

    correo = str(datos.get("correo") or "").strip()
    if not correo:
        errores["correo"] = "El correo es obligatorio."
    else:
        try:
            validate_email(correo)
        except ValidationError:
            errores["correo"] = "Correo electrónico no válido."

    fecha = _limpiar_fecha(datos.get("fecha"))
    if not datos.get("fecha"):
        errores["fecha"] = "La fecha es obligatoria."
    elif fecha is None:
        errores["fecha"] = "Fecha no válida."
    elif fecha < timezone.localdate():
        errores["fecha"] = "La fecha no puede ser en el pasado."

    hora = _limpiar_hora(datos.get("hora"))

    comensales = _limpiar_comensales(datos.get("comensales"))
    if comensales is None:
        errores["comensales"] = "Indica entre 1 y 20 comensales."

    if errores:
        return JsonResponse({"ok": False, "errores": errores}, status=400)

    reserva = Reserva.objects.create(
        nombre=nombre,
        correo=correo,
        telefono=str(datos.get("telefono") or "").strip(),
        fecha=fecha,
        hora=hora,
        comensales=comensales,
        mensaje=str(datos.get("mensaje") or "").strip(),
    )

    return JsonResponse(
        {
            "ok": True,
            "mensaje": "Reserva recibida correctamente.",
            "reserva": {
                "id": reserva.id,
                "nombre": reserva.nombre,
                "fecha": reserva.fecha.isoformat(),
                "hora": reserva.hora.strftime("%H:%M") if reserva.hora else None,
                "comensales": reserva.comensales,
                "estado": reserva.estado,
            },
        },
        status=201,
    )
