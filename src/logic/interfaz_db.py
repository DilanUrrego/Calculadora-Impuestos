from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Importar la clase Item y las funciones necesarias
from db import Item, insert_item, update_item, delete_item, display_items

# Configuración de la base de datos
Base = declarative_base()
engine = create_engine('sqlite:///items.db')  # Cambia esto según tu base de datos
Session = sessionmaker(bind=engine)

class ItemManagerCLI:
    def _init_(self):
        self.session = Session()

    def start(self):
        while True:
            self.show_menu()
            choice = input("Selecciona una opción: ").strip()
            if choice == '1':
                self.add_item()
            elif choice == '2':
                self.update_item()
            elif choice == '3':
                self.delete_item()
            elif choice == '4':
                self.show_items()
            elif choice == '5':
                self.exit_program()
            else:
                print("Opción inválida. Inténtalo de nuevo.")

    def show_menu(self):
        print("\n--- Menú de Gestión de Ítems ---")
        print("1. Agregar ítem")
        print("2. Actualizar ítem")
        print("3. Eliminar ítem")
        print("4. Consultar ítems")
        print("5. Salir")

    def add_item(self):
        price = float(input("Introduce el precio del ítem: "))
        quantity = int(input("Introduce la cantidad del ítem: "))
        tax_type = self.get_valid_tax_type()
        insert_item(self.session, price, quantity, tax_type)
        print("Ítem agregado con éxito.")

    def update_item(self):
        item_id = int(input("Introduce el ID del ítem que deseas actualizar: "))
        new_price = float(input("Introduce el nuevo precio: "))
        new_quantity = int(input("Introduce la nueva cantidad: "))
        new_tax_type = self.get_valid_tax_type()
        update_item(self.session, item_id, new_price, new_quantity, new_tax_type)
        print("Ítem actualizado con éxito.")

    def delete_item(self):
        item_id = int(input("Introduce el ID del ítem que deseas eliminar: "))
        delete_item(self.session, item_id)
        print("Ítem eliminado con éxito.")

    def show_items(self):
        items = display_items(self.session)
        if items:
            for item in items:
                print(item)
        if not items:
            print ("No hay items en la base de datos.")

    def exit_program(self):
        print("Saliendo del programa...")
        self.session.close()
        exit()

    def get_valid_tax_type(self):
        while True:
            tax_type = input("Introduce el tipo de impuesto ('fixed', 'exempt' o porcentaje): ").strip()
            if tax_type in ['fixed', 'exempt'] or (tax_type[:-1].isdigit() and tax_type.endswith('%')):
                return tax_type
            print("Tipo de impuesto inválido. Debe ser 'fixed', 'exempt' o un porcentaje válido.")

if _name_ == "_main_":
    cli = ItemManagerCLI()
    cli.start()