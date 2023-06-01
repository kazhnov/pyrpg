from classes import *
if language_choice == "en":
    import en as language
if language_choice == "ru":
    import ru as language
from items import *
from npcs import *
from random import randint, randrange
import os
from sys import exit
from msvcrt import getwch
import copy
wcls= lambda: os.system('cls')

erase = '\033[1A\x1b[2K'
up = '\033[1A'

def rename():
    if language_choice == "en":
        return
    for i in dictionary:
        if i.id in language.items:
            i.name = language.items[i.id]
            i.namecrop = (i.name + " "*20)[:20]
            
    for i in common_items:
        if i.id in language.items:
            i.name = language.items[i.id]
            i.namecrop = (i.name + " "*20)[:20]
            
    for i in uncommon_items:
        if i.id in language.items:
            i.name = language.items[i.id]
            i.namecrop = (i.name + " "*20)[:20]
            
    for i in rare_items:
        if i.id in language.items:
            i.name = language.items[i.id]
            i.namecrop = (i.name + " "*20)[:20]
            
    for i in loot_items:
        if i.id in language.items:
            i.name = language.items[i.id]
            i.namecrop = (i.name + " "*20)[:20]
            
    for i in debug_items:
        if i.id in language.items:
            i.name = language.items[i.id]
            i.namecrop = (i.name + " "*20)[:20]
            
            
def clear(player, world):
    wcls()
    l = []
    for i in range(len(world.main)):
        s = []
        for j in range(len(world.main[i])):
            if i == player.y and j == player.x:
                s.append("@")
            else:
                s.append(world.main[i][j])
        print(" ".join(s))
        s = "".join(s)
        l.append(s)
            
def make_dictionary():
    with open('dictionary.txt', 'w', encoding="utf-8") as f:
        k = 0
        #f.write("\nCOMMON ITEMS\n")
        for i in common_items:
            f.write(f'"{i.id}": "{i.name}",\n')
            k+= 1
        #f.write("\nUNCOMMON ITEMS\n")
        for i in uncommon_items:
            f.write(f'"{i.id}": "{i.name}",\n')
            k+= 1
        #f.write("\nRARE ITEMS\n")
        for i in rare_items:
            f.write(f'"{i.id}": "{i.name}",\n')
            k+= 1  
        #f.write("\nLOOT ITEMS\n") 
        for i in loot_items:
            f.write(f'"{i.id}": "{i.name}",\n')
            k+= 1
        #f.write("\nDEBUG ITEMS\n")
        for i in debug_items:
            f.write(f'"{i.id}": "{i.name}",\n')
            k+= 1 


def fight(player, enemy, world):
    print(language.fight_1, enemy.name)
    while enemy.dead != 1:
        menu(player, enemy, world)
        if player.escaped == 1:
            player.escaped -= 1
            break #Если получилось смыться
        if player.dead == 1:
            clear(player, world)
            print(language.fight_2, player.name, language.fight_3)
            print()
            print(language.fight_4)
            while True:
                ans = getwch()
                if ans:
                    break
            if ans == "r" or ans == "R" or ans == "к" or ans == "К":
                restart(world, player)
            else:
                input(language.fight_5)
                exit()
        result = randint(1, player.damage + enemy.damage)
        if result <= player.damage:
            win(player, enemy, world)
        else:
            lose(player, enemy, world)
    enemy.dead = 0
    
        
def win(player, enemy, world):
    print(erase*9)
    your_damage = int(player.damage * (player.damage/(player.damage + enemy.defense))) + randint(0,1) #Формула для вычисления дамага с учётом брони и рандома
    if enemy.health <= your_damage:
        player.level += 1
        print(language.win_1, enemy.name, language.win_2)
        enemy.dead = 1
        world.main[player.y][player.x] = "¤"
        while True:
            ans = getwch()
            if ans:
                break
        clear(player, world)
    else:
        print(enemy.name, language.win_3, your_damage, "hp")
        print()
        enemy.health -= your_damage
    
