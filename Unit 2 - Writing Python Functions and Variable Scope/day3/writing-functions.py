from math import pi
def printMessage():
    print("Welcome to ICD2O!")

def subtract(x,y):
    return (x-y)

num1 = int(input("Give me a number: "))
num2 = int(input("Give me another number: "))

# printMessage()
print (subtract(num1,num2))

def greet(name):
    return f"Hello, {name}!"
print (greet("Steve"))

def cube(num):
    return num**3

print (cube(5))

def area_rectangle(length, width):
    return length * width

print(area_rectangle(5, 7))

def format_pi(decimals):
    return f"Pi is {pi:.{decimals}f}"

print (format_pi(7))

def seconds(hours):
    return hours*3600

print (seconds(4))

def total_with_tax(price, tax_rate):
    return f"Total: {round(price*tax_rate+price,2)}"

print (total_with_tax(9.99, .13))

def bmi(weight, height):
    return round(weight/height**2,2)

print (bmi(100, 1.7))

def greeting_with_age(name, age):
    return f"Hi {name}, you are {age} years old."

print (greeting_with_age("George", 43))

def pay(hours, rate):
    return f"Pay: ${round(rate*hours,2)}"

print (pay(2.00, 20.00))

def format_score(score, decimals):
    return f"Score: {score:.{decimals}f}%"

print (format_score(87.4563417851, 3))

def format_circle_area(radius, decimals):
    return f"Area is {pi*radius**2:.{decimals}f}"

print (format_circle_area(9,2))

def velocity(distance, time, decimals):
    return f"Speed: {distance/time:.{decimals}f} m/s"

print (velocity(10,3,2))

def format_total_price(price, quantity, tax, decimals):
    return f"Total: ${price*quantity*tax+price*quantity:.{decimals}f}"

print (format_total_price(9.99, 3, .13, 2))

def temperature_report(celsius, decimals):
    return f"Temp: {celsius*9/5+32:.{decimals}f}°F"

print (temperature_report(10, 2))

def travel_summary(distance, hours, decimals):
    return f"You travelled {distance} km in {hours} hours.", f"Avg speed: {distance/hours:.{decimals}f} km/h"

sum1, sum2 = travel_summary(550.0, 5.0, 1)

print (sum1)
print (sum2)