"""
PyDnD is a python package for integrating DnD rulesets into external
applications.

{License_info}

Player Modules is responsible for setting and getting player skills, experience, and related information
that pertains strictly to the Player Character.
"""

# Built-in/Generic Imports
import json
from uuid import uuid4
import math
import warnings

# Import LevelingSystem
from .LevelingSystem import LevelingSystem
from .Roll import Roll
from .Inventory import Inventory, ItemNotInInventory, InventoryIsFull

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


class Player(object):
    """Player Object deals with all aspects of the player character
    
    Player Object deals with all aspects of the player character to include
    name, age, gender, description, biography, level, wealth, and all
    player Ability scores.  All can be omitted to create a blank, level 1 
    player and all values can be manually adjusted via the calling 
    application.
    
    All given Args populate self.argname
    
    Args:
        name         (str): Player character's name
        age          (str): Player character's age
        gender       (str): Player character's gender
        alignment    (str): Player character's two letter alignment
        description  (str): Physical description of Player character
        biography    (str): Backstory of Player character
        
        level        (int): Player character's starting level
        wealth       (int): Player character's starting wealth
        
        strength     (int): Player character's starting strength Ability Score
        dexterity    (int): Player character's starting dexterity Ability Score
        constitution (int): Player character's starting constitution Ability Score
        wisdom       (int): Player character's starting wisdom Ability Score
        intelligence (int): Player character's starting intelligence Ability Score
        charisma     (int): Player character's starting charisma Ability Score
        hp           (int): Player character's starting hitpoint value
        mp           (int): Player character's starting mp value (may convert to SPD)
        
    Returns:
        This object returns nothing.  Instead all Args populate self.argname
    """

    # Class Attributes
    VALID_ALIGNMENTS = {
            "LG":"Lawful Good",
            "NG":"Neutral Good",
            "CG":"Chaotic Good",
            "LN":"Lawful Neutral",
            "TN":"Neutral (True Neutral)",
            "CN":"Chaotic Neutral",
            "LE":"Lawful Evil",
            "NE":"Neutral Evil",
            "CE":"Chaotic Evil"
    }

    def __init__(
        self,
        name:               str = None,
        age:                str = None, 
        gender:             str = None, 
        alignment:          str = None,
        description:        str = None,
        biography:          str = None,
        level:              int = 1,
        wealth:             int = 0,
        strength:           int = None,
        dexterity:          int = None,
        constitution:       int = None,
        wisdom:             int = None,
        intelligence:       int = None,
        charisma:           int = None,
        hp:                 int = 1,
        mp:                 int = 0,
        inventory_size:     int = 10):
        """Object Initialization
    
        Object initialization, grabs all given Args and sets them to self.argname
        note that all Args can be omitted and a Level 1, blank character will be
        generated instead.
        
        Returns:
            Nothing
        """
        self.uid = uuid4()
        self.name = name
        self.age = age
        self.gender = gender
        self.description = description
        self.biography = biography
        self.alignment = alignment
        self.level = level
        self._experience = 0
        self.leveling_system = LevelingSystem(self)
        self.leveling_system.getCurrentExperience()
        self.wealth = wealth
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.wisdom = wisdom
        self.intelligence = intelligence
        self.charisma = charisma
        self.hp = hp
        self.mp = mp
        self.skillpoints = 0
        self.featpoints = 0
        self.inventory = Inventory(max_size=inventory_size)


    # UID Property
    @property
    def uid(self):
        return self.__uid

    @uid.setter
    def uid(self, value):
        self.__uid = value

    # Name Property
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = Player._validate_string(value, "Name")

    # Age Property
    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        self.__age = Player._validate_string(value, "Age")

    # Gender Property
    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, value):
        self.__gender = Player._validate_string(value, "Gender")

    # Description Property
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = Player._validate_string(value, "Description")

    # Biography Property
    @property
    def biography(self):
        return self.__biography

    @biography.setter
    def biography(self, value):
        self.__biography = Player._validate_string(value, "Biography")

    # Alignment Property
    @property
    def alignment(self):
        return self.__alignment

    @alignment.setter
    def alignment(self, value):
        if value is not None:
            value = value.upper() # Normalize value
            value = Player._validate_string(value, "Alignment")
            if len(value) != 2 or not Player.__validate_alignment(value):
                raise ValueError("Alignment must be a valid two-letter code(e.g., LE, NG, CG)")
        self.__alignment = value

    # Level Property
    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        if value is not None:
            value = Player._validate_integer(value, "Level")
            if value < 1:
                raise ValueError("Level cannot be lower than 1")
        self.__level = value

    # Experience Property
    @property
    def experience(self):
        """
        Gets the current experience of the player.

        Returns:
            int: The current experience points of the player.
        """
        return self._experience  
        
    @experience.setter
    def experience(self, value):
        """
        Sets the experience of the player and checks for level up or down.

        This setter method ensures that the player's experience is correctly updated.
        It automatically checks if the player should level up or down and triggers
        the appropriate actions.

        Args:
            value (int): The new experience value to set for the player.
        """
        self._experience = value
        # Recalculate experience needed for the next level
        self.leveling_system.getExpForNextLevel()

        # Check for level up
        while self.leveling_system.LeveledUp():
            self.leveling_system.levelUp()

        # Check for level down
        while self.leveling_system.LeveledDown():
            self.leveling_system.levelDown()  

    @property
    def nextLvlExperience(self):
        """
        Gets the experience required for the next level.

        Returns:
            int: The experience points needed to reach the next level.
        """
        return self.leveling_system.nextLvlExperience

    # Wealth Property
    @property
    def wealth(self):
        return self.__wealth

    @wealth.setter
    def wealth(self, value):
        if value is not None:
            value = Player._validate_integer(value, "Wealth")
            if value < 0:
                raise ValueError("Wealth cannot be negative")
        self.__wealth = value

    # Strength Property
    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, value):
        if value is not None:
            value = Player._validate_integer(value, "Strength")
            if value < 0:
                raise ValueError("Strength can not be negative")
            self.__strength = value
        else:
            # If strength is None, lets roll for it
            self.__strength = Roll.roll(4,6, drop_lowest=1)

    # Dexterity Property
    @property
    def dexterity(self):
        return self.__dexterity

    @dexterity.setter
    def dexterity(self, value):
        if value is not None:
            value = Player._validate_integer(value, "Dexterity")
            if value < 0:
                raise ValueError("Dexterity can not be negative")
            self.__dexterity = value
        else:
            # If strength is None, lets roll for it
            self.__dexterity = Roll.roll(4,6, drop_lowest=1)

    # Constitution Property
    @property
    def constitution(self):
        return self.__constitution

    @constitution.setter
    def constitution(self, value):
        if value is not None:
            value = Player._validate_integer(value, "Constitution")
            if value < 0:
                raise ValueError("Constitution can not be negative")
            self.__constitution = value
        else:
            # If strength is None, lets roll for it
            self.__constitution = Roll.roll(4,6, drop_lowest=1)     

    # Wisdom Property
    @property
    def wisdom(self):
        return self.__wisdom

    @wisdom.setter
    def wisdom(self, value):
        if value is not None:
            value = Player._validate_integer(value, "Wisdom")
            if value < 0:
                raise ValueError("Wisdom can not be negative")
            self.__wisdom = value
        else:
            # If strength is None, lets roll for it
            self.__wisdom = Roll.roll(4,6, drop_lowest=1)       

    # Intelligence Property
    @property
    def intelligence(self):
        return self.__intelligence

    @intelligence.setter
    def intelligence(self, value):
        if value is not None:
            value = Player._validate_integer(value, "Intelligence")
            if value < 0:
                raise ValueError("Wisdom can not be negative")
            self.__intelligence = value
        else:
            self.__intelligence = Roll.roll(4,6, drop_lowest=1)

    # Charisma Property
    @property
    def charisma(self):
        return self.__charisma

    @charisma.setter
    def charisma(self, value):
        if value is not None:
            value = Player._validate_integer(value, "Charisma")
            if value < 0:
                raise ValueError("Charisma can not be negative")
            self.__charisma = value
        else:
            self.__charisma = Roll.roll(4,6, drop_lowest=1)

    # HP Property
    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, value):
        if value is not None:
            value = Player._validate_integer(value, "HP")
            if value <= 0:
                raise ValueError("HP can not be negative or 0")
            self.__hp = value
        else:
            self.__hp = 1

    # mp Property
    @property
    def mp(self):
        return self.__mp

    @mp.setter
    def mp(self, value):
        if value is not None:
            value = Player._validate_integer(value, "MP")
            if value < 0:
                raise ValueError("MP can not be negative")
            self.__mp = value
        else:
            self.__mp = 0

    # Skillpoints Property
    @property
    def skillpoints(self):
        return self.__skillpoints

    @skillpoints.setter
    def skillpoints(self, value):
        if value is not None:
            value = Player._validate_integer(value, "Skillpoints")
            if value < 0:
                raise ValueError("Skillpoints can not be negative")
            self.__skillpoints = value
        else:
            self.__skillpoints = 0

    # Featpoints Property
    @property
    def featpoints(self):
        return self.__featpoints

    @featpoints.setter
    def featpoints(self, value):
        if value is not None:
            value = Player._validate_integer(value, "Featpoints")
            if value < 0:
                raise ValueError("Featpoints can not be negative")
            self.__featpoints = value
        else:
            self.__featpoints = 0                    

    # Inventory Methods
    def add_item_to_inventory(self, item, quantity=1):
        self.inventory.add_item(item, quantity)

    def remove_item_from_inventory(self, item, quantity=1):
        self.inventory.remove_item(item, quantity)

    def get_inventory(self):
        return self.inventory.items

    def get_inventory_max_size(self):
        return self.inventory.get_inventory_max_size()

    def giveExp(self, xp):
        self.leveling_system.giveExp(xp)

    def removeExp(self, xp):
        self.leveling_system.removeExp(xp)

    def LeveledUp(self):
        """This will be removed in version 1.1.0"""
        return self.leveling_system.LeveledUp()

    def LeveledDown(self):
        """This will be removed in version 1.1.0"""
        return self.leveling_system.LeveledDown()

    def levelUp(self):
        """This will be removed in version 1.1.0"""
        self.leveling_system.levelUp()

    def levelDown(self):
        """This will be removed in version 1.1.0"""
        self.leveling_system.levelDown()

    # Serialization/Deserialization
    # Json
    def serialize_to_json(self, filepath):
        """
        Serializes the Player object, including the inventory, into a JSON file.

        Args:
            filepath (str): The file path where the JSON will be saved.
        """
        player_data = {
            'uid': str(self.uid),
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'description': self.description,
            'biography': self.biography,
            'alignment': self.alignment,
            'level': self.level,
            'experience': self.experience,
            'nextLvlExperience': self.nextLvlExperience,
            'wealth': self.wealth,
            'strength': self.strength,
            'dexterity': self.dexterity,
            'constitution': self.constitution,
            'wisdom': self.wisdom,
            'intelligence': self.intelligence,
            'charisma': self.charisma,
            'hp': self.hp,
            'mp': self.mp,
            'skillpoints': self.skillpoints,
            'featpoints': self.featpoints,
            'inventory': self.inventory.items,  # Assuming inventory is a list of items
        }

        with open(filepath, 'w') as json_file:
            json.dump(player_data, json_file, indent=4)

        print(f"Player data serialized to {filepath}")

    # Get Modifier for Stat
    def get_modifier(self, stat):
        """Returns modifier for given stat

        Args:
            stat (int): The player ability score to calculate the modifier for

        Returns:
            modifier(int): The modifier for the given stat
        """
        return math.floor(stat/2)-5

    @staticmethod
    def deserialize_from_json(filepath):
        """
        Deserializes the Player object from a JSON file.

        Args:
            filepath (str): The file path where the JSON is stored.

        Returns:
            Player: The reconstructed Player object.
        """
        with open(filepath, 'r') as json_file:
            player_data = json.load(json_file)

        # Create a new Player object and populate its fields
        player = Player(
            name=player_data.get('name'),
            age=player_data.get('age'),
            gender=player_data.get('gender'),
            alignment=player_data.get('alignment'),
            description=player_data.get('description'),
            biography=player_data.get('biography'),
            level=player_data.get('level'),
            wealth=player_data.get('wealth'),
            strength=player_data.get('strength'),
            dexterity=player_data.get('dexterity'),
            constitution=player_data.get('constitution'),
            wisdom=player_data.get('wisdom'),
            intelligence=player_data.get('intelligence'),
            charisma=player_data.get('charisma'),
            hp=player_data.get('hp'),
            mp=player_data.get('mp'),
            inventory_size=10  # Set a default or modify based on the data if needed
        )

        # Set experience and skill/feat points
        player._experience = player_data.get('experience')
        player.skillpoints = player_data.get('skillpoints')
        player.featpoints = player_data.get('featpoints')

        # Reconstruct the inventory
        for item in player_data.get('inventory', []):
            player.add_item_to_inventory(item)

        print(f"Player data deserialized from {filepath}")
        return player        

    # Static Helper Methods
    @staticmethod
    def _validate_string(value, name):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(f"{name} must be a string")
        return value

    @staticmethod
    def _validate_integer(value, name):
        if value is not None:
            if not isinstance(value, int):
                raise ValueError(f"{name} must be an integer")
        return value

    @staticmethod
    def _validate_float(value, name):
        if value is not None:
            if not isinstance(value, float):
                raise ValueError(f"{name} must be a float")
        return value
        
    @staticmethod
    def __validate_alignment(alignment_key):
        return alignment_key in Player.VALID_ALIGNMENTS