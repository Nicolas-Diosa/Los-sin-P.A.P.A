from core.Persistencia.DB_manager import DB_Manager
from core.models import Actividad
from django.db.models import Count


def listar_actividades_conteo():

    db = DB_Manager()
    qs = db.read_all(Actividad)
    qs = qs.annotate(participantes_count=Count('participanteactividad__id_actividad'))
    return qs


def obtener_detalle_actividad(actividad_id):
    """Devuelve la actividad con id `actividad_id` anotada con participantes_count.
    Retorna None si no existe.
    """
    if not actividad_id:
        return None
    try:
        db = DB_Manager()
        qs = db.read_all(Actividad).filter(id=actividad_id)
        qs = qs.annotate(participantes_count=Count('participanteactividad__id_usuario'))
        return qs.first()
    except Exception:
        return None
