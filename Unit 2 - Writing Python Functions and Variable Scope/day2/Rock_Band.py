# Calculates ticket revenue
# Accepts ticket price (float) and number of tickets sold (int)
# Returns total revenue (float)
def calculate_revenue(price, sold):
    return price * sold

# Adds a new city to the tour schedule
# Accepts tour list and city name (str)
# Adds city to the list (in-place)
def add_city(tour, city):
    tour.append(city)

# Calculates band’s popularity score
# Accepts number of fans (int) and albums sold (int)
# Returns popularity score (int)
def calculate_popularity(fans, albums):
    return fans + (albums * 10)

# Displays your current tour schedule
# Accepts tour list
# Returns nothing, just prints
def display_tour(tour):
    print("Tour Schedule:")
    for stop in tour:
        print("- " + stop)

# Signs a new sponsor deal
# Accepts sponsor name (str), deal amount (float)
# Returns a message and the deal amount
def sign_sponsor(name, amount):
    return f"Signed with {name} for ${amount}", amount

# Records a new album
# Accepts album title (str), number of songs (int)
# Returns a string summary and average song length (float)
def record_album(title, songs):
    avg_length = 3.5  # assume average song length
    return f"Album '{title}' recorded with {songs} tracks", songs * avg_length

# Calculates band expense
# Accepts travel cost (float), food cost (float), and gear cost (float)
# Returns total expense (float)
def calculate_expenses(travel, food, gear):
    return travel + food + gear

# Promotes a single
# Accepts song title (str)
# Returns nothing, prints a message
def promote_single(song):
    print(f"🔥 New single '{song}' is trending on RockTube!")

# Checks if band is eligible for award
# Accepts albums sold (int), years active (int)
# Returns True or False
def is_award_eligible(albums, years):
    return albums >= 5 and years >= 3

# Gets band status
# Accepts name (str), popularity score (int), current city (str)
# Returns a formatted status string
def band_status(name, popularity, city):
    return f"{name} is rocking {city} with a score of {popularity}!"

tourlist = []
print (f"Revenue: ${calculate_revenue(3000,45)}")
add_city(tourlist, 'Los Angeles')
add_city(tourlist, 'Nashville')
display_tour(tourlist)
print (f'Popularity Score: {calculate_popularity(8000,300)}')
print (sign_sponsor('Guitar King Inc.', 150000.00))
print (record_album("Loud and Legendary", 12))
print (f"Expenses: ${calculate_expenses(12000, 4000, 6000)}")
promote_single("Neon Lightning")
eligibility = is_award_eligible(7,4)
if eligibility == True:
    print ("We are eligible for an award!")
else:
    print ("We are not eligible for an award yet...")
print (band_status("Thunder Strike", 15000, "Chicago"))
       

