from django.shortcuts import render, get_object_or_404, redirect
from core.Negocio.auth import *
from core.Negocio.actividades import listar_actividades_conteo
from django.db.models import Count
from core.Persistencia.DB_manager import DB_Manager
from core.Negocio.actividades import obtener_detalle_actividad
from django.http import Http404
from django.utils import timezone
from core.models import Usuario
from core.Negocio.actividad_service import ActividadService
from .forms import CustomUserCreationForm
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'core/login.html')

    if request.method == 'POST':
        auth_service = Auth(DB_Manager())
        success, errors = auth_service.login_user(request.POST, request)

        if success:
            return redirect('/actividades/')
        else:
            return render(request, 'core/login.html',{'errors':errors})
                                                       
def signup(request):
    if request.method == 'GET':
        return render(request, 'core/signup.html')

    if request.method == 'POST':
        auth_service = Auth(DB_Manager())
        success, errors = auth_service.register_user(request.POST, request)

        if success:
            return render(request, 'core/signup_success.html')
        else:
            return render(request, 'core/signup.html', {'errors': errors})

def ver_actividades(request):
    username = request.session.get('username', 'Invitado')
    actividades = listar_actividades_conteo()

    return render(request, 'core/ver_actividades.html', {
        'username': username,
        'actividades': actividades,
    })

def ver_area_priv(request):
    username = request.session.get('username', 'Invitado')
    actividades = listar_actividades_conteo()

    return render(request, 'core/area_privada.html', {
        'username': username,
        'actividades': actividades,
    })

def logout(request):
    request.session.flush()
    return redirect('home')
def detalles_actividad(request, id):
    """Vista de detalles de actividad. Usa la capa de negocio para obtener datos."""
    actividad = obtener_detalle_actividad(id)
    if not actividad:
        raise Http404('Actividad no encontrada')

    return render(request, 'core/detalles_actividad.html', {
        'actividad': actividad,
        'username': request.session.get('username') or request.session.get('nombre_usuario') or 'Invitado'
    })

def crear_actividad(request):
    service = ActividadService()

    if request.method == "POST":
        datos = {
            'nombre_actividad': request.POST.get('nombre_actividad'),
            'descripcion': request.POST.get('descripcion'),
            'categoria': request.POST.get('categoria'),
            'ubicacion': request.POST.get('ubicacion'),
            'fecha_hora_inicio': request.POST.get('fecha_hora_inicio'),
            'fecha_hora_fin': request.POST.get('fecha_hora_fin'),
            'cupos': request.POST.get('cupos'),
        }
        foto = request.FILES.get('foto_actividad')

        try:
            # ⚠️ Usa un usuario temporal si no hay sesión iniciada
            service.crear_actividad(request, datos=datos,  foto=foto)
            return redirect('actividad_creada')
        except Exception as e:
            return render(request, 'core/crear_actividad.html', {'error': str(e)})

    return render(request, 'core/crear_actividad.html')



def actividad_creada(request):
    return render(request, 'core/actividad_creada.html')