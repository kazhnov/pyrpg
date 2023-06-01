from classes import *
from functions import *
from items import *
from npcs import *
rename()
world = World(16, 8)
world.generate()
John = Player("John", 1)
clear(John, world)
John.add_item(id("copper_dagger"), 2)
John.add_item(id("copper_chestplate"))
John.add_item(id("small_agility_potion"), 2)
John.add_item(id("skeleton_heart"), 3)
John.add_item(id("wooden_shield"))
world.add_item(id("copper_dagger"), 0, 0)
world.add_item(id("small_healing_potion"), 0, 0)
world.add_item(id("iron_sword"), 0, 0)
world.add_item(id("medium_healing_potion"), 0, 0)
main(world, John)
