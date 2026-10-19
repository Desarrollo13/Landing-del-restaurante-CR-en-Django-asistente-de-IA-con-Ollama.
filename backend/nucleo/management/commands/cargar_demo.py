from decimal import Decimal

from django.core.management.base import BaseCommand

from galeria.models import ImagenGaleria
from platos.models import Categoria, Plato
from testimonios.models import Testimonio


class Command(BaseCommand):
    help = "Carga datos de demostración: carta, galería y testimonios."

    def handle(self, *args, **options):
        categorias = {}
        for orden, nombre in enumerate(["Entrantes", "Principales", "Postres"], start=1):
            categoria, _ = Categoria.objects.get_or_create(
                nombre=nombre, defaults={"orden": orden}
            )
            categorias[nombre] = categoria

        platos = [
            {
                "categoria": "Entrantes",
                "nombre": "Ensalada de temporada",
                "descripcion": "Verduras frescas, aguacate y vinagreta de la casa.",
                "precio": "8.50",
                "imagen_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80",
                "destacado": True,
                "calorias": 320,
                "es_vegetariano": True,
                "es_vegano": False,
                "sin_gluten": True,
                "alergenos": "",
                "etiquetas": "ligero, saludable, fresco",
            },
            {
                "categoria": "Principales",
                "nombre": "Pizza artesanal",
                "descripcion": "Masa madre, mozzarella fresca y albahaca.",
                "precio": "12.00",
                "imagen_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80",
                "destacado": False,
                "calorias": 780,
                "es_vegetariano": True,
                "es_vegano": False,
                "sin_gluten": False,
                "alergenos": "gluten, lactosa",
                "etiquetas": "contundente",
            },
            {
                "categoria": "Principales",
                "nombre": "Plato del chef",
                "descripcion": "Selección diaria de carne, guarnición y salsa.",
                "precio": "18.00",
                "imagen_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80",
                "destacado": True,
                "calorias": 640,
                "es_vegetariano": False,
                "es_vegano": False,
                "sin_gluten": False,
                "alergenos": "",
                "etiquetas": "alto en proteína",
            },
            {
                "categoria": "Postres",
                "nombre": "Pancakes del chef",
                "descripcion": "Con frutos rojos, sirope de arce y mantequilla.",
                "precio": "9.00",
                "imagen_url": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=800&q=80",
                "destacado": False,
                "calorias": 520,
                "es_vegetariano": True,
                "es_vegano": False,
                "sin_gluten": False,
                "alergenos": "gluten, lactosa, huevo",
                "etiquetas": "dulce, postre",
            },
        ]

        campos_salud = ("calorias", "es_vegetariano", "es_vegano", "sin_gluten", "alergenos", "etiquetas")
        for datos in platos:
            plato, creado = Plato.objects.get_or_create(
                nombre=datos["nombre"],
                defaults={
                    "categoria": categorias[datos["categoria"]],
                    "descripcion": datos["descripcion"],
                    "precio": Decimal(datos["precio"]),
                    "imagen_url": datos["imagen_url"],
                    "destacado": datos["destacado"],
                    **{campo: datos[campo] for campo in campos_salud},
                },
            )
            if not creado and plato.calorias is None:
                for campo in campos_salud:
                    setattr(plato, campo, datos[campo])
                plato.save()

        galeria = [
            ("Mesa servida", "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?auto=format&fit=crop&w=800&q=80"),
            ("Ambiente del restaurante", "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80"),
            ("Plato saludable", "https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=800&q=80"),
            ("Plato gourmet", "https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=800&q=80"),
            ("Postre de la casa", "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=1200&q=80"),
        ]
        for indice, (titulo, url) in enumerate(galeria, start=1):
            ImagenGaleria.objects.get_or_create(
                titulo=titulo, defaults={"imagen_url": url, "orden": indice}
            )

        testimonios = [
            ("María Gómez", "Clienta habitual", "Comida espectacular y trato inmejorable. Volveremos sin duda.", "https://i.pravatar.cc/80?img=12"),
            ("Carlos Ruiz", "Foodie", "El mejor sitio para celebrar. Cada plato es una obra de arte.", "https://i.pravatar.cc/80?img=32"),
            ("Laura Pérez", "Crítica gastronómica", "Ambiente perfecto y sabores que sorprenden. Muy recomendado.", "https://i.pravatar.cc/80?img=5"),
        ]
        for orden, (nombre, cargo, texto, foto) in enumerate(testimonios, start=1):
            Testimonio.objects.get_or_create(
                nombre=nombre,
                defaults={"cargo": cargo, "texto": texto, "foto_url": foto, "orden": orden},
            )

        self.stdout.write(self.style.SUCCESS("Datos de demostración cargados correctamente."))
