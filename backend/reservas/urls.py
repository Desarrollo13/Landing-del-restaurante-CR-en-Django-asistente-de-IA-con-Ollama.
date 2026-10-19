from django.urls import path

from . import views

app_name = "reservas"

urlpatterns = [
    path("salud/", views.salud, name="salud"),
    path("reservas/", views.crear_reserva, name="crear"),
]
