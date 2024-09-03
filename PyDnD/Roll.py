"""
PyDnD is a python package for integrating DnD rulesets into external
applications.

{License_info}

Roll Module is responsible for Rolling stats, dice, and any randomness that the application requires
"""

# Built-in/Generic Imports
from random import SystemRandom

# META Data
__author__ = 'CFDeadlines'
__copyright__ = 'Copyright 2024, CFDeadlines'
__credits__ = ['CFDeadlines (Lead Programmer, Creator)']
__license__ = '{license}'
__version__ = '1.0.0'
__maintainer__ = 'CFDeadlines'
__email__ = 'cookm0803@gmail.com'
__status__ = 'Open'

################
#  Exceptions  #
################
class DoNotRunDirectly(Exception):
    pass

# Import Dice functionality
from .Dice import Dice

############################
#  Do not run if __main__  #
############################
if __name__ == "__main__":
    raise DoNotRunDirectly("This library is not meant to be called as __main__, import it instead.")

class Roll(object):
    """
    Utility class for performing various types of dice rolls using the Dice object.
    
    Provides a single roll method that can be used for all types of rolls, 
    allowing the caller to specify the number of dice, sides, modifiers, 
    and any other options.
    """
    
    @staticmethod
    def roll(num_dice: int = 1, sides: int = 6, modifier: int = 0, drop_lowest: int = 0, return_rolls: bool = False):
        """
        Rolls a specified number of dice with a given number of sides, applying 
        any modifiers and optionally dropping the lowest rolls.
        
        Args:
            num_dice (int): Number of dice to roll.
            sides (int): Number of sides on each die.
            modifier (int, optional): Modifier to add to the total roll. Default is 0.
            drop_lowest (int, optional): Number of lowest dice rolls to drop. Default is 0.
            return_rolls (bool, optional): Whether to return the list of individual rolls along with the total. Default is False.

        Returns:
            int or tuple: The total result of the roll, including any modifiers. If `return_rolls` is True, returns a tuple of (total, list of rolls).
        
        Example:
            result = Roll.roll(num_dice=4, sides=6, drop_lowest=1)
            print(result)  # The sum of the highest 3 rolls out of 4d6

            total, rolls = Roll.roll(num_dice=4, sides=6, drop_lowest=1, return_rolls=True)
            print(total, rolls)  # The total and the list of individual rolls
        """
        dice = Dice(num_dice=num_dice, sides=sides, modifier=modifier, drop_lowest=drop_lowest)
        dice.roll()
        if return_rolls:
            return dice.value, dice.rolls
        else:
            return dice.value