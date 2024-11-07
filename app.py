# Para las aplicaciones web creadas con Flask, debemos importar siempre el modulo 
from flask import Flask    

# Para poder servir plantillas HTML desde archivos, es necesario importar el modulo render_template
from flask import render_template, request, session, flash, redirect, url_for
from functools import wraps

from src.controllers.users_controller import ControladorUsuarios


try:
    if ControladorUsuarios.TablaUsuariosExiste():
        print("La tabla 'usuarios' ya existe. Continuando...")
    else:
        print("La tabla 'usuarios' no existe. Creando tabla...")
        ControladorUsuarios.CrearTabla()
except Exception as e:
    print(f"Error verificando/creando la tabla: {str(e)}")


# Flask constructor: crea una variable que nos servirá para comunicarle a Flask
# la configuración que queremos para nuestra aplicación
app = Flask(__name__)     


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Por favor, inicia sesión para acceder a esta página", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__, template_folder='src/templates')
app.secret_key = 'your_secret_key'

# decorator: se usa para indicar el URL Path por el que se va a invocar nuestra función
@app.route('/')      
def index():
    return render_template('index.html')

@app.route('/calcular')      
def calcular():
    return render_template('calcular.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        contrasena = request.form['password']
        
        if ControladorUsuarios.verificar_credenciales(usuario, contrasena):
            return redirect(url_for('calcular'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['username']
        contrasena = request.form['password']
        confirmacion_contrasena = request.form['confirmPassword']

        # Validar que el usuario no esté en uso
        if ControladorUsuarios.usuario_existe(nombre):
            flash("El usuario ya está registrado. Intente con otro.", "danger")
            return redirect(url_for('register'))

        # Validar que las contraseñas coincidan
        if contrasena != confirmacion_contrasena:
            flash("Las contraseñas no coinciden. Inténtelo de nuevo.", "danger")
            return redirect(url_for('register'))

        # Crear el usuario en la base de datos
        try:
            ControladorUsuarios.agregar_usuario(nombre, contrasena)
            flash("Usuario registrado correctamente.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error al registrar el usuario: {e}", "danger")
            return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        nombre = request.form['username']
        contrasena = request.form['currentpassword']
        nueva_contrasena = request.form['newpassword']
        if ControladorUsuarios.contrasena_es_igual(nombre, contrasena):
            ControladorUsuarios.cambiar_contrasena(nombre, nueva_contrasena)
            return redirect(url_for('login'))
    return render_template('change_password.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        nombre = request.form['username']
        contrasena = request.form['password']
        if ControladorUsuarios.verificar_credenciales(nombre, contrasena):
            ControladorUsuarios.eliminar_usuario(nombre, contrasena)
            return redirect(url_for('login'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
            return redirect(url_for('login'))
    return render_template('delete.html')


if __name__=='__main__':
   app.run( debug=True)
   