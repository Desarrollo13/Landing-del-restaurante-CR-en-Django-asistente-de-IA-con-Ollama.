from django.db import models


class ImagenGaleria(models.Model):
    titulo = models.CharField("Título", max_length=120, blank=True)
    imagen = models.ImageField(
        "Imagen (archivo)",
        upload_to="galeria/",
        blank=True,
        help_text="Sube una imagen desde tu equipo.",
    )
    imagen_url = models.URLField(
        "Imagen (URL alternativa)",
        max_length=500,
        blank=True,
        help_text="O pega un enlace a la imagen (por ejemplo, de Unsplash).",
    )
    orden = models.PositiveSmallIntegerField("Orden", default=0)
    activa = models.BooleanField("Activa", default=True)
    creada = models.DateTimeField("Creada", auto_now_add=True)

    class Meta:
        ordering = ["orden", "-creada"]
        verbose_name = "Imagen de galería"
        verbose_name_plural = "Imágenes de galería"

    def __str__(self):
        return self.titulo or f"Imagen #{self.pk}"

    @property
    def imagen_src(self):
        if self.imagen:
            return self.imagen.url
        return self.imagen_url

    def clean(self):
        from django.core.exceptions import ValidationError

        if not self.imagen and not self.imagen_url:
            raise ValidationError("Debes subir una imagen o indicar una URL.")
