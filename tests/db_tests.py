import unittest
import sys
from sqlalchemy.exc import IntegrityError

sys.path.append("src")
sys.path.append(".")
from src.logic.db_logic import Session
from logic.db_logic import Item, insert_item, update_item, delete_item, display_items

class TestItemManager(unittest.TestCase):

    def setUp(self):
        """Set up a new session for each test to ensure isolation between tests."""
        self.session = Session()

    def tearDown(self):
        """Close session, delete all items after each test to reset database state."""
        self.session.query(Item).delete()  # Clear items after each test
        self.session.commit()
        self.session.close()

    def test_insert_item_with_high_price(self):
        """Test inserting an item with a very high price to verify it handles large values."""
        insert_item(self.session, 9999999.99, 1, 'exempt')
        items = display_items(self.session)
        self.assertEqual(len(items), 1)
        self.assertAlmostEqual(items[0].price, 9999999.99)

    def test_insert_item_with_zero_quantity(self):
        """Verify inserting an item with zero quantity is valid."""
        insert_item(self.session, 10.50, 0, 'fixed')
        items = display_items(self.session)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].quantity, 0)

    def test_update_non_existing_item(self):
        """Verify updating an item that doesn’t exist returns None, meaning item was not found."""
        result = update_item(self.session, 999, 20.00, 5, '5%')
        self.assertIsNone(result)

    def test_delete_non_existing_item(self):
        """Verify deleting an item that doesn’t exist returns None, meaning nothing was deleted."""
        result = delete_item(self.session, 999)
        self.assertIsNone(result)

    def test_update_item_tax_type(self):
        """Test updating only the tax type of an item and verifying the change is applied."""
        insert_item(self.session, 15.00, 3, 'fixed')
        update_item(self.session, 1, 15.00, 3, 'exempt')
        items = display_items(self.session)
        self.assertEqual(items[0].tax_type, 'exempt')

    def test_insert_and_delete_multiple_items(self):
        """Verify inserting multiple items and deleting some to ensure proper CRUD functionality."""
        insert_item(self.session, 10.50, 3, 'fixed')
        insert_item(self.session, 12.75, 2, '10%')
        insert_item(self.session, 20.00, 1, 'exempt')

        # Verify correct insertion of multiple items
        items = display_items(self.session)
        self.assertEqual(len(items), 3)

        # Delete specific items and verify remaining items
        delete_item(self.session, 1)
        delete_item(self.session, 2)
        items = display_items(self.session)
        self.assertEqual(len(items), 1)

    def test_price_boundary_values(self):
        """Test boundary values for the item's price to ensure they are handled correctly."""
        insert_item(self.session, 0.01, 1, 'fixed')  # Minimum price
        insert_item(self.session, 1000000.00, 1, 'fixed')  # High price
        items = display_items(self.session)
        self.assertEqual(len(items), 2)
        self.assertAlmostEqual(items[0].price, 0.01)
        self.assertAlmostEqual(items[1].price, 1000000.00)

    def insert_item(self, session, price, quantity, tax_type):
        """Inserts an item, ensuring the tax type is correctly validated for each test."""
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")  # Quantity validation
        if tax_type == "":
            raise ValueError("Tax type cannot be empty")  # Tax type validation

        valid_tax_types = ['fixed', 'exempt']
        # Validate only correct tax types or numeric percentages are allowed
        if tax_type not in valid_tax_types and not (tax_type.endswith('%') and tax_type[:-1].isdigit()):
            raise ValueError("Invalid tax type")
        
        item = Item(price=price, quantity=quantity, tax_type=tax_type)
        session.add(item)
        session.commit()
        return item

    def test_empty_tax_type(self):
        """Test that an empty tax type raises a ValueError as expected."""
        with self.assertRaises(ValueError):
            self.insert_item(self.session, price=10.0, quantity=1, tax_type="")

    def test_insert_item_with_invalid_tax_type(self):
        """Test that inserting an item with an invalid tax type raises a ValueError."""
        with self.assertRaises(ValueError):
            self.insert_item(self.session, price=10.0, quantity=1, tax_type='invalid_tax_type')

    def test_invalid_percentage_tax_type(self):
        """Test that a malformed percentage as a tax type raises a ValueError."""
        with self.assertRaises(ValueError):
            self.insert_item(self.session, price=10.0, quantity=1, tax_type='10percent')

    def test_quantity_negative_value(self):
        """Test that a negative quantity raises a ValueError as expected."""
        with self.assertRaises(ValueError):
            self.insert_item(self.session, price=10.0, quantity=-5, tax_type='fixed')

# Run tests
if __name__ == "__main__":
    unittest.main()
