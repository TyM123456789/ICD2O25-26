dist = float(input("how far did you go (km)? "))
time = float(input("how many hours did it take? "))

speed = dist/time

print (f"DISTANCE: {dist}\nTIME: {time}\nSPEED: {round(speed, 1)}")