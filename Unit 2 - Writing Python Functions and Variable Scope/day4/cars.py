observations = {
    1: {
        "time": "2:38",
        "cars": 100,
        "pedestrians": 7,
        "bikes": 1,
        "intersection_type": "4-way stop",
        "infractions": "None",
        "notes": "Gordon looked away for abit, most pedestrians and cars, sunny, heavy traffic"
    },
    2: {
        "time": "2:40",
        "cars": 79,
        "pedestrians": 2,
        "bikes": 0,
        "intersection_type": "4-way stop",
        "infractions": "None",
        "notes": "someone was counting next to Gordon, sunny, medium traffic"
    },
    3: {
        "time": "2:42",
        "cars": 89,
        "pedestrians": 5,
        "bikes": 0,
        "intersection_type": "4-way stop",
        "infractions": "1 Speeder",
        "notes": "sunny, high traffic"
    },
    4: {
        "time": "2:44",
        "cars": 69,
        "pedestrians": 3,
        "bikes": 0,
        "intersection_type": "4-way stop",
        "infractions": "None",
        "notes": "started stopping Gordon earlier. sunny, medium traffic"
    },
    5: {
        "time": "2:46",
        "cars": 47,
        "pedestrians": 1,
        "bikes": 0,
        "intersection_type": "4-way stop",
        "infractions": "None",
        "notes": "sunny, low traffic"
    },
    6: {
        "time": "2:48",
        "cars": 69,
        "pedestrians": 3,
        "bikes": 2,
        "intersection_type": "4-way stop",
        "infractions": "None",
        "notes": "most bikes, sunny, medium traffic"
    },
    7: {
        "time": "2:50",
        "cars": 89,
        "pedestrians": 3,
        "bikes": 0,
        "intersection_type": "4-way stop",
        "infractions": "None",
        "notes": "sunny, high traffic"
    }
}


# ===============================
#   ACCESSING A SINGLE OBSERVATION
# ===============================

def get_observation(observations, number):
    # Returns the observation dictionary for a specific observation number.
    # For example: get_observation(observations, 1) returns the first observation.
    # Returns: dict (e.g. {'time': '10:05', 'cars': 14, ...})
    return observations[number]


# ===============================
#   ACCESSING INDIVIDUAL DATA POINTS
# ===============================

def get_observation_time(obs):
    # Returns the time string from a single observation.
    # Returns: str
    return obs["time"]

def get_observation_cars(obs):
    # Returns the number of cars counted during one observation.
    # Returns: int
    return obs["cars"]

def get_observation_pedestrians(obs):
    # Returns the number of pedestrians counted during one observation.
    # Returns: int
    return obs["pedestrians"]

def get_observation_bikes(obs):
    # Returns the number of bikes counted during one observation.
    # Returns: int
    return obs["bikes"]

def get_observation_type(obs):
    # Returns the type of intersection (e.g. '4-way stop', 'Traffic light').
    # Returns: str
    return obs["intersection_type"]

def get_observation_notes(obs):
    # Returns the notes recorded for a single observation.
    # Returns: str
    return obs["notes"]


# ===============================
#   AGGREGATION FUNCTIONS (WORK FOR ANY SIZE DICTIONARY)
# ===============================

def get_num_observations(observations):
    # Returns the total number of observations recorded.
    # Returns: int
    return len(observations)

def get_total_cars(observations):
    # Calculates the total number of cars across all observations.
    # Returns: int
    total = 0
    for obs_num in observations:
        obs = get_observation(observations, obs_num)
        total += get_observation_cars(obs)
    return total

def get_total_pedestrians(observations):
    # Calculates the total number of pedestrians across all observations.
    # Returns: int
    total = 0
    for obs_num in observations:
        obs = get_observation(observations, obs_num)
        total += get_observation_pedestrians(obs)
    return total

def get_average_bikes(observations):
    # Calculates the average number of bikes per observation.
    # Returns: float
    total = 0
    for obs_num in observations:
        obs = get_observation(observations, obs_num)
        total += get_observation_bikes(obs)
    return total / get_num_observations(observations)


# ===============================
#   FORMATTING & PRINTING HELPERS
# ===============================

def format_observation_row(obsnum):
    # Takes in observation number (1-7)
    # Formats a single row of observation data for display in a table.
    # Returns: str (a nicely formatted line of data)
    obs = get_observation(observations, obsnum)
    print(f"{obsnum:<6}| {get_observation_time(obs):<6}| {get_observation_cars(obs):<4}| {get_observation_pedestrians(obs):<5}| {get_observation_bikes(obs):<6}| {get_observation_type(obs):<13}| {get_observation_notes(obs):<13}") # replace print with your code

def print_table_header():
    # Prints the header section for the table of observations.
    # Returns: None
    print("INTERSECTION OBSERVATIONS")
    print_line()
    print (f"Obs # | {"Time":<6}| {"Cars":<4}| {"Peds":<5}| {"Bikes":<6}| {"Type":<13}| Notes")
    print_line()

def print_line():
    # Prints a line
    # Returns: None
    print ("-"*130)

def print_totals(total_cars, total_peds, avg_bikes): 
    # Prints the total cars, total pedestrians, and average bikes
    # after all observations are displayed.
    # Returns: None
    print(f"TOTAL CARS: {total_cars}  \nTOTAL PEDESTRIANS: {total_peds}  \nAVERAGE BIKES: {avg_bikes}") # replace print with your code

#starting

print_table_header()

# For each observation row, use format_observation_row()
for ob in observations:
    format_observation_row(ob)
print_line()

#print totals
print_totals(get_total_cars(observations), get_total_pedestrians(observations), round(get_average_bikes(observations),2))