age = 17
is_teen_low = age >= 13
is_teen_high = age <= 19
print(is_teen_low and is_teen_high)



answer = " YeS "  # exactly one leading and one trailing space
clean = answer.lower()[1:-1]   # remove 1 char from start and end
print(clean == "yes" or clean == "no")



word = "Processing"
print(word[:3].lower() == "pro" and word[-3:].lower() == "ing")


pressure = 198
max_pressure = 200
min_pressure = 120
print(pressure >= min_pressure and pressure <= max_pressure)


message = "Disk ERROR: temp high"
print("error" in message.lower() and "ignored" not in message.lower())