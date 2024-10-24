from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Item(Base):
    """Model for the 'items' table."""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    tax_type = Column(String, nullable=False)

    def __repr__(self):
        return f"<Item(id={self.id}, price={self.price}, quantity={self.quantity}, tax_type='{self.tax_type}')>"

# Database configuration
engine = create_engine('sqlite:///items.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# CRUD functions with exception handling
def insert_item(session, price, quantity, tax_type):
    try:
        new_item = Item(price=price, quantity=quantity, tax_type=tax_type)
        session.add(new_item)
        session.commit()
        print(f"Item inserted: {new_item}")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting item: {e}")

def display_items(session):
    try:
        items = session.query(Item).all()
        return items
    except SQLAlchemyError as e:
        print(f"Error retrieving items: {e}")
        return []

def update_item(session, item_id, new_price, new_quantity, new_tax_type):
    try:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            item.price = new_price
            item.quantity = new_quantity
            item.tax_type = new_tax_type
            session.commit()
            print(f"Item updated: {item}")
        else:
            print(f"Item with ID {item_id} not found.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating item: {e}")

def delete_item(session, item_id):
    try:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item:
            session.delete(item)
            session.commit()
            print(f"Item with ID {item_id} deleted.")
        else:
            print(f"Item with ID {item_id} not found.")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting item: {e}")
