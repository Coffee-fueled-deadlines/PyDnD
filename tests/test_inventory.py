import unittest
from PyDnD.Inventory import Inventory, ItemNotInInventory, InventoryIsFull

class TestInventory(unittest.TestCase):

    def setUp(self):
        """Set up a fresh inventory for each test."""
        self.inventory = Inventory(max_size=10)

    def test_add_item_single(self):
        """Test adding a single item to the inventory."""
        self.inventory.add_item("Healing Potion")
        self.assertEqual(self.inventory.items, ["Healing Potion"])

    def test_add_item_multiple(self):
        """Test adding multiple items to the inventory."""
        self.inventory.add_item("Healing Potion", quantity=3)
        self.assertEqual(self.inventory.items, ["Healing Potion"] * 3)

    def test_add_item_over_capacity(self):
        """Test adding items beyond the inventory capacity."""
        self.inventory.add_item("Healing Potion", quantity=8)
        with self.assertRaises(InventoryIsFull):
            self.inventory.add_item("Healing Potion", quantity=3)

    def test_remove_item_single(self):
        """Test removing a single item from the inventory."""
        self.inventory.add_item("Healing Potion", quantity=3)
        self.inventory.remove_item("Healing Potion")
        self.assertEqual(self.inventory.items, ["Healing Potion"] * 2)

    def test_remove_item_multiple(self):
        """Test removing multiple items from the inventory."""
        self.inventory.add_item("Healing Potion", quantity=5)
        self.inventory.remove_item("Healing Potion", quantity=3)
        self.assertEqual(self.inventory.items, ["Healing Potion"] * 2)

    def test_remove_item_not_enough(self):
        """Test attempting to remove more items than are present."""
        self.inventory.add_item("Healing Potion", quantity=2)
        with self.assertRaises(ItemNotInInventory):
            self.inventory.remove_item("Healing Potion", quantity=3)

    def test_remove_item_not_in_inventory(self):
        """Test attempting to remove an item that doesn't exist in the inventory."""
        with self.assertRaises(ItemNotInInventory):
            self.inventory.remove_item("Mjolnir")

    def test_inventory_is_full(self):
        """Test that the inventory is full after adding the maximum number of items."""
        self.inventory.add_item("Healing Potion", quantity=10)
        self.assertTrue(self.inventory.is_full())

    def test_inventory_is_not_full(self):
        """Test that the inventory is not full before reaching capacity."""
        self.inventory.add_item("Healing Potion", quantity=9)
        self.assertFalse(self.inventory.is_full())

    def test_add_invalid_quantity(self):
        """Test adding an item with an invalid (non-positive) quantity."""
        with self.assertRaises(ValueError):
            self.inventory.add_item("Healing Potion", quantity=0)
        with self.assertRaises(ValueError):
            self.inventory.add_item("Healing Potion", quantity=-1)

    def test_remove_invalid_quantity(self):
        """Test removing an item with an invalid (non-positive) quantity."""
        self.inventory.add_item("Healing Potion", quantity=5)
        with self.assertRaises(ValueError):
            self.inventory.remove_item("Healing Potion", quantity=0)
        with self.assertRaises(ValueError):
            self.inventory.remove_item("Healing Potion", quantity=-1)

if __name__ == '__main__':
    unittest.main()