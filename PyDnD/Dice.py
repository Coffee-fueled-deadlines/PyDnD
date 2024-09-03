"""
PyDnD is a python package for integrating DnD rulesets into external
applications.

{License_info}

Dice Module is for creating dice objects used by any other modules
"""

# Built-in Imports
import random
from typing import List

# META Data
__author__ = 'CFDeadlines'
__copyright__ = 'Copyright 2024, CFDeadlines'
__credits__ = ['CFDeadlines (Lead Programmer, Creator)']
__license__ = '{license}'
__version__ = '1.0.0'
__maintainer__ = 'CFDeadlines'
__email__ = 'cookm0803@gmail.com'
__status__ = 'Open'

class Dice(object):
    """
    Dice object that handles rolling of dice using SystemRandom for better randomness.

    Args:
        num_dice (int): Number of dice to roll.
        sides (int): Number of sides on each die.
        modifier (int, optional): Modifier to add to the total roll. Default is 0.
        drop_lowest (int, optional): Number of lowest dice rolls to drop. Default is 0.

    Example:
        dice = Dice(num_dice=4, sides=6, drop_lowest=1)
        dice.roll()
        print(dice.value)  # The sum of the highest 3 rolls out of 4d6

    Attributes:
        value (int): The total result of the roll, including any modifiers.
        rolls (List[int]): The list of individual dice rolls.
    """

    def __init__(self, num_dice: int = 1, sides: int = 6, modifier: int = 0, drop_lowest: int = 0):
        if num_dice < 1 or sides < 1:
            raise ValueError("Number of dice and sides must be greater than 0.")
        if drop_lowest >= num_dice:
            raise ValueError("Cannot drop more dice than are rolled.")

        self.num_dice = num_dice
        self.sides = sides
        self.modifier = modifier
        self.drop_lowest = drop_lowest
        self.value = 0
        self.rolls = []
        self.random_generator = random.SystemRandom()

    def roll(self) -> None:
        """Rolls the dice and calculates the total value, applying any modifiers."""
        self.rolls = sorted([self.random_generator.randint(1, self.sides) for _ in range(self.num_dice)], reverse=True)
        if self.drop_lowest > 0:
            self.value = sum(self.rolls[:-self.drop_lowest]) + self.modifier
        else:
            self.value = sum(self.rolls) + self.modifier

    def __repr__(self):
        return f"<Dice: {self.num_dice}d{self.sides}+{self.modifier} (drop lowest {self.drop_lowest}) = {self.value}>"
