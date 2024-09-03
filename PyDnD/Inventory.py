"""
PyDnD is a python package for integrating DnD rulesets into external
applications.

{License_info}

Inventory Module is creating and managing player inventories
"""

# META Data
__author__ = 'CFDeadlines'
__copyright__ = 'Copyright 2024, CFDeadlines'
__credits__ = ['CFDeadlines (Lead Programmer, Creator)']
__license__ = '{license}'
__version__ = '1.0.0'
__maintainer__ = 'CFDeadlines'
__email__ = 'cookm0803@gmail.com'
__status__ = 'Open'

# Custom exceptions
class ItemNotInInventory(Exception):
    pass

class InventoryIsFull(Exception):
    pass

class Inventory(object):
    """
    Inventory class to manage the player's items and track inventory size.

    Attributes:
        items (list): A list to hold items in the inventory.
        max_size (int): The maximum number of items the inventory can hold.
    """

    def __init__(self, max_size=10):
        """
        Initializes an empty inventory with a maximum size.

        Args:
            max_size (int): The maximum number of items that can be stored in the inventory. Default is 10.
        """
        self.items = []
        self.max_size = max_size

    def add_item(self, item, quantity=1):
        """
        Adds a specified quantity of an item to the inventory if there is space.

        Args:
            item (str): The item to add.
            quantity (int): The number of items to add. Default is 1.

        Raises:
            ValueError: If the quantity is not a positive integer.
            InventoryIsFull: If there is not enough space in the inventory.
        """
        if quantity <= 0:
            raise ValueError("Quantity to add must be a positive integer.")
            
        available_space = self.max_size - len(self.items)
        if available_space < quantity:
            raise InventoryIsFull(f"Not enough space in inventory to add {quantity} '{item}'. Space remaining: {available_space}.")

        for _ in range(quantity):
            self.items.append(item)

    def remove_item(self, item, quantity=1):
        """
        Removes an item from the inventory.

        Args:
            item (str): The item to remove.

        Raises:
            ValueError: If the item is not found in the inventory.
        """
        if quantity <= 0:
            raise ValueError("Quantity to remove must be a positive integer")

        if item not in self.items:
            raise ItemNotInInventory(f"Item '{item}' not found in inventory.")

        item_count = self.items.count(item)
        if item_count < quantity:
            raise ItemNotInInventory(f"There are only {item_count} '{item}' in the inventory, but {quantity} were requested to be removed.")

        for _ in range(quantity):
            self.items.remove(item)

    def get_inventory_max_size(self):
        """
        Returns the maximum size of the inventory

        Returns:
            int: The maximum size of the inventory
        """
        return self.max_size

    def get_inventory_size(self):
        """
        Returns the number of items in the inventory.

        Returns:
            int: The number of items in the inventory.
        """
        return len(self.items)

    def is_full(self):
        """
        Checks if the inventory is full.

        Returns:
            bool: True if the inventory is full, False otherwise.
        """
        return len(self.items) >= self.max_size

    def __str__(self):
        """
        Returns a string representation of the inventory.

        Returns:
            str: A comma-separated list of items in the inventory.
        """
        return ", ".join(self.items) if self.items else "Inventory is empty."