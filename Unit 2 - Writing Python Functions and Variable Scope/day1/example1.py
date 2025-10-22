# Prints a welcome message to the user
# Parameters: none
# Returns: nothing
def show_welcome():
    print("Welcome to the program! Let's learn functions.")

# Calculates and returns the area of a rectangle
# Parameters: width (float), height (float)
# Returns: area (float)
def calculate_area(width, height):
    return width * height

# Prints a simple greeting with a name
# Parameters: name (string)
# Returns: nothing
def greet(name):
    print("Hello, " + name + "!")

# Converts Celsius to Fahrenheit
# Parameters: temp_c (float)
# Returns: temperature in Fahrenheit (float)
def celsius_to_fahrenheit(temp_c):
    return temp_c * 9 / 5 + 32

# Adds two numbers and returns the sum
# Parameters: num1 (int), num2 (int)
# Returns: sum (int)
def add_numbers(num1, num2):
    return num1 + num2

# Prints a horizontal divider line
# Parameters: none
# Returns: nothing
def print_divider():
    print("-------------------------")

show_welcome()

print (calculate_area(6.7,6.9))

print (f"the temperature in north york in F is {celsius_to_fahrenheit(21.0)}")

x=6
y=8

print (f"{x} plus {y} is {add_numbers(x,y)}")

print_divider()