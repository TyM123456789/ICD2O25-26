#house dimensions
len = float(input("What is the length of one wall of the house (meters)? "))
width = float(input("What is the width of one wall of the house (meters)? "))
height = float(input("How tall is the house (meters)? "))
#brick cost/dimensions
bcost = round(float(input("How much does each brick cost? ")),2)
blen = float(input("How long are the bricks (cm)?"))/100
bwidth = float(input("How wide are the bricks (cm)?"))/100
bheight = float(input("How tall are the bricks (cm)?"))/100

#surface area/cost
wallsa = len*height*4
bricknum = (len/blen)*(height/bheight)*4
print (len/blen)
print (height/bheight)
tcost=round(bricknum*bcost,2)

#print

print (f"House Details:\n- Wall Surface Area: {wallsa} square meters\n- Bricks Required: {bricknum} bricks\n- Total Cost of Bricks: {tcost} dollars.")