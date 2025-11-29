from core.Persistencia.DB_manager import DB_Manager
from datetime import datetime
from core import models

class MateriaEventoValidator:

    def semestre_valido(self, semestre):
        try:
            semestre = int(semestre)
            return 1 <= semestre <= 10
        except (ValueError, TypeError):
            return False
    
    def prioridad_valida(self, prioridad):
        try:
            prioridad = int(prioridad)
            return 1 <= prioridad <= 3
        except (ValueError, TypeError):
            return False
    
    def ingreso_nombre(self, nombre):
        return nombre is not None and nombre.strip() != ''
    
    def dia_valido(self, dia):
        dias_validos = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return dia in dias_validos

    def hora_valida(self, hora_inicio, hora_fin):
        if hora_inicio is None or hora_fin is None or hora_inicio == '' or hora_fin == '':
            return False
        try:
            inicio = datetime.strptime(hora_inicio, '%H:%M')
            fin = datetime.strptime(hora_fin, '%H:%M')
            return inicio < fin
        except ValueError:
            return False

    def fecha_hora_valida(self, fecha_hora_inicio, fecha_hora_fin):
        if fecha_hora_inicio is None or fecha_hora_fin is None or fecha_hora_inicio == '' or fecha_hora_fin == '':
            return False
        
        inicio = datetime.fromisoformat(fecha_hora_inicio)
        fin = datetime.fromisoformat(fecha_hora_fin)

        if inicio < datetime.now():
            return False
        return inicio < fin

class AreaPrivada:
    def __init__(self, user):
        self.user = user
        self.db= DB_Manager()
        self.validator = MateriaEventoValidator()


    def crear_materia(self, data:dict):
        dia = data.get('day')
        hora_inicio = data.get('start')
        hora_fin = data.get('end')

        errors = {}

        if not self.validator.ingreso_nombre(data.get('nombre_materia')):
            errors['nombre_materia'] = 'Ingresa un nombre para la materia.'

        if not self.validator.semestre_valido(data.get('semestre')):
            errors['semestre'] = 'Ingresa un semestre.'

        if not self.validator.prioridad_valida(data.get('prioridad')):
            errors['prioridad'] = 'Selecciona una prioridad.'

        if not self.validator.dia_valido(dia):
            errors['day'] = 'Selecciona un día.'

        if not self.validator.hora_valida(hora_inicio, hora_fin):
            errors['time'] = 'Ingresa un horario válido, ' \
            'recuerda que la hora de inicio debe ser menor a la de fin.'
        
        if errors:
            return False, errors

        self.db.create_materia(
            id_usuario=self.user,
            nombre_materia=data.get('nombre_materia'),
            semestre=int(data.get('semestre')),
            horario_materia=f"{dia} {hora_inicio}-{hora_fin}",
            prioridad=int(data.get('prioridad')),
            estado_materia='Cursando'
        )

        return True, {}

    def crear_evento(self, data: dict):

        fecha_hora_inicio_str = data.get('fecha_hora_inicio')
        fecha_hora_fin_str = data.get('fecha_hora_fin')

        errors = {}

        if not self.validator.ingreso_nombre(data.get('nombre_evento')):
            errors['nombre_evento'] = 'Ingresa un nombre para el evento.'

        if not self.validator.prioridad_valida(data.get('prioridad')):
            errors['prioridad'] = 'Selecciona una prioridad.'

        if not self.validator.fecha_hora_valida(fecha_hora_inicio_str, fecha_hora_fin_str):
            errors['time_fecha'] = 'Ingresa una fecha válida, ' \
            'recuerda que la fecha de inicio debe ser menor a la de fin.'

        if errors:
            return False, errors

        fecha_hora_inicio = datetime.fromisoformat(fecha_hora_inicio_str)
        fecha_hora_fin = datetime.fromisoformat(fecha_hora_fin_str)

        self.db.create_evento_calendario(
            id_usuario=self.user,
            id_materia=None,
            nombre_evento=data.get('nombre_evento'),
            fecha_hora_inicio=fecha_hora_inicio,
            fecha_hora_fin=fecha_hora_fin,
            prioridad=int(data.get('prioridad'))
        )

        return True, {}

    def get_calendar_data(self, id_usuario):

        uid = id_usuario

        materias_qs = self.db.get_materias_by_usuario(uid)
        eventos_qs = self.db.get_eventos_by_usuario(uid)

        materias = []
        for m in materias_qs:
            materias.append({
                'id': str(m.id),
                'name': m.nombre_materia,
                'horario': m.horario_materia,
                'prioridad': m.prioridad,
                'type': 'materia'
            })

        eventos = []
        for e in eventos_qs:
            eventos.append({
                'id': str(e.id),
                'name': e.nombre_evento,
                'start': e.fecha_hora_inicio.isoformat() if e.fecha_hora_inicio else None,
                'end': e.fecha_hora_fin.isoformat() if e.fecha_hora_fin else None,
                'prioridad': e.prioridad,
                'type': 'evento'
            })

        return {'materias': materias, 'eventos': eventos}
    
    def eliminar_elementos(self,idelemento, tipoelemento):
        if tipoelemento == "evento":
            self.db.delete(models.EventoCalendario, "id", idelemento)
        else:
            self.db.delete(models.Materia, "id", idelemento)
        
