from django.contrib import admin

from .models import ImagenGaleria


@admin.register(ImagenGaleria)
class ImagenGaleriaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "orden", "activa", "creada")
    list_editable = ("orden", "activa")
    search_fields = ("titulo",)
