# Rolls a 20-sided die and returns the result
def roll_d20():
    import random
    return random.randint(1, 20)

# Calculates attack damage
# Accepts base damage (int) and bonus (int)
# Returns total damage (int)
def calculate_damage(base, bonus):
    return base + bonus

# Calculates health after damage taken
# Accepts current health and damage
# Returns new health (int)
def take_damage(health, damage):
    return health - damage

# Heals the character
# Accepts current health and heal amount
# Returns new health and a string status
def heal(health, amount):
    new_health = health + amount
    return new_health, "You feel stronger!"

# Adds an item to inventory
# Accepts the inventory list and item (str)
# Modifies the inventory directly
def add_item(inventory, item):
    inventory.append(item)

# Displays all items in inventory
# Accepts inventory list
# Returns nothing
def display_inventory(inventory):
    print("Inventory contains:")
    for item in inventory:
        print("- " + item)

# Determines if attack was a critical hit
# Accepts a d20 roll (int)
# Returns True or False
def is_critical_hit(roll):
    return roll == 20

# Returns character's status
# Accepts name (str), health (int), inventory (list)
# Returns a formatted string with player status
def get_status(name, health, inventory):
    return f"{name} has {health} HP and carries: {', '.join(inventory)}"

# Calculates experience needed for next level
# Accepts current level (int)
# Returns required experience (int)
def exp_to_next_level(level):
    return level * 1000

# Combines weapon stats
# Accepts weapon name (str), base damage (int), and magic bonus (int)
# Returns a string summary and total damage (int)
def weapon_summary(name, base, bonus):
    return (f"{name} does {base}+{bonus} damage, {base + bonus}")

inventory = []
initiative = roll_d20()
print (f"Initiative: {initiative}")
totdam = calculate_damage(6,2)
print (f"Damage: {totdam}")
health = (30,12)
print (f"Health: {health}")
health = (health,10)
print (f"Health: {health}")
add_item(inventory,"Magic Wand")
add_item(inventory,"Healing Potion")
display_inventory(inventory)
crit = is_critical_hit(20)
if crit == True:
    print ("You got a crit!")
else:
    print ("You didn't crit...")
print (get_status("Elaria", 25, inventory))
expneeded = exp_to_next_level(5)
print (f"You need {expneeded} more exp to get to level 5")
print (weapon_summary("Flaming Sword", 8, 3))