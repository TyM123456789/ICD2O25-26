
# ---------- Task 1: Character Creation ----------
def create_character():
    name = input("Enter your character's name: ")

    character_class = input("Choose a class (Warrior, Mage, Archer): ")
    # Simple validation: if it isn't one of the three, default to Warrior
    if character_class != "Warrior" and character_class != "Mage" and character_class != "Archer":
        print("Invalid class. You will be a Warrior.")
        character_class = "Warrior"

    health_text = input("Enter starting health (50–100): ")

    # Basic validation for health
    try:
        health = int(health_text)
    except:
        print("That was not a number. Health set to 75.")
        health = 75

    if health < 50:
        print("Health too low. Set to 50.")
        health = 50

    if health > 100:
        print("Health too high. Set to 100.")
        health = 100

    return name, character_class, health


# ---------- Task 2: Game Introduction ----------
def game_intro(character_name, character_class):
    print("\n--- Welcome to the Land of Emberfall ---")
    print("Long ago, a dark shadow fell over these lands.")
    print("Only a true hero can restore the light.")
    print(character_name + " the " + character_class + ", your journey begins now.\n")


# ---------- Task 3: Decision Making ----------
def make_decision():
    direction = input("You reach a crossroads. Do you go LEFT or RIGHT? ").lower()

    # Simple validation: anything else becomes "left"
    if direction != "left" and direction != "right":
        print("You hesitate too long. The path forces you to the left.")
        direction = "left"

    return direction


# ---------- Task 4: Encounter ----------
def encounter_scenario(direction):
    # Returns damage_taken and bonus_points (for Task 6)
    if direction == "left":
        print("\nYou walk along a sunny forest path.")
        print("A friendly spirit appears and blesses you.")
        print("You take no damage and feel a bit stronger.")
        damage_taken = 0
        bonus_points = 10
        print("You gain 10 bonus points for choosing the peaceful path.")
    else:  # direction == "right"
        print("\nYou step into a dark canyon.")
        print("A fierce goblin jumps out and attacks!")
        use_item = input("Do you use your magic amulet? (yes/no): ").lower()

        if use_item == "yes":
            print("The amulet glows and blocks part of the attack.")
            damage_taken = 15
            bonus_points = 15
            print("You still get hurt, but you gain 15 bonus points for using a clever strategy.")
        else:
            print("You fight without the amulet and take a heavy blow.")
            damage_taken = 30
            bonus_points = 0

    return damage_taken, bonus_points


# ---------- Task 5: Health Management ----------
def manage_health(current_health, damage_taken):
    new_health = current_health - damage_taken

    if new_health <= 0:
        print("\nYour health has dropped to " + str(new_health) + ".")
        print("You fall to the ground as darkness closes in...")
        print("GAME OVER.")
    else:
        print("\nYou survive the encounter.")
        print("Your health is now " + str(new_health) + ".")

    return new_health


# ---------- Main Game (Tasks 6 & 7) ----------
def main():
    score = 0

    # Task 1
    name, char_class, health = create_character()

    # Task 2
    game_intro(name, char_class)

    # Task 3
    direction = make_decision()

    # Task 4 + Task 6 (bonus points)
    damage, bonus = encounter_scenario(direction)
    score = score + bonus

    # Task 5
    health = manage_health(health, damage)

    # Task 7: Game completion after a single encounter
    print("\n--- Adventure Result ---")
    if health > 0:
        print(name + " the " + char_class + " survives the first challenge of Emberfall!")
    else:
        print(name + " the " + char_class + " has fallen on this quest.")

    if health < 0:
        health = 0

    print("Final Health: " + str(health))
    print("Final Score: " + str(score))
    print("Thanks for playing!")

# Run the game
main()
