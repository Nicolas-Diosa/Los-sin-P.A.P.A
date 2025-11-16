from core.Persistencia.DB_manager import DB_Manager
from datetime import datetime

class AreaPrivada:
    def __init__(self, user):
        self.user = user
        self.db= DB_Manager()


    def crear_materia(self, data):
        dia = data.get('day')
        hora_inicio = data.get('start')
        hora_fin = data.get('end')

        self.db.create_materia(
            id_usuario=self.user,
            nombre_materia=data.get('nombre_materia'),
            semestre=int(data.get('semestre')),
            horario_materia=f"{dia} {hora_inicio}-{hora_fin}",
            prioridad=int(data.get('prioridad')),
            estado_materia='Cursando'
        )

    def crear_evento(self, data):

        fecha_hora_inicio_str = data.get('fecha_hora_inicio')
        fecha_hora_fin_str = data.get('fecha_hora_fin')

        # Convertir a objetos datetime
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
