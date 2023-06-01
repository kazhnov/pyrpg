from classes import Weapon, Armor, Support, Shield, language_choice
   
common_items = 	[Weapon("Copper dagger", 3 ), Support("Small Healing Potion","hp", 2),  Armor("Copper Helmet", 1, 0), Armor("Copper Chestplate", 2, 1), Armor("Copper Leggins", 2, 2),    Support("Small Agility Potion", "ap", 3), Shield("Wooden Shield", 4, 10, 10),
                 Armor("Leather Helmet", 1, 0 ), Armor("Leather Cout", 1, 1 ), Armor("Leather Pants", 1, 2 )
				]
uncommon_items =[Weapon("Iron Sword", 5),    Support("Medium Healing Potion", "hp", 4), Armor("Iron Helmet", 2, 0), Armor("Iron Chestplate", 4, 1),    Armor("Iron Leggins", 3, 2),  Support("Medium Agility Potion", "ap", 6), Shield("Steel Shield", 6, 20, 2)
				]
rare_items = 	[Weapon("Excalibur", 7),     Support("Big Healing Potion", "hp", 6),    Armor("Diamond Helmet", 4, 0),Armor("Diamond Chestplate", 6, 1), Armor("Diamond Leggins", 5, 2),  Support("Big Agility Potion", "ap", 9), Shield("Titanium Shield", 10, 40, 0.5)
				]
loot_items = 	[Weapon("Zombie Bone", 4),   Support("Skeleton Heart", "hb", 5),        Armor("Slime Gel", 3, 1),            Support("Spider Leg", "ab", 5),            Weapon("Wand of dishonest", 0)
				]
debug_items = [Weapon("ITEM NOT FOUND", 0, "error"), Weapon("Fist", 1)]


dictionary = []
for i in common_items:
    dictionary.append(i)
for i in uncommon_items:
    dictionary.append(i)
for i in rare_items:
    dictionary.append(i)
for i in loot_items:
    dictionary.append(i)
for i in debug_items:
    dictionary.append(i)
