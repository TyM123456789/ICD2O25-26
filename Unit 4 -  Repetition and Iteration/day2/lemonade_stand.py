import random
from time import sleep
day = 0
money = 2.00
lem_cost = .02
weather = ""
weather_options = ["sunny", "sunny", "cloudy", "hot and dry", "thunderstorms!"]
customers = 0
def opening_message():
    print ("Hi! Welcome to Lemonsville, California!\nIn this small town, you are in charge of running your own lemonade stand.\nAre you starting a new game? (yes or no)")
    ans = ""
    while True:
        ans = (input ("Type your answer and hit return ==> ")).lower()
        if ans == "yes":
            return True
        elif ans == "no":
            return False
        else:
            ans = (input ("Type your answer and hit return ==> ")).lower()
def tutorial ():
    print ("To manage your lemonade stand, you will need to make these decisions every day:\n1. How many glasses of lemonade to make (only one batch is made every morning)")
    print ("2. How many advertising signs to make (the signs cost fifteen cents each)\n3. What price to charge for each glass")
    print ("You will begin with $2.00 cash (assets). Because your mother gave you some sugar, your cost to make lemonade is two cents a glass (this may change in the future).")
    ans = ""
    while ans != "ok":
        ans = (input(" Type OK to continue ==>")).lower()
    print ("Your expenses are the sum of the cost of the lemonade and the cost of the signs.\nYour profits are the difference between the income from sales and your expenses.")
    print ("The number of glasses you sell each day depends on the price you charge, and the number of adverising signs you use. ")
    print ("Keep track of your assets, because you can't spend more money than you have!")
    ans = ""
    while ans != "ok":
        ans = (input(" Type OK to continue ==>")).lower()
def game_intro():
    x = opening_message()
    if not x:
        print ("GAME QUIT")
        return False
    else:
        tutorial()
        return True
def decide_weather():
    weather = random.choice(weather_options)
    print ("Lemonsville Weather Report")
    print (f"{weather.upper():^25}")
    return weather
def choice(day):
    print (f"On day {day}, the cost of lemonade is ${lem_cost:.2f}.")
    print (f"Assets: ${money:.2f}")
    glass_cost = money +1
    sign_cost = money+1
    lemonade_cost = -1
    done_choosing = False
    while done_choosing == False:
        while glass_cost > money or glass_cost < 0:
            glasses = int(input("How many glasses of lemonade do you wish to make ? "))
            glass_cost = lem_cost*glasses
            if glass_cost > money:
                print(f"Think Again!!! You have only ${money:.2f} and to make {glasses} glasses of lemonade you need $ {glass_cost:.2f} in cash. ")
            elif glasses < 0:
                print ("Come on, let's be reasonable now!!! Try again.")     
        while sign_cost + glass_cost > money or sign_cost < 0:
            signs = int(input("How many advertising signs (15 cents each) do you want to make ? "))
            sign_cost = .15*signs
            if sign_cost + glass_cost > money:
                print(f"Think again, you have only ${money-glass_cost:.2f} in cash left after making your lemonade.")  
            elif signs < 0:
                print ("Come on, be reasonable!!! Try again.")  
        while lemonade_cost < 0:
            lemonade_cost = (int(input("What price (in cents) do you wish to charge for lemonade?")))
            if lemonade_cost < 0:
                print ("Come on, be reasonable!!! Try again.")  
        ans = input("Would you like to change anything?").lower()
        if ans != "yes":
            done_choosing = True
    return glasses, signs, lemonade_cost, (glass_cost+sign_cost)
def get_customers(weather, signs):
    if weather == "sunny":
        customers = random.randint(20,30)
    elif weather == "cloudy":
        customers = random.randint(7, 15)
    elif weather == "hot and dry":
        customers = random.randint(30, 50)
    elif weather == "thunderstorms!":
        customers = 3
    customers *= 1 + (.07 * signs)
    return round(customers)
def glasses_sold(customers, glass_count):
    sold = 0
    minmax = random.randint(8,10)
    maxmax = random.randint(13,17)
    for x in range(customers):
        if x+1 <= glass_count:
            max = random.randint(minmax,maxmax)
            if max >= lemonade_cost:
                sold += 1
    return sold, sold*(lemonade_cost/100)
def earnings_report(day, glasses, signs, lemonade_cost, lemonade_sold, earnings, costs, assets):
    print ("$$ Lemonsville Daily Financial Report $$")
    print (f"   Day {day}")
    print (f"  {lemonade_sold:<4}Glasses Sold")
    print (f"$.{lemonade_cost:<4}Per Glass           Income ${round(earnings,2):.2f}")
    print (f"  {glasses:<4}Glasses Made")
    print (f"  {signs:<4}Signs Made          Expenses ${round(costs,2):.2f}")
    print (f"              Profit ${round(earnings - costs,2):.2f}")
    print (f"              Assets ${round(assets+(earnings - costs),2):.2f}")
    return assets+(earnings - costs)


x= game_intro()
while x:
    day +=1
    weather = decide_weather()
    sleep(1)
    if day == 2:
        lem_cost=.03
        print ("Your mom stopped giving you sugar. Lemonade now costs $" + str(lem_cost))
    if day == 5:
        lem_cost=.04
        print ("Inflation has caused sugar prices to go up. Lemonade now costs $" + str(lem_cost))
    if day == 10:
        lem_cost=.05
        print ("The apocalypse wiped out global sugar supplies. Lemonade now costs $" + str(lem_cost))
    sleep(1)
    glasses, signs, lemonade_cost, expenses = choice(day)
    customer_amount = get_customers(weather, signs)
    lemonade_sold, earnings = glasses_sold(customer_amount, glasses)
    money = earnings_report(day, glasses, signs, lemonade_cost, lemonade_sold, earnings, expenses, money)
    sleep(1)
    if money < lem_cost:
        print ("You ran out of money.")
        x=False
    else:
        ans = input("Do you want to stop playing? yes or no ").lower()
        if ans == "yes": 
            x=False