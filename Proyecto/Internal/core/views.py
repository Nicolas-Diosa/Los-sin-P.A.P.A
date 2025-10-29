from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from core.Negocio.auth import *
from core.Negocio.actividades import listar_actividades_conteo, obtener_usuario_por_id
from .forms import CustomUserCreationForm
from .models import Actividad, Usuario
from django.db.models import Count

# Create your views here.

def view_register(request):
    if request.method == 'GET':
        return render(request, 'core/register.html', {
            'form': CustomUserCreationForm
        })
    else:
        return auth.register_user(request=request)
def home(request):
    return render(request, 'core/home.html')


def ver_actividades(request):
    username = 'Juanito'
    actividades = listar_actividades_conteo()

    return render(request, 'core/ver_actividades.html', {
        'username': username,
        'actividades': actividades,
    })