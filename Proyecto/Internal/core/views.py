from django.shortcuts import render, get_object_or_404, redirect
from core.Negocio.auth import *
from core.Negocio.actividades import listar_actividades_conteo
from django.db.models import Count
from core.Persistencia.DB_manager import DB_Manager
from core.Negocio.actividades import obtener_detalle_actividad
from django.http import Http404
from django.utils import timezone
from core.models import Usuario, Actividad
from core.Negocio.actividad_service import ActividadService
from datetime import datetime
from core.Negocio.materias_eventos import AreaPrivada
import json

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
            return render(request, 'core/login.html', {'errors': errors})


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
    service = AreaPrivada(usuario)

    data = service.get_calendar_data(usuario)
    materias_data = data['materias']
    eventos_data = data['eventos']

    return render(request, 'core/area_privada.html', {
        'materias_json': json.dumps(materias_data),
        'eventos_json': json.dumps(eventos_data),
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
    
    db = DB_Manager()
    actividad = Actividad.objects.get(id=actividad_id)
    usuario = db.get_usuario_by_nombre_usuario(request.session['username'])

    if request.method == 'POST':
        hora_llegada = request.POST.get('hora_llegada')
        hora_salida = request.POST.get('hora_salida')

        if not hora_llegada or not hora_salida:
            return render(request, 'core/registrar_asistencia.html', {
                'actividad': actividad,
                'error': 'Debe ingresar ambas horas (llegada y salida).'
            })

        try:

            fecha_base = actividad.fecha_hora_inicio.date()
            hora_llegada_dt = timezone.make_aware(
                datetime.combine(fecha_base, datetime.strptime(hora_llegada, '%H:%M').time()),
                timezone.get_current_timezone()
            )
            hora_salida_dt = timezone.make_aware(
                datetime.combine(fecha_base, datetime.strptime(hora_salida, '%H:%M').time()),
                timezone.get_current_timezone()
            )
        except ValueError:
            return render(request, 'core/registrar_asistencia.html', {
                'actividad': actividad,
                'error': 'Formato de hora inválido. Use HH:MM.'
            })

        if hora_llegada_dt >= hora_salida_dt:
            return render(request, 'core/registrar_asistencia.html', {
                'actividad': actividad,
                'error': 'La hora de salida debe ser posterior a la hora de llegada.'
            })

        inicio_actividad = actividad.fecha_hora_inicio
        fin_actividad = actividad.fecha_hora_fin or actividad.fecha_hora_inicio.replace(hour=23, minute=59)

        inicio_actividad = timezone.make_aware(inicio_actividad, timezone.get_current_timezone()) if timezone.is_naive(inicio_actividad) else inicio_actividad
        fin_actividad = timezone.make_aware(fin_actividad, timezone.get_current_timezone()) if timezone.is_naive(fin_actividad) else fin_actividad

        if not (inicio_actividad <= hora_llegada_dt <= fin_actividad and inicio_actividad <= hora_salida_dt <= fin_actividad):
            return render(request, 'core/registrar_asistencia.html', {
                'actividad': actividad,
                'error': f'El rango permitido es entre {inicio_actividad.strftime("%H:%M")} y {fin_actividad.strftime("%H:%M")}.'
            })

        db.create_part_actividad(
            id_actividad=actividad,
            id_usuario=usuario,
            hora_llegada=hora_llegada_dt,
            hora_salida=hora_salida_dt,
            estado_participante="Registrado"
        )

        return render(request, 'core/asistencia_registrada.html', {'actividad': actividad})

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
        service.crear_evento(request.POST)
        return redirect('/area_privada/')

    return render(request, 'core/agregar_evento.html')

def agregar_materia(request):
    if not request.session.get('inicio_sesion'):
        return redirect('login')

    usuario = Auth.obtener_usuario_desde_sesion(request)
    service = AreaPrivada(usuario)

    if request.method == 'POST':
        service.crear_materia(request.POST)
        return redirect('/area_privada/')

    return render(request, 'core/agregar_materia.html')
