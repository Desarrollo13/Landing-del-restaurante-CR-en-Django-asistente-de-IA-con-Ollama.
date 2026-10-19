from django.contrib import admin

from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "fecha", "hora", "comensales", "estado", "creada")
    list_filter = ("estado", "fecha")
    search_fields = ("nombre", "correo", "telefono")
    date_hierarchy = "fecha"
    list_editable = ("estado",)
    readonly_fields = ("creada",)
