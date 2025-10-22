# Prints the app title
# Parameters: none
# Returns: nothing
def show_app_title():
    print("🌦️ Weather Wizard – Your Forecast Friend")

# Converts Celsius to Fahrenheit
# Parameters: temp_c (float)
# Returns: Fahrenheit temperature (float)
def to_fahrenheit(temp_c):
    return temp_c * 9 / 5 + 32

# Calculates wind chill based on temp (°C) and wind speed (km/h)
# Parameters: temp (float), wind_speed (float)
# Returns: wind chill value (float)
def wind_chill(temp, wind_speed):
    return 13.12 + 0.6215 * temp - 11.37 * wind_speed**0.16 + 0.3965 * temp * wind_speed**0.16

# Prints weather summary
# Parameters: city (string), temp (float)
# Returns: nothing
def report(city, temp):
    print("The temperature in " + city + " is " + str(temp) + "°C.")




# 1. Call show_app_title().
# 2. Store "Toronto" in city.
# 3. Store -5 in celsius_temp.
# 4. Call report(city, celsius_temp).
# 5. Convert temp to Fahrenheit and print it.
# 6. Store 30 in wind_speed.
# 7. Call wind_chill(celsius_temp, wind_speed) and store result.
# 8. Print the calculated wind chill.


show_app_title()
city = "Toronto" 
celsius_temp = -5
report(city, celsius_temp)
print (f"In Fahrenheit, that is {to_fahrenheit(celsius_temp)}F.")
wind_speed = 30
wind_chil = wind_chill(celsius_temp, wind_speed)
print (f"The windchill is {wind_chil:.2f}")

