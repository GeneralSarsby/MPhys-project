from grapher08 import *
output = latexOutput()
output.setOutput("test08.pdf")
output.graphSize=[7,6]
output.marginSize=[0.2,1,2,0.3]



myGrapher = grapher(output)
y = series(output)
x = series(output)
#z = series(output)
#set y info
ypos = []
y.setData(ypos)
y.title = "$y$ position"
y.units = "AU"
#y.update(-7000000,None)

xpos = []
x.setData(xpos)
x.title = "$x$ position"
x.units = "AU"

#z.setData(ages)
#z.title = "log ages"
#z.units = "\log(years)"
output.openOutput()
#z.applyFunction("math.log10(x)")
#z.update(None,None)
#y.applyFunction("x/149.6e9")
#x.applyFunction("x/149.6e9")
#y.update(-2,None)
#x.update(-2,None)
#myGrapher.drawLablesSide(x,0)
#myGrapher.drawLablesSide(x,1)
#myGrapher.drawLablesSide(y,2)
#myGrapher.drawLablesSide(z,3)
#myGrapher.drawNotchesSide(x,0)
#myGrapher.drawNotchesSide(x,1)
#myGrapher.drawNotchesSide(z,3)
#myGrapher.drawNotchesSide(y,2)
#myGrapher.drawMinorNotchesSide(x,0,1)
#myGrapher.drawMinorNotchesSide(x,0,0)
#myGrapher.drawMinorNotchesSide(y,0,2)
#myGrapher.drawMinorNotchesSide(z,0,3)

#myGrapher.drawMajorGridDirection(x,1)
#myGrapher.drawMajorGridDirection(y,0)

#myGrapher.drawPlotAreaBorder()
#myGrapher.drawGraphBorder()
#myGrapher.drawXYScatter(x,y,"dot")
#myGrapher.drawXYScatterWithColor(x,z,"box","red")
myGrapher.AutoPlotScatterXY(x,y)
output.closeOutput()
