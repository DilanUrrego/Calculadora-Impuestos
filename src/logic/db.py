from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Crear base de datos
Base = declarative_base()

class Item(Base):
    """Modelo de la tabla 'items'."""
    _tablename_ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    tax_type = Column(String, nullable=False)

    def _repr_(self):
        return f"<Item(id={self.id}, price={self.price}, quantity={self.quantity}, tax_type='{self.tax_type}')>"

# Configuración de la base de datos
engine = create_engine('sqlite:///items.db')  # Cambia la URL según tu base de datos
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def insert_item(session, price, quantity, tax_type):
    """Inserta un nuevo ítem en la base de datos."""
    new_item = Item(price=price, quantity=quantity, tax_type=tax_type)
    session.add(new_item)
    session.commit()
    print(f"Ítem insertado: {new_item}")

def display_items(session):
    """Muestra todos los ítems en la base de datos."""
    items = session.query(Item).all()
    if not items:
        print("No hay ítems en la base de datos.")
    else:
        for item in items:
            print(item)

def update_item(session, item_id, new_price, new_quantity, new_tax_type):
    """Actualiza un ítem existente en la base de datos."""
    item = session.query(Item).filter(Item.id == item_id).first()
    if item:
        item.price = new_price
        item.quantity = new_quantity
        item.tax_type = new_tax_type
        session.commit()
        print(f"Ítem actualizado: {item}")
    else:
        print(f"No se encontró el ítem con ID {item_id}.")

def show_items(session):
    items = display_items(session)
    if items:
        print("\n--- Lista de Ítems ---")
        for item in items:
            print(item)
    else:
        print("No hay ítems en la base de datos.")


def delete_item(session, item_id):
    """Elimina un ítem de la base de datos."""
    item = session.query(Item).filter(Item.id == item_id).first()
    if item:
        session.delete(item)
        session.commit()
        print(f"Ítem con ID {item_id} eliminado.")
    else:
        print(f"No se encontró el ítem con ID {item_id}.")



def main():
    """Función principal que ejecuta el flujo del programa."""
    print("== Insertar datos ==")
    insert_item(session, 10.99, 2, 'fixed')
    insert_item(session, 15.75, 5, '10%')
    
    print("\n== Seleccionar datos ==")
    display_items(session)

    print("\n== Actualizar datos ==")
    update_item(session, 1, 12.50, 2, 'fixed')
    
    print("\n== Seleccionar después de actualizar ==")
    display_items(session)

    print("\n== Eliminar datos ==")
    delete_item(session, 1)
    
    print("\n== Seleccionar después de eliminar ==")
    display_items(session)



# Ejecutar la función principal si este archivo es el principal
if _name_ == "_main_":
    main()

# Cerrar la sesión al final
session.close()