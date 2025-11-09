from core.Persistencia.DB_manager import DB_Manager
from django.core.exceptions import ObjectDoesNotExist
import re

class UserValidator:
    

    def __init__(self, db_manager: DB_Manager):
        self.db = db_manager

    def passwords_match(self, pass1, pass2):
        return pass1 == pass2

    def username_available(self, username):
        try:
            self.db.get_usuario_by_nombre_usuario(username)
            return False
        except ObjectDoesNotExist:
            return True

    def email_available(self, email):
        try:
            self.db.get_usuario_by_email(email)
            return False
        except ObjectDoesNotExist:
            return True
        
    def is_valid_email(self, email):
        return (
            re.search(r'@', email)
        )

    def is_valid_password_policy(self, password):
        
        return (
            len(password) >= 8
            and re.search(r'\d', password)
            and re.search(r'[^A-Za-z0-9]', password)
        )


class Auth:
    

    def __init__(self, db_manager: DB_Manager):
        self.db = db_manager
        self.validator = UserValidator(db_manager)

    def register_user(self, data: dict, request):
        username = data.get('user')
        email = data.get('email')
        pass1 = data.get('pass1')
        pass2 = data.get('pass2')

        errors = {}

        # Validaciones
        if not self.validator.username_available(username):
            errors['user'] = "El nombre de usuario ya está registrado."

        if not self.validator.email_available(email):
            errors['email'] = "El correo electrónico ya está registrado."
        
        if not self.validator.is_valid_email(email):
            errors['email_validity'] = "El correo electrónico no es valido."

        if not self.validator.passwords_match(pass1, pass2):
            errors['password'] = "Las contraseñas no coinciden."

        if not self.validator.is_valid_password_policy(pass1):
            errors['policy'] = "La contraseña no cumple con la política (mínimo 8 caracteres, un número y un símbolo)."

        if errors:
            return False, errors

        self.db.create_usuario(username, email, pass1, None, None, None)
        request.session['inicio_sesion'] = True
        request.session['username'] = request.POST.get('user')
        return True, {}
