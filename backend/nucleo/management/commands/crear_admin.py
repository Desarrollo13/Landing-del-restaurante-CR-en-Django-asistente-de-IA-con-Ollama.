import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Crea o actualiza un superusuario usando las variables de entorno "
        "ADMIN_USERNAME, ADMIN_EMAIL y ADMIN_PASSWORD. Útil en despliegues sin "
        "acceso a shell (por ejemplo, el plan gratuito de Render)."
    )

    def handle(self, *args, **options):
        usuario = os.environ.get("ADMIN_USERNAME", "").strip()
        correo = os.environ.get("ADMIN_EMAIL", "").strip()
        clave = os.environ.get("ADMIN_PASSWORD", "")

        if not usuario or not clave:
            self.stdout.write(
                "ADMIN_USERNAME y/o ADMIN_PASSWORD no definidos: se omite la creación del superusuario."
            )
            return

        Usuario = get_user_model()
        usuario_obj, creado = Usuario.objects.get_or_create(
            username=usuario, defaults={"email": correo}
        )
        usuario_obj.is_staff = True
        usuario_obj.is_superuser = True
        if correo:
            usuario_obj.email = correo
        usuario_obj.set_password(clave)
        usuario_obj.save()

        accion = "creado" if creado else "actualizado"
        self.stdout.write(
            self.style.SUCCESS(f"Superusuario '{usuario}' {accion} correctamente.")
        )
