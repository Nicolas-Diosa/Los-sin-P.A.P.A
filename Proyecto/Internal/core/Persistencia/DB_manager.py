from core.models import Usuario, Actividad, ParticipanteActividad, Materia, EventoCalendario, Tarea, Chat
from django.db.models import Model


class DB_Manager:
    instancia = None

    def __new__(cls):
        if cls.instancia is None:
            cls.instancia = super().__new__(cls)  # Crea el objeto volviendo a la superclase object y a su método new que es el que instancia la clase
        return cls.instancia

    '''INICIO CREATE'''

    def create_usuario(cls, nombre_usuario, email, contrasena, nombre, bio, foto_perfil):
        Usuario.objects.create(nombre_usuario=nombre_usuario, email=email, contrasena=contrasena, nombre=nombre, bio=bio, foto_perfil=foto_perfil)

    def create_actividad(cls, id_creador, nombre_actividad, descripcion, categoria, ubicacion, lat, lng, fecha_hora_inicio, fecha_hora_fin, cupos, foto_actividad, estado, fecha_hora_creacion, fecha_hora_actualizacion):
        Actividad.objects.create(id_creador=id_creador, nombre_actividad=nombre_actividad, descripcion=descripcion, categoria=categoria, ubicacion=ubicacion, lat=lat, lng=lng, fecha_hora_inicio=fecha_hora_inicio, fecha_hora_fin=fecha_hora_fin, cupos=cupos, foto_actividad=foto_actividad, estado=estado, fecha_hora_creacion=fecha_hora_creacion, fecha_hora_actualizacion=fecha_hora_actualizacion)

    def create_part_actividad(cls, id_actividad, id_usuario, hora_llegada, hora_salida, estado_participante):
        ParticipanteActividad.objects.create(id_actividad=id_actividad, id_usuario=id_usuario, hora_llegada=hora_llegada, hora_salida=hora_salida, estado_participante=estado_participante)

    def create_materia(cls, id_usuario, nombre_materia, semestre, horario_materia, prioridad, estado_materia):
        Materia.objects.create(id_usuario=id_usuario, nombre_materia=nombre_materia, semestre=semestre, horario_materia=horario_materia, prioridad=prioridad, estado_materia=estado_materia)

    def create_evento_calendario(cls, id_usuario, id_materia, nombre_evento, fecha_hora_inicio, fecha_hora_fin, prioridad):
        EventoCalendario.objects.create(id_usuario=id_usuario, id_materia=id_materia, nombre_evento=nombre_evento, fecha_hora_inicio=fecha_hora_inicio, fecha_hora_fin=fecha_hora_fin, prioridad=prioridad)

    def create_tarea(cls, id_usuario, id_materia, nombre_tarea, descripcion_tarea, prioridad, fecha_vencimiento, es_recurrente, recurrencia, estado_tarea, creacion_tarea, completada_en):
        Tarea.objects.create(id_usuario=id_usuario, id_materia=id_materia, nombre_tarea=nombre_tarea, descripcion_tarea=descripcion_tarea, prioridad=prioridad, fecha_vencimiento=fecha_vencimiento, es_recurrente=es_recurrente, recurrencia=recurrencia, estado_tarea=estado_tarea, creacion_tarea=creacion_tarea, completada_en=completada_en)

    def create_chat(cls, id_actividad, id_emisor, contenido, hora_creacion):
        Chat.objects.create(id_actividad=id_actividad, id_emisor=id_emisor, contenido=contenido, hora_creacion=hora_creacion)

    '''INICIO READ'''

    def read_all(cls, tabla: Model):
        return tabla.objects.all()

    # -------------------- USUARIOS -------------------

    def get_usuario_by_nombre_usuario(cls, nombre_usuario):
        return Usuario.objects.get(nombre_usuario=nombre_usuario)

    def get_usuario_by_email(cls, email):
        return Usuario.objects.get(email=email)
    
    def get_usuario_by_id(self, id_usuario):
        return Usuario.objects.get(id=id_usuario)

    # -------------------- ACTIVIDADES --------------------

    def get_actividad_by_nombre_actividad(cls, nombre_actividad):
        return Actividad.objects.get(nombre_actividad=nombre_actividad)


    # -------------------- PARTICIPANTES ACTIVIDAD --------------------

    def get_participante_actividad(cls, id_actividad, id_usuario):
        return ParticipanteActividad.objects.get(id_actividad=id_actividad, id_usuario=id_usuario)


    # -------------------- MATERIAS --------------------

    def get_materia_by_nombre_materia(cls, nombre_materia):
        return Materia.objects.get(nombre_materia=nombre_materia)

    def get_materias_by_usuario(self, id_usuario):
        return Materia.objects.filter(id_usuario=id_usuario)
    
    def get_materia_by_id(self, id_materia):
        return Materia.objects.get(id=id_materia)


    # -------------------- EVENTOS CALENDARIO --------------------

    def get_evento_calendario_by_nombre_evento(cls, nombre_evento):
        return EventoCalendario.objects.get(nombre_evento=nombre_evento)

    def get_eventos_by_usuario(self, id_usuario):
        return EventoCalendario.objects.filter(id_usuario=id_usuario)


    # -------------------- TAREAS --------------------

    def get_tarea_by_nombre_tarea(cls, nombre_tarea):
        return Tarea.objects.get(nombre_tarea=nombre_tarea)


    # -------------------- CHATS --------------------
    def get_chat_by_id_actividad(cls, id_actividad):
        return Chat.objects.get(id_actividad=id_actividad)


    '''INICIO UPDATE'''


    def update(cls, tabla: Model, campo, valor, **kwargs):
        tabla.objects.filter(**{campo: valor}).update(**kwargs)


    '''INICIO DELETE'''


    def delete(cls, tabla: Model, campo, valor):
        tabla.objects.filter(**{campo: valor}).delete()
