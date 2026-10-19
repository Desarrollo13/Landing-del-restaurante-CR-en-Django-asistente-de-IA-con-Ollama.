from django.db import models


class Categoria(models.Model):
    nombre = models.CharField("Nombre", max_length=80, unique=True)
    descripcion = models.CharField("Descripción", max_length=200, blank=True)
    orden = models.PositiveSmallIntegerField("Orden", default=0)
    activa = models.BooleanField("Activa", default=True)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Plato(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="platos",
        verbose_name="Categoría",
    )
    nombre = models.CharField("Nombre", max_length=120)
    descripcion = models.TextField("Descripción", blank=True)
    precio = models.DecimalField("Precio", max_digits=8, decimal_places=2)
    imagen = models.ImageField(
        "Imagen (archivo)",
        upload_to="platos/",
        blank=True,
        help_text="Sube una imagen desde tu equipo.",
    )
    imagen_url = models.URLField(
        "Imagen (URL alternativa)",
        max_length=500,
        blank=True,
        help_text="O pega un enlace a la imagen (por ejemplo, de Unsplash).",
    )
    destacado = models.BooleanField("Destacado", default=False)
    disponible = models.BooleanField("Disponible", default=True)

    # Datos para el asistente de IA / información saludable
    calorias = models.PositiveIntegerField("Calorías (aprox.)", null=True, blank=True)
    es_vegetariano = models.BooleanField("Vegetariano", default=False)
    es_vegano = models.BooleanField("Vegano", default=False)
    sin_gluten = models.BooleanField("Sin gluten", default=False)
    alergenos = models.CharField(
        "Alérgenos",
        max_length=200,
        blank=True,
        help_text="Separados por comas. Ej: gluten, lactosa, frutos secos.",
    )
    etiquetas = models.CharField(
        "Etiquetas",
        max_length=200,
        blank=True,
        help_text="Separadas por comas. Ej: ligero, alto en proteína, picante.",
    )

    orden = models.PositiveSmallIntegerField("Orden", default=0)
    creado = models.DateTimeField("Creado", auto_now_add=True)

    class Meta:
        ordering = ["orden", "nombre"]
        verbose_name = "Plato"
        verbose_name_plural = "Platos"

    def __str__(self):
        return f"{self.nombre} ({self.precio} €)"

    @property
    def imagen_src(self):
        if self.imagen:
            return self.imagen.url
        return self.imagen_url
