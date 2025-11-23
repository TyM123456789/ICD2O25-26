#THINGS TO ADD OR FIX FOR LATER
# 2. Pauses to make text easier to read
# 3. Make it so u cant buy intimidate/strong start more than once (a bit op)
# 4. add more comments (stopped commenting at def attack())
# 5. change stats screen
#resets attack modifiers for player and enemy
def reset_modifiers():
    global platk, enatk, pldef, endef, permplatk, permenatk, permpldef, permendef
    #uses permplatk instead of just 0 in case player bought Intimidate or Strong Start
    platk = permplatk
    enatk = permenatk
    pldef = permpldef
    endef = permendef
#imports randint
from random import randint
from time import sleep
from copy import deepcopy
# dictionary of pokemon
# call by poke_dict[1]["Name"]
poke_dict = {
    1: {"Name": "Charmander", "Type": ["","Fire"], "Health": 150, "Move": ["", "Growl", "Tackle", "Ember"]},
    2: {"Name": "Bulbasaur", "Type": ["","Grass"], "Health": 150, "Move": ["", "Growl", "Tackle", "Vine Whip"]},
    3: {"Name": "Squirtle", "Type": ["","Water"], "Health": 150, "Move": ["", "Growl", "Tackle", "Water Gun"]},
}
#dictionary of moves. 
#call by move_dict[(move#)]["Name"]
move_dict = {
    1: {"Name": "Growl", "Type": "Normal", "Damage": 0, "Effect": "d1A-"},
    2: {"Name": "Tackle", "Type": "Normal", "Damage": 30, "Effect": ""},
    3: {"Name": "Ember", "Type": "Fire", "Damage": 20, "Effect": ""},
    4: {"Name": "Vine Whip", "Type": "Grass", "Damage": 20, "Effect": ""},
    5: {"Name": "Water Gun", "Type": "Water", "Damage": 20, "Effect": ""}
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
#gets player name and starter pokemon. makes global
def create_character():
    global name, pokemon, party, shop
    #gets name. name is used in end stats
    name = input("Enter your character's name: ")
    #choose a pokemon
    print (f"What Pokemon do you want to start with? {poke_dict[1]["Name"]}(1), {poke_dict[2]["Name"]}(2), or {poke_dict[3]["Name"]}(3)")
    pokemon = int(input(""))
    #if answer wasn't one of the options
    if pokemon > 3 or pokemon < 1:
        print ("That is not one of the options. You will use Charmander.")
        pokemon = 1
    party = [poke_dict[pokemon]["Name"]]
#starting shop
def start_shop():
    global bag, coins
    exit = False
    print (f"Before embarking on your journey, you go to the Pokeshop.")
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
        print ("Exit (3)")
        #sets item to 0 for later use
        item = 0
        #while loop lets player keep choosing until they settle on a possible option
        while item < 1 or item > 3:
            #takes input
            item = int(input(""))
            #gives error if answer isnt an option
            if item < 1 or item > 3:
                print ("That is not an option. Try Again.")
        #lets player exit
        if item == 3:
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
    for x in range(1,pokemon_caught+1):
        killed_tot += randint(13,15)
    for x in range(1,len(party)):
        if x != 0:
            caught_tot += randint(15,17)
            del party[1]
    print (f"You killed {pokemon_killed} Pokemon in the past {fights_won} fights!")
    print (f"You sold their bodies for a total of {killed_tot} Pokedollars!")
    print (f"You caught {pokemon_caught} Pokemon in the past {fights_won} fights!")
    print (f"You sold their bodies for a total of {caught_tot} Pokedollars!")
    coins += killed_tot + caught_tot
#shop at 5 fights won
def midway_shop():
    #same as other shop but with more options.
    global bag, coins, shop, permplatk, permenatk, plhp
    exit = False
    print (f"Along your journey, you see a Pokeshop.")
    midshop = shop
    for product in midshop:
        midshop[product]["Cost"] = item_cost(product, midshop)
    while exit == False:
        print (f"{"Items":<14}{f"Pokedollars: {coins}":>50}")
        print ("-"*65)
        for x in midshop:
            format_row(midshop[x]["Name"], midshop[x]["Amount"], x, midshop[x]["Description"], midshop[x]["Cost"])
        print ("-"*65)
        print (f"Exit ({len(midshop)+1})")
        item = 0
        while item < 1 or item > len(midshop)+1:
            item = int(input(""))
            if item < 1 or item > len(midshop)+1:
                print ("That is not an option. Try Again.")
        if item == len(midshop)+1:
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
                    plhp = poke_dict[pokemon]["Health"]
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
    global plhp, coins, permenatk, permplatk, permendef, permpldef, pokemon_caught, pokemon_killed
    #resets all stats
    permplatk = 0
    permenatk = 0
    permpldef = 0
    permendef = 0
    coins = 75
    #draws from dictionary
    plhp = poke_dict[pokemon]["Health"]
    pokemon_killed = 0
    pokemon_caught = 0
#randomizes and enemy between the available pokemon and prints a small message
def encounter():
    global enemy, enhp, fights_won
    #generates an enemy
    enemy = randint(1,3)
    print(f"In Route {fights_won+1}, you stumble across a wild {poke_dict[enemy]["Name"]}!")
    #sets enemy health
    enhp = poke_dict[enemy]["Health"]
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
        print (f"Back ({item_num})")
        #takes input
        choice = int(input(""))
        if choice == item_num:
            player_turn()
        #ends turn if answer isn't accepted
        elif choice >item_num or choice < 1 or bag[choice]["Amount"] == 0:
            print ("You couldn't find the item you were looking for.")
        elif bag[choice]["Name"] == "Potion":
            bag[choice]["Amount"]-=1
            global plhp
            plhp = heal(plhp,80)
        elif bag[choice]["Name"] == "Pokeball":
            bag[choice]["Amount"]-=1
            throw_pokeball()
    #calculates whether opponent pokemon is weak to chosen attack. resist - 50% dam. weak - 200% dam
    def weakness(attack, opp_poke):
        #checks weakness and returns mult value.
        mult = 1
        attack_type = move_dict[attack]["Type"]
        enemy_type = poke_dict[opp_poke]["Type"]
        #for each enemy type (all enemies i have rn only have one type)
        for type in enemy_type:
            if type in type_chart.get(attack_type, {}):
                mult *= type_chart[attack_type][type]
        return mult
    #checks if pokemon type is same as attack type. if so, 50% dam boost
    def stab(attack, poke):
        #the mechanic STAB (same type attack bonus) provides 1.5x mult if pokemon type is same is it's move
        attack_type = move_dict[attack]["Type"]
        player_type = poke_dict[poke]["Type"]
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
        catch_num = randint(1,poke_dict[enemy]["Health"])
        #if catch value is more than or equal to 90% of enemy health
        if catch_num >= enhp*.9:
            enhp = "Caught"
            print ("Catch Successful!")
            pokemon_caught +=1
            party.append(poke_dict[enemy]["Name"])
        else:
            print ("Catch Failed...")
    #calculates heal
    def heal(health, amount):
        #calculates heal
        if health + amount <= poke_dict[pokemon]["Health"]:
            print (f"Your {poke_dict[pokemon]["Name"]} is now at {health + amount} HP.")
            return health + amount
        #makes so health cant go above max
        else:
            print (f"Your {poke_dict[pokemon]["Name"]} is now at {poke_dict[pokemon]["Health"]} HP.")
            return poke_dict[pokemon]["Health"]
    #move in poke_dict to move in move_dict
    def poke_to_move_dict(poke, move):
        #poke: pokemon with chosen move
        #move: index of move in the chosen pokemons list of moves
        name = poke_dict[poke]["Move"][move]
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
        rawdam = move_dict[attack]["Damage"]
        random = (randint(85,100))
        crit = crit_calc()
        #damage * attack stat * 1/opponent defense * weakness or resistance * STAB (same type attack bonus) * randomness (.85 to 1) * crit (1/24 for 1.5x)
        #also prints to check math
        #print (f"{rawdam} * {pokeatk} * (1/{oppdef}) * {weakness(attack, opppoke)} * {stab(attack, poke)} * ({random}/100)1 * {crit}")
        return (rawdam * stg_to_mod(pokeatk) * (1/stg_to_mod(oppdef)) * weakness(attack, opppoke) * stab(attack, poke) * random/100 * crit), crit
    #stg to mod
    def stg_to_mod(stg):
        #translates stage of stat (+1) atk for example to modifier (in +1 attack's case, it would be 3/2)
        if stg<0:
            return 2/(2+stg*-1)
        else:
            return (2+stg)/2    
    #add/subtract effect
    def mod_effect(stg, direction, amount):
        #changes stage
        if direction and stg != 6:
            stg+=1*amount
        elif not direction and stg != -6:
            stg-=1*amount
        return stg
    #calculates effects
    def apply_effect(movenum, aatk, adef, datk, ddef):
        #translates the modifier code to meaning
        move = move_dict[movenum]["Effect"]
        if move[0] == "a":
            if move[2] == "A":
                stg = mod_effect(aatk, move[1]=="+", int(move[1]))
                return stg, "a", "a"
            elif move[2] == "D":
                stg = mod_effect(adef, move[1]=="+", int(move[1]))
                return stg, "d", "a"   
        elif move[0] == "d":
            if move[2] == "A":
                stg = mod_effect(datk, move[1]=="+", int(move[1]))
                return stg, "a", "d"
            elif move[2] == "D":
                stg = mod_effect(ddef, move[1]=="+", int(move[1]))
                return stg, "d", "d"                       
    #uses player choice to apply attack.
    def attack():
        global enatk, platk, pldef, endef, enhp, pokemon_killed
        print (f"Growl (1)\nTackle (2)\n{poke_dict[pokemon]["Move"][3]} (3)")
        print (f"Back ({len(poke_dict[pokemon]["Move"])})")
        choice = int(input(""))
        if choice >len(poke_dict[pokemon]["Move"]) or choice < 1:
            print (f"Your {poke_dict[pokemon]["Name"]} didn't understand your command.")
            choice = 0
        elif choice == len(poke_dict[pokemon]["Move"]):
            player_turn()
        elif move_dict[choice]["Damage"] > 0:
            damage, crit = damage_calc(pokemon, enemy, choice, platk, endef)
            global enhp
            enhp -= damage
            enhp = int(round(enhp,0))
            print (f"Your {poke_dict[pokemon]["Name"]} used {poke_dict[pokemon]["Move"][choice]}")
            if crit == 1.5:
                print ("It was a critical hit!")
            if enhp > 0:
                print (f"It did {int(round(damage,0))} damage! The enemy {poke_dict[enemy]["Name"]} is now at {int(round(enhp,0))} health!")
            else:
                print (f"You did {int(round(damage,0))} damage! The enemy {poke_dict[enemy]["Name"]} fainted.")
                pokemon_killed += 1
                enhp = "Dead"
        if len(move_dict[choice]["Effect"]) == 4:
            print (f"Your {poke_dict[pokemon]["Name"]} used {poke_dict[pokemon]["Move"][choice]}")
            stg, type, targ = apply_effect(choice, platk, pldef, enatk, endef)
            if type == "a" and targ == "a":
                platk = stg
                print (f"Your {poke_dict[pokemon]["Name"]}'s attack is now at stage {platk} ({round(stg_to_mod(platk,2))}x)") 
            elif type == "a" and targ == "d":
                enatk = stg
                print (f"The enemy {poke_dict[enemy]["Name"]}'s attack is now at stage {enatk} ({round(stg_to_mod(enatk),2)}x)")
            elif type == "d" and targ == "a":
                pldef = stg
                print (f"Your {poke_dict[pokemon]["Name"]}'s attack is now at stage {pldef} ({round(stg_to_mod(pldef),2)}x)")
            else:
                endef = stg
                print (f"The enemy {poke_dict[enemy]["Name"]}'s defense is now at stage {endef} ({round(stg_to_mod(endef),2)}x)")
    #enemy attack
    def enemy_attack():
        global enatk, platk, pldef, endef, plhp, enhp, party
        if turn == 1:        
            print (f"The enemy {poke_dict[enemy]["Name"]} used {poke_dict[enemy]["Move"][1]}")
            stg, type, targ = apply_effect(1, enatk, endef, platk, pldef)
            if type == "a" and targ == "a":
                enatk = stg
                print (f"The enemy {poke_dict[enemy]["Name"]}'s attack is now at {enatk} ({round(stg_to_mod(enatk),2)}x)") 
            elif type == "a" and targ == "d":
                platk = stg
                print (f"Your {poke_dict[pokemon]["Name"]}'s attack is now at stage {platk} ({round(stg_to_mod(platk),2)}x)")
            elif type == "d" and targ == "a":
                endef = stg
                print (f"The enemy {poke_dict[enemy]["Name"]}'s defense is now at stage {endef} ({round(stg_to_mod(endef),2)}x)")
            else:
                pldef = stg
                print (f"Your {poke_dict[pokemon]["Name"]}'s attack is now at stage {pldef} ({round(stg_to_mod(pldef),2)}x)")   
        else:
            best_move = 1
            move_damage = 0
            moves = poke_dict[enemy]["Move"]
            for move in moves:
                move_num = moves.index(move)
                if move_num != 0:
                    dam , crit = damage_calc(enemy, pokemon, move_num, enatk, pldef)
                    if dam > move_damage:
                        best_move = move
                        move_damage = dam
                        crit = crit
                    else:
                        crit = 1
            damage = move_damage
            plhp -= damage
            plhp = int(round(plhp,0))
            print (f"The enemy {poke_dict[enemy]["Name"]} used {best_move}")
            if crit == 1.5:
                print ("It was a critical hit!")
            if plhp > 0:
                print (f"It did {int(round(damage,0))} damage! Your {poke_dict[pokemon]["Name"]} is now at {int(round(plhp,0))} health!")
            else:
                print (f"It did {int(round(damage,0))} damage! Your {poke_dict[pokemon]["Name"]} fainted.")  
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
    print (f"Name: {name}\nStarter: {poke_dict[pokemon]["Name"]}\nTotal Turns: {turn}")
    print (f"Fights Won: {fights_won}\nPokemon Caught: {pokemon_caught}\nPokemon Killed: {pokemon_killed}")
    print (f"Coins: {coins}\nPotions: {bag[1]["Amount"]}\nPokeballs: {bag[2]["Amount"]}")
create_character()
turn = 0
fights_won = 0
setup()
start_shop()
print (shop)
while plhp != "Dead" and fights_won < 10:
    if fights_won == 5:
        sell_pokemon()
        midway_shop()
    encounter()
    reset_modifiers()
    turn += battle()
    if plhp != "Dead":
        fights_won +=1
end_screen()