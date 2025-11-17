'''
Hace el test de la función is_valid_password de la clase UserValidator en el archivo auth.py


En este test existen los siguientes casos:


Caso 1: La contraseña tiene una longitud mayor o igual a 8 simbolos
        y tiene al menos un número y tiene al menos un simbolo especial (true)

Caso 2: La contraseña no cumple con las 3 condiciones (false):
        - No tiene una longitud mayor o igual a 8 simbolos
        - No tiene al menos un número
        - No tiene al menos un simbolo especial

    En este caso existe el caso limite: la contraseña tiene exactamente 8 simbolos,
    la contraseña tiene exactamente un número, la contraseña tiene exactamente un simbolo especial.
'''


import unittest
from core.Negocio.auth import UserValidator

class Test_is_valid_password_policy(unittest.TestCase):

    def setUp(self):
        self.validator = UserValidator()

    def test_is_valid_password_policy(self):
        casos = [
            ("", False),                         # Cadena vacía (0 simbolos)
            ("corto1*", False),                  # Contraseña con longitud menor a 8 (7 simbolos)
            ("*contrasenasinnumero", False),     # No tiene digitos
            ("contrasenasinsimbolo12", False),   # No tiene símbolos
            ("contraseñasinsimbolo12", True),    # Es la misma contraseña de arriba pero ñ cuenta como simbolo especial
            ("Valida8!", True),                  # Contraseña con longitud 8, con número y símbolo (Limite)
            ("12345678*", True),                 # Contraseña con solo digitos y simbolo
            ("@@@2@@@@", True),                  # Contraseña con solo simbolos y digito
        ]

        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                self.assertEqual(self.validator.is_valid_password_policy(entrada), esperado)


if __name__ == '__main__':
    unittest.main()
