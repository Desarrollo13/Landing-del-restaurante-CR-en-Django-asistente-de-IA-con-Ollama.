from django.urls import path

from . import views

app_name = "asistente"

urlpatterns = [
    path("asistente/salud/", views.salud, name="salud"),
    path("asistente/", views.chat, name="chat"),
]
