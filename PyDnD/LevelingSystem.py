"""
PyDnD is a python package for integrating DnD rulesets into external
applications.

{License_info}

Leveling system is responsible for giving/removing experience giving/removing levels and tracking how much
experience is needed to next levels.
"""

# Built-in/Generic Imports
import operator as op
from functools import reduce

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

############################
#  Do not run if __main__  #
############################
if __name__ == "__main__":
    raise DoNotRunDirectly("This library is not meant to be called as __main__, import it instead.")

class LevelingSystem(object):
    """
    A class to handle the leveling system for a player character in a DnD game.

    This class manages the experience points of a player, determines when the player levels up or down,
    and calculates the experience thresholds required for each level. It is tightly integrated with the
    `Player` class and relies on it to track the player's current level and experience.
    
    Attributes:
        player (Player): The player object associated with this leveling system.
        nextLvlExperience (int): The amount of experience needed to reach the next level.
    """

    def __init__(self, player):
        """
        Initializes the LevelingSystem object with a player and calculates the experience required 
        for the next level.

        Args:
            player (Player): The player object for which this leveling system is responsible.
        """
        self.player = player
        self.nextLvlExperience = 0
        self.getCurrentExperience()  # Initialize current experience
        self.getExpForNextLevel()

    def giveExp(self, xp):
        """
        Increments the experience points of the player.

        This method adds the specified amount of experience points to the player's total. It also
        checks if the player has gained enough experience to level up, and if so, increases the player's
        level accordingly.

        Args:
            xp (int): The amount of experience points to add.
        """
        self.player._experience += xp
        while self.LeveledUp():
            self.levelUp()
        else:
            self.getExpForNextLevel()

    def removeExp(self, xp):
        """
        Decrements the experience points of the player.

        This method subtracts the specified amount of experience points from the player's total. It also
        checks if the player has lost enough experience to level down, and if so, decreases the player's
        level accordingly.

        Args:
            xp (int): The amount of experience points to subtract.
        """
        self.player._experience -= xp
        while self.LeveledDown():
            if self.player.level == 1:
                if xp > self.player._experience:
                    self.player._experience = 0
                break
            else:
                self.levelDown()
        else:
            self.getExpForNextLevel()

    def LeveledUp(self):
        """
        Checks if the player has gained enough experience to level up.

        Returns:
            bool: True if the player's experience points are greater than or equal to the threshold for the
            next level, False otherwise.
        """
        return self.player._experience >= self.getThresholdForNextLevel()

    def LeveledDown(self):
        """
        Checks if the player has lost enough experience to level down.

        Returns:
            bool: True if the player's experience points are less than the threshold for the
            current level, False otherwise.
        """
        return self.player._experience < self.getThresholdForCurrentLevel()

    def getCurrentExperience(self):
        """
        Calculates and sets the player's current experience points based on their level.

        This method attempts to use the player's current experience value, and if it is not set,
        it calculates the experience based on the player's current level.
        """
        try:
            self.player._experience = self.player._experience
        except exception as e:
            self.player._experience = int(1000 * (self.player.level + LevelingSystem.nCr(self.player.level, 2))) - (self.player.level * 1000)

    def getExpForNextLevel(self):
        """
        Calculates and sets the remaining experience points required to reach the next level.

        This method determines how much more experience the player needs to gain in order to level up.
        """
        if self.player.level == 1:
            # Experience needed to reach level 2
            self.nextLvlExperience = 1000 - self.player._experience
        else:
            # Calculate total experience required to reach the next level
            next_level_total_exp = int(1000 * ((self.player.level + 1) + LevelingSystem.nCr((self.player.level + 1), 2))) - ((self.player.level + 1) * 1000)
            # Calculate remaining experience required to reach the next level
            self.nextLvlExperience = next_level_total_exp - self.player._experience

    def getThresholdForNextLevel(self):
        """
        Calculates the total experience points required to reach the next level.

        Returns:
            int: The experience points required to reach the next level.
        """
        return int(1000 * ((self.player.level + 1) + LevelingSystem.nCr((self.player.level + 1), 2))) - ((self.player.level + 1) * 1000)

    def getThresholdForCurrentLevel(self):
        """
        Calculates the total experience points required to reach the current level.

        Returns:
            int: The experience points required to reach the current level.
        """
        return int(1000 * (self.player.level + LevelingSystem.nCr(self.player.level, 2))) - (self.player.level * 1000)

    def levelUp(self):
        """
        Increments the player's level by one.

        This method is called when the player gains enough experience to level up. It also recalculates
        the experience needed for the next level.
        """
        self.player.level += 1
        self.getExpForNextLevel()

    def levelDown(self):
        """
        Decrements the player's level by one.

        This method is called when the player loses enough experience to level down. If the player is
        already at level 1, it resets the player's experience to 0 instead of lowering the level further.
        """
        if self.player.level > 1:
            self.player.level -= 1
        self.getExpForNextLevel()

    @staticmethod
    def nCr(n, r):
        """
        Calculates combinations (nCr).

        This method is used to calculate the binomial coefficient, which is the number of ways to choose
        `r` elements from a set of `n` elements without regard to the order of selection.

        Args:
            n (int): The total number of items.
            r (int): The number of items to choose.

        Returns:
            float: The number of combinations (nCr).
        """
        r = min(r, n - r)
        numer = reduce(op.mul, range(n, n - r, -1), 1)
        denom = reduce(op.mul, range(1, r + 1), 1)
        return numer / denom
