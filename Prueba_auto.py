import unittest
from unittest.mock import patch
import os
import csv
import hashlib
import sys
from io import StringIO
import Main

class TestRegistroUsuario(unittest.TestCase):

    def setUp(self):
        if os.path.exists('usuarios.csv'):
            os.remove('usuarios.csv')
        self.assertFalse(os.path.exists('usuarios.csv'))  # Confirmar que no existe

    def generar_datos_usuario(self):
        return ['Juan', 'Perez', '12345678', '01/01/1990', 'Calle Falsa 123', '5551234', 'contraseña', 'contraseña']

    @patch('builtins.input', side_effect=generar_datos_usuario())
    def test_registro_exitoso(self, mock_inputs):
        Main.registrar_usuario()
        self.assertTrue(os.path.exists('usuarios.csv'))
        with open('usuarios.csv', 'r', encoding='utf-8') as f:
            contenido = f.read()
            self.assertIn('Juan', contenido)

    @patch('builtins.input', side_effect=generar_datos_usuario())
    def test_fallo_por_duplicidad(self, mock_inputs):
        contraseña_encriptada = hashlib.sha256('contraseña'.encode()).hexdigest()
        with open('usuarios.csv', 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Juan', 'Perez', '12345678', '01/01/1990', 'Calle Falsa 123', '5551234', contraseña_encriptada])

        captured_output = StringIO()
        sys.stdout = captured_output
        Main.registrar_usuario()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        self.assertIn('Error: El usuario ya existe', output)
        with open('usuarios.csv', 'r', encoding='utf-8') as f:
            contenido = f.readlines()
            self.assertEqual(len(contenido), 1)

    @patch('builtins.input', side_effect=[
        '', 'Perez', 'abc', '32/13/1990', 'Calle', 'teléfono', 'contraseña', 'contraseña'
    ])
    def test_fallo_por_datos_invalidos(self, mock_inputs):
        captured_output = StringIO()
        sys.stdout = captured_output
        Main.registrar_usuario()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue().strip()
        self.assertIn('Error: Esta cédula ya se encuentra registrada en el sistema.', output)
        if os.path.exists('usuarios.csv'):
            with open('usuarios.csv', 'r', encoding='utf-8') as f:
                contenido = f.read()
                self.assertEqual(contenido, '')
        else:
            self.assertFalse(os.path.exists('usuarios.csv'))

if __name__ == '__main__':
    unittest.main()
