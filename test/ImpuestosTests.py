import unittest
import sys
import os

# Ensure the path to the source code is included
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from logic.logica import calculate_item_total, calculate_total_purchase

class TestCalculateTotalItem(unittest.TestCase):
    """Tests for the calculate_item_total function."""

    def test_vehicle_over_200cc(self):
        """Test: Vehicle with engine capacity over 200cc should have an 8% tax."""
        price, quantity, tax_rate = 50000000, 1, 8
        expected_tax, expected_total = 4000000, 54000000
        self._assert_calculation(price, quantity, tax_rate, expected_tax, expected_total)

    def test_liquor_under_35_degrees(self):
        """Test: Liquor with alcohol content under 35% should have a 25% tax."""
        price, quantity, tax_rate = 100000, 2, 25
        expected_tax, expected_total = 50000, 250000
        self._assert_calculation(price, quantity, tax_rate, expected_tax, expected_total)

    def test_wine_low_alcohol(self):
        """Test: Wine with alcohol content under 14% should have a 20% tax."""
        price, quantity, tax_rate = 30000, 5, 20
        expected_tax, expected_total = 30000, 180000
        self._assert_calculation(price, quantity, tax_rate, expected_tax, expected_total)

    def test_liquor_high_alcohol(self):
        """Test: Liquor with alcohol content over 35% should have a 40% tax."""
        price, quantity, tax_rate = 150000, 1, 40
        expected_tax, expected_total = 60000, 210000
        self._assert_calculation(price, quantity, tax_rate, expected_tax, expected_total)

    def test_plastic_bags(self):
        """Test: Plastic bags should have a fixed tax per bag."""
        price, quantity, tax_rate = 0, 10, 'fixed'
        expected_tax, expected_total = 660, 660
        self._assert_calculation(price, quantity, tax_rate, expected_tax, expected_total)

    def test_exempt_item(self):
        """Test: Exempt item should have no tax."""
        price, quantity, tax_rate = 20000, 3, 'exempt'
        expected_tax, expected_total = 0, 60000
        self._assert_calculation(price, quantity, tax_rate, expected_tax, expected_total)

    def test_negative_price(self):
        """Test: Negative price should raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_item_total(-10000, 1, 19)

    def test_negative_tax(self):
        """Test: Negative tax rate should raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_item_total(10000, 1, -19)

    def test_zero_price(self):
        """Test: Zero price should raise ValueError."""
        with self.assertRaises(ValueError):
            calculate_item_total(0, 1, 19)

    def test_invalid_tax_type(self):
        """Test: Invalid tax type should raise TypeError."""
        with self.assertRaises(TypeError):
            calculate_item_total(10000, 1, "invalid")

    def _assert_calculation(self, price, quantity, tax_rate, expected_tax, expected_total):
        """Helper method to assert the correctness of tax and total calculations."""
        total_tax, total_item = calculate_item_total(price, quantity, tax_rate)
        self.assertAlmostEqual(total_tax, expected_tax)
        self.assertAlmostEqual(total_item, expected_total)


class TestCalculateTotalPurchase(unittest.TestCase):
    """Tests for the calculate_total_purchase function."""

    def test_multiple_items(self):
        """Test: Multiple items with different taxes."""
        items = [(50000, 2, 19), (150000, 1, 40), (30000, 3, 20)]
        expected_tax, expected_total = 99500, 495500
        self._assert_purchase(items, expected_tax, expected_total)

    def test_plastic_bags_in_purchase(self):
        """Test: Purchase with plastic bags and taxed items."""
        items = [(10000, 1, 19), (0, 10, 'fixed')]
        expected_tax, expected_total = 2560, 12560
        self._assert_purchase(items, expected_tax, expected_total)

    def test_exempt_and_taxed_items(self):
        """Test: Purchase with both exempt and taxed items."""
        items = [(100000, 1, 'exempt'), (20000, 5, 5)]
        expected_tax, expected_total = 5000, 200000
        self._assert_purchase(items, expected_tax, expected_total)

    def test_only_exempt_items(self):
        """Test: Purchase with only exempt items."""
        items = [(100000, 1, 'exempt'), (50000, 2, 'exempt')]
        expected_tax, expected_total = 0, 200000
        self._assert_purchase(items, expected_tax, expected_total)

    def test_high_quantity_items(self):
        """Test: Purchase with high quantity items."""
        items = [(1000, 1000, 19), (500, 2000, 19)]
        expected_tax, expected_total = 85500, 535500
        self._assert_purchase(items, expected_tax, expected_total)

    def test_multiple_taxes(self):
        """Test: Purchase with multiple taxes."""
        items = [(100000, 1, 19), (50000, 1, 25), (20000, 2, 5)]
        expected_tax, expected_total = 40500, 230000
        self._assert_purchase(items, expected_tax, expected_total)

    def test_negative_price_in_purchase(self):
        """Test: Negative price in any item should raise ValueError."""
        items = [(-10000, 1, 19), (150000, 1, 40)]
        with self.assertRaises(ValueError):
            calculate_total_purchase(items)

    def test_negative_quantity_in_purchase(self):
        """Test: Negative quantity in any item should raise ValueError."""
        items = [(10000, -1, 19), (150000, 1, 40)]
        with self.assertRaises(ValueError):
            calculate_total_purchase(items)

    def test_invalid_tax_type_in_purchase(self):
        """Test: Invalid tax type in any item should raise TypeError."""
        items = [(10000, 1, "invalid"), (150000, 1, 40)]
        with self.assertRaises(TypeError):
            calculate_total_purchase(items)

    def test_empty_items_in_purchase(self):
        """Test: Empty items list should return zero tax and total."""
        items = []
        expected_tax, expected_total = 0, 0
        self._assert_purchase(items, expected_tax, expected_total)

    def _assert_purchase(self, items, expected_tax, expected_total):
        """Helper method to assert the correctness of total tax and purchase calculations."""
        total_tax, total_purchase = calculate_total_purchase(items)
        self.assertAlmostEqual(total_tax, expected_tax)
        self.assertAlmostEqual(total_purchase, expected_total)


if __name__ == '__main__':
    unittest.main()
