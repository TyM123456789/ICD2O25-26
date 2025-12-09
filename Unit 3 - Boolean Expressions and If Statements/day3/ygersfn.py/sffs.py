str = "xxxx10burnxxxx"
status = "burn"
if str.find(status) !=-1:
    loc = str.find(status)
    print (str[loc-2:loc])