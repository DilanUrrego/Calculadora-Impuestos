import sys
sys.path.append( "src" )

import SecretConfig
import psycopg2
from psycopg2 import Error
from psycopg2 import sql

class ControladorUsuarios:
    @staticmethod
    def obtener_cursor():
        try:
            connection = psycopg2.connect(
                database=SecretConfig.PGDATABASE,
                user=SecretConfig.PGUSER,
                password=SecretConfig.PGPASSWORD,
                host=SecretConfig.PGHOST,
                port=SecretConfig.PGPORT,
                sslmode='require'
            )
            cursor = connection.cursor()
            return cursor, connection
        except (Exception, Error) as error:
            print("Error al conectar a la base de datos usuarios:", error)
            return None, None

    def CrearTabla():
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            """ Crea la tabla de usuario en la BD """
            cursor.execute("""create table usuarios (
                nombre text,
                contrasena text
                ); """)
            connection.commit()
            cursor.close()
            connection.close()


    @staticmethod
    def TablaUsuariosExiste():
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            """Verifica si la tabla 'usuarios' ya existe en la base de datos."""
            try:
                query = sql.SQL("""
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'usuarios'
                    );
                """)
                cursor.execute(query)
                existe = cursor.fetchone()[0]
                return existe  # True si la tabla existe, False en caso contrario
            except psycopg2.Error as e:
                print(f"Error al verificar la tabla: {e}")
                return False
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def agregar_usuario(nombre, contrasena):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = "INSERT INTO usuarios (nombre, contrasena) VALUES (%s, %s)"
                cursor.execute(query, (nombre, contrasena))
                connection.commit()
                print("Usuario agregado correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al agregar usuario: {e}")
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def verificar_credenciales(nombre, contrasena):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = "SELECT nombre, contrasena FROM usuarios WHERE nombre = %s AND contrasena = %s"
                cursor.execute(query, (nombre, contrasena))
                result = cursor.fetchone()
                connection.close()
                data = (nombre, contrasena)
                if result == data:
                    return True
                else:
                    return False
            except Exception as e:
                print("Error al verificar las credenciales:", e)
                connection.close()
                return None
            
    @staticmethod
    def usuario_existe(nombre):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = "SELECT contrasena FROM usuarios WHERE nombre = %s"
                cursor.execute(query, (nombre,))
                usuario = cursor.fetchone()
                return usuario is not None
            except Exception as e:
                print(f"Error al verificar si el usuario existe: {e}")
                return False
            finally:
                cursor.close()
                connection.close()

    @staticmethod
    def contrasena_es_igual(nombre, contrasena):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = "SELECT contrasena FROM usuarios WHERE nombre = %s AND contrasena = %s"
                cursor.execute(query, (nombre, contrasena))
                result = cursor.fetchone()[0]
                connection.close()
                if result == contrasena:
                    return True
                else:
                    return False
            except Exception as e:
                print("Error al verificar las credenciales:", e)
                connection.close()
                return None
            
    @staticmethod
    def cambiar_contrasena(nombre, new_contrasena):
        cursor, connection = ControladorUsuarios.obtener_cursor()
        if cursor:
            try:
                query = "UPDATE usuarios SET contrasena = %s WHERE nombre = %s"
                cursor.execute(query, (new_contrasena, nombre))
                connection.commit()
                print("Contraseña editada correctamente.")
            except Exception as e:
                connection.rollback()
                print(f"Error al editar contraseña: {e}")
            finally:
                cursor.close()
                connection.close()
            