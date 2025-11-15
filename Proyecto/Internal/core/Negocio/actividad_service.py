from datetime import datetime
from core.Persistencia.DB_manager import DB_Manager
import datetime

def validar_nombre_actividad(nombre: str) -> bool:
    if not nombre or len(nombre.strip()) < 3:
        return False
   
    # Al menos una letra
    if not any(c.isalpha() for c in nombre):
        return False

    return True

def validar_cupos(cupos_raw):
    """Valida el número de cupos."""
    if cupos_raw in ["", None]:
        return False
    
    try:
        cupos = int(cupos_raw)
    except ValueError:
        return False
    
    if cupos < 0:
        return False
    
    return True


class ActividadService:
    """Capa de negocio para manejar la lógica de actividades."""
    def crear_actividad(self, request, datos, foto=None):
        """Crea una nueva actividad validando los datos antes de guardarla."""
        db = DB_Manager()
        # Buscar el usuario (creador)
        try:
            creador = db.get_usuario_by_nombre_usuario(request.session['username'])
        except db.get_usuario_by_nombre_usuario(request.session['username']).DoesNotExist:
            raise ValueError("Usuario no encontrado en la base de datos.")

        # Validaciones
        nombre = datos.get('nombre_actividad', '')

        if not validar_nombre_actividad(nombre):
            raise ValueError("El nombre de la actividad no es válido.")

        fecha_inicio_raw = datos.get('fecha_hora_inicio')
        fecha_fin_raw = datos.get('fecha_hora_fin')

        if not fecha_inicio_raw:
            raise ValueError("La fecha de inicio es obligatoria.")

        if not fecha_fin_raw:
            raise ValueError("La fecha de fin es obligatoria.")

        try:
            fecha_inicio = datetime.datetime.fromisoformat(fecha_inicio_raw)
            fecha_fin = datetime.datetime.fromisoformat(fecha_fin_raw)
        except Exception:
            raise ValueError("Las fechas deben estar en formato ISO YYYY-MM-DDTHH:MM.")

        if fecha_fin <= fecha_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio.")
        
        cupos_raw = datos.get('cupos')

        if not validar_cupos(cupos_raw):
            raise ValueError("Los cupos deben ser un entero mayor o igual a 0.")

        cupos = int(cupos_raw)

        # Guardar actividad
        actividad = db.create_actividad(
            id_creador=creador,
            nombre_actividad=datos['nombre_actividad'],
            descripcion=datos.get('descripcion', ''),
            categoria=datos.get('categoria', ''),
            ubicacion=datos.get('ubicacion', ''),
            lat=0,
            lng=0,
            fecha_hora_inicio=datos['fecha_hora_inicio'],
            fecha_hora_fin=datos.get('fecha_hora_fin'),
            cupos=datos.get('cupos') or 0,
            foto_actividad=foto.name if foto else '',
            estado='Activa',
            fecha_hora_creacion=datetime.datetime.now(),
            fecha_hora_actualizacion=datetime.datetime.now(),
        )

        return actividad
