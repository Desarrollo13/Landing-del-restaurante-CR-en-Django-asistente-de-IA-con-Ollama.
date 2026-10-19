from django.db.models import Count, Prefetch, Q
from django.shortcuts import render

from galeria.models import ImagenGaleria
from platos.models import Categoria, Plato
from testimonios.models import Testimonio


def inicio(request):
    categorias = (
        Categoria.objects.filter(activa=True)
        .annotate(platos_disponibles=Count("platos", filter=Q(platos__disponible=True)))
        .filter(platos_disponibles__gt=0)
        .prefetch_related(
            Prefetch(
                "platos",
                queryset=Plato.objects.filter(disponible=True).order_by("orden", "nombre"),
            )
        )
        .order_by("orden", "nombre")
    )

    contexto = {
        "categorias": categorias,
        "imagenes_galeria": ImagenGaleria.objects.filter(activa=True),
        "testimonios": Testimonio.objects.filter(activo=True),
    }
    return render(request, "index.html", contexto)
