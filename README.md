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


# proyecto hecho por
daniel calle, juliana franco

# Sistema de Gestión de Artículos
Este proyecto proporciona un sistema de gestión de artículos basado en CLI (Interfaz de Línea de Comandos) con funcionalidades CRUD, utilizando SQLAlchemy para las interacciones con la base de datos y unittest para las pruebas.

# Tabla de Contenidos
Requisitos Previos
Instalación
Estructura del Proyecto
Configuración de la Base de Datos
Ejecución de la CLI
Pruebas

1. Requisitos Previos
Asegúrate de tener el siguiente software instalado en tu sistema:

Python 3.x (https://www.python.org/downloads/)
pip (instalador de paquetes de Python)

2. Instalación
Clona el repositorio:
git clone https://github.com/dcalle14/Codigo-Limpio.git
cd codigo-limpio

Instala los paquetes de Python requeridos:
pip install -r requirements.txt
El archivo requirements.txt debe contener las siguientes bibliotecas:
sqlalchemy

3. Estructura del Proyecto
Aquí tienes una descripción general de la estructura del proyecto:

.
├── src
│   └── logic
│       ├── db_logic.py        # Base de datos y funciones CRUD
│       └── cli.py             # CLI para gestionar artículos
├── tests
│   └── test_db_logic.py       # Pruebas unitarias para las funciones de la base de datos
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación del proyecto


4. Configuración de la Base de Datos
El proyecto utiliza SQLite como base de datos, que no requiere configuración adicional ya que el archivo de base de datos (items.db) se crea automáticamente en la primera ejecución. SQLAlchemy gestiona la conexión y la creación de tablas.

Motor de Base de Datos: Definido en db_logic.py:

engine = create_engine('sqlite:///items.db')
Creación de Tabla: Ejecutada automáticamente en db_logic.py:
Base.metadata.create_all(engine)

5. Ejecución de la CLI
La CLI permite agregar, actualizar, eliminar y mostrar artículos en la base de datos. Aquí se explica cómo utilizarla:

Ejecuta la CLI:
python src/logic/cli.py

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

6. Pruebas
El proyecto incluye pruebas unitarias para las operaciones de base de datos. Ejecuta las pruebas para validar la corrección de las operaciones CRUD.

Ejecuta las pruebas:
python -m unittest discover -s tests -p "test_*.py"

Pruebas con Cobertura (opcional): Para obtener información más detallada sobre las pruebas, instala coverage:
pip install coverage

Ejecuta las pruebas con cobertura:
coverage run -m unittest discover -s tests -p "test_*.py"

Luego, genera un informe de cobertura:
coverage report -m