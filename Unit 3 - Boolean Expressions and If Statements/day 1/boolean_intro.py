age = 15
print(age >= 16)         # False

temp_c = -2
print(temp_c <= 0)       # True

speed = 72
limit = 80
print(speed > limit)     # False

length = 19.9
target = 20.0
print(length != target)  # True

username = "Admin"
print(username.lower() == "admin")    #true

msg = "System OK"
print("ok" in msg.lower())   #True (in means in)

password = "secret42"
print(len(password) >= 8)     #True

word = "preheating"
print(word[:3].lower() == "pre")  # starts with        TRUE
print(word[-3:].lower() == "ing") # ends with           TRUE

title = "The Hobbit"
print(title[:3].lower() == "the")   #ttttttrue

name = "maria"
print(name != "" and name[0].lower() < "m")  # alphabet check (guard empty)                     %trygtrwueotklrtrue