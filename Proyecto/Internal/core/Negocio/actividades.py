from core.Persistencia.DB_manager import DB_Manager
from core.models import Actividad
from django.db.models import Count
from django.utils import timezone


def actividad_disponible(actividad: Actividad) -> bool:
    """Devuelve True si la actividad tiene fecha_hora_inicio en el futuro.

    Parámetros:
    - actividad: instancia de `Actividad` (puede ser un objeto de queryset o None)

    """
    if not actividad:
        return False
    inicio = getattr(actividad, 'fecha_hora_inicio', None)
    if not inicio:
        return False
    return inicio > timezone.now()


def listar_actividades_conteo():

    db = DB_Manager()
    qs = db.read_all(Actividad)
    ids = [a.id for a in qs if actividad_disponible(a)]
    qs = qs.filter(id__in=ids)
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
        qs = qs.annotate(participantes_count=Count('participanteactividad__id_actividad'))
        return qs.first()
    except Exception:
        return None
    

