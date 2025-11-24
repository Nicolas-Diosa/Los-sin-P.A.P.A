from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers.json import DjangoJSONEncoder
from core.Negocio.auth import *
from core.Negocio.actividades import listar_actividades_conteo
from django.db.models import Count
from core.Negocio.actividades import obtener_detalle_actividad
from core.Negocio.perfil_service import PerfilService
from core.Negocio.asistencia_service import AsistenciaService
from django.contrib import messages
from django.http import Http404
from django.utils import timezone
from core.models import Usuario, Actividad
from core.Negocio.actividad_service import ActividadService
from datetime import datetime
from core.Negocio.materias_eventos import AreaPrivada
import json
from core.Negocio.tareas import TareasService


# Create your views here.


def home(request):
    return render(request, 'core/home.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'core/login.html')

    if request.method == 'POST':
        auth_service = Auth()
        success, errors = auth_service.login_user(request.POST, request)

        if success:
            return redirect('/actividades/')
        else:
            return render(request, 'core/login.html', {'errors': errors})


def signup(request):
    if request.method == 'GET':
        return render(request, 'core/signup.html')

    if request.method == 'POST':
        auth_service = Auth()
        success, errors = auth_service.register_user(request.POST, request)

        if success:
            return render(request, 'core/signup_success.html')
        else:
            return render(request, 'core/signup.html', {'errors': errors})


def ver_actividades(request):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    username = request.session.get('username', 'Invitado')
    actividades = listar_actividades_conteo()

    return render(request, 'core/ver_actividades.html', {
        'username': username,
        'actividades': actividades,
    })


def ver_area_priv(request):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    usuario = Auth.obtener_usuario_desde_sesion(request)
    tareas = TareasService(usuario).obtener_tareas_ordenadas_por_realizar()
    service = AreaPrivada(usuario)

    data = service.get_calendar_data(usuario)
    materias_data = data['materias']
    eventos_data = data['eventos']

    return render(request, 'core/area_privada.html', {
        'materias_json': json.dumps(materias_data),
        'eventos_json': json.dumps(eventos_data),
        "tareas": tareas,
    })


def logout(request):
    request.session.flush()
    return redirect('home')


def detalles_actividad(request, id):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    """Vista de detalles de actividad. Usa la capa de negocio para obtener datos."""
    actividad = obtener_detalle_actividad(id)
    if not actividad:
        raise Http404('Actividad no encontrada')

    return render(request, 'core/detalles_actividad.html', {
        'actividad': actividad,
        'username': request.session.get('username') or request.session.get('nombre_usuario') or 'Invitado'
    })


def crear_actividad(request):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    service = ActividadService()

    if request.method == "POST":
        fin_raw = (request.POST.get('fecha_hora_fin') or '').strip()
        datos = {
            'nombre_actividad': request.POST.get('nombre_actividad'),
            'descripcion': request.POST.get('descripcion'),
            'categoria': request.POST.get('categoria'),
            'ubicacion': request.POST.get('ubicacion'),
            'fecha_hora_inicio': request.POST.get('fecha_hora_inicio'),
            'fecha_hora_fin': fin_raw or None,
            'cupos': request.POST.get('cupos'),
        }
        foto = request.FILES.get('foto_actividad')

        try:
            # Usa un usuario temporal si no hay sesión iniciada
            service.crear_actividad(request, datos=datos,  foto=foto)
            return redirect('actividad_creada')
        except Exception as e:
            return render(request, 'core/crear_actividad.html', {'error': str(e)})

    return render(request, 'core/crear_actividad.html')


def actividad_creada(request):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    return render(request, 'core/actividad_creada.html')


def registrar_asistencia(request, actividad_id):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    service = AsistenciaService()
    username = request.session.get('username')

    try:
        actividad = Actividad.objects.get(id=actividad_id)
    except Actividad.DoesNotExist:
        raise Http404("Actividad no encontrada.")

    if request.method == 'POST':
        hora_llegada = request.POST.get('hora_llegada')
        hora_salida = request.POST.get('hora_salida')

        try:
            actividad_registrada = service.registrar_asistencia(
                username=username,
                actividad_id=actividad_id,
                hora_llegada_raw=hora_llegada,
                hora_salida_raw=hora_salida
            )

            return redirect('asistencia_registrada', actividad_id=actividad_registrada.id)

        except ValueError as e:
            return render(request, 'core/registrar_asistencia.html', {
                'actividad': actividad,
                'error': str(e),
                'hora_llegada_default': hora_llegada,
                'hora_salida_default': hora_salida
            })

    return render(request, 'core/registrar_asistencia.html', {'actividad': actividad})


def asistencia_registrada(request, actividad_id):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    actividad = get_object_or_404(Actividad, id=actividad_id)
    return render(request, 'core/asistencia_registrada.html', {'actividad': actividad})


def agregar_evento(request):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    usuario = Auth.obtener_usuario_desde_sesion(request)
    service = AreaPrivada(usuario) 

    if request.method == 'POST':
        success, errors = service.crear_evento(request.POST)
        if success:
            return redirect('/area_privada/')
        else:
            return render(request, 'core/agregar_evento.html', {
                'errors': errors
            })

    return render(request, 'core/agregar_evento.html')

def agregar_materia(request):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    usuario = Auth.obtener_usuario_desde_sesion(request)
    service = AreaPrivada(usuario)

    if request.method == 'POST':
        success, errors = service.crear_materia(request.POST)

        if success:
            return redirect('/area_privada/')
        else:
            return render(request, 'core/agregar_materia.html', {
                'errors': errors
            })

    return render(request, 'core/agregar_materia.html')


def ver_perfil(request):
    """Muestra la vista de perfil (solo lectura)."""
    service = PerfilService()
    username = request.session.get('username')
    if not username:
        # no logueado -> redirigir a login
        messages.error(request, "Debe iniciar sesión.")
        return redirect('/login/')

    usuario = service.obtener_usuario(username)
    if not usuario:
        messages.error(request, "Usuario no encontrado.")
        return redirect('/login/')

    return render(request, 'core/perfil.html', {
        'usuario': usuario
    })


def editar_perfil(request):
    """GET: mostrar formulario con datos. POST: validar y guardar."""
    service = PerfilService()
    username = request.session.get('username')
    if not username:
        messages.error(request, "Debe iniciar sesión.")
        return redirect('/login/')

    usuario = service.obtener_usuario(username)
    if not usuario:
        messages.error(request, "Usuario no encontrado.")
        return redirect('/login/')

    if request.method == 'GET':
        return render(request, 'core/editar_perfil.html', {
            'nombre_usuario': usuario.nombre_usuario,
            'bio': usuario.bio or ''
        })

    # POST -> procesar
    nuevo_nombre = request.POST.get('nombre_usuario', '').strip()
    nueva_bio = request.POST.get('bio', '').strip()

    try:
        service.editar_perfil(username, {
            'nombre_usuario': nuevo_nombre,
            'bio': nueva_bio
        })
    except Exception as e:
        # Mostrar error en el formulario
        return render(request, 'core/editar_perfil.html', {
            'nombre_usuario': nuevo_nombre,
            'bio': nueva_bio,
            'error': str(e)
        })

    # si cambió el username, actualizar la sesión
    request.session['username'] = nuevo_nombre
    return redirect('perfil_actualizado')


def perfil_actualizado(request):
    """Página de confirmación después de editar perfil."""
    username = request.session.get('username')
    if not username:
        return redirect('/login/')

    service = PerfilService()
    usuario = service.obtener_usuario(username)
    return render(request, 'core/perfil_actualizado.html', {
        'usuario': usuario
    })


def crear_tarea(request):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    usuario = Auth.obtener_usuario_desde_sesion(request)

    if request.method == 'POST':
        success, errors = TareasService(usuario).crear_tarea(request.POST)

        if success:
            return redirect('/area_privada/')
        else:
            materias = TareasService(usuario).obtener_materias_usuario()
            return render(request, 'core/crear_tarea.html', {
                'materias': materias,
                'errors': errors
            })

    materias = TareasService(usuario).obtener_materias_usuario()
    return render(request, 'core/crear_tarea.html', {
        'materias': materias
    })

def tareas_realizadas(request):
    usuario = Auth.obtener_usuario_desde_sesion(request)
    tareas_realizadas = TareasService(usuario).obtener_tareas_ordenadas_realizadas().values('nombre_tarea','prioridad','completada_en')
    print(tareas_realizadas)
    return render(request, 'core/tarea_realizada.html', {
        "tareas_realizadas": json.dumps(list(tareas_realizadas),cls=DjangoJSONEncoder),
    })


def calendario(request):
    usuario = Auth.obtener_usuario_desde_sesion(request)
    service = AreaPrivada(usuario)
    data = service.get_calendar_data(usuario)
    materias_data = data['materias']
    eventos_data = data['eventos']
    return render(request, 'core/calendario.html', {
        'materias_json': json.dumps(materias_data),
        'eventos_json': json.dumps(eventos_data),
    })

def marcar_tarea(request):
    usuario = Auth.obtener_usuario_desde_sesion(request)

    if request.method == "POST":
        idtarea = request.POST.get('id_tarea')
        success = TareasService(usuario).marcar_tarea_como_realizada(idtarea)
        
        if success:
            return redirect('/area_privada/')

    return redirect('area_privada')



def eventos_y_materias(request):
    usuario = Auth.obtener_usuario_desde_sesion(request)
    service = AreaPrivada(usuario)
    data = service.get_calendar_data(usuario)
    materias_data = data['materias']
    eventos_data = data['eventos']
    elementos = materias_data+eventos_data
    if request.method == "POST":
        idelemento = str(request.POST.get('elemento_a_eliminar'))
        tipoelemento = str(request.POST.get('tipo_elemento'))
        TareasService(usuario).eliminar_tareas_asociadas(idelemento,tipoelemento)
        service.eliminar_elementos(idelemento, tipoelemento)
        return redirect('/materias_y_eventos/')
    return render(request, 'core/evmat.html', {
        'elementos_json': json.dumps(elementos),
    })