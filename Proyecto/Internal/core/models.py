from django.db import models
import uuid

# ===========================
#  MODELO: USUARIOS
# ===========================
class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_usuario = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=255, unique=True)
    contrasena = models.CharField(max_length=255)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=280, blank=True, null=True)
    foto_perfil = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


# ===========================
#  MODELO: ACTIVIDADES
# ===========================
class Actividad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_creador = models.ForeignKey('Usuario', on_delete=models.CASCADE, db_column='id_creador')
    nombre_actividad = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=40, blank=True, null=True)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(blank=True, null=True)
    cupos = models.IntegerField(blank=True, null=True)
    foto_actividad = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    fecha_hora_creacion = models.DateTimeField()
    fecha_hora_actualizacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'actividades'


# ===========================
#  MODELO: PARTICIPANTES ACTIVIDAD
# ===========================
class ParticipanteActividad(models.Model):
    id_actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, db_column='id_actividad', primary_key=True)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, db_column='id_usuario')
    hora_llegada = models.DateTimeField(blank=True, null=True)
    hora_salida = models.DateTimeField(blank=True, null=True)
    estado_participante = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'participantes_actividad'
        unique_together = (('id_actividad', 'id_usuario'),)

# ===========================
#  MODELO: MATERIAS
# ===========================
class Materia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, db_column='id_usuario')
    nombre_materia = models.CharField(max_length=80)
    semestre = models.IntegerField(blank=True, null=True)
    horario_materia = models.TextField(blank=True, null=True)
    prioridad = models.IntegerField(blank=True, null=True)
    estado_materia = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materias'


# ===========================
#  MODELO: EVENTOS CALENDARIO
# ===========================
class EventoCalendario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, db_column='id_usuario')
    id_materia = models.ForeignKey('Materia', on_delete=models.SET_NULL, db_column='id_materia', blank=True, null=True)
    nombre_evento = models.CharField(max_length=120)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    prioridad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eventos_calendario'


# ===========================
#  MODELO: TAREAS
# ===========================
class Tarea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, db_column='id_usuario')
    id_materia = models.ForeignKey('Materia', on_delete=models.SET_NULL, db_column='id_materia', blank=True, null=True)
    nombre_tarea = models.CharField(max_length=120)
    descripcion_tarea = models.CharField(max_length=280, blank=True, null=True)
    prioridad = models.IntegerField(blank=True, null=True)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)
    es_recurrente = models.BooleanField(default=False)
    recurrencia = models.TextField(blank=True, null=True)
    estado_tarea = models.CharField(max_length=12, blank=True, null=True)
    creacion_tarea = models.DateTimeField()
    completada_en = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tareas'


# ===========================
#  MODELO: CHATS
# ===========================
class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE, db_column='id_actividad', unique=True)
    id_emisor = models.ForeignKey('Usuario', on_delete=models.CASCADE, db_column='id_emisor')
    contenido = models.TextField()
    hora_creacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'chats'
