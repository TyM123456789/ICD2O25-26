#THINGS TO ADD OR FIX FOR LATER
# 1. add more comments (stopped commenting at def attack())
# 2. change stats screen
# 3. could make some code shorter by making a dict for repetitive with slightly different wording (like the stat mod code)
# 4. Change enemy ai abit. some updates to how effects are used for player may have some effect on enemy ai if i change that
# 5. multiple effects?? (boosts atk but loses def)
# 6. damaging self for boost -1/4 health for +3 atk
# 7. move order (needs speed stat)
# 8. accuracy
# 9. add more temporary stat boosts (evasion, spatk, spdef). right now, atk/def boosts boost both sp attacks and ph attacks
#resets attack modifiers for player and enemy
def reset_modifiers():
    global platk, enatk, pldef, endef, permplatk, permenatk, permpldef, permendef
    #uses permplatk instead of just 0 in case player bought Intimidate or Strong Start
    platk = permplatk
    enatk = permenatk
    pldef = permpldef
    endef = permendef
#imports randint
from random import randint, choice
from time import sleep
from copy import deepcopy
from math import floor
#sets amount of time to sleep between text
s = 0
def printsleep(str, time):
    print (str)
    sleep(time)
# dictionary of pokemon
# call by poke_dict[1]["Name"]
poke_dict = {
    1: {"Name": "Charmander", "Type": ["","Fire"], "Health": 0, "Move": ["", "Growl", "Tackle", "Ember"], "lvl": 1, "hp": 39, "atk": 52, "def": 43, "spatk": 60, "spdef": 50, "spd": 65},
    2: {"Name": "Bulbasaur", "Type": ["","Grass", "Poison"], "Health": 0, "Move": ["", "Growl", "Tackle", "Vine Whip"], "lvl": 1, "hp": 45, "atk": 49, "def": 65, "spatk": 65, "spdef": 45, "spd": 45},
    3: {"Name": "Squirtle", "Type": ["","Water"], "Health": 0, "Move": ["", "Tail Whip", "Tackle", "Water Gun"], "lvl": 1, "hp": 44, "atk": 48, "def": 65, "spatk": 50, "spdef": 64, "spd": 43},
    4: {"Name": "Pikachu", "Type": ["","Electric"], "Health": 0, "Move": ["", "Growl", "Tail Whip", "Tackle", "Thunder Shock"], "lvl": 1, "hp": 35, "atk": 55, "def": 40, "spatk": 50, "spdef": 50, "spd": 90},
    5: {"Name": "A Gun", "Type": ["","Steel"], "Health": 0, "Move": ["", "Shoot Hands", "Shoot Chest", "Load Explosive Ammo", "Shoot Head"], "lvl": 100, "hp": 120, "atk": 120, "def": 120, "spatk": 120, "spdef": 120, "spd": 120},
    6: {"Name": "Punching Bag", "Type": ["","Fighting"], "Health": 0, "Move": ["", "Brace For Impact"], "lvl": 100, "hp": 180, "atk": 60, "def": 180, "spatk": 60, "spdef": 180, "spd": 60}
}
#list of all possible enemies/starters
enemies = [3]
starters = [1, 2, 3]
#dictionary of moves. 
#call by move_dict[(move#)]["Name"]    if effect is 4 char, first char is targ, 2nd char is amount, 3rd is stat, last is direction
move_dict = {
    1: {"Name": "Growl", "Type": "Normal", "Power": 0, "Effect": "d1A-", "MoveType": "Status"},
    2: {"Name": "Tail Whip", "Type": "Normal", "Power": 0, "Effect": "d1D-", "MoveType": "Status"},
    3: {"Name": "Tackle", "Type": "Normal", "Power": 40, "Effect": "", "MoveType": "Phys"},
    4: {"Name": "Ember", "Type": "Fire", "Power": 40, "Effect": "", "MoveType": "Spec"},
    5: {"Name": "Vine Whip", "Type": "Grass", "Power": 45, "Effect": "", "MoveType": "Phys"},
    6: {"Name": "Water Gun", "Type": "Water", "Power": 40, "Effect": "", "MoveType": "Spec"},
    7: {"Name": "Thunder Shock", "Type": "Electric", "Power": 40, "Effect": "", "MoveType": "Spec"},
    8: {"Name": "Shoot Head", "Type": "Steel", "Power": 150, "Effect": "", "MoveType": "Phys"},
    9: {"Name": "Shoot Chest", "Type": "Steel", "Power": 75, "Effect": "d9D-", "MoveType": "Phys"},
    10: {"Name": "Shoot Hands", "Type": "Steel", "Power": 60, "Effect": "d9A-", "MoveType": "Phys"},
    11: {"Name": "Load Explosive Ammo", "Type": "Steel", "Power": 0, "Effect": "a9A+", "MoveType": "Status"},
    12: {"Name": "Brace For Impact", "Type": "Fighting", "Power": 0, "Effect": "a9D+", "MoveType": "Status"}
}
#type list
type_chart = {
    "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
    "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 2, "Bug": 2, "Rock": 0.5, "Dragon": 0.5, "Steel": 2},
    "Water": {"Fire": 2, "Water": 0.5, "Grass": 0.5, "Ground": 2, "Rock": 2, "Dragon": 0.5},
    "Grass": {"Fire": 0.5, "Water": 2, "Grass": 0.5, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Bug": 0.5, "Rock": 2, "Dragon": 0.5, "Steel": 0.5},
    "Electric": {"Water": 2, "Grass": 0.5, "Electric": 0.5, "Ground": 0, "Flying": 2, "Dragon": 0.5},
    "Ice": {"Water": 0.5, "Grass": 2, "Ice": 0.5, "Ground": 2, "Flying": 2, "Dragon": 2, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dark": 2, "Steel": 2, "Fairy": 0.5},
    "Poison": {"Grass": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0, "Fairy": 2},
    "Ground": {"Fire": 2, "Electric": 2, "Grass": 0.5, "Poison": 2, "Flying": 0, "Bug": 0.5, "Rock": 2, "Steel": 2},
    "Flying": {"Electric": 0.5, "Grass": 2, "Fighting": 2, "Bug": 2, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Dark": 0, "Steel": 0.5},
    "Bug": {"Fire": 0.5, "Grass": 2, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2, "Ghost": 0.5, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2, "Ice": 2, "Fighting": 0.5, "Ground": 0.5, "Flying": 2, "Bug": 2, "Steel": 0.5},
    "Ghost": {"Normal": 0, "Psychic": 2, "Ghost": 2, "Dark": 0.5},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {"Fighting": 0.5, "Psychic": 2, "Ghost": 2, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2, "Rock": 2, "Steel": 0.5, "Fairy": 2},
    "Fairy": {"Fire": 0.5, "Fighting": 2, "Poison": 0.5, "Dragon": 2, "Dark": 2, "Steel": 0.5}
}
#item bag call by bag[(item#)]["Name"]
bag = {
    1: {"Name": "Potion","Amount": 0},
    2: {"Name": "Pokeball","Amount": 0}
}
#shop inventory call by shop[(item#)]["Name"]
shop = {
    1: {"Name": "Potion", "Description": "Heals Pokemon by 50 HP", "Cost": 4, "Multiple": True, "Amount": 99},
    2: {"Name": "Pokeball", "Description": "Chance to catch enemy Pokemon","Cost": 6, "Multiple": True, "Amount": 99},
    3: {"Name": "Intimidate", "Description": "Enemy starts fight with -1 atk", "Cost": 10, "Multiple": False, "Amount": 1},
    4: {"Name": "Strong Start", "Description": "Start fight with +1 atk", "Cost": 10, "Multiple": False, "Amount": 1},
    5: {"Name": "Full Heal", "Description": "Heals Pokemon to full health", "Cost": 8, "Multiple": False, "Amount": 1}
}
#calculates pokemon max hp
def hp_calc(poke):
    return floor((2*poke["hp"]*poke["lvl"])/100+poke["lvl"]+10)
#gets player name and starter pokemon. makes global
def create_character():
    global name, pokemon, party, shop
    #gets name. name is used in end stats
    name = input("Enter your character's name: ")
    #choose a pokemon
    print (f"What Pokemon do you want to start with? {poke_dict[starters[0]]["Name"]}(1), {poke_dict[starters[1]]["Name"]}(2), or {poke_dict[starters[2]]["Name"]}(3)")
    choice = int(input(""))
    #if answer wasn't one of the options
    if choice > 3 or choice < 1:
        choice = starters[0]
        print (f"That is not one of the options. You will use {poke_dict[starters[0]]["Name"]}.")
    pokemon = deepcopy(poke_dict[starters[choice - 1]])
    pokemon["Health"] = hp_calc(pokemon)
    party = [pokemon["Name"]]
#short intro
def game_intro():
    printsleep (f"Welcome to the Kanto region, {name}!", s)
    printsleep (f"Your starter Pokemon is {pokemon["Name"]}.", s)
    printsleep (f"Your journey will be difficult, but you will meet many friends and partners along the way!", s)
#starting shop
def start_shop():
    global bag, coins
    exit = False
    printsleep (f"Before embarking on your journey, you go to the Pokeshop.", s)
    #creates new dictionary to not mod original shop values
    startshop = deepcopy(shop)
    #assigns costs for each item (costs are random)
    for product in startshop:
        startshop[product]["Cost"] = item_cost(product, startshop)
    #makes it so player can go to shop menu multiple times to buy multiple things. cancelled by exitting
    while exit == False:
        #prints headers
        print (f"{"Items":<14}{f"Pokedollars: {coins}":>50}")
        print ("-"*65)
        #for each product, format a row
        for x in range (1,3):
            format_row(startshop[x]["Name"],  startshop[x]["Amount"], x, startshop[x]["Description"], startshop[x]["Cost"])
        print ("-"*65)
        #tells player how to exit
        print ("Exit (0)")
        #sets item to 0 for later use
        item = -1
        #while loop lets player keep choosing until they settle on a possible option
        while item < 0 or item > 2:
            #takes input
            item = int(input(""))
            #gives error if answer isnt an option
            if item < 0 or item > 2:
                print ("That is not an option. Try Again.")
        #lets player exit
        if item == 0:
            print ("You exit the shop.")
            exit = True
        else:
            #asks for another input and explains how to exit
            print (f"How many {startshop[item]["Name"]}'s do you want to buy? Press 0 to exit.")
            #for later use
            totcost = 100000
            amount = 0
            #while total cost too expensive (lets player enter again if answer is invalid)
            while coins < totcost or amount > startshop[item]["Amount"]:
                amount = int(input(""))
                #calculates cost
                totcost = amount * startshop[item]["Cost"]
                #gives error if cost is too high
                if totcost > coins:
                    print (f"You can't afford {amount} {startshop[item]["Name"]}'s")
                elif amount > startshop[item]["Amount"]:
                    print (f"There are only {startshop[item]["Amount"]} {startshop[item]["Name"]}'s in stock.")
            #subtracts cost
            coins -= totcost
            #adds item to bag
            startshop[item]["Amount"] -= amount
            bag[item]["Amount"] += amount
#sells caught/killed pokemon
def sell_pokemon():
    global party, pokemon_caught, pokemon_killed, fights_won, coins
    killed_tot = 0
    caught_tot = 0
    #adds up mmoney made from selling dead/caught pokemon. uses for loop to increase randomness
    for x in range(1,pokemon_killed+1):
        killed_tot += randint(13,15)
        print ("test")
    for x in range(1,len(party)):
        if x != 0:
            caught_tot += randint(15,17)
            del party[1]
    printsleep (f"You killed {pokemon_killed} Pokemon in the past {fights_won} fights!", s)
    printsleep (f"You sold their bodies for a total of {killed_tot} Pokedollars!", s)
    printsleep (f"You caught {pokemon_caught} Pokemon in the past {fights_won} fights!", s)
    printsleep (f"You sold their bodies for a total of {caught_tot} Pokedollars!", s)
    coins += killed_tot + caught_tot
#shop at 5 fights won
def midway_shop():
    #same as other shop but with more options.
    global bag, coins, permplatk, permenatk, plhp
    exit = False
    printsleep (f"Along your journey, you see a Pokeshop.", s)
    midshop = deepcopy(shop)
    for product in midshop:
        midshop[product]["Cost"] = item_cost(product, midshop)
    while exit == False:
        print (f"{"Items":<14}{f"Pokedollars: {coins}":>50}")
        print ("-"*65)
        for x in midshop:
            format_row(midshop[x]["Name"], midshop[x]["Amount"], x, midshop[x]["Description"], midshop[x]["Cost"])
        print ("-"*65)
        print (f"Exit (0)")
        item = -1
        while item < 0 or item > len(midshop):
            item = int(input(""))
            if item < 0 or item > len(midshop):
                print ("That is not an option. Try Again.")
        if item == 0:
            print ("You exit the shop.")
            exit = True
        elif midshop[item]["Multiple"]==True:
            print (f"How many {midshop[item]["Name"]}'s do you want to buy? Press 0 to exit.")
            totcost = 100000
            while coins < totcost or amount > midshop[item]["Amount"]:
                amount = int(input(""))
                totcost = amount * midshop[item]["Cost"]
                if totcost > coins:
                    print (f"You can't afford {amount} {midshop[item]["Name"]}'s")
                elif amount > midshop[item]["Amount"]:
                    print (f"There are only {midshop[item]["Amount"]} {midshop[item]["Name"]}'s in stock.")
            coins -= totcost
            bag[item]["Amount"] += amount
        else:
            if midshop[item]["Cost"] <= coins and midshop[item]["Amount"] >0:
                if midshop[item]["Name"] == "Strong Start":
                    permplatk += 1
                    midshop[item]["Amount"] -= 1
                    coins -= midshop[item]["Cost"]
                elif midshop[item]["Name"] == "Intimidate":
                    permenatk -= 1
                    midshop[item]["Amount"] -= 1
                    coins -= midshop[item]["Cost"]
                elif midshop[item]["Name"] == "Full Heal":
                    plhp = pokemon["Health"]
                    midshop[item]["Amount"] -= 1
                    coins -= midshop[item]["Cost"]
                print (f"You bought {midshop[item]["Name"]}!")
            elif midshop[item]["Cost"] > coins:
                print (f"You can't afford {midshop[item]["Name"]}.")
            elif midshop[x]["Amount"] <= 0:
                print (f"There are no more {midshop[item]["Name"]}'s in stock.")
#formats shop row
def format_row(name, amount, num, desc, cost):
    #formats shop row
    print (f"{name:<15}{f"{amount}x":<4}{f"({num})":<5}{desc:<30}{cost:>10}P")
#generates item cost 
def item_cost(item, shop_cata):
    #creates a random item cost
    return randint(shop_cata[item]["Cost"]-1, shop_cata[item]["Cost"]+1)
#sets up player hp and enemy hp and makes global
def setup():
    global plhp, coins, permenatk, permplatk, permendef, permpldef, pokemon_caught, pokemon_killed, xp
    #resets all stats
    permplatk = 0
    permenatk = -6
    permpldef = 0
    permendef = 0
    coins = 75
    xp = 0
    #draws from dictionary
    plhp = pokemon["Health"]
    pokemon_killed = 0
    pokemon_caught = 0
#level up
def level_up():
    global xp, pokemon
    xp = 0
    pokemon["lvl"]+=1
    pokemon["Health"] = hp_calc(pokemon)
#randomizes and enemy between the available pokemon and prints a small message
def encounter():
    global enemy, enhp, fights_won
    #generates an enemy
    enemy = choice(enemies)
    printsleep (f"In Route {fights_won+1}, you stumble across a wild {poke_dict[enemy]["Name"]}!", s)
    enemy = deepcopy(poke_dict[enemy])
    #sets enemy lvl
    enemy["lvl"] = 1
    #sets enemy health
    enemy["Health"] = hp_calc(enemy)
    enhp = enemy["Health"]
def battle():
    #lets player choose between attacking or entering bag
    def player_turn():
        #prints headers
        print (f"Turn: {turn}     Health: {plhp}     Enemy Health: {enhp}")
        #gives options
        print ("Attack (1)\nItems (2)")
        choice = int(input(""))
        #if player enters an incorrect option
        if choice >2 or choice < 1:
            print ("That is not an option. You took too long and missed your turn.")
        elif choice == 1:
            attack()
        else:
            open_bag()
    #opens bag
    def open_bag():
        #used to keep track of amount of different items. Not needed rn but maybe later
        item_num = 1
        #prints out all items
        for item in bag:
            print (f"{bag[item]["Name"]} x{bag[item]["Amount"]} ({item_num})")
            item_num+=1
        #shows player how to go back
        print (f"Back (0)")
        #takes input
        choice = int(input(""))
        if choice == 0:
            player_turn()
        #ends turn if answer isn't accepted
        elif choice >item_num or choice < 1 or bag[choice]["Amount"] == 0:
            print ("You couldn't find the item you were looking for.")
        elif bag[choice]["Name"] == "Potion":
            bag[choice]["Amount"]-=1
            global plhp
            plhp = heal(pokemon, plhp, 20)
        elif bag[choice]["Name"] == "Pokeball":
            bag[choice]["Amount"]-=1
            throw_pokeball()
    #calculates whether opponent pokemon is weak to chosen attack. resist - 50% dam. weak - 200% dam
    def weakness(attack, opp_poke):
        #checks weakness and returns mult value.
        mult = 1
        attack_type = move_dict[attack]["Type"]
        enemy_type = opp_poke["Type"]
        #for each enemy type (all enemies i have rn only have one type)
        for type in enemy_type:
            if type in type_chart.get(attack_type, {}):
                mult *= type_chart[attack_type][type]
        return mult
    #prints message based on effectiveness
    def effect_text(effectiveness):
        if effectiveness == 4:
            printsleep ("It was extremely effective!", s)
        elif effectiveness == 2:
            printsleep ("It was super effective!", s)
        elif effectiveness == .5:
            printsleep ("It was not very effective...", s)
        elif effectiveness == .25:
                printsleep ("It was mostly ineffective...", s)
        elif effectiveness == 0:
            printsleep ("It has no effect...", s)        
    #checks if pokemon type is same as attack type. if so, 50% dam boost
    def stab(attack, poke):
        #the mechanic STAB (same type attack bonus) provides 1.5x mult if pokemon type is same is it's move
        attack_type = move_dict[attack]["Type"]
        player_type = poke["Type"]
        if attack_type in player_type:
            return 1.5
        else:
            return 1
    #1/24 chance of 50% damage boost
    def crit_calc():
        num = randint(1,24)
        if num == 1:
            return 1.5
        else:
            return 1
    # calculates catch
    def throw_pokeball():
        global enhp, pokemon_caught
        #gives value from 1 to max enemy hp
        catch_num = randint(1,enemy["Health"])
        #if catch value is more than or equal to 90% of enemy health
        printsleep (".", s*1.5)
        printsleep ("..", s*1.5)
        if catch_num >= enhp*.9:
            printsleep ("...", s*1.5)
            enhp = "Caught"
            print ("Catch Successful!")
            pokemon_caught +=1
            party.append(enemy["Name"])
        else:
            print ("Catch Failed...")
    #calculates heal
    def heal(poke, health, amount):
        #calculates heal
        if health + amount <= poke["Health"]:
            printsleep (f"Your {poke["Name"]} is now at {health + amount} HP.", s)
            return health + amount
        #makes so health cant go above max
        else:
            printsleep (f"Your {poke["Name"]} is now at {poke["Health"]} HP.", s)
            return pokemon["Health"]
    #move in poke_dict to move in move_dict
    def poke_to_move_dict(poke, move):
        #poke: pokemon with chosen move
        #move: index of move in the chosen pokemons list of moves
        name = poke["Move"][move]
        for move in move_dict:
            #if name of move in move_dict matches move name
            if move_dict[move]["Name"] == name:
                #return move number
                return move
    #calculates damage. uses above functions
    def damage_calc(poke, opppoke, attack, pokeatk, oppdef):
        #translates move in poke dict to move in move dict
        attack = poke_to_move_dict(poke, attack)
        #finds damage value of move
        power = move_dict[attack]["Power"]
        random = (randint(85,100))
        crit = crit_calc()
        lvl = poke["lvl"]
        if move_dict[attack]["MoveType"] == "Phys":
            raw_atk = floor(((2 * poke["atk"] + 31) * lvl) / 100) + 5
            raw_def = floor(((2 * opppoke["def"] + 31) * lvl) / 100) + 5
        elif move_dict[attack]["MoveType"] == "Spec":
            raw_atk = floor(((2 * poke["spatk"] + 31) * lvl) / 100) + 5
            raw_def = floor(((2 * opppoke["spdef"] + 31) * lvl) / 100) + 5
        modAtk = floor(raw_atk * stg_to_mod(pokeatk))
        modDef = floor(raw_def * stg_to_mod(oppdef))
        Type = weakness(attack, opppoke)
        modifier = Type * stab(attack, poke) * random/100 * crit
        A = floor((2*lvl)/5+2)
        B = floor(A*power*(modAtk/modDef))
        C = floor(B/50)+2
        final = floor(C * modifier)
        if Type != 0:
            return max(1, final), crit
        else:
            return 0
    #stg to mod
    def stg_to_mod(stg):
        #translates stage of stat (+1) atk for example to modifier (in +1 attack's case, it would be 3/2)
        if stg<0:
            return 2/(2+stg*-1)
        else:
            return (2+stg)/2    
    #add/subtract effect
    def mod_effect(stg, direction, amount):
        print (stg)
        #changes stage
        if direction:
            stg+=1*amount
            print (stg)
        elif not direction:
            stg-=1*amount
            print (stg)
        if stg > 6:
            stg = 6
        elif stg < -6:
            stg = -6
        return stg
    #calculates effects
    def apply_effect(poke, move, aatk, adef, datk, ddef):
        move = poke_to_move_dict(poke, move)
        #translates the modifier code to meaning
        move = move_dict[move]["Effect"]
        if move[0] == "a":
            if move[2] == "A":
                stg = mod_effect(aatk, move[3]=="+", int(move[1]))
                return stg, "a", "a"
            elif move[2] == "D":
                stg = mod_effect(adef, move[3]=="+", int(move[1]))
                return stg, "d", "a"   
        elif move[0] == "d":
            if move[2] == "A":
                stg = mod_effect(datk, move[3]=="+", int(move[1]))
                print (stg)
                return (stg),("a"), ("d")
            elif move[2] == "D":
                stg = mod_effect(ddef, move[3]=="+", int(move[1]))
                return stg, "d", "d"                       
    #uses player choice to apply attack.
    def attack():
        global enatk, platk, pldef, endef, enhp, pokemon_killed
        for move in range(1,len(pokemon["Move"])):
            if move != "":
                print (f"{pokemon["Move"][move]} ({move})")
        print (f"Back (0)")
        choice = int(input(""))
        if choice != 0 and choice >len(pokemon["Move"])-1 or choice < 0:
            print (f"Your {pokemon["Name"]} didn't understand your command.")
            choice = 0
        elif choice == 0:
            player_turn()
        elif move_dict[poke_to_move_dict(pokemon, choice)]["Power"] > 0:
            damage, crit = damage_calc(pokemon, enemy, choice, platk, endef)
            global enhp
            enhp -= damage
            enhp = floor(enhp)
            printsleep (f"Your {pokemon["Name"]} used {pokemon["Move"][choice]}", s)
            move_effect = weakness(poke_to_move_dict(pokemon, choice), enemy)
            effect_text(move_effect)
            if crit == 1.5:
                printsleep ("It was a critical hit!", s)
            if enhp > 0:
                printsleep (f"It did {int(round(damage,0))} damage! The enemy {enemy["Name"]} is now at {int(round(enhp,0))} health!", s)
            else:
                printsleep (f"You did {int(round(damage,0))} damage! The enemy {enemy["Name"]} fainted.", s)
                pokemon_killed += 1
                enhp = "Dead"
        if choice != 0 and len(move_dict[poke_to_move_dict(pokemon, choice)]["Effect"]) == 4 and enhp != "Dead":
            if move_dict[poke_to_move_dict(pokemon, choice)]["Power"] == 0:
                printsleep (f"Your {pokemon["Name"]} used {pokemon["Move"][choice]}", s)
            stg, type, targ = apply_effect(pokemon, choice, platk, pldef, enatk, endef)
            if type == "a" and targ == "a":
                platk = stg
                printsleep (f"Your {pokemon["Name"]}'s attack is now at stage {platk} ({round(stg_to_mod(platk), 2)}x)", s) 
            elif type == "a" and targ == "d":
                enatk = stg
                printsleep (f"The enemy {enemy["Name"]}'s attack is now at stage {enatk} ({round(stg_to_mod(enatk),2)}x)", s)
            elif type == "d" and targ == "a":
                pldef = stg
                printsleep (f"Your {pokemon["Name"]}'s attack is now at stage {pldef} ({round(stg_to_mod(pldef),2)}x)", s)
            else:
                endef = stg
                printsleep (f"The enemy {enemy["Name"]}'s defense is now at stage {endef} ({round(stg_to_mod(endef),2)}x)", s)
    #enemy attack
    def enemy_attack():
        global enatk, platk, pldef, endef, plhp, enhp, party
        if turn == 1:        
            printsleep (f"The enemy {enemy["Name"]} used {enemy["Move"][1]}", s)
            stg, type, targ = apply_effect(enemy, 1, enatk, endef, platk, pldef)
            if type == "a" and targ == "a":
                enatk = stg
                printsleep (f"The enemy {enemy["Name"]}'s attack is now at {enatk} ({round(stg_to_mod(enatk),2)}x)", s) 
            elif type == "a" and targ == "d":
                platk = stg
                printsleep (f"Your {pokemon["Name"]}'s attack is now at stage {platk} ({round(stg_to_mod(platk),2)}x)", s)
            elif type == "d" and targ == "a":
                endef = stg
                printsleep (f"The enemy {enemy["Name"]}'s defense is now at stage {endef} ({round(stg_to_mod(endef),2)}x)", s)
            else:
                pldef = stg
                printsleep (f"Your {pokemon["Name"]}'s defense is now at stage {pldef} ({round(stg_to_mod(pldef),2)}x)", s)   
        else:
            best_move = 1
            move_damage = 0
            moves = enemy["Move"]
            for move in moves:
                move_num = moves.index(move)
                if move_num != 0 and move_dict[poke_to_move_dict(enemy, move_num)]["Power"]>0:
                    dam, crit = damage_calc(enemy, pokemon, move_num, enatk, pldef)
                    if dam > move_damage:
                        best_move = move
                        best_move_num = move_num
                        move_damage = dam
                        move_crit = crit
            move_effect = weakness(poke_to_move_dict(enemy, best_move_num), pokemon)
            damage = move_damage
            plhp -= damage
            plhp = floor(plhp)
            printsleep (f"The enemy {enemy["Name"]} used {best_move}", s)
            effect_text(move_effect)
            if move_crit == 1.5:
                printsleep ("It was a critical hit!", s)
            if plhp > 0:
                printsleep (f"It did {int(round(damage,0))} damage! Your {pokemon["Name"]} is now at {int(round(plhp,0))} health!", s)
            else:
                printsleep (f"It did {int(round(damage,0))} damage! Your {pokemon["Name"]} fainted.", s)  
                del party[0] 
                plhp = "Dead"    
    #counts turns
    turn = 0
    #while loop so game doesn't end until someone dies
    while enhp != "Dead" and plhp != "Dead" and enhp != "Caught":
        turn += 1
        player_turn()
        if enhp != "Dead" and enhp != "Caught":
            enemy_attack()
    return turn
def end_screen():
    global turn, fights_won, pokemon_caught, pokemon_killed, coins, bag
    print (f"Name: {name}\nStarter: {pokemon["Name"]}\nTotal Turns: {turn}")
    print (f"Fights Won: {fights_won}\nPokemon Caught: {pokemon_caught}\nPokemon Killed: {pokemon_killed}")
    print (f"Coins: {coins}\nPotions: {bag[1]["Amount"]}\nPokeballs: {bag[2]["Amount"]}")
create_character()
game_intro()
turn = 0
fights_won = 0
setup()
start_shop()
while plhp != "Dead" and fights_won < 10:
    if fights_won == 5:
        sell_pokemon()
        midway_shop()
    encounter()
    reset_modifiers()
    turn += battle()
    if plhp != "Dead":
        fights_won +=1
        xp +=1
        if xp/(1+pokemon["lvl"]) == 1:
            level_up()
end_screen()