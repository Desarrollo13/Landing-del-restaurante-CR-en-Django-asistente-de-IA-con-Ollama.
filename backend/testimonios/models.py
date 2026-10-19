from django.db import models


class Testimonio(models.Model):
    nombre = models.CharField("Nombre", max_length=120)
    cargo = models.CharField("Cargo o relación", max_length=120, blank=True)
    texto = models.TextField("Testimonio")
    foto = models.ImageField(
        "Foto (archivo)",
        upload_to="testimonios/",
        blank=True,
        help_text="Sube una foto desde tu equipo.",
    )
    foto_url = models.URLField(
        "Foto (URL alternativa)",
        max_length=500,
        blank=True,
        help_text="O pega un enlace a la foto.",
    )
    activo = models.BooleanField("Activo", default=True)
    orden = models.PositiveSmallIntegerField("Orden", default=0)
    creado = models.DateTimeField("Creado", auto_now_add=True)

    class Meta:
        ordering = ["orden", "-creado"]
        verbose_name = "Testimonio"
        verbose_name_plural = "Testimonios"

    def __str__(self):
        return self.nombre

    @property
    def foto_src(self):
        if self.foto:
            return self.foto.url
        return self.foto_url
