'''
Hace el test de la función username_available de la clase UserValidator en el archivo auth.py

En este test únicamente existen dos casos posibles:

Caso 1: El nombre de usuario está disponible para ser registrado (True)
Caso 2: El nombre de usuario no está disponible para ser registrado (False) 

'''

from core.Negocio.auth import UserValidator
from core.models import Usuario
import unittest

class Test_username_available(unittest.TestCase):
    def test_username_available(self):
        # Los datos 
        casos = [
            ("nombre disponible", True),
            ("nombre ya ocupado", False) 
        ]
        userV = UserValidator()
        
        for entrada, esperado in casos:
            # Contexto
            userV.db.create_usuario("usuarioTestUserAvaibable","nombre ya ocupado","contraseñaTestUserAvaibable",None,None,None)

            with self.subTest(entrada=entrada):
                # Lo que se espera
                self.assertEqual(userV.email_available(entrada), esperado)
            userV.db.delete(Usuario,"nombre_usuario","usuarioTestUserAvaibable")
        

if __name__ == '__main__':
    unittest.main()