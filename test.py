
import ast

dictTest={0:1, 1:2, 2:3, 3:2, 4:0, 5:1, 6:2, 7:3, 8:4, 9:4 , 10:5, 11:6, 12:7, 13:8, 14:9, 15:0, 16:0, 17:1, 18:1, 19:2, 20:2, 21:1, 22:0, 23:9, 24:1, 25:1, 26:9}


dictStr = str(dictTest)


afer = ast.literal_eval(dictStr)
print("Typ dic "+type(afer).__name__)
print(afer)