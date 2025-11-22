# 1) Temperature classifier (°C):
#    Print one of: cold (<0), cool (0–15), warm (16–25), hot (>25) based on temp_c.
#    hot (>25) based on temp_c. prints "warm"
temp_c = 23
if temp_c < 0:
    print("cold")
elif temp_c < 15:
    print("cool")
elif temp_c < 25:
    print("warm")
else:
    print("hot")


# 2) Letter grades:
#    Print A (90+), B (80–89), C (70–79), D (60–69), 
#    or F (<60) based on percent.

percent = 85
if percent >= 90:
    print ("A")
elif percent >= 80:
    print ("B")
elif percent >= 70:
    print ("C")
elif percent >= 60:
    print ("D")
else: 
    print ("F")

# 3) Password strength by length:
#    Print weak (<8), ok (8–11), or strong (12+) using len(password).

password = "qwerty"
plen = len(password)
if plen<8:
    print ("weak")
elif plen<=11:
    print ("ok")
else:
    print ("strong")

# 4) Greeting by hour (0–23):
#    Print Good morning (5–11), Good afternoon (12–16), 
#    Good evening (17–21), or Good night (other).

hour = 14
if 5 <= hour <= 11:
    print ("Good morning")
elif 12 <= hour <= 16:
    print ("Good afternoon")
elif 17 <= hour <= 21:
    print ("Good evening")
else: 
    print ("Good night")

# 5) Course code (strings):
#    If it begins with "ics" (case-insensitive) print "Computer Studies".
#    Elif it ends with "py" print "Python file".
#    Else print "Unknown".
#    (Use only lower(), len(), and slicing.)

ccode = "ICS.PdY"
if ccode.lower()[0:3] == "ics":
    print ("Computer Studies")
elif ccode[-2:] == "py":
    print ("Python file")
else:
    print ("Unknown")

# 6) Ticket price category by age:
#    Print child (0–12), student (13–17), adult (18–64), or senior (65+).

age = 14
if age <= 12:
    print ("child")
elif age <= 17:
    print ("student")
elif age <= 64:
    print ("adult")
else:
    print ("senior")

# 7) Shipping fee by weight (kg):
#    Print light (<=1.0), standard (<=5.0), or heavy (>5.0).

weight = 6.70
if weight <= 1.0:
    print ("light")
elif weight <= 5.0:
    print ("standard")
else:
    print ("heavy")

# 8) Honour roll:
#    If gpa >= 3.7 and attendance >= 95, print "Honour Roll".
#    Elif gpa >= 3.0, print "Good Standing".
#    Else print "Keep Going".

gpa = 3.8
attendance = 94
if gpa >= 3.7 and attendance >= 95:
    print ("Honour Roll")
elif gpa >= 3.0:
    print ("Good Standing")
else:
    print ("Keep Going")

# 9) File type by extension (strings):
#    If filename ends with ".py" -> print "Python".
#    Elif it ends with ".txt" -> print "Text".
#    Else -> "Other".
#    (Use only lower() and slicing.)

file = "if_statement_examples.py"
if file.lower()[-3:] == ".py":
    print ("Python")
elif file.lower()[-4:] == ".txt":
    print ("Text")
else:
    print ("Other")
    
# 10) Team placement (ints/floats):
#    If age < 13 -> "U13".
#    Elif 13–14 and height_m >= 1.65 -> "U15-Tall".
#    Elif 13–14 and height_m < 1.65 -> "U15".
#    Else -> "U17+".

age = 14
height_m = 1.67
if age < 13:
    print ("U13")
elif age <= 14 and height_m >= 1.65:
    print ("U15-Tall")
elif age <= 14 and height_m < 1.65:
    print ("U15")
else: 
    print ("U17")

# Challenge (optional):
#    Rewrite #8 using a nested if inside the gpa >= 3.7 branch (check attendance inside).

gpa = 3.8
attendance = 94
if gpa >= 3.7:
    if attendance >= 95:
        print ("Honour Roll")
    else:
        print ("Good Standing")
elif gpa >= 3.0:
    print ("Good Standing")
else:
    print ("Keep Going")