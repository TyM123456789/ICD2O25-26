# name = input("please enter ur name: ")
# mood = input(f"hi {name}. how r u today? ")
# print (f"i am glad u are {mood}, {name}!")

# n1 = input("enter a number: ")
# n2 = input("enter another 1 pls: ")

# sum = n1 + n2
# print (sum)

#make sure to turn input into int for numbers or else it will just add the strings together (like 6 + 7 = 67)

n1 = (input("enter a number: "))
n2 = (input("enter another 1 pls: "))

sum = int(n1) + int(n2)
print (sum)

#to permanently make n1 and n2 into ints, either do it on their own line (n1 = int(n1)) or do it in the input (n1 = int(input("...")))