# Programa para el Cálculo de Impuestos

Este programa calcula el total de impuestos y el precio total de un artículo o una compra compuesta por varios artículos, teniendo en cuenta diferentes tipos de impuestos aplicables según las normativas colombianas.

## Funciones

### `calculate_item_total(price, quantity, tax_type)`

Calcula el total de impuestos y el precio total de un solo artículo.

- **Parámetros de entrada**:
  - `price`: Precio unitario del artículo.
  - `quantity`: Cantidad de artículos.
  - `tax_type`: Tipo de impuesto (porcentaje, fijo, o "exempt" para exento).

- **Proceso**:
  - Calcula impuestos según el tipo especificado.
  - Devuelve el total de impuestos y el precio total.

- **Salida**:
  - Tupla con el total de impuestos y el precio total del artículo.

### `calculate_total_purchase(items)`

Calcula el total de impuestos y el precio total de una compra con múltiples artículos.

- **Parámetros de entrada**:
  - `items`: Lista de tuplas, cada una con `(precio_unitario, cantidad, tipo_impuesto)`.

- **Proceso**:
  - Itera sobre cada artículo y suma impuestos y precios totales.

- **Salida**:
  - Tupla con el total de impuestos y el precio total de la compra.


# proyecto realizado por:
Daniel calle y Juliana franco
Dilan Urrego y Santiago Cordoba - Entrega Web y Refactoring

# Sistema de Gestión de Artículos
Este proyecto proporciona un sistema de gestión de artículos basado en CLI (Interfaz de Línea de Comandos) con funcionalidades CRUD, utilizando SQLAlchemy para las interacciones con la base de datos y unittest para las pruebas.

# Estructura
logic/db_logic.py: Contiene la lógica de negocio, con las funciones de CRUD y el modelo de base de datos.
console/interfaz_db.py: Contiene la interfaz de línea de comandos (CLI) para interactuar con la aplicación.
test/db_test.py: Contiene las pruebas unitarias para verificar la funcionalidad de la aplicación.


1. Requisitos Previos
Asegúrate de tener el siguiente software instalado en tu sistema:

Python 3.x (https://www.python.org/downloads/)
pip (instalador de paquetes de Python)
SQLAlchemy: El código depende de SQLAlchemy para las operaciones de base de datos.

Clona o Descarga el Código del Proyecto: Descarga los archivos del proyecto y navega al directorio raíz donde están ubicadas las carpetas src y logic y el archivo principal del CLI.

Instala las Dependencias: Abre el símbolo del sistema e instala los paquetes necesarios ejecutando: pip install sqlalchemy


2. Instalación
Clona el repositorio:
git clone https://github.com/dcalle14/Codigo-Limpio.git
cd codigo-limpio

Instala los paquetes de Python requeridos:
pip install -r requirements.txt
El archivo requirements.txt debe contener las siguientes bibliotecas:
sqlalchemy


3. Configuración de la Base de Datos
El proyecto utiliza SQLite como base de datos, que no requiere configuración adicional ya que el archivo de base de datos (items.db) se crea automáticamente en la primera ejecución. SQLAlchemy gestiona la conexión y la creación de tablas.

Navega al Directorio del Proyecto: En el símbolo del sistema, ve a la carpeta principal del proyecto:
cd github.com/dcalle14/Codigo-Limpio.git

jecuta la Aplicación CLI: Ejecuta el CLI que se encuentra en la carpeta console/:
python -m console.interfaz_db



4. Ejecución de la CLI
La CLI permite agregar, actualizar, eliminar y mostrar artículos en la base de datos. Aquí se explica cómo utilizarla:

Ejecuta la CLI:
python src/console/cli.py

Opciones de la CLI: La CLI muestra un menú con las siguientes opciones:

--- Menú de Gestión de Artículos ---
1. Agregar artículo
2. Actualizar artículo
3. Eliminar artículo
4. Ver artículos
5. Salir

Opción 1 - Agregar artículo: Ingresa el precio, la cantidad y el tipo de impuesto (fixed, exempt o porcentaje como 10%).
Opción 2 - Actualizar artículo: Ingresa el ID del artículo a actualizar, seguido de nuevos valores para el precio, cantidad y tipo de impuesto.
Opción 3 - Eliminar artículo: Ingresa el ID del artículo que deseas eliminar.
Opción 4 - Ver artículos: Muestra una lista de todos los artículos en la base de datos.
Opción 5 - Salir: Cierra la CLI y la sesión de la base de datos.

5. Pruebas

Ejecuta las Pruebas Unitarias: Para ejecutar las pruebas que se encuentran en db_test.py dentro de la carpeta test/, usa el siguiente comando:
python -m unittest discover -s tests -p "db_test.py"

6. Iniciar aplicación

Ejecuta el archivo app.py para iniciar el servidor web:

> $> python app.py

Esto debería iniciar el servidor en modo desarrollo en ``` http://127.0.0.1:5000 ```

Luego abre tu navegador web y ve a ``` http://127.0.0.1:5000 ```  para ver la aplicación en funcionamiento.
