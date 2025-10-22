
#start print
print ("Upper School Resource Density Calculator\n----------------------------------------")

#amount of each
classrooms = int(input("How many classrooms are in the Upper School? "))
water_fountains = int(input("How many student water fountains? "))
restrooms = int(input("How many student restrooms? "))
additional = input("Enter ONE additional resource to track (e.g., vending machines): ").lower()
additional_amount = int(input(f"How many {additional}? "))

#cond of each
water_fountain_cond = input("Condition of fountains: ")
restroom_cond = input("Condition of restrooms: ")
additional_cond = input(f"Condition of {additional}: ")

#density calcs
fountain_density = round(water_fountains/classrooms,2)
restroom_density = round(restrooms/classrooms,2)
additional_density = round(additional_amount/classrooms,2)

#print
print (f"\nResults\n-------")
print (f"Fountains per classroom: {fountain_density} (Condition: {water_fountain_cond})")
print (f"Restrooms per classroom: {restroom_density} (Condition: {restroom_cond})")
print (f"{additional.title()} per classroom: {additional_density} (Condition: {additional_cond})")
print ("\nThanks for helping map our Upper School resources!")

#reflection

#1. how did calculating resource density help you understand the usefulness of data in real life?
#   It helped me learn that data can help you make modifications. For example, if you had a density of .1 restrooms per classroom, you would know to get more restrooms.
#2 if you had more time, what feature or analysis would you add to your program?
#   I would let the user find density using students or teachers instead of classrooms.