# Displays the header for the stat tracker
# Parameters: none
# Returns: nothing
def show_tracker_header():
    print("Baseball Performance Tracker")
# Calculates batting average
# Parameters: hits (int), at_bats (int)
# Returns: batting average (float)
def get_batting_average(hits, at_bats):
    return hits / at_bats
# Prints a summary of a player's game stats
# Parameters: name (string), hits (int), at_bats (int)
# Returns: nothing
def print_game_summary(name, hits, at_bats):
    print(name + " had " + str(hits) + " hits in " + str(at_bats) + " at-bats.")
# Returns total bases and slugging percentage
# Parameters: singles (int), doubles (int), triples (int), home_runs (int), at_bats (int)
# Returns: (total bases (int), slugging (float))
def get_power_stats(singles, doubles, triples, home_runs, at_bats):
    total_bases = singles + 2 * doubles + 3 * triples + 4 * home_runs
    slugging = total_bases / at_bats
    return total_bases, slugging
# Converts a speed from miles per hour to kilometers per hour
# Parameters: mph (float)
# Returns: speed in kph (float)
def mph_to_kph(mph):
    return mph * 1.60934
# Prints a player's pitch velocity and location
# Parameters: speed (float), location (string)
# Returns: nothing
def log_pitch(speed, location):
    print("Pitch thrown at " + str(speed) + " mph to " + location + ".")
# Returns the ERA (earned run average) for a pitcher
# Parameters: earned_runs (int), innings_pitched (float)
# Returns: ERA (float)
def calculate_era(earned_runs, innings_pitched):
    return (earned_runs * 9) / innings_pitched
# Returns the strikeout-to-walk ratio
# Parameters: strikeouts (int), walks (int)
# Returns: ratio (float)
def get_kbb_ratio(strikeouts, walks):
    return strikeouts / walks
# Returns player name and position in a formatted string
# Parameters: name (string), position (string)
# Returns: summary string (string)
def format_player_info(name, position):
    return name + " plays " + position
# Displays a closing message
# Parameters: none
# Returns: nothing
def end_tracker():
    print("End of performance report.")

show_tracker_header()
avg = get_batting_average(3,5)
print_game_summary('Jaylen', 2, 4)
totbases,totslugging = get_power_stats(1, 1, 0, 1, 4)
kph = mph_to_kph(92.5)
print (f"Speed in km/h: {kph:.2f}")
log_pitch(89.6, 'outside corner')
era = calculate_era(2,6.2)
print (f"ERA: {era:.2f}")
kbb_ratio = get_kbb_ratio(9,3)
print (f"KBB ratio: {kbb_ratio}")
summary = format_player_info('Liam', 'shortstop')
end_tracker()