def lose(player, enemy, world):
    print(erase*9)
    enemy_damage = int(enemy.damage * (enemy.damage/(enemy.damage + player.defense))) + randint(0,1)
    if isinstance(player.right_hand, Shield):
        if player.right_hand.break_check(enemy.damage-enemy_damage) > randint(0,100):
            player.right_hand = Weapon("Fist", 1, "fist")
    if player.health <= enemy_damage:
        player.health = 0
        player.dead = 1
    else:
        print(player.name, language.lose, enemy_damage, "hp")
        player.health -= enemy_damage #Формула для вычисления дамага с учётом брони и рандома

def menu(player, enemy, world):
    print(enemy.name, language.menu_1, enemy.health, language.menu_2, enemy.damage)
    print(player.name, language.menu_1, player.health, language.menu_3, player.power, "+", player.weapon_damage, language.menu_4, player.defense)
    print(language.menu_5, str(int(player.damage/(player.damage + enemy.damage)*100))+"%")
    print(language.menu_6, str(int((player.agility)/(player.agility + enemy.agility)*100))+"%")
    print()
    print(language.menu_7)
    while True:
        ans = getwch()
        if ans:
            break
    if ans == "a" or ans == "ф":
        return
    elif ans == "e" or ans == "у":
        clear(player, world)
        open_inventory(player, world)
        menu(player, enemy, world)
    elif ans == "c" or ans == "с":
        run(player, enemy, world)
    else:
        clear(player, world)
        menu(player, enemy, world)
    
def open_inventory(player, world):
    ans = None
    pointer = 0
    while ans != "q" and ans != "й":
        clear(player, world)
        print()
        player.stats()
        player.show_inventory(pointer)
        print()
        print(f"{make_long(language.inventory_1, 30)} | {player.left_hand.print()} | {player.armor[0].print()}")
        print(f"{make_long(language.inventory_2, 30)} | {player.right_hand.print()} | {player.armor[1].print()}")
        print(f"{make_long(language.inventory_3, 30)} |                            | {player.armor[2].print()}")
        while True:
            ans = getwch()
            if ans:
                break
        if ans == "q" or ans == "й":
            clear(player, world)
        if ans == "s" or ans == "ы":
            pointer += 1
            if pointer == len(player.inventory):
                pointer = 0
        elif ans  ==  "w" or ans == "ц":
            pointer -= 1
            if pointer < 0:
                pointer = len(player.inventory) - 1
        elif ans == "a" or ans == "ф":
            player.put_left(pointer)
            pointer = 0
        elif ans == "d" or ans == "в":
            player.put_right(pointer)
            pointer = 0
        elif ans == "c" or ans == "с":
            player.put_armor(pointer)
            pointer = 0
        elif ans == "e" or ans == "у":
            use_from_inventory(player, pointer)
            pointer = 0
        

def use_from_inventory(player, number):
    item = player.inventory[number]
    if isinstance(item, Support): #Если это саппорт
        if item.type == "hp": #Хилка
            player.health += item.strength
            if player.health>player.max_health:
                player.health = player.max_health
            print(erase*(9+len(player.inventory))+language.use_heal_from_inventory, item.strength, "hp")
            if player.inventory[number].quantity <= 1:
                del player.inventory[number]
            else:
                player.inventory[number].increase(-1)
        if item.type == "ap": #Зелье проворства
            player.agility += item.strength
            print(erase*(9+len(player.inventory))+language.use_agility_from_inventory)
            if player.inventory[number].quantity <= 1:
                del player.inventory[number]
            else:
                player.inventory[number].increase(-1)
        if isinstance(item, Enemy):
            player.add_item(item.loot)
    else:
        print(erase*(9+len(player.inventory))+language.use_unhelpful_item)
    
    while True:
            ans = getwch()
            if ans:
                break
            
