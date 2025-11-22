x=0
y=0
q=0
import time
while True:
    if x <= 9:
        z="0"
    else:
        z=""
    if y <= 9:
        z2="0"
    else:
        z=""
    print (f"{q}:{z2}{y}:{z}{x}")
    x+=1
    if x == 60:
        y+=1
        x-=60
    if y == 60:
        q+=1
        y-=60
    time.sleep(1)