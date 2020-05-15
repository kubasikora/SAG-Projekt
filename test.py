
import itertools


lista = ["1", "2", "3","4" , "5", "6", "7", "8", "9","9", "9", "9", "9", "9", "1", "2", "3", "4", "5", "6", "7", "8"]


def unique_prem(ser):
    return {"".join(p) for p in itertools.permutations(ser)}

perm = unique_prem(lista)


k = 0
for i in range(2000000):
    k = k+1
print("end "+str(k))