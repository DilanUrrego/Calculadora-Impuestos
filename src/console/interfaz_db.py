import sys
sys.path.append("src")
sys.path.append(".")
from src.logic.db_logic import Session
from logic.db_logic import Item, insert_item, update_item, delete_item, display_items

# CLI for Item Management
class ItemManagerCLI:
    def __init__(self):
        """Initialize a new CLI instance and database session for managing items."""
        self.session = Session()

    def start(self):
        """Start the CLI, showing the menu and handling user choices in a loop."""
        while True:
            self.show_menu()
            choice = input("Select an option: ").strip()
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
                print("Invalid option. Please try again.")

    def show_menu(self):
        """Display the main menu with available options for item management."""
        print("\n--- Item Management Menu ---")
        print("1. Add item")
        print("2. Update item")
        print("3. Delete item")
        print("4. View items")
        print("5. Exit")

    def add_item(self):
        """Prompt user for item details and add the item to the database."""
        try:
            # Collect item data
            price = float(input("Enter the item price: "))
            quantity = int(input("Enter the item quantity: "))
            tax_type = self.get_valid_tax_type()
            # Insert item into the database
            insert_item(self.session, price, quantity, tax_type)
        except ValueError:
            print("Error: Invalid input for price or quantity.")

    def update_item(self):
        """Prompt user for item ID and new details, then update the item."""
        try:
            # Collect item update details
            item_id = int(input("Enter the ID of the item you want to update: "))
            new_price = float(input("Enter the new price: "))
            new_quantity = int(input("Enter the new quantity: "))
            new_tax_type = self.get_valid_tax_type()
            # Update item in the database
            update_item(self.session, item_id, new_price, new_quantity, new_tax_type)
        except ValueError:
            print("Error: Invalid input for ID, price, or quantity.")

    def delete_item(self):
        """Prompt user for item ID and delete the corresponding item."""
        try:
            # Collect item ID to delete
            item_id = int(input("Enter the ID of the item you want to delete: "))
            # Delete item from the database
            delete_item(self.session, item_id)
        except ValueError:
            print("Error: Invalid ID.")

    def show_items(self):
        """Retrieve and display all items from the database."""
        items = display_items(self.session)
        if items:
            # Print each item
            for item in items:
                print(item)
        else:
            print("No items in the database.")

    def exit_program(self):
        """Close the session and exit the program."""
        print("Exiting the program...")
        self.session.close()
        exit()

    def get_valid_tax_type(self):
        """Prompt user for a valid tax type, ensuring it is correctly formatted."""
        while True:
            tax_type = input("Enter the tax type ('fixed', 'exempt', or percentage): ").strip()
            if tax_type in ['fixed', 'exempt'] or (tax_type[:-1].isdigit() and tax_type.endswith('%')):
                return tax_type
            print("Invalid tax type. Must be 'fixed', 'exempt', or a valid percentage.")


if __name__ == "__main__":
    cli = ItemManagerCLI()
    cli.start()