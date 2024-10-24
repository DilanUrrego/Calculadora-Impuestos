import unittest
from sqlalchemy.exc import IntegrityError

from logic.db_logic import Item, insert_item , update_item , delete_item , display_items


class TestItemManager(unittest.TestCase):
    
    def test_insert_item_with_high_price(self):
        """Prueba la inserción de un ítem con un precio muy alto."""
        insert_item(self.session, 9999999.99, 1, 'exempt')
        items = display_items(self.session)
        self.assertEqual(len(items), 1)
        self.assertAlmostEqual(items[0].price, 9999999.99)

    def test_insert_item_with_zero_quantity(self):
        """Prueba que insertar un ítem con cantidad cero sea válido."""
        insert_item(self.session, 10.50, 0, 'fixed')
        items = display_items(self.session)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].quantity, 0)

    def test_update_non_existing_item(self):
        """Prueba actualizar un ítem que no existe en la base de datos."""
        result = update_item(self.session, 999, 20.00, 5, '5%')
        self.assertIsNone(result)  # Asegura que no se ha encontrado el ítem

    def test_delete_non_existing_item(self):
        """Prueba eliminar un ítem que no existe."""
        result = delete_item(self.session, 999)
        self.assertIsNone(result)  # Asegura que no se eliminó nada

    def test_insert_item_with_invalid_tax_type(self):
        """Prueba que insertar un ítem con un tipo de impuesto inválido falle."""
        with self.assertRaises(ValueError):
            insert_item(self.session, 20.00, 5, 'invalid_tax_type')

    def test_update_item_tax_type(self):
        """Prueba actualizar sólo el tipo de impuesto de un ítem."""
        insert_item(self.session, 15.00, 3, 'fixed')
        update_item(self.session, 1, 15.00, 3, 'exempt')
        items = display_items(self.session)
        self.assertEqual(items[0].tax_type, 'exempt')

    def test_insert_and_delete_multiple_items(self):
        """Prueba insertar y eliminar varios ítems y verifica que todo esté correcto."""
        insert_item(self.session, 10.50, 3, 'fixed')
        insert_item(self.session, 12.75, 2, '10%')
        insert_item(self.session, 20.00, 1, 'exempt')

        # Verificar que los ítems fueron insertados correctamente
        items = display_items(self.session)
        self.assertEqual(len(items), 3)

        # Eliminar ítems
        delete_item(self.session, 1)
        delete_item(self.session, 2)

        # Verificar que sólo queda 1 ítem
        items = display_items(self.session)
        self.assertEqual(len(items), 1)

    def test_price_boundary_values(self):
        """Prueba valores límite en el precio del ítem."""
        insert_item(self.session, 0.01, 1, 'fixed')  # Precio mínimo permitido
        insert_item(self.session, 1000000.00, 1, 'fixed')  # Precio muy alto permitido
        items = display_items(self.session)
        self.assertEqual(len(items), 2)
        self.assertAlmostEqual(items[0].price, 0.01)
        self.assertAlmostEqual(items[1].price, 1000000.00)

    def test_quantity_negative_value(self):
        """Prueba que la cantidad negativa lanza un error."""
        with self.assertRaises(ValueError):
            insert_item(self.session, 20.00, -5, 'fixed')

    def test_empty_tax_type(self):
        """Prueba que un tipo de impuesto vacío lanza un error."""
        with self.assertRaises(ValueError):
            insert_item(self.session, 20.00, 5, '')

    def test_invalid_percentage_tax_type(self):
        """Prueba que un porcentaje mal formado como impuesto lanza un error."""
        with self.assertRaises(ValueError):
            insert_item(self.session, 25.00, 2, '10percent')

            

if __name__ == "__main__":
    unittest.main()
