import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from src.controllers.users_controller import ControladorUsuarios

class TestControladorUsuarios(unittest.TestCase):

    @patch("src.controllers.users_controller.ControladorUsuarios.obtener_cursor")
    def test_CrearTabla(self, mock_obtener_cursor):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_obtener_cursor.return_value = (mock_cursor, mock_connection)

        ControladorUsuarios.CrearTabla()

        mock_cursor.execute.assert_called_once_with("""create table usuarios (
                nombre text,
                contrasena text
                ); """)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("src.controllers.users_controller.ControladorUsuarios.obtener_cursor")
    def test_TablaUsuariosExiste_true(self, mock_obtener_cursor):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_cursor.fetchone.return_value = [True]
        mock_obtener_cursor.return_value = (mock_cursor, mock_connection)

        existe = ControladorUsuarios.TablaUsuariosExiste()
        self.assertTrue(existe)

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("src.controllers.users_controller.ControladorUsuarios.obtener_cursor")
    def test_TablaUsuariosExiste_false(self, mock_obtener_cursor):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_cursor.fetchone.return_value = [False]
        mock_obtener_cursor.return_value = (mock_cursor, mock_connection)

        existe = ControladorUsuarios.TablaUsuariosExiste()
        self.assertFalse(existe)

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("src.controllers.users_controller.ControladorUsuarios.obtener_cursor")
    def test_agregar_usuario(self, mock_obtener_cursor):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_obtener_cursor.return_value = (mock_cursor, mock_connection)

        ControladorUsuarios.agregar_usuario("testuser", "testpassword")

        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO usuarios (nombre, contrasena) VALUES (%s, %s)", ("testuser", "testpassword")
        )
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("src.controllers.users_controller.ControladorUsuarios.obtener_cursor")
    def test_verificar_credenciales_correctas(self, mock_obtener_cursor):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_cursor.fetchone.return_value = ("testuser", "testpassword")
        mock_obtener_cursor.return_value = (mock_cursor, mock_connection)

        resultado = ControladorUsuarios.verificar_credenciales("testuser", "testpassword")
        self.assertTrue(resultado)

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("src.controllers.users_controller.ControladorUsuarios.obtener_cursor")
    def test_verificar_credenciales_incorrectas(self, mock_obtener_cursor):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_obtener_cursor.return_value = (mock_cursor, mock_connection)

        resultado = ControladorUsuarios.verificar_credenciales("testuser", "wrongpassword")
        self.assertFalse(resultado)

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("src.controllers.users_controller.ControladorUsuarios.obtener_cursor")
    def test_usuario_existe_true(self, mock_obtener_cursor):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_cursor.fetchone.return_value = ("testpassword",)
        mock_obtener_cursor.return_value = (mock_cursor, mock_connection)

        existe = ControladorUsuarios.usuario_existe("testuser")
        self.assertTrue(existe)

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("src.controllers.users_controller.ControladorUsuarios.obtener_cursor")
    def test_usuario_existe_false(self, mock_obtener_cursor):
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_obtener_cursor.return_value = (mock_cursor, mock_connection)

        existe = ControladorUsuarios.usuario_existe("nonexistentuser")
        self.assertFalse(existe)

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
