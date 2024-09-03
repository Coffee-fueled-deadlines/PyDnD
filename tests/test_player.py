import unittest
from PyDnD.Player import Player
from PyDnD.Inventory import ItemNotInInventory, InventoryIsFull

class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Set up a basic player for testing."""
        self.player = Player(
            name="Test Player",
            age="25",
            gender="Male",
            alignment="NG",
            description="A brave warrior",
            biography="Born to be a hero",
            level=1,
            wealth=100,
            strength=15,
            dexterity=12,
            constitution=14,
            wisdom=10,
            intelligence=13,
            charisma=8,
            hp=10,
            mp=5,
            inventory_size=10
        )

    def test_initialization(self):
        """Test that the player is initialized correctly."""
        self.assertEqual(self.player.name, "Test Player")
        self.assertEqual(self.player.age, "25")
        self.assertEqual(self.player.gender, "Male")
        self.assertEqual(self.player.alignment, "NG")
        self.assertEqual(self.player.description, "A brave warrior")
        self.assertEqual(self.player.biography, "Born to be a hero")
        self.assertEqual(self.player.level, 1)
        self.assertEqual(self.player.wealth, 100)
        self.assertEqual(self.player.strength, 15)
        self.assertEqual(self.player.dexterity, 12)
        self.assertEqual(self.player.constitution, 14)
        self.assertEqual(self.player.wisdom, 10)
        self.assertEqual(self.player.intelligence, 13)
        self.assertEqual(self.player.charisma, 8)
        self.assertEqual(self.player.hp, 10)
        self.assertEqual(self.player.mp, 5)
        self.assertEqual(len(self.player.inventory.items), 0)

    def test_experience_and_leveling(self):
        """Test the experience and leveling system."""
        self.player.giveExp(1000)
        self.assertEqual(self.player.level, 2)
        self.assertEqual(self.player.experience, 1000)
        self.assertEqual(self.player.nextLvlExperience, 2000)

        self.player.removeExp(500)
        self.assertEqual(self.player.level, 1)
        self.assertEqual(self.player.experience, 500)
        self.assertEqual(self.player.nextLvlExperience, 500)

    def test_inventory_addition(self):
        """Test adding items to the player's inventory."""
        self.player.add_item_to_inventory("Sword", quantity=9)  # Fill inventory to 9/10 slots
        self.assertEqual(len(self.player.get_inventory()), 9)
        
        self.player.add_item_to_inventory("Shield")  # 10/10 slots now
        self.assertEqual(len(self.player.get_inventory()), 10)

        with self.assertRaises(InventoryIsFull):
            self.player.add_item_to_inventory("Helmet")  # Should raise InventoryIsFull since it's full


    def test_inventory_removal(self):
        """Test removing items from the player's inventory."""
        self.player.add_item_to_inventory("Potion", quantity=2)
        self.player.remove_item_from_inventory("Potion")  # Removes one potion
        self.assertEqual(self.player.get_inventory().count("Potion"), 1)

        with self.assertRaises(ItemNotInInventory):
            self.player.remove_item_from_inventory("Potion", quantity=2)  # Only 1 potion left, removing 2 should raise error


    def test_alignment_validation(self):
        """Test alignment validation."""
        with self.assertRaises(ValueError):
            self.player.alignment = "ABC"

    def test_negative_hp(self):
        """Test that negative HP raises an error."""
        with self.assertRaises(ValueError):
            self.player.hp = -5

    def test_invalid_stat(self):
        """Test that invalid stats raise an error."""
        with self.assertRaises(ValueError):
            self.player.strength = -1
        with self.assertRaises(ValueError):
            self.player.dexterity = "high"

    def test_inventory_full(self):
        """Test that adding too many items raises an InventoryIsFull exception."""
        self.player.add_item_to_inventory("Gold Coin", quantity=10)
     
