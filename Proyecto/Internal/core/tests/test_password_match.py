'''
Hace el test de la función password_match de la clase UserValidator en el archivo auth.py


En este test existen dos casos posibles:


Caso 1: Las contraseñas coinciden (true)
Caso 2: Las contraseñas no coinciden (false)


'''


import unittest
from unittest.mock import MagicMock
from core.Negocio.auth import UserValidator


class Test_password_match(unittest.TestCase):
    def setUp(self):
        # Mock del DB_Manager
        self.mock_db = MagicMock()
        self.validator = UserValidator(self.mock_db)

    def test_passwords_match(self):
        casos = [
            ("abc123", "abc123", True),                    # Son iguales
            ("", "", True),                                # Ambas vacías (Iguales)
            ("Nosequeponer", "yasupequeponer", False),     # Diferentes
            ("abc123", "ABC123", False),                   # Mayúsculas las hacen diferentes
            ("password", None, False),                     # Una es None (Diferentes)
        ]

        for pass1, pass2, esperado in casos:
            with self.subTest(p1=pass1, p2=pass2):
                self.assertEqual(self.validator.passwords_match(pass1, pass2), esperado)



if __name__ == '__main__':
    unittest.main()
