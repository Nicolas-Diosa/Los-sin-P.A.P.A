from core.Persistencia.DB_manager import DB_Manager
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

class auth:
    def register(request):
        db = DB_Manager()
        if checkers.check_register_password(request) and checkers.check_register_user(request) and checkers.check_register_email(request):
            db.create_usuario(request.POST.get('user'), request.POST.get('email'), request.POST.get('pass1'), None, None, None)
            return 'core/signup_success.html'
        return 'core/signup_conflict.html'
    
class checkers:
        
    def check_register_password(request):
        if request.POST.get('pass1') == request.POST.get('pass2'):
            return True
        return False
    
    def check_register_user(request):
        db = DB_Manager()
        try:
            db.get_usuario_by_nombre_usuario(request.POST.get('user'))
            return False
            
        except ObjectDoesNotExist:
            return True

    def check_register_email(request):
        db = DB_Manager()
        try:
            db.get_usuario_by_email(request.POST.get('email'))
            return False
            
        except ObjectDoesNotExist:
            return True
        
    def check_login(request):
        db = DB_Manager()
        try:
            db.get_usuario_by_nombre_usuario(request.POST.get('user'))
            return True
            
        except ObjectDoesNotExist:
            return False
        