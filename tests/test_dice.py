import unittest
from PyDnD.Dice import Dice

class TestDice(unittest.TestCase):

    def test_single_die_roll(self):
        """Test rolling a single die."""
        dice = Dice(num_dice=1, sides=6)
        dice.roll()
        self.assertIn(dice.value, range(1, 7), "Roll value should be between 1 and 6")
        self.assertEqual(len(dice.rolls), 1, "Should have only one roll")

    def test_multiple_dice_roll(self):
        """Test rolling multiple dice."""
        dice = Dice(num_dice=3, sides=6)
        dice.roll()
        # Ensure the total value is within the expected range for 3d6
        self.assertIn(dice.value, range(3, 19), "Roll value should be between 3 and 18")
        self.assertEqual(len(dice.rolls), 3, "Should have 3 rolls")

    def test_dice_with_modifier(self):
        """Test rolling dice with a modifier."""
        dice = Dice(num_dice=2, sides=6, modifier=2)
        dice.roll()
        # Minimum roll with modifier: 2 * 1 + 2 = 4
        # Maximum roll with modifier: 2 * 6 + 2 = 14
        self.assertIn(dice.value, range(4, 15), "Roll value with modifier should be between 4 and 14")

    def test_dice_with_drop_lowest(self):
        """Test rolling dice and dropping the lowest roll."""
        dice = Dice(num_dice=4, sides=6, drop_lowest=1)
        dice.roll()
        # Check the number of rolls and the value after dropping the lowest
        self.assertEqual(len(dice.rolls), 4, "Should have 4 rolls")
        self.assertTrue(3 <= dice.value <= 18, "Roll value after dropping lowest should be between 3 and 18")

    def test_dice_with_invalid_num_dice(self):
        """Test rolling with an invalid number of dice."""
        with self.assertRaises(ValueError):
            Dice(num_dice=0, sides=6)

    def test_dice_with_invalid_sides(self):
        """Test rolling with an invalid number of sides."""
        with self.assertRaises(ValueError):
            Dice(num_dice=1, sides=0)

    def test_dice_with_invalid_drop_lowest(self):
        """Test rolling with drop_lowest greater than num_dice."""
        with self.assertRaises(ValueError):
            Dice(num_dice=2, sides=6, drop_lowest=3)

if __name__ == '__main__':
    unittest.main()
