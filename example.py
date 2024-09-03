from PyDnD import Player
from PyDnD import Roll



if __name__ == '__main__':
		
	newPlayer = Player(name='Thor Odinson', age='34', gender='Male', description='Looks like a pirate angel', biography='Born on Asgard, God of Thunder')
		
	# newPlayer is created, lets display some stats
	print( "Name:" + newPlayer.name )
	print( "Age: " +newPlayer.age)
	print( "Gender:" + newPlayer.gender )
	print( "Description: " + newPlayer.description )
	print( "Biography: " + newPlayer.biography )
	print( "\n" )
	
	print( "\tLevel: " + str( newPlayer.level ) ) # Level isn't specified in creation, so level is 1
	print( "\tCurrent Experience: " + str( newPlayer.experience ) ) # Level wasn't specified, so current xp is 0
	print( "\tEXP to next Level: " + str( newPlayer.nextLvlExperience ) ) # 1000 Experience is required to get to level 2
	print( "\n\t--Stats--\n")
	print( "\t\tStrength is: " + str( newPlayer.strength ))
	print( "\t\tDexterity is: " + str( newPlayer.dexterity ))
	print( "\t\tConsitution is: " + str( newPlayer.constitution ))
	print( "\t\tWisdom is: " + str( newPlayer.wisdom ))
	print( "\t\tIntelligence is: " + str( newPlayer.intelligence ))
	print( "\t\tCharisma is: " + str( newPlayer.charisma ))
	print( "\n\t--Inventory--\n" )

	# Lets give Thor his hammer
	newPlayer.add_item_to_inventory("Mjolnir")
	print( f"\t\tThor's inventory is: \n\t\t\t{newPlayer.get_inventory()}\n" )
	
	# Oh no he's not worthy
	newPlayer.remove_item_from_inventory("Mjolnir")
	print( f"\t\tThor's inventory is: \n\t\t\t{newPlayer.get_inventory()}\n" )
	print( "\n" )

	print( "LEVEL UP")

	print("\n\n")
	# Lets see what Thor looks like as a level 2
	newPlayer.giveExp(1000)
	print( "\tNew Level: " + str( newPlayer.level ) ) # newPlayer.level is automatically increased when XP threshold increases
	print( "\tCurrent Experience: " + str( newPlayer.experience ) ) # Current, experience after leveling up
	print( "\tEXP to next Level: " + str( newPlayer.nextLvlExperience ) ) # 3000 Experience total is required to get to level 3
	print( "\n\t--Stats--\n")
	print( "\t\tStrength is: " + str( newPlayer.strength ))
	print( "\t\tDexterity is: " + str( newPlayer.dexterity ))
	print( "\t\tConsitution is: " + str( newPlayer.constitution ))
	print( "\t\tWisdom is: " + str( newPlayer.wisdom ))
	print( "\t\tIntelligence is: " + str( newPlayer.intelligence ))
	print( "\t\tCharisma is: " + str( newPlayer.charisma ))
	print( "\n\t--Inventory--\n" )

	# Lets give Thor back his hammer
	newPlayer.add_item_to_inventory("Mjolnir")
	print( f"\t\tThor's inventory is: \n\t\t\t{newPlayer.get_inventory()}\n" )
	
	# Oh no he's not worthy again
	newPlayer.remove_item_from_inventory("Mjolnir")
	print( f"\t\tThor's inventory is: \n\t\t\t{newPlayer.get_inventory()}\n" )
	print("\n\n")

	print( "LEVEL DOWN")

	print("\n\n")
	# Lets see what Thor looks like as a level 2
	newPlayer.removeExp(500)
	print( "\tNew Level: " + str( newPlayer.level ) ) # newPlayer.level is automatically increased when XP threshold increases
	print( "\tCurrent Experience: " + str( newPlayer.experience ) ) # Current, experience after leveling up
	print( "\tEXP to next Level: " + str( newPlayer.nextLvlExperience ) ) # 3000 Experience total is required to get to level 3
	print( "\n\t--Stats--\n")
	print( "\t\tStrength is: " + str( newPlayer.strength ))
	print( "\t\tDexterity is: " + str( newPlayer.dexterity ))
	print( "\t\tConsitution is: " + str( newPlayer.constitution ))
	print( "\t\tWisdom is: " + str( newPlayer.wisdom ))
	print( "\t\tIntelligence is: " + str( newPlayer.intelligence ))
	print( "\t\tCharisma is: " + str( newPlayer.charisma ))
	print( "\n\t--Inventory--\n" )

	# Lets give Thor back his hammer
	newPlayer.add_item_to_inventory("Mjolnir")
	print( f"\t\tThor's inventory is: \n\t\t\t{newPlayer.get_inventory()}\n" )
	
	# Oh no he's not worthy again
	newPlayer.remove_item_from_inventory("Mjolnir")
	print( f"\t\tThor's inventory is: \n\t\t\t{newPlayer.get_inventory()}\n" )
	print("\n\n")