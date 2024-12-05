import unittest
from test_Main import TestRegistroUsuario

# Crear y ejecutar un test específico
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestRegistroUsuario("test_registro_exitoso"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
