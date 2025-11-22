import time
starters = ["", "Pikachu", "Bulbasaur", "Charmander"]
random = ["", "Caterpie", "Squirtle"]
p = .5
def printsleep(str, timee):
    print (str)
    time.sleep(timee)
def create_character():
    name = input("Enter your character's name: ")
    pokemon = int(input("What Pokemon do you want to start with? (Pikachu(1), Bulbasaur(2), or Charmander(3))"))
    if pokemon > 2 or pokemon < 0:
        printsleep ("That is not one of the options. You will use Charmander.", p)
        pokemon = 3
    pokemon_count = 1
    return name, pokemon, pokemon_count
def game_intro(name, player_pokemon, starters):
    printsleep (f"Welcome to the Kanto region, {name}!", p)
    printsleep (f"Your starter Pokemon is {starters[player_pokemon]}.", p)
    printsleep (f"Your journey will be difficult, but you will meet many friends and partners along the way!", p)
def make_decision1():
    ans = int(input("In Pallet Town, you stumble across a PokeShop! Do you want to buy a potion(1) or find a Pokemon(2)?"))
    if ans == 1:
        printsleep ("After buying a potion, you decide to go to route 1.", p)
    if ans > 2 or ans < 1:
        printsleep ("That is not one of the options. You will find a Pokemon.", p)
        ans = 2
    return ans
def make_decision2(random_poke, random):
    ans = int(input(f"In Route 1, you stumble across a wild {random[random_poke]}! Do you want to battle (1) or catch (2) the Pokemon?"))
    if ans > 2 or ans < 1:
        printsleep ("That is not one of the options. You will battle a Pokemon.", p)
        ans = 1
    return ans, random_poke
def pokemon_battle(action, player_pokemon, starters, random_poke, random):
    if action == 1:
        printsleep (f"You attack it with your {starters[player_pokemon]}! It fainted, but {starters[player_pokemon]} took some damage.", p)
        return 1, "", manage_health(100,damage_calc(starters[player_pokemon], random[random_poke]), starters[player_pokemon])
    elif action ==2:
        printsleep (f"You hit it with a weak attack, and it works!", p)
        printsleep (f"You throw your Pokeball!", p*1.5)
        printsleep (".", p*1.5)
        printsleep ("..", p*1.5)
        printsleep ("...", p*1.5)
        printsleep (f"You caught the wild {random[random_poke-1]}!", p)
        pokemon_count = 2
        return pokemon_count, random_poke, 100
def damage_calc(pokemon, enemy):
    if pokemon == "Charmander" and enemy == "Caterpie" or pokemon == "Bulbasaur" and enemy == "Squirtle":
        return 10
    elif pokemon == "Charmander" and enemy == "Squirtle":
        return 100
    else:
        return 20
def manage_health(current_health, damage_taken, player_pokemon):
    global dead
    dead = False
    current_health -= damage_taken
    printsleep (f"Your {player_pokemon} took {damage_taken} damage.", p)
    if current_health <= 0:
        dead = True
        printsleep (f"{player_pokemon} is deceased...", p)
    else:
        printsleep (f"{player_pokemon} is now at {current_health} HP.", p)
    return current_health
def game_end(name, player_pokemon, current_health, pokemon_count, starters):
    printsleep (f"Congratulations for completing our game!", p)
    printsleep (f"Here are your stats:", p)
    print (f"Name: {name}\nStarter: {starters[player_pokemon]}\nStarter Health: {current_health}\nPokemon Count: {pokemon_count}")
def game_loss(name, player_pokemon, current_health, pokemon_count, starters):
    printsleep (f"Congratulations for  failing our game!", p)
    printsleep (f"Here are your stats:", p)
    printsleep (f"Name: {name}\nStarter: {starters[player_pokemon]}\nStarter Health: {current_health}\nPokemon Count: {pokemon_count}",p)
    print ("Try again")

name, pokemon, pokemon_count = create_character()
game_intro(name, pokemon, starters)
choice1 = make_decision1()
choice2, random_poke = make_decision2(choice1, random)
pokemon_count, pokemon2, health = pokemon_battle(choice2, pokemon, starters, random_poke, random)
if dead:
    pokemon_count-=1
    health = "Dead"
    game_loss(name, pokemon, health, pokemon_count, starters)
if not dead:
    game_end(name, pokemon, health, pokemon_count, starters)    