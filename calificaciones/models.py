from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Instrumento(models.Model):
    nombre = models.CharField(max_length=80)
    mercado = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.nombre} ({self.mercado})"


class Calificacion(models.Model):
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    factor = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        self.factor = self.monto / 100  # cálculo del factor
        super().save(*args, **kwargs)

        # Registrar acción en bitácora
        from .models import Bitacora
        accion = "CREAR" if es_nuevo else "MODIFICAR"
        Bitacora.objects.create(
            usuario=self.usuario_creacion,
            accion=accion,
            descripcion=f"Calificación {self.instrumento} ({self.periodo}) − monto {self.monto}"
        )

class Bitacora(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.accion} ({self.fecha:%d/%m/%Y %H:%M})"