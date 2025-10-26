from core.Persistencia.DB_manager import DB_Manager
from django.http import HttpResponse

class auth:
    def register_user(request):
        db = DB_Manager()
        if request.POST.get('password1') == request.POST.get('password2'):
            db.create_usuario(request.POST.get('username'), request.POST.get('email'), request.POST.get('password1'), None, None, None)
            return HttpResponse('El usuario ha sido registrado de manera exitosa')
        return HttpResponse('La contraseña no está verificada')