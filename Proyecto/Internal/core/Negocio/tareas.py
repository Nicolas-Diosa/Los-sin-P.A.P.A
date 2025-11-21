from core.Persistencia.DB_manager import DB_Manager
from datetime import datetime
import re


# ========== FUNCIONES DE VALIDACIÓN ==========

def descripcion_valida(descripcion):
    """Valida que la descripción tenga entre 0 y 280 caracteres."""
    if descripcion is None:
        return True
    if not isinstance(descripcion, str):
        return False
    return 0 <= len(descripcion) <= 280


def fecha_valida(fecha):
    """Valida que la fecha sea futura."""
    if isinstance(fecha, datetime):
        return fecha > datetime.now()
    
    return False


def icalendar_valido(texto):
    """
    Valida formato básico de iCalendar RRULE.
    Ejemplo: FREQ=DAILY;INTERVAL=1 o FREQ=WEEKLY;BYDAY=MO,WE
    """
    if not texto:
        return False
    
    # Patrón básico: debe empezar con FREQ= seguido de valores válidos
    patron = r'^FREQ=(DAILY|WEEKLY|MONTHLY|YEARLY)(;[A-Z]+=[A-Z0-9,]+)*$'
    
    return bool(re.match(patron, texto))


def estado_valido(estado):
    """Valida que el estado sea uno de los permitidos."""
    estados_validos = ['Por realizar', 'Realizando', 'Realizada']
    return estado in estados_validos


def prioridad_valida(prioridad):
    """Valida que la prioridad sea 1, 2 o 3."""
    if isinstance(prioridad, int):
        return prioridad in [1, 2, 3]
    return False


def validar_datos_tarea(usuario, nombre, descripcion, prioridad, fecha_vencimiento, es_recurrente, recurrencia, estado):
    """
    Valida todos los datos necesarios para crear una tarea.
    Lanza ValueError si alguna validación falla.
    """
    if not usuario:
        raise ValueError("El usuario es obligatorio.")
    
    if not nombre:
        raise ValueError("El nombre de la tarea es obligatorio.")
    
    if not descripcion_valida(descripcion):
        raise ValueError("Descripción inválida (máximo 280 caracteres).")
    
    if not prioridad_valida(prioridad):
        raise ValueError("Prioridad debe ser 1, 2 o 3.")
    
    if not fecha_valida(fecha_vencimiento):
        raise ValueError("La fecha de vencimiento debe ser futura.")
    
    if es_recurrente:
        if not icalendar_valido(recurrencia):
            raise ValueError("Formato de recurrencia iCalendar inválido (ej: FREQ=DAILY;INTERVAL=1).")
    
    if not estado_valido(estado):
        raise ValueError("Estado debe ser: 'Por realizar', 'Realizando' o 'Realizada'.")


# ========== CLASE DE SERVICIO ==========

class TareasService:
    def __init__(self, usuario):
        self.usuario = usuario
        self.db = DB_Manager()

    def obtener_materias_usuario(self):
        """
        Obtiene todas las materias del usuario.
        Retorna una lista de objetos Materia.
        """
        return self.db.get_materias_by_usuario(self.usuario)

    def crear_tarea(self, datos):
        """
        Crea una tarea validando datos mínimos.
        datos: QueryDict del request.POST
        """
        nombre = datos.get("nombre_tarea", "").strip()
        descripcion = datos.get("descripcion_tarea")
        prioridad = int(datos.get("prioridad"))
        fecha_vencimiento = datetime.fromisoformat(datos.get("fecha_vencimiento"))
        es_recurrente = datos.get("es_recurrente") == "on"
        recurrencia = datos.get("recurrencia", "") if es_recurrente else None
        estado = datos.get("estado_tarea")
        
        validar_datos_tarea(self.usuario, nombre, descripcion, prioridad, 
                            fecha_vencimiento, es_recurrente, recurrencia, estado)

        materia_ref = None
        nombre_materia = datos.get("nombre_materia")
        if nombre_materia:
            try:
                materia_ref = self.db.get_materia_by_nombre_materia(nombre_materia)
                if not materia_ref:
                    raise ValueError(f"Materia '{nombre_materia}' no encontrada.")
            except Exception as e:
                raise ValueError(f"Error al buscar materia: {str(e)}")

        self.db.create_tarea(
            id_usuario=self.usuario,
            id_materia=materia_ref,
            nombre_tarea=nombre,
            descripcion_tarea=descripcion,
            prioridad=prioridad,
            fecha_vencimiento=fecha_vencimiento,
            es_recurrente=es_recurrente,
            recurrencia=recurrencia,
            estado_tarea=estado,
            creacion_tarea=datetime.now(),
            completada_en=None
        )
    