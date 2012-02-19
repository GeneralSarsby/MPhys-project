##fewest coins solution..

## all currencies in pennies..
def coin_formater(s):
    if s < 100:
        return str(s) + "c"
    elif str(s)[-2:] == "00":
        return "$" + str(s/100)
    else:
        return "$" + str(s/100) + "." + str(s)[-2:]
    
total = 456 #

def get_coins(total):
    coins = []
    while total != 0:
        base = 10 ** (len(str(total))-1)
        for i in [5,2,2,1,1]:
            if base * i  <= total:
                total -= base * i
                coins += [base * i]
    return coins
            
coins = get_coins(total)
print total, "=",
for i in coins:
    print coin_formater(i),
print 

values = []
total_coins = []
for i in range(1,10000):
    print i, len(get_coins(i))
    values += [i]
    total_coins += [len(get_coins(i))]
    
from grapher08 import *
output = latexOutput()
output.setOutput("coins.pdf")
output.graphSize=[21,15]
output.marginSize=[0.2,1,2,0.3]

myGrapher = grapher(output)
myGrapher.dotsize = 0.05
y = series(output)
x = series(output)

y.setData(total_coins)
y.title = "total coins"
y.units = ""

x.setData(values)
x.title = "total"


output.openOutput()
myGrapher.drawMajorGridDirection(x,1)
myGrapher.AutoPlotScatterXY(x,y)
output.closeOutput()
