'''
Hace el test de la función incorrect_password de la clase UserValidator en el archivo auth.py

En este test únicamente existen dos casos posibles:

Caso 1: La contraseña coincide y está asignada para el usuario (false)
Caso 2: La contraseña no coincide para el usuario (true)

'''

from core.Negocio.auth import UserValidator
from core.models import Usuario
import unittest

class Test_incorrect_password(unittest.TestCase):
    def test_incorrect_password(self):
        # Los datos 
        casos = [
            ("contraseña_asociada_a_usuario", False),
            ("contraseña_no_asociada_a_usuario", True) 
        ]
        userV = UserValidator()
        
        for entrada, esperado in casos:
            # Contexto
            userV.db.create_usuario("userTestincorrect_password","emailTestincorrect_password","contraseña_asociada_a_usuario",None,None,None)

            with self.subTest(entrada=entrada):
                # Lo que se espera
                self.assertEqual(userV.incorrect_password("userTestincorrect_password",entrada), esperado)
            userV.db.delete(Usuario,"nombre_usuario","userTestincorrect_password")
        

if __name__ == '__main__':
    unittest.main()