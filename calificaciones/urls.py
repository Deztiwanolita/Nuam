from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('calificaciones/', views.lista, name='lista'),
    path('nuevo/', views.crear, name='crear'),
    path('auditoria/', views.auditoria, name='auditoria'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('config/', views.configuracion, name='config'),
    path('reportes/', views.reportes, name='reportes'),
    path('bitacora/', views.ver_bitacora, name='bitacora'),
]