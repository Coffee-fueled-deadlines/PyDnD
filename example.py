from PyDnD import Roll

# Lets roll a D20
print( Roll.roll(num_dice=1, sides=20) )

# Lets roll 2 D20
print( Roll.roll(num_dice=2, sides=20) )

# Lets add a modifier
print( Roll.roll(num_dice=2, sides=20, modifier=4) )

# Lets roll a Stat using 4d6 and drop the lowest one
strength_stat = Roll.roll(num_dice=4, sides=6, drop_lowest=1)
print( f"Strength Stat is: {strength_stat}" )

# Now lets say that we want to see each of those rolls
# Lets tell the roller
strength_stat = Roll.roll(num_dice=4, sides=6, drop_lowest=1, return_rolls=True)
print( f"Strength Stat is: {strength_stat[0]} and the rolls where: {strength_stat[1]}" )

