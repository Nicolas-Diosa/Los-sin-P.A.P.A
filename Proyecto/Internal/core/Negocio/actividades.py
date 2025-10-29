from core.Persistencia.DB_manager import DB_Manager
from core.models import Actividad, Usuario
from django.db.models import Count


def listar_actividades_conteo():

    db = DB_Manager()
    qs = db.read_all(Actividad)
    qs = qs.annotate(participantes_count=Count('participanteactividad__id_actividad'))
    return qs


def obtener_usuario_por_id(user_id):
    """Intenta recuperar un Usuario por su id (UUID). Devuelve None si no existe."""
    if not user_id:
        return None
    try:
        db = DB_Manager()
        return db.read_all(Usuario).filter(id=user_id).first()
    except Exception:
        return None
