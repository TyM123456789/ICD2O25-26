D = int(input())
E = int(input())
for i in range (E):
    T = input()
    Q = int(input())
    if T == "+":
        D += Q
    elif T == "-":
        D -= Q
print (D)