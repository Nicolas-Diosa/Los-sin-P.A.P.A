from core.Persistencia.DB_manager import DB_Manager
from core.models import Actividad, ParticipanteActividad
from datetime import datetime
from django.utils import timezone


class AsistenciaService:
    """Capa de negocio para registrar y validar la asistencia a actividades."""

    def __init__(self):
        self.db = DB_Manager()

    def registrar_asistencia(self, username: str, actividad_id: str, hora_llegada_raw: str, hora_salida_raw: str):
        """
        Valida y registra la asistencia de un usuario a una actividad.
        Lanza ValueError si la validación falla.
        """

        try:
            usuario = self.db.get_usuario_by_nombre_usuario(username)
        except self.db.get_usuario_by_nombre_usuario(username).DoesNotExist:
            raise ValueError("Usuario no encontrado.")

        try:
            actividad = Actividad.objects.get(id=actividad_id)
        except Actividad.DoesNotExist:
            raise ValueError("Actividad no encontrada.")

        if not hora_llegada_raw or not hora_salida_raw:
            raise ValueError("Debe ingresar ambas horas (llegada y salida).")

        try:
            fecha_base = actividad.fecha_hora_inicio.date()

            hora_llegada_dt = timezone.make_aware(
                datetime.combine(fecha_base, datetime.strptime(hora_llegada_raw, '%H:%M').time()),
                timezone.get_current_timezone()
            )
            hora_salida_dt = timezone.make_aware(
                datetime.combine(fecha_base, datetime.strptime(hora_salida_raw, '%H:%M').time()),
                timezone.get_current_timezone()
            )
        except ValueError:
            raise ValueError("Formato de hora inválido. Use HH:MM.")

        if hora_llegada_dt >= hora_salida_dt:
            raise ValueError("La hora de salida debe ser posterior a la hora de llegada.")

        inicio_actividad = actividad.fecha_hora_inicio
        fin_actividad = actividad.fecha_hora_fin or actividad.fecha_hora_inicio.replace(hour=23, minute=59)

        if timezone.is_naive(inicio_actividad):
            inicio_actividad = timezone.make_aware(inicio_actividad, timezone.get_current_timezone())
        if timezone.is_naive(fin_actividad):
            fin_actividad = timezone.make_aware(fin_actividad, timezone.get_current_timezone())

        if not (inicio_actividad <= hora_llegada_dt <= fin_actividad and inicio_actividad <= hora_salida_dt <= fin_actividad):
            rango_inicio = inicio_actividad.strftime("%H:%M")
            rango_fin = fin_actividad.strftime("%H:%M")
            raise ValueError(f'El rango permitido para registrar es entre {rango_inicio} y {rango_fin}.')

        try:
            self.db.create_part_actividad(
                id_actividad=actividad,
                id_usuario=usuario,
                hora_llegada=hora_llegada_dt,
                hora_salida=hora_salida_dt,
                estado_participante="Registrado"
            )
        except Exception:
            raise ValueError("Ya existe un registro de asistencia para este usuario y actividad.")

        return actividad
