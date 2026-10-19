from django.db import models


class Reserva(models.Model):
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_CONFIRMADA = "confirmada"
    ESTADO_CANCELADA = "cancelada"
    ESTADOS = [
        (ESTADO_PENDIENTE, "Pendiente"),
        (ESTADO_CONFIRMADA, "Confirmada"),
        (ESTADO_CANCELADA, "Cancelada"),
    ]

    nombre = models.CharField("Nombre", max_length=120)
    correo = models.EmailField("Correo electrónico")
    telefono = models.CharField("Teléfono", max_length=30, blank=True)
    fecha = models.DateField("Fecha")
    hora = models.TimeField("Hora", null=True, blank=True)
    comensales = models.PositiveSmallIntegerField("Comensales")
    mensaje = models.TextField("Mensaje", blank=True)
    estado = models.CharField("Estado", max_length=12, choices=ESTADOS, default=ESTADO_PENDIENTE)
    creada = models.DateTimeField("Creada", auto_now_add=True)

    class Meta:
        ordering = ["-creada"]
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def __str__(self):
        return f"{self.nombre} · {self.fecha} · {self.comensales} pax"
