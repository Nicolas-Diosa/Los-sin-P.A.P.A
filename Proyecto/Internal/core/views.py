from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from core.Negocio.auth import *
from .forms import CustomUserCreationForm
from .models import Actividad, Usuario, ParticipanteActividad
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
    """Renderiza la plantilla de actividades mostrando el usuario activo y las actividades de la BD.

    Comportamiento razonable cuando no hay sistema de auth completo:
    - intenta obtener `user_id` o `username` desde la sesión
    - si encuentra un usuario en la BD muestra su nombre, si no, muestra 'Invitado'
    - lista todas las actividades ordenadas por fecha de inicio y añade conteo de participantes
    """
    # Determinar nombre del usuario
    username = None
    user = None
    # posibles claves de sesión que podrían usarse en este proyecto
    for key in ('user_id', 'id_usuario', 'usuario_id'):
        if request.session.get(key):
            try:
                user = Usuario.objects.filter(id=request.session.get(key)).first()
            except Exception:
                user = None
            break
    # si no se obtuvo por id, buscar nombre en sesión
    if not user:
        username = request.session.get('username') or request.session.get('nombre_usuario')
    else:
        username = user.nombre or user.nombre_usuario

    if not username:
        username = 'Invitado'

    # Consultar actividades y contar participantes
    actividades = Actividad.objects.all().order_by('fecha_hora_inicio')
    # añadir conteo de participantes por actividad
    # Nota: la tabla participantes_actividad no tiene columna 'id' en la BD legacy,
    # por eso evitamos que Django intente contar por la PK implícita y en su lugar
    # contamos las filas usando la columna existente 'id_usuario'.
    actividades = actividades.annotate(participantes_count=Count('participanteactividad__id_actividad'))

    return render(request, 'core/ver_actividades.html', {
        'username': username,
        'actividades': actividades,
    })