def run(player, enemy, world): #Смывка
    clear(player, world)
    result = randint(1, player.agility + enemy.agility)
    if result <= player.agility:
        print(language.run_1)
        player.escaped += 1
    else:
        print(language.run_2, enemy.damage, "hp")
        print()
        if player.health > enemy.damage:
            player.health -= enemy.damage
            menu(player, enemy, world)
        else:
            player.dead = 1

def main(world, player):
    rename()
    make_dictionary()
    while player.dead != 1:
        print()
        print(language.main)
        while True:
            ans = getwch()
            if ans:
                break
            
        if (ans == "w" or ans == "ц") and player.y>0:
            deltapos = [0, -1]
            check_position(world, player, deltapos)
        elif (ans == "s" or ans == "ы") and player.y<world.y-1:
            deltapos = [0, 1]
            check_position(world, player, deltapos)
        elif (ans == "a" or ans == "ф") and player.x>0:
            deltapos = [-1, 0]
            check_position(world, player, deltapos)
        elif (ans == "d" or ans == "в") and player.x<world.x-1:
            deltapos = [1, 0]
            check_position(world, player, deltapos)
        elif ans == "e" or ans == "у":
            open_inventory(player, world)
            main(world, player)
        elif ans == "f" or ans == "а":
            clear(player, world)
            inspection(world, player)
        clear(player, world)
        
def inspection(world, player):
    x = player.x
    y = player.y
    ans = None
    pointer = 0
    pointer2 = 0
    while ans != "q" and ans != "й":
        player.stats()
        player.inspect(world.meta[y][x], pointer, pointer2)
        print(language.inspection)
        while True:
            ans = getwch()
            if ans:
                break
        if ans == "s" or ans == "ы":
            pointer += 1
            
        if ans  ==  "w" or ans == "ц":
            pointer -= 1
                
        if ans == "a" or ans == "ф":
            pointer2 -= 1
        
        if ans == "d" or ans == "в":
            pointer2 += 1
            
        if (ans == "e" or ans == "у") and len(world.meta[y][x]) != 0:
            item = copy.deepcopy(world.meta[y][x][pointer2])
            item.quantity = 1
            player.add_item(item)
            world.increase(x, y, pointer2, -1)
                
        if (ans == "r" or ans == "к") and len(player.inventory) != 0:
            item = copy.deepcopy(player.inventory[pointer])
            item.quantity = 1
            world.add_item(item, x, y)
            if player.inventory[pointer].quantity > 1:
                player.inventory[pointer].increase(-1)
            else:
                print (player.inventory[pointer].quantity)
                del player.inventory[pointer]
        
        if pointer2 == len(world.meta[y][x]):
            pointer2 = 0
        if pointer2 < 0:
            pointer2 = len(world.meta[y][x])-1
        if pointer == len(player.inventory):
            pointer = 0
        if pointer < 0:
            pointer = len(player.inventory)-1        
        
        clear(player, world)
    clear(player, world)

def check_position(world, player, deltapos):
    y = player.y + deltapos[1]
    x = player.x + deltapos[0]
    clear(player, world)
    if isinstance(world.meta[y][x], Block) and world.meta[y][x].is_solid == True:
        return
    player.x += deltapos[0]
    player.y += deltapos[1]
    clear(player, world)
    if world.main[y][x] == "i":
        clear(player, world)
    if world.main[y][x] == "e":
        print()
        fight(player, world.meta[y][x][0], world)
        if world.check(Enemy) == 0:
            finish(player, world)

def finish(player, world):
    #clear(player, world)
    print(language.finish)
    while True:
        ans = getwch()
        if ans:
            break
    if ans == "r" or ans == "к":
        restart(world, player)
    else:
        exit()
        
def restart(world, player):
    world.main = []
    world.meta = []
    world.generate()
    player = Player(player.name, 1)
    player.add_item(common_items[0])
    player.add_item(common_items[1])
    player.add_item(common_items[2])
    player.add_item(common_items[3])
    clear(player, world)
    main(world, player)

