from random import randrange, randint
import copy

language_choice = input("English (en) or РУсский (ru)?\n")
if language_choice == "en":
    import en as language
elif language_choice == "ru":
    import ru as language
    
def make_long(string, num):
    string = string + " "*20
    string = string[:num]
    return string

class Enemy:
    def __init__(self, name, damage, health, loot, id, defense = 0, level = 1):
        self.name = name
        self.id = id
        self.damage = damage * level
        self.health = health * level
        self.level = level
        self.defense = defense
        self.agility = 10
        self.dead = 0
        self.loot = loot
        self.quantity = 1
        
    def print(self):
        return f"{self.quantity}xDead {self.name} lvl {self.level}"

    def __str__(self):
        return f"{self.name} lvl {self.level}"

class Item:
    def __init__(self):
        pass
        

class Weapon(Item):
    def __init__(self, name, damage, id = "", level = 0, quantity = 1):
        self.namecrop = (name + " "*20)[:20]
        self.name = name
        if id != "":
            self.id = id
        else:
            self.id = name.lower().replace(" ", "_")
        self.level = level
        self.damage = damage
        self.quantity = quantity
    
    def increase(self, num):
        self.quantity += num
        
    def print(self):
        return f"{self.quantity}x{self.namecrop} ({self.damage})"
    
    def __str__(self):
        return f"{self.quantity}x{self.namecrop} | damage: {self.damage}"

class Armor(Item):
    def __init__(self, name, value, position, id = "", level = 0, quantity = 1):
        self.namecrop = (name + " "*20)[:20]
        self.name = name
        if id != "":
            self.id = id
        else:
            self.id = name.lower().replace(" ", "_")
        self.position = position
        self.level = level
        self.defense = value
        self.quantity = quantity

    def increase(self, num):
        self.quantity += num
    
    def print(self):
        return f"{self.quantity}x{self.namecrop} ({self.defense})"
    
    def __str__(self):
        return f"{self.quantity}x{self.namecrop} | armor: {self.defense}"

class Support(Item):
    def __init__(self, name, type, value, id = "", quantity = 1):
        self.namecrop = (name + " "*20)[:20]
        self.name = name
        if id != "":
            self.id = id
        else:
            self.id = name.lower().replace(" ", "_")
        self.type = type
        self.quantity = quantity
        if type == "hp":
            self.suport_type = "healing potion"
            self.strength = value
        if type == "ap":
            self.suport_type = "agility potion"
            self.strength = value
        if type == "hb":
            self.suport_type = "health boost"
            self.strength = value
        if type == "ab":
            self.suport_type = "agility boost"
            self.strength = value

    def increase(self, num):
        self.quantity += num
    
    def print(self):
        self.name = (self.name + " "*20)[:20]
        return f"{self.quantity}x{self.namecrop} ({self.strength})"
        
    def __str__(self):
        return f"{self.quantity}x{self.namecrop} | type: {self.suport_type} ({self.strength})"

class Shield(Item):
    def __init__(self, name, defense, base_durability, breaking_chance,  id = "", level = 0, quantity = 1):
        self.namecrop = (name + " "*20)[:20]
        self.name = name
        if id != "":
            self.id = id
        else:
            self.id = self.name.lower().replace(" ", "_")
        self.level = level
        self.defense = defense
        self.base_durability = base_durability
        self.durability = self.base_durability
        self.breaking_chance = breaking_chance
        self.quantity = quantity
    
    def increase(self, num):
        self.quantity += num
    
    def break_check(self, damage):
        self.durability -= damage
        return int(100*((self.base_durability - self.durability)/self.base_durability)/self.breaking_chance)
                
    def print(self):
        return f"{self.quantity}x{self.namecrop} ({self.defense})"
    
    def __str__(self):
        return f"{self.quantity}x{self.namecrop} | defense: {self.defense}"
            

class Block:
    def __init__(self, name, appearance, is_solid = True):
        self.name = name      
        self.appearance = appearance
        self.is_solid = is_solid
        
#Those files have entries of written above classes, so I import them after the program made classes
from items import *
from npcs import *
from blocks import *

def id(id):
    found = False
    for i in dictionary:
        if i.id == id:
            found = True
            return copy.deepcopy(i)
    if not(found):
        for i in dictionary:
            if i.id == "error":
                return copy.deepcopy(i)

