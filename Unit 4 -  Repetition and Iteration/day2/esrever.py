def reverse(str):
    wordslist = [""]
    wordsstr = ""
    for x in str:
        if x != " ":
            wordslist[-1]+=x
        else:
            wordslist.append("")
    for x in range(0,len(wordslist)):
        wordslist[x] = wordslist[x][-1::-1]
    for x in wordslist:
        wordsstr += x + " "
    return wordsstr
print (reverse(""))