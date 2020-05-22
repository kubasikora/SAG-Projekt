
def parseSets(string): # the format of the string [[[],[], ..], 'break', [[],[],...]]
    string = string.replace(" ", "")
    lists = string.split("break")
    toReturn = []
    for l in lists:
        l = l.replace("'", "")
        sigmas = l.split("]")
        converted = []
        for sigma in sigmas:
            sigma = sigma.replace("[", "")            
            if( len(sigma)> 0 and sigma[0] == ","):
                sigma = sigma[1:]
            if(len(sigma)) > 0:
                nums = sigma.split(",")
                convertedSigma = []
                for n in nums:
                    convertedSigma.append(int(n))
                converted.append(convertedSigma)
        toReturn.append(converted)

    return toReturn



listaA = [[[1, 2, 3, 4, 5],[3, 4, 5]],'break', [[1, 2, 3]]]

zbiory = parseSets(str(listaA))
print(zbiory)


listaC = [[[1, 2, 3, 4, 5],[3, 4, 5]],'break', []]

print(parseSets(str(listaC)))