import unittest
from PyDnD.Roll import Roll

class TestRoll(unittest.TestCase):

    def test_single_die_roll(self):
        """Test rolling a single die without modifiers or drop_lowest."""
        result = Roll.roll(num_dice=1, sides=6)
        self.assertIn(result, range(1, 7), "Roll value should be between 1 and 6")

    def test_multiple_dice_roll(self):
        """Test rolling multiple dice without modifiers or drop_lowest."""
        result = Roll.roll(num_dice=3, sides=6)
        self.assertIn(result, range(3, 19), "Roll value should be between 3 and 18")

    def test_dice_with_modifier(self):
        """Test rolling dice with a positive modifier."""
        result = Roll.roll(num_dice=2, sides=6, modifier=2)
        self.assertIn(result, range(4, 15), "Roll value with modifier should be between 4 and 14")

    def test_dice_with_negative_modifier(self):
        """Test rolling dice with a negative modifier."""
        result = Roll.roll(num_dice=2, sides=6, modifier=-2)
        self.assertIn(result, range(0, 13), "Roll value with negative modifier should be between 0 and 13")

    def test_dice_with_drop_lowest(self):
        """Test rolling dice and dropping the lowest roll."""
        result = Roll.roll(num_dice=4, sides=6, drop_lowest=1)
        self.assertIn(result, range(3, 19), "Roll value after dropping lowest should be between 3 and 18")

    def test_roll_with_return_rolls(self):
        """Test rolling dice and returning the individual rolls."""
        total, rolls = Roll.roll(num_dice=5, sides=6, return_rolls=True)
        self.assertEqual(len(rolls), 5, "Should return a list of 5 rolls")
        for roll in rolls:
            self.assertIn(roll, range(1, 7), "Each roll should be between 1 and 6")
        self.assertEqual(total, sum(rolls), "Total should be the sum of the rolls")

    def test_invalid_num_dice(self):
        """Test that an invalid number of dice raises a ValueError."""
        with self.assertRaises(ValueError):
            Roll.roll(num_dice=0, sides=6)

    def test_invalid_sides(self):
        """Test that an invalid number of sides raises a ValueError."""
        with self.assertRaises(ValueError):
            Roll.roll(num_dice=1, sides=0)

    def test_invalid_drop_lowest(self):
        """Test that dropping more dice than rolled raises a ValueError."""
        with self.assertRaises(ValueError):
            Roll.roll(num_dice=2, sides=6, drop_lowest=3)

if __name__ == '__main__':
    unittest.main()
