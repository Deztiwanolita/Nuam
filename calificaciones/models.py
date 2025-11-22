from django.db import models

from django.contrib.auth.models import User


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
        # Calcular factor: monto / 100 como ejemplo
        self.factor = self.monto / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.instrumento} – {self.periodo}"
