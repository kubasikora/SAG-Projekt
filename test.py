
def parseMessage(string): # the format of the string [], 'break', []
    string = string.replace(" ", "")
    lists = string.split("break")
    toReturn = []
    for l in lists:
        l = l.replace("'", "")
        l = l.replace("]", "")
        l = l.replace("[", "")
        if(l[0] == ","):
            l = l[1:]
        print(l[len(l)-1])
        if(l[len(l)-1] ==","):
            l = l[:-1]
            print("jestem ")
        print(l)
        nums = l.split(",")
        sigma = []
        for n in nums:
            sigma.append(int(n))
        toReturn.append(sigma)
    return toReturn

