Players = int(input())
starplayers=0
for i in range(P):
    P = int(input())
    F = int(input())
    score = P*5 - F*3
    if score > 40:
        starplayers+=1
x=""
if starplayers == Players:
    x = "+"
print (f"{starplayers}{x}")

