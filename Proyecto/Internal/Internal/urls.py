
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('actividades/', views.ver_actividades, name='actividades'),
    path('area_privada/', views.ver_area_priv, name='area_privada'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('crear_actividad/', views.crear_actividad, name='crear_actividad'),
    path('actividad_creada/', views.actividad_creada, name='actividad_creada'),
    path('actividades/<uuid:id>/', views.detalles_actividad, name='detalles_actividad'),
    path('actividad/<uuid:actividad_id>/asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('actividad/<uuid:actividad_id>/asistencia/confirmacion/', views.asistencia_registrada, name='asistencia_registrada'),
    path('actividades/<uuid:id>/', views.detalles_actividad, name='detalles_actividad'),
    path('agregar_evento/', views.agregar_evento, name='agregar_evento'),
    path('agregar_materia/', views.agregar_materia, name='agregar_materia'),
    path('perfil/', views.ver_perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/actualizado/', views.perfil_actualizado, name='perfil_actualizado'),
    path('tareas_realizadas/', views.tareas_realizadas, name='tareas_realizadas'),
    path('calendario/', views.calendario, name='calendario'),
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('materias_y_eventos/', views.eventos_y_materias, name='materias_y_eventos'),
    path('marcar_realizada/', views.marcar_tarea, name='marcar_realizada'),
        path('eliminar_tarea/', views.eliminar_tarea, name='eliminar_tarea'),
]
