from django.contrib import admin
from .models import Instrumento, Calificacion

@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'mercado')

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('instrumento', 'periodo', 'monto', 'factor', 'usuario_creacion', 'fecha')
    list_filter = ('periodo', 'instrumento')