def count_letters(stri):
    #creates list
    letter_list=""
    checked = ""
    for x in stri:
        if x not in checked and x.isalpha():
            count = 0
            for y in stri:
                if x == y:
                    count +=1
            letter_list += x+str(count)
            checked += x
    return letter_list

print (count_letters("hello"))