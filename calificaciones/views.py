from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Calificacion, Bitacora
from .forms import CalificacionForm
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone




@login_required
def dashboard(request):
    return render(request, "dashboard.html")

def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST["username"],
                            password=request.POST["password"])
        if user:
            login(request, user)
            return redirect("lista")
        else:
            messages.error(request, "⚠️ Credenciales incorrectas")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def lista(request):
    calificaciones = Calificacion.objects.all().order_by('-fecha')
    return render(request, "calificaciones/lista.html", {"calificaciones": calificaciones})


@login_required
def crear(request):
    if request.method == "POST":
        form = CalificacionForm(request.POST)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.usuario_creacion = request.user
            nueva.save()
            messages.success(request, "Calificación guardada")
            return redirect("lista")
    else:
        form = CalificacionForm()
    return render(request, "calificaciones/crear.html", {"form": form})

@login_required
def auditoria(request):
    registros = Calificacion.objects.all().order_by('-fecha')
    return render(request, "auditoria.html", {"registros": registros})

@login_required
def usuarios(request):
    usuarios = User.objects.all().order_by('username')
    return render(request, "usuarios.html", {"usuarios": usuarios})

@login_required
def configuracion(request):
    return render(request, "config.html")

@login_required
def reportes(request):
    # Totales generales
    total_calificaciones = Calificacion.objects.count()
    
    # Filtrado por mes actual
    mes_actual = timezone.now().month
    calificaciones_mes = Calificacion.objects.filter(fecha__month=mes_actual).count()
    
    # Resumen por instrumento
    resumen = (Calificacion.objects
               .values('instrumento__nombre')
               .annotate(total=Count('id'), monto_total=Sum('monto'))
               .order_by('-total'))
    
    contexto = {
        'total_calificaciones': total_calificaciones,
        'calificaciones_mes': calificaciones_mes,
        'resumen': resumen,
    }
    return render(request, "reportes.html", contexto)

@login_required
def ver_bitacora(request):
    registros = Bitacora.objects.all().order_by("-fecha")
    return render(request, "ver_bitacora.html", {"registros": registros})