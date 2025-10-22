#     Item             Quantity          Price($)
#     Apples                 12              0.75
#     Bananas                20              0.60
#     Oranges                 8              2.50
#     Cherries              123              4.42
i1 = "Apples"
i2 = "Bananas"
i3 = "Oranges"
i4 = "Cherries" 

q1 = 12
q2 = 20
q3 = 8
q4 = 123

p1 = 0.75
p2 = 0.60
p3 = 2.50
p4 = 4.42

print (f"{"Item":<10}{"Quantity":>12}{"Price($)":>16}")
print (f"{i1:<10}{q1:>12}{p1:>16}")
print (f"{i2:<10}{q2:>12}{p2:>16}")
print (f"{i3:<10}{q3:>12}{p3:>16}")
print (f"{i4:<10}{q4:>12}{p4:>16}")