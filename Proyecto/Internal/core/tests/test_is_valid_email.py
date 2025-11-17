'''
Hace el test de la función is_valid_email de la clase UserValidator en el archivo auth.py

En este test existen varios casos posibles:

Caso válido:

1. Que el email cumpla con el nombre, el arroba, el dominio, y el sufijo con su punto respectivo

Casos inválidos:
1. Que la primera parte del nombre esté vacía
2. Que no exista el arroba
3. Que no exista el dominio
4. Que no exista el punto que separa el dominio del .com o .co
5. Que no exista la última parte referida al .co y ese tipo de sufijos
6. Que tenga puntos seguidos en la parte del dominio (@hola..com)

'''

from core.Negocio.auth import UserValidator
import unittest

class Test_is_valid_email(unittest.TestCase):
    def test_is_valid_email(self):
        # Los datos 
        casos = [
            ("@notienenombre.co", False),
            ("emailsinarroba.co", False),
            ("emailsindominio@.co", False),
            ("emailsinpuntoseparador@dominioco", False),
            ("emailsinpartefinaldominio@dominio.", False),
            ("dominioconpuntosseguidos@dominio..com", False),
            ("emailcorrecto@email.co", True),
            ("emailcorrecto@unal.edu.co", True)
        ]
        userV = UserValidator()
        
        for entrada, esperado in casos:
            # Contexto
            with self.subTest(entrada=entrada):
                # Lo que se espera
                self.assertEqual(userV.is_valid_email(entrada), esperado)

if __name__ == '__main__':
    unittest.main()