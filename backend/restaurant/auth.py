from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameBackend(ModelBackend):
    """Permite iniciar sesión con el nombre de usuario o con el correo electrónico."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        Usuario = get_user_model()
        if username is None:
            username = kwargs.get(Usuario.USERNAME_FIELD)
        if username is None or password is None:
            return None

        try:
            usuario = Usuario.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except Usuario.DoesNotExist:
            # Ejecuta el hasher para no revelar por tiempos si el usuario existe.
            Usuario().set_password(password)
            return None
        except Usuario.MultipleObjectsReturned:
            usuario = (
                Usuario.objects.filter(
                    Q(username__iexact=username) | Q(email__iexact=username)
                )
                .order_by("id")
                .first()
            )

        if usuario.check_password(password) and self.user_can_authenticate(usuario):
            return usuario
        return None
