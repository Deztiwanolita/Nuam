from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Calificacion
from .forms import CalificacionForm
from django.contrib.auth.models import User


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
    lista = User.objects.all()
    return render(request, "usuarios.html", {"usuarios": lista})

@login_required
def configuracion(request):
    return render(request, "config.html")