from django.contrib import admin

from .models import Categoria, Plato


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "orden", "activa")
    list_editable = ("orden", "activa")
    search_fields = ("nombre",)


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "destacado", "disponible", "orden")
    list_filter = ("categoria", "destacado", "disponible", "es_vegetariano", "es_vegano", "sin_gluten")
    list_editable = ("precio", "destacado", "disponible", "orden")
    search_fields = ("nombre", "descripcion")
    autocomplete_fields = ("categoria",)
    fieldsets = (
        (None, {"fields": ("categoria", "nombre", "descripcion", "precio")}),
        ("Imagen", {"fields": ("imagen", "imagen_url")}),
        (
            "Información saludable",
            {
                "fields": (
                    "calorias",
                    "es_vegetariano",
                    "es_vegano",
                    "sin_gluten",
                    "alergenos",
                    "etiquetas",
                )
            },
        ),
        ("Visibilidad", {"fields": ("destacado", "disponible", "orden")}),
    )
