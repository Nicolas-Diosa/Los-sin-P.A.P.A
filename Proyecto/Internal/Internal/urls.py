
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('', views.home, name='home'),
    path ('actividades/', views.ver_actividades, name='actividades'),
    path ('area_privada/', views.ver_area_priv, name='area_privada'),
    path ('signup/', views.signup, name='signup'),
    path ('login/', views.login, name='login'),
    path ('logout/', views.logout, name='logout'),
    path ('actividades/<uuid:id>/', views.detalles_actividad, name='detalles_actividad')
]