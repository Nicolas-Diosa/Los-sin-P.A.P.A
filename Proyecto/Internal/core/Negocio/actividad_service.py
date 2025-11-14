from datetime import datetime
from core.Persistencia.DB_manager import DB_Manager
import datetime


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
        if not datos.get('nombre_actividad'):
            raise ValueError("El nombre de la actividad es obligatorio.")
        if not datos.get('fecha_hora_inicio'):
            raise ValueError("La fecha de inicio es obligatoria.")

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
