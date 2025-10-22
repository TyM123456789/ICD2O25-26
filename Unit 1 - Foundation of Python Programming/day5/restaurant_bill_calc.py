drink = round(float(input("How much did your drink cost? ")),2)
app = round(float(input("How much did your appetizer cost? ")),2)
entree = round(float(input("How much did your entree cost? ")),2)
dessert = round(float(input("How much did your dessert cost? ")),2)

subtot = drink+app+entree+dessert

tip = int(input("How much did you tip(%)? "))/100
doltip = round(subtot*tip,2)
totcost= subtot + doltip

print(f"Bill Summary:\nSubtotal: {subtot}\nTip: ({tip}%): {doltip}\nTotal Cost: {totcost}")