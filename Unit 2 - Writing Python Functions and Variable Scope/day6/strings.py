str1 = "hello"
str2 = "alpha"
str3 = "bet"
str4 = "alphabet"

print (len(str1))
print (len(str4))
print (len("Ryan"))            #largest pos index is len - 1
print (len("Enzo"))

print (str4[3])                #use [] to select a specific index
print (str4[-5])               #same thing using neg index

print ("hello"[2])             #same l
print ("hello"[-3])

# print("hello"[100])          #biggest index is 4
# print("hello"[len("hello")]) #len("hello") = 5. 5>4


#[start:end:step]

print (str4[2:5])              #6666666667 pha

print ("Enzo"[2:4])            # "zo" 2 inclusive 4 exclusive

print (str4[5:8])              #bet
print (str4[-3:8])             #bet
print (str4[-3:])              #bet if end is left empty goes to end
print (str4[5:])               #bet

print ("0123456789"[0:10:2])   #02468 step does every {step}th character
print ("0123456789"[0:10:3])   #0369

print ("0123456789"[-1:-11:-1])#backkwords

print (str4[::2])              #apae

print (str4[2::2])            #pae