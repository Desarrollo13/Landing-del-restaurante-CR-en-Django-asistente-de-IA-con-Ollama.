from django.contrib import admin

from .models import Testimonio


@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cargo", "activo", "orden")
    list_editable = ("activo", "orden")
    search_fields = ("nombre", "texto")
