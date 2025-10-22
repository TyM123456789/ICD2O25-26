dist = float(input("How long is the trip? "))
fueleff = float(input("How far can your car go on one litre of gas (fuel efficiency)? "))
cost = round(float(input("How much does one litre of fuel cost? ")),2)
psngr = int(input("How many passengers are in your vehicle? "))

fuelcost = round(dist/fueleff,2)
totcost = round(fuelcost*cost,2)
costperpass = round(totcost/psngr,2)

print (f"The total fuel cost of this trip is {fuelcost} litres. The total    cost of this trip is ${totcost}. Split between each passenger, the cost is ${costperpass}.")
