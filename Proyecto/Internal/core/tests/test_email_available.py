'''
Hace el test de la función email_available de la clase UserValidator en el archivo auth.py

En este test únicamente existen dos casos posibles:

Caso 1: El email está disponible para ser registrado (True)
Caso 2: El email no está disponible para ser registrado (False) 

'''

from core.Negocio.auth import UserValidator
from core.models import Usuario
import unittest

class Test_email_available(unittest.TestCase):
    def test_email_available(self):
        # Los datos 
        casos = [
            ("email disponible", True),
            ("email ya ocupado", False) 
        ]
        userV = UserValidator()
        
        for entrada, esperado in casos:
            # Contexto
            userV.db.create_usuario("usuarioTestEmailAvaibable","email ya ocupado","contraseñaTestEmailAvaibable",None,None,None)

            with self.subTest(entrada=entrada):
                # Lo que se espera
                self.assertEqual(userV.email_available(entrada), esperado)
            userV.db.delete(Usuario,"nombre_usuario","usuarioTestEmailAvaibable")
        

if __name__ == '__main__':
    unittest.main()