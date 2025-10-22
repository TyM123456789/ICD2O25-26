number = 42

print (f"|{number}|")    #|42|
print (f"|{number:>5}|") #|   42|
print (f"|{number:<5}|") #|42   |
print (f"|{number:^5}|") #| 42  |
print (f"|{number:^10}|")#|    42    |

value = 123.456789
print (f"{value}")
print (f"{value:.2f}")
print (f"{value:.3f}")

value = 7.5
print (f"{value:.2f}")

percentage = 15/17
print (f"{percentage:.1%}")


cost = 5.67

print(f"${cost:.2f}")