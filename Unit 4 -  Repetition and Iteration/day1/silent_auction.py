N = int(input())
highest = 0
winner = "none"
for i in range(N):
    name = input()
    bid = int(input())
    if bid > highest:
        winner = name
        highest = bid
print (winner)
