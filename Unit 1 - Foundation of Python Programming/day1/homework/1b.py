answer = str(input("""
Who teaches ICD20?
    a. Mr. Stott
    b. Mr. Deslauriers
    c. Ms. Landau
    d. Ms. K
"""))
if answer.lower() == "b":
    print ("correct!")
elif answer.lower() == "a" or "c" or "d":
    print ("wrong. the answer is b.")
else:
    print ("that is not one of the answers.")