class Player:
    def __init__(self, name, level = 0):
        self.name = name
        self.level = level

        self.base_health = 5
        self.health = self.base_health
        self.max_health = self.base_health
        self.healthboost = 0

        self.inventory = []
        self.right_hand = id("fist")
        self.left_hand = id("fist")
        self.armor = [id("leather_helmet"), id("leather_cout"), id("leather_pants")]

        self.power = 1
        self.weapon_damage = self.right_hand.damage + self.left_hand.damage
        self.damage = self.power + self.weapon_damage

        self.defense = 0

        self.base_agility = 3
        self.agility = self.base_agility
        self.agilityboost = 0
        
        self.y = 0
        self.x = 0
        
        self.dead = 0
        self.escaped = 0

    #Update stats on call    
    def update(self):
        self.weapon_damage = 0
        self.defense = 0
        self.agility -= self.agilityboost
        self.health -= self.healthboost
        self.healthboost = 0
        self.agilityboost = 0
        for i in self.inventory:
            if isinstance(i, Support):
                if i.type == "hb":
                    self.healthboost += int(i.strength)*i.quantity
                    self.health += self.healthboost
                    self.max_health = self.base_health + self.healthboost
                if i.type == "ab":
                    self.agilityboost += i.strength*i.quantity
        for j in self.armor:
            if isinstance(j, Armor):
                self.defense += j.defense
        if isinstance(self.right_hand, Shield):
            self.defense += self.right_hand.defense
        if isinstance(self.left_hand, Shield):
            self.defense += self.left_hand.defense
            
        if isinstance(self.right_hand, Weapon):
            self.weapon_damage += self.right_hand.damage
        if isinstance(self.left_hand, Weapon):
            self.weapon_damage += self.left_hand.damage
        
        self.damage = self.power + self.weapon_damage
        
        self.agility += self.agilityboost

    #Show stats
    def stats(self):
        self.update()
        print(self.name+"("+str(self.level)+")")
        print("Health: " + str(self.health) + " | Defense: " + str(self.defense))
        print("Strength: " + str(self.power) + "+" + str(self.weapon_damage))
        print("Agility: " + str(self.agility))
        print("")

    def show_inventory(self, pointer):
        k = 0
        print("inventory:")
        for i in self.inventory:
            if k == pointer:
                print(">" + str(i))
            else:
                print(" " + i.print())
            k += 1
            
    def inspect(self, items, pointer1, pointer2):
        print(language.classes_inspect)
        k = 0
        l = 0
        inspected = []
        for j in items:
            if l == pointer2:
                inspected.append(">" + str(j))
            else:
                inspected.append(" " + j.print())
            l += 1
        
        if len(self.inventory) > len(items):
            lenght = len(self.inventory)
        else:
            lenght = len(items)
        
        for i in range(0, lenght):
            if i < len(self.inventory):
                i = self.inventory[i]
            
            if k == pointer1 and k < len(items) and k < len(self.inventory):
                print((">" + str(i) + " "*40)[:40], inspected[k])
            elif k == pointer1 and k < len(self.inventory):
                print(">" + str(i))
            elif k < len(items)  and k < len(self.inventory):
                print((" " + i.print() + " "*40)[:40], inspected[k])
            elif k < len(self.inventory):
                print(" " + i.print())
            elif k < len(items):
                print(" "*40, inspected[k])
            k += 1
    
    def check_item(self, item):
        for i in self.inventory:
            if i.id == item.id:
                return self.inventory.index(i)
        return -1
            
    #Put chosen item in player's inventory
    def add_item(self, item, num = 1):
        for i in range(num):
            index = self.check_item(item)
            if index >= 0:
                self.inventory[index].increase(1)
            else:
                self.inventory.append(copy.deepcopy(item))
            self.update()
    
    def insert_item(self, item, insert_index):
        index = self.check_item(item)
        if index >=0:
            item2 = self.inventory.pop(index)
            self.inventory.insert(insert_index, item2)
            self.inventory[index].increase(1)
        else:
            self.inventory.insert(insert_index, item)
        self.update()

    
    def use(self, number):
        item = self.inventory[number]
        if isinstance(item, Support): #Если это саппорт
            if item.type == "hp": #Хилка
                self.health += item.strength
                if self.health>self.max_health:
                    self.health = self.max_health
                del self.inventory[number]
            if item.type == "ap": #Зелье проворства
                self.agility += item.strength
                del self.inventory[number]

    #Put item in either hand
    #TODO: make item instead of nums
    def put_right(self, num):
        if (isinstance(self.inventory[num], Weapon) or isinstance(self.inventory[num], Shield) )and self.right_hand != self.inventory[num]:
            item = copy.deepcopy(self.inventory[num])
            item.quantity = 1
            if self.inventory[num].quantity > 1:
                self.inventory[num].increase(-1)
            else:
                del self.inventory[num]
            self.add_item(self.right_hand)
            self.right_hand = item
            self.update()
            
    def put_left(self, num):
        if (isinstance(self.inventory[num], Weapon) or isinstance(self.inventory[num], Shield)) and self.left_hand != self.inventory[num]:
            item = copy.deepcopy(self.inventory[num])
            item.quantity = 1
            if self.inventory[num].quantity > 1:
                self.inventory[num].increase(-1)
            else:
                del self.inventory[num]
            self.add_item(self.left_hand)
            self.left_hand = item
            self.update()
    
    def put_armor(self, num):
        if isinstance(self.inventory[num], Armor):
            pos = self.inventory[num].position
            item = copy.deepcopy(self.inventory[num])
            item.quantity = 1
            if self.inventory[num].quantity > 1:
                self.inventory[num].increase(-1)
            else:
                del self.inventory[num]
            self.add_item(self.armor[pos])
            self.armor[pos] = item
            self.update()

