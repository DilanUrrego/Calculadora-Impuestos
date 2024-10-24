from logic.db_logic import Item, insert_item , update_item , delete_item , display_items
# CLI for Item Management
class ItemManagerCLI:
    def __init__(self):
        self.session = Session()

    def start(self):
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
        print("\n--- Item Management Menu ---")
        print("1. Add item")
        print("2. Update item")
        print("3. Delete item")
        print("4. View items")
        print("5. Exit")

    def add_item(self):
        try:
            price = float(input("Enter the item price: "))
            quantity = int(input("Enter the item quantity: "))
            tax_type = self.get_valid_tax_type()
            insert_item(self.session, price, quantity, tax_type)
        except ValueError:
            print("Error: Invalid input for price or quantity.")

    def update_item(self):
        try:
            item_id = int(input("Enter the ID of the item you want to update: "))
            new_price = float(input("Enter the new price: "))
            new_quantity = int(input("Enter the new quantity: "))
            new_tax_type = self.get_valid_tax_type()
            update_item(self.session, item_id, new_price, new_quantity, new_tax_type)
        except ValueError:
            print("Error: Invalid input for ID, price, or quantity.")

    def delete_item(self):
        try:
            item_id = int(input("Enter the ID of the item you want to delete: "))
            delete_item(self.session, item_id)
        except ValueError:
            print("Error: Invalid ID.")

    def show_items(self):
        items = display_items(self.session)
        if items:
            for item in items:
                print(item)
        else:
            print("No items in the database.")

    def exit_program(self):
        print("Exiting the program...")
        self.session.close()
        exit()

    def get_valid_tax_type(self):
        while True:
            tax_type = input("Enter the tax type ('fixed', 'exempt', or percentage): ").strip()
            if tax_type in ['fixed', 'exempt'] or (tax_type[:-1].isdigit() and tax_type.endswith('%')):
                return tax_type
            print("Invalid tax type. Must be 'fixed', 'exempt', or a valid percentage.")

if __name__ == "__main__":
    cli = ItemManagerCLI()
    cli.start()



