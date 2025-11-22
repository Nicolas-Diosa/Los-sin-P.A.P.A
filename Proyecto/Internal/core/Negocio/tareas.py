from core.Persistencia.DB_manager import DB_Manager
from datetime import datetime
import re


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
    Retorna un diccionario de errores. Si está vacío, no hay errores.
    """
    errors = {}
    
    if not usuario:
        errors['usuario'] = "El usuario es obligatorio."
    
    if not nombre:
        errors['nombre_tarea'] = "El nombre de la tarea es obligatorio."
    
    if not descripcion_valida(descripcion):
        errors['descripcion_tarea'] = "Descripción inválida (máximo 280 caracteres)."
    
    if not prioridad_valida(prioridad):
        errors['prioridad'] = "Prioridad debe ser 1, 2 o 3."
    
    if not fecha_valida(fecha_vencimiento):
        errors['fecha_vencimiento'] = "La fecha de vencimiento debe ser futura."
    
    if es_recurrente:
        if not icalendar_valido(recurrencia):
            errors['recurrencia'] = "Formato de recurrencia iCalendar inválido (ej: FREQ=DAILY;INTERVAL=1)."
    
    if not estado_valido(estado):
        errors['estado_tarea'] = "Estado debe ser: 'Por realizar', 'Realizando' o 'Realizada'."
    
    return errors


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
        Retorna (success: bool, errors: dict)
        """
        errors = {}
        
        nombre = datos.get("nombre_tarea", "").strip()
        descripcion = datos.get("descripcion_tarea")
        try:
            prioridad = int(datos.get("prioridad"))
        except (TypeError, ValueError):
            prioridad = None
            errors['prioridad'] = "La prioridad debe ser un número válido."
        
        try:
            fecha_vencimiento = datetime.fromisoformat(datos.get("fecha_vencimiento"))
        except (TypeError, ValueError):
            fecha_vencimiento = None
            errors['fecha_vencimiento'] = "La fecha de vencimiento no es válida."
        
        es_recurrente = datos.get("es_recurrente") == "on"
        recurrencia = datos.get("recurrencia", "") if es_recurrente else None
        estado_default = "Por realizar"
        estado = estado_default
        
        if datos.get("id_materia"):
            id_materia = self.db.get_materia_by_id(datos.get("id_materia"))
        else:
            id_materia = None

        validation_errors = validar_datos_tarea(self.usuario, nombre, descripcion, prioridad, 
                            fecha_vencimiento, es_recurrente, recurrencia, estado)
        errors.update(validation_errors)



        if errors:
            return False, errors

        self.db.create_tarea(
            id_usuario=self.usuario,
            id_materia=id_materia,
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
       
        return True, {}
    
    def obtener_tareas_ordenadas_por_realizar(self):

        return self.db.get_tareas_by_usuario(
            usuario=self.usuario,
            estado= "Por realizar",
            order_by=["fecha_vencimiento", "-prioridad"]
        )
    
    def marcar_tarea_como_realizada(self, nombre_tarea):

        try:
            tarea = self.db.get_tarea_by_nombre_tarea(self.usuario, nombre_tarea)
            if tarea.id_usuario != self.usuario:
                return False
            
            tarea.estado_tarea = "Realizada"
            tarea.completada_en = datetime.now()
            tarea.save()
            return True

        except Exception as e:
            print(f"Error al marcar tarea: {e}")
            return False