class World:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.main = []
        self.meta = []

    def generate(self):
        self.main = []
        self.meta = []
        none = 0
        gloot = 1
        enemy = 2
        block = 3
        for k in range(self.y):
            y_main = []
            y_meta = []
            for l in range(self.x):
               y_main.append("¤")
               y_meta.append([])
            self.main.append(y_main)
            self.meta.append(y_meta)
        
        for y in range(1, self.y-1):
            for x in range(1, self.x-1):
                spawn_seed = randint(0,100)
                if spawn_seed <30:
                    spawn_type = block
                    self.meta[y][x] = self.block_gen()
                    self.main[y][x] = self.meta[y][x].appearance
                if spawn_seed <80:
                    spawn_type = none
                elif spawn_seed<90:
                    spawn_type = gloot
                    for i in range(spawn_type%3+1): #For generating different amount of items
                        self.add_item(self.gloot_gen(), x, y)
                else:
                    spawn_type = enemy
                    self.add_npc(self.enemy_gen(), x, y)
    
    def gloot_gen(self): #Generation of loot that lies on land
        loot_type = randint(0,100)
        if loot_type < 50:
            seed = randrange(len(common_items))
            i = common_items[seed]
        elif loot_type < 75:
            seed = randrange(len(uncommon_items))
            i = uncommon_items[seed]
        else:
            seed = randrange(len(rare_items))
            i = rare_items[seed]
        return i

    def enemy_gen(self):
        seed = randrange(len(enemies)-1)
        i = enemies[seed]
        return i
    def block_gen(self):
        seed = randrange(len(blocks))
        i = blocks[seed]
        return i
    def show_main(self):
        for i in self.main:
            print(" ".join(i))

    def check_item(self, item, j):
        for k in j:
            if k.id == item.id:
                return j.index(k)
        return -1
    
    def add_item(self, item, x, y):
        if self.main[y][x] != "e":
            self.main[y][x] = "i"
        index = self.check_item(item, self.meta[y][x])
        if index+1:
            self.meta[y][x][index].increase(1)
        else:
            self.meta[y][x].append(item)
        
    def increase(self, x, y, num, increment):
        if self.meta[y][x][num].quantity <= 0-increment:
            del self.meta[y][x][num]
            if len(self.meta[y][x]) == 0:
                self.main[y][x] = "¤"
            return 
        self.meta[y][x][num].increase(increment)
        
        
    def add_npc(self, npc, x, y):
        self.main[y][x] = "e"
        self.meta[y][x].append(npc)

    def show_meta(self):
        for i in self.meta:
            s = []
            for j in i:
                if j == "+":
                    s.append(j)
                else:
                    s.append(j.name)
            print(" ".join(s))
    
    def check(self, type):
        l = 0
        for i in self.meta:
            for j in i:
                if not(isinstance(j, Block)):
                    for k in j:
                       if isinstance(j, type):
                           l+=1
        return k
    