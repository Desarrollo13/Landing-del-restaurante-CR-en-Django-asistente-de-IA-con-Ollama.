from django.conf import settings
from django.http import HttpResponse


class CorsMiddleware:
    """Minimal CORS support so the landing page (served by XAMPP) can consume the API."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "OPTIONS" and "access-control-request-method" in request.headers:
            response = HttpResponse(status=204)
        else:
            response = self.get_response(request)

        allowed = getattr(settings, "CORS_ALLOWED_ORIGINS", ["*"])
        origin = request.headers.get("Origin")

        if "*" in allowed:
            response["Access-Control-Allow-Origin"] = "*"
        elif origin and origin in allowed:
            response["Access-Control-Allow-Origin"] = origin
            response["Vary"] = "Origin"

        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"
        response["Access-Control-Max-Age"] = "86400"
        return response
