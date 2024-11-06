from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError


# Base class for the declarative model
Base = declarative_base()

class Item(Base):
    """Model for the 'items' table."""
    _tablename_ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Unique ID for each item
    price = Column(Float, nullable=False)  # Price of the item, cannot be null
    quantity = Column(Integer, nullable=False)  # Quantity of the item, cannot be null
    tax_type = Column(String, nullable=False)  # Type of tax applied to the item, cannot be null

    def _repr_(self):
        """Provide a string representation for easy debugging."""
        return f"<Item(id={self.id}, price={self.price}, quantity={self.quantity}, tax_type='{self.tax_type}')>"

# Database configuration
engine = create_engine('sqlite:///items.db')  # Define SQLite engine, connecting to 'items.db'
Base.metadata.create_all(engine)  # Create tables if they do not exist
Session = sessionmaker(bind=engine)  # Bind session factory to the engine
session = Session()  # Instantiate a session for database interactions

# CRUD functions with exception handling

def insert_item(session, price, quantity, tax_type):
    """Insert a new item into the database with given price, quantity, and tax type."""
    try:
        new_item = Item(price=price, quantity=quantity, tax_type=tax_type)
        session.add(new_item)  # Add item to session for insertion
        session.commit()  # Commit changes to the database
        print(f"Item inserted: {new_item}")
    except SQLAlchemyError as e:
        session.rollback()  # Rollback changes on error
        print(f"Error inserting item: {e}")

def display_items(session):
    """Retrieve and return all items from the database."""
    try:
        items = session.query(Item).all()  # Fetch all items from the 'items' table
        return items  # Return list of items
    except SQLAlchemyError as e:
        print(f"Error retrieving items: {e}")
        return []  # Return empty list if an error occurs

def update_item(session, item_id, new_price, new_quantity, new_tax_type):
    """Update an existing item with new values for price, quantity, and tax type."""
    try:
        item = session.query(Item).filter(Item.id == item_id).first()  # Find item by ID
        if item:
            # Update item attributes if found
            item.price = new_price
            item.quantity = new_quantity
            item.tax_type = new_tax_type
            session.commit()  # Commit changes to the database
            print(f"Item updated: {item}")
        else:
            print(f"Item with ID {item_id} not found.")
    except SQLAlchemyError as e:
        session.rollback()  # Rollback changes on error
        print(f"Error updating item: {e}")

def delete_item(session, item_id):
    """Delete an item from the database by its ID."""
    try:
        item = session.query(Item).filter(Item.id == item_id).first()  # Find item by ID
        if item:
            session.delete(item)  # Mark item for deletion
            session.commit()  # Commit deletion to the database
            print(f"Item with ID {item_id} deleted.")
        else:
            print(f"Item with ID {item_id} not found.")
    except SQLAlchemyError as e:
        session.rollback()  # Rollback changes on error
        print(f"Error deleting item: {e}")
        