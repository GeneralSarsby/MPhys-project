import os
import math
class latexOutput():
	caption = ""
	graphSize = [10,5] #in cm
	marginSize = [.3,1,2,.3] #t b l r in cm
	#output = "output.tex"
	output = "test.tex"
	okNums = range(-6,7,1) #do not change
	runPDF = False
	def setGraphSize(self,newsize):
		if len(newsize)==2:
			graphSize = newsize
		else:
			self.target.putComment("new graph size is wrong length")
	def setMarginSize(self,newsize):
		if len(newsize)==4:
			narginSize = newsize
		else:
			self.target.putComment("new margin size is worng length")
	def setOutput(self,newoutput):
		self.output = newoutput
	def openOutput(self):
		if self.output == "shell":
			return
		if self.output[-4:]==".pdf":
			self.output = self.output[:-4]+".tex"
			self.runPDF=True
		self.outFile = open(self.output,"w")
		w = self.graphSize[0]
		h = self.graphSize[1]
		if self.runPDF:
			a=["documentclass{article}","usepackage{amsmath}","usepackage[pdftex]{color,graphicx}"]
			a+=["usepackage{rotating}"]
			ws = "{"+str(w+0.2)+"cm}"
			hs = "{"+str(h+0.2)+"cm}"
			a+=["setlength{\paperwidth}"+ws]
			a+=["setlength{\paperheight}"+hs]
			a+=["usepackage[top=0.1cm, bottom=0.0cm, left=0.0cm, right=0.0cm]{geometry}"]
			a+=["usepackage{color}"]
			a+=["usepackage[pdftex,pdfauthor={Matthew Sarsby}, pdftitle={The Title}]{hyperref}"]
			a+=["begin{document}","noindent"]
			for b in a:self.putCommand(b)
		self.putCommand("setlength{\unitlength}{1.0cm}")
		
		s = "begin{picture}("+str(w)+","+str(h)+")(0,0)"
		self.putCommand(s)
	def closeOutput(self):
		self.putCommand("end{picture}")	
		if self.output == "shell":
			return
		else:
			if self.runPDF: self.putCommand("end{document}")
			self.putComment("file wirtten to "+ str(self.output))
			self.outFile.close()
		if self.runPDF:
			a = "latex " + str(self.output)
			os.system(a)
	def put(self,text):
		"Do not call directally, will be called from other functions"
		if self.output == "shell":
			print text
		else:
			self.outFile.write(text+"\n")
	def putComment(self,text):
		if not self.output=="shell":
			print text
		s = "%"+str(text)
		self.put(s)
	def putObject(self,x,y,object):
		if (x < 0) or (x > self.graphSize[0]):
			self.putComment("will not plot of the graph, x out of range")
		if (y < 0) or (y > self.graphSize[1]):
			self.putComment("will not plot of the graph, y out of range")		
		s = "\put("+str(x)+","+str(y)+"){"+object+"}"
		self.put(s)
	def getLine(self,x,y,l):
		#\line(x1, y1){length}
		
		if (x in self.okNums) and (y in self.okNums):
			s = "\line("+str(x)+","+str(y)+"){"+str(l)+"}"
		else:
			print "can not make a line with x and y vectores"
		return s
	def getQbezier(self,x1,y1,x2,y2,x3,y3):
		#print "this should not be called, something is already wrong, sorry."
		s = "\qbezier("+str(x1)+","+str(y1)+")("+str(x2)+","+str(y2)+")("+str(x3)+","+str(y3)+")"
		return s
	def putQbezier(self,x1,y1,x2,y2,x3,y3):
		self.put(self.getQbezier(x1,y1,x2,y2,x3,y3))
	def putQbezierFromG(self,x1,y1,x2,y2,m1,m2):
		x = float(m2*x2-m1*x1+y1-y2) / (m2-m1)
		u = y1+m1*(x-x1)
		v = y2+m2*(x-x2)
		y = 0.5*(u+v)
		self.putQbezier(x1,y1,x,y,x2,y2)
	def putLineXYXY(self,x1,y1,x2,y2):
		l = ((x2-x1)**2+(y2-y1)**2)**0.5
		dx = x2-x1
		dy = y2-y1
		if (dx in self.okNums) and (dy in self.okNums):
			s = self.getLine(dx,dy,l)
			self.putObject(x1,y1,s)
		else:
			self.putQbezier(x1,y1,(x1+x2)/2,(y1+y2)/2,x2,y2)
	def putLineXYAngleLength(self,x,y,angle,length):
		return
	def putRec(self,x,y,w,h):
		self.putObject(x,y,self.getLine(1,0,w))
		self.putObject(x,y,self.getLine(0,1,h))
		self.putObject(x+w,y,self.getLine(0,1,h))
		self.putObject(x,y+h,self.getLine(1,0,w))
	def putMan(self,x,y,w):
		w=float(w)
		ring = self.getCircle(w*4+0.02)
		self.putObject(x,y,ring)
		y-=w/2
		line = self.getLine(0,1,3*w/2)#body
		self.putObject(x,y,line)
		x-=w/2
		line = self.getLine(1,0,w)#pelvis
		self.putObject(x,y,line)
		line = self.getLine(0,-1,3*w/2)#l leg
		self.putObject(x,y,line)
		x+=w
		line = self.getLine(0,-1,3*w/2)#r leg
		self.putObject(x,y,line)
		x-=w/2
		y+=3*w/2
		x-=w
		line = self.getLine(1,0,2*w)#arms
		self.putObject(x,y,line)
		x+=w
		y+=w/2
		head = self.getCircle(w)
		self.putObject(x,y,head)
		
	def getDot(self,r):
		s = "\circle*{"+str(r)+"}"
		return s
	def putCommand(self,size):
		"""size is already known, is is a string e.g. small, footnotesize, tiny, normalsize, large"""
		self.put("\\"+size)
	def getCircle(self,r):
		s = "\circle{"+str(r)+"}"
		return s
	def multiputObject(self,x,y,dx,dy,n,object):
		s = "\multiput("+str(x)+","+str(y)+")("+str(dx)+","+str(dy)+"){"+str(n)+"}{"+object+"}"
		self.put(s)
	def getRotatedText(self,text):
		#\begin{sideways}Paper\end{sideways}
		s = "\\begin{sideways}"+text+"\end{sideways}"
		return s
	def plotSize(self):
		sizex = self.graphSize[0]-(self.marginSize[2]+self.marginSize[3])
		sizey = self.graphSize[1]-(self.marginSize[0]+self.marginSize[1])
		return [sizex,sizey]
	def beginColor(self,color):
		colours = ["black","white","red","green","blue","yellow","cyan","magenta"]
		if color not in colours:
			self.putComment(str(color)+" is not an available color")
			return
		s = "color{"+color+"}"
		self.putCommand(s)
	def endColor(self):
		s = "color{black}"
		self.putCommand(s)
class series():
	title = "Title"
	units = "Units"
	data=[]
	target=0
	values = [1,2,5]
	power = 0
	minWidth = 0.6 # in cm
	maxWidth = 1.6
	low=list() #x y lower value - data units
	high=list() #x, y hiver values - data units
	intervals=list() #x y number of invervals = nodes-1
	intervalsWidth=list() # x y intervals width in cm
	lables=list() # a list for the lables that would be plotted on the axies e.g.(1,2,3 and
	# 0.2,0.4,0.6) can be text eg. pi, pi/2
	lablespos=list() #is the position in data chords where the labes should be.
	scale=list()
	def __init__(self,targetOutput):
		self.target = targetOutput
	def __len__(self):
		return len(self.data)
	def __getitem__(self,item):
		return self.data[item]
	def __setitem__(self,item,newcontent):
		self.data[item] = newcontent
	def __repr__(self):
		s="{"
		for a in self.data:
			s+=str(a)+", "
		s=s[:-2]
		s+= "} "+self.title + " (" + self.units + ")"
		return s
	def setTarget(self,newtarget):
		self.target = newtarget
		self.update(None,None)
	def update(self,low,high):
		self.analize(low,high)
		self.setLables()
	def max(self):
		return max(self.data)
	def min(self):
		return min(self.data)
	def expandSeries(self,series):
		newmin = min([self.min(),series.min()])
		newmax = max([self.max(),series.max()])
		self.update(newmin,newmax)
	def setData(self,newdata):
		self.data=newdata[:]
		self.low=[0,0]
		self.high=[0,0]
		self.intervals=[0,0]
		self.intervalsWidth=[0,0]
		self.lables=[0,0]
		self.scale=[0,0]
		self.lablespos=[0,0]
		self.update(None,None)
	def setValuesFromSeries(self,series):
		self.target=series.target
		self.power =series.power
		self.minWidth = series.minWidth
		self.maxWidth = series.minWidth
		self.low = series.low[:]
		self.high= series.high[:]
		self.intervals= series.intervals[:]
		self.intervalsWidth=series.intervalsWidth[:]
		self.lables=series.lables[:]
		self.lablespos=series.lablespos[:]
		self.scale=series.scale[:]
	def applyFunction(self,func):
		for a in range(0,len(self.data)):
			x = self.data[a]
			u = eval(func)
			self.data[a]=u
	def analize(self,low,high):
		if low == None: low = min(self.data)
		if high == None : high = max(self.data)
		if self.target == 0:
			self.target.putComment("Oops, series has no target")
		plotSize = self.target.plotSize()
		for a in [0,1]:
			notgood = 1
			currentval = 0
			self.power = 0
			t = 0
			while notgood:
				scale = self.values[currentval]*10**self.power
				sections = int(high/scale)-int(low/scale)+1
				if sections == 0:
					width = 10000
				else:
					width = float(plotSize[a])/(sections)
				if width < self.minWidth:
					currentval+=1
				elif width > self.maxWidth:
					currentval-=1
				else: notgood = 0
				if currentval == 3:
					currentval = 0
					self.power +=1
				if currentval == -1:
					currentval = 2
					self.power -=1
			self.intervals[a] =  sections
			self.intervalsWidth[a] = width
			self.low[a] = int(low/scale)*scale
			self.high[a] = (int(high/scale)+1)*scale
			self.scale[a] = scale
	def setLables(self):
		for a in [0,1]:
			lables=[]
			for b in range(0,self.intervals[a]+1):
				lables.append(str(self.low[a]+b*self.scale[a]))
			dps=[]
			for i in lables:
				dps.append(self.getdp(i))
			maxdp=max(dps)
			for i in range(0,len(lables)):
				lables[i] = self.setdp(lables[i],maxdp)
			self.lables[a]=lables
			self.lablespos[a]=lables
	def SFNumber(self,num,sf):
		return
	def numberOfMinorNotches(self,axis):
		fewnotches = [4,3,4]#125
		lotsnotches = [9,7,9]
		b = float(self.lablespos[axis][1])-float(self.lablespos[axis][0])
		a =str(self.scientificForm(b))[0]
		a = self.values.index(int(a))
		if self.intervalsWidth[axis]<(self.maxWidth+self.minWidth)/2:
			#if a == "2":return 3
			#if a == "5":return 4
			#if a == "1":return 4
			return fewnotches[a]
		else:
			#if a == "2":return 7
			#if a == "5":return 9
			#if a == "1":return 9
			return lotsnotches[a]
	def setdp(self,num,dp):
		x = str(num)
		if "e" in x:
			v = x.split("e")
			m = str(int(v[1]))
			x=v[0]
			hasexp=True
		else: hasexp=False
		u = ""
		for a in range(0,len(x)):
			if x[a]==".":
				#x.append(x[a])
				for b in range(0,dp+1):
					try:
						u+= x[a+b]
					except IndexError:
						u+= "0"
				break
			u+=x[a]
		if not "." in u and not dp == 0:
			u+="."+"0"*dp
		if hasexp:
			u = u+"e"+m
		return u
	def getdp(self,num):
		try:
			a = (str(num).split(".")[1])
			if "e" in a: return len(str(a).split("e")[0])
			else: return len(a)
		except IndexError:
			return 0
	def scientificForm(self,num):
		num = float(num)
		power = 0
		a = len(str(int(num)))
		if int(num)==0:a=2
		while  a<>1:
			if num>1:
				num = num/10
				power+=1
			else:
				num = num*10
				power-=1
			a = len(str(int(num)))
			if int(num)==0:a=2
		return str(num)+"e"+str(power)
	def convertPointToUnits(self,index,axis):
		""" index is the index in the data, and axis is ether 0 or 1 for x or y.."""
		#return (float(self.data[index]-self.low[axis])/self.scale[axis])*self.interv
		#alsWidth[axis]+self.target.marginSize[2-axis]
		return self.convertValueToUnits(self.data[index],axis)
	def convertValueToUnits(self,value,axis):
		return (float(value-self.low[axis])/self.scale[axis])*self.intervalsWidth[axis]+self.target.marginSize[2-axis]
class grapher():
	dotsize = 0.1
	lableindent=[.4,.2]
	textheight=0.2
	textwidth=0.10
	notchlength=0.1
	minornotchlength=0.05
	def __init__(self,targetOutput):
		self.target = targetOutput
		#self.target.openOutput()
	def drawGraphBorder(self):
		self.target.putComment("Drawing Graph Border")
		s = self.target.graphSize
		self.target.putRec(0,0,s[0],s[1])
	def getSortedXYForAxis(self,xseries,yseries,axis):
		if not len(xseries.data)==len(yseries.data):
			self.target.putComment("Data is not of the same lengths.")
			return
		oldx=xseries.data[:]
		oldy=yseries.data[:]
		x=[]
		y=[]
		for a in range(0,len(xseries.data)):
			if axis == 0:minval =oldx.index(min(oldx))
			elif axis == 1:minval =oldy.index(min(oldy))
			else: pass
			y.append(oldy.pop(minval))
			x.append(oldx.pop(minval))
		newx =series(self.target)
		newy =series(self.target)
		newx.setData(x)
		newy.setData(y)
		newx.setValuesFromSeries(xseries)
		newy.setValuesFromSeries(yseries)
		return [newx,newy]
	def drawBottomAndLeftPlotArea(self):
		self.target.putComment("Drawing bottom left plot area lines")
		s = self.target.plotSize()
		line = self.target.getLine(1,0,s[0])
		x = self.target.marginSize[2]
		y=self.target.marginSize[1]
		self.target.putObject(x,y,line)
		line = self.target.getLine(0,1,s[1])
		self.target.putObject(x,y,line)
	def drawPlotAreaBorder(self):
		self.target.putComment("Drawing plot area border")
		p = self.target.plotSize()
		m = self.target.marginSize
		self.target.putRec(m[2],m[1],p[0],p[1])
	def drawXYScatter(self,xseries,yseries,dottype):
		""" dot type will be dot, or circle, cross etc."""
		self.target.putComment("Dawing an x - y scatter of "+xseries.title+" and "+yseries.title)
		if not len(xseries.data)==len(yseries.data):
			self.target.putComment("Data is not of the same lengths.")
			return
		for a in range(0,len(xseries.data)):
			x = xseries.convertPointToUnits(a,0)
			y = yseries.convertPointToUnits(a,1)
			if dottype == "dot":
				dot = self.target.getDot(self.dotsize)
				self.target.putObject(x,y,dot)
			elif dottype == "circle":
				dot = self.target.getCircle(self.dotsize)
				self.target.putObject(x,y,dot)
			elif dottype == "cdot":
				dot = self.target.getDot(float(self.dotsize)/10)
				self.target.putObject(x,y,dot)
				dot = self.target.getCircle(self.dotsize)
				self.target.putObject(x,y,dot)
			elif dottype == "box":
				x -= self.dotsize/2
				y-= self.dotsize/2
				self.target.putRec(x,y,self.dotsize,self.dotsize)
			elif dottype == "cross":
				x -= self.dotsize/2
				y-= self.dotsize/2
				self.target.putLineXYXY(x,y,x+self.dotsize,y+self.dotsize)
				y += self.dotsize	
				self.target.putLineXYXY(x,y,x+self.dotsize,y-self.dotsize)
			elif dottype == "man":
				self.target.putMan(x,y,self.dotsize)
			else:
				#this is to help feedback to the user wft they did.
				self.target.putObject(x,y,dottype)
	def drawXYScatterWithColor(self,xseries,yseries,dottype,color):
		self.target.beginColor(color)
		self.drawXYScatter(xseries,yseries,dottype)
		self.target.endColor()
	def drawConnectingLineXY(self,xseries,yseries):
		"Draws a line in order from the first xy pare to the last xy pair"
		self.target.putComment("Dawing commecting lines")
		if not len(xseries.data)==len(yseries.data):
			self.target.putComment("Data is not of the same lengths.")
			return
		for a in range(0,len(xseries.data)-1):
			x1 = xseries.convertPointToUnits(a,0)
			x2 = xseries.convertPointToUnits(a+1,0)
			y1 = yseries.convertPointToUnits(a,1)
			y2 = yseries.convertPointToUnits(a+1,1)
			self.target.putLineXYXY(x1,y1,x2,y2)
	def drawConnectingLineXYSortedAxis(self,xseries,yseries,axis):
		"draws a line from the yx pair with the smallest x to the xy pair with the largest x"
		new = self.getSortedXYForAxis(xseries,yseries,axis)
		self.drawConnectingLineXY(new[0],new[1])

	def drawConnectingCurvedLineXYSortedAxis(self,xseries,yseries,axis):
		"draws a line from the yx pair with the smallest x to the xy pair with the largest x"
		new = self.getSortedXYForAxis(xseries,yseries,axis)
		self.drawConnectingCurvedLineXY(new[0],new[1])
	def drawConnectingCurvedLineXY(self,xseries,yseries):
		"""
		This currentally does not work. Needs Fixing.
		"""
		if not len(xseries.data)==len(yseries.data):
			self.target.putComment("Data is not of the same lengths.")
			return
		m1 = 0
		m2 = 0
		for a in range(0,len(xseries.data)-2):
			x1 = xseries.convertPointToUnits(a,0)
			x2 = xseries.convertPointToUnits(a+1,0)
			y1 = yseries.convertPointToUnits(a,1)
			y2 = yseries.convertPointToUnits(a+1,1)
			m1=m2
			dx1 = xseries.convertPointToUnits(a+1,0)-xseries.convertPointToUnits(a,0)
			dy1 = yseries.convertPointToUnits(a+1,1)-yseries.convertPointToUnits(a,1)
			dx2 = xseries.convertPointToUnits(a+2,0)-xseries.convertPointToUnits(a+1,0)
			dy2 = yseries.convertPointToUnits(a+2,1)-yseries.convertPointToUnits(a+1,1)
			try:
				mf=float(dy1)/dx1
			except ZeroDivisionError:
				mf = 1000.0
			try:
				mn=float(dy2)/dx2
			except ZeroDivisionError:
				mn = 1000.0
			m2 = (mf+mn)/2
			#m2 = -1.0/m2
			print m1, m2
			self.target.putQbezierFromG(x1,y1,x2,y2,m1,m2)
	def drawXYLables(self,xseries,yseries):
		return
	def drawLablesLeft(self,series):
		self.drawLablesSide(series,2)
	def drawLablesBottom(self,series):
		self.drawLablesSide(series,1)
	def drawLablesSide(self, series, side):
		"tblr"
		self.target.putCommand("footnotesize")
		plotsize = self.target.plotSize()
		if side in [0,1]:
			if side == 1:
				y = self.target.marginSize[1]-self.lableindent[1] - self.textheight
			if side == 0:
				y = self.target.marginSize[1] +self.lableindent[1] + plotsize[1]
			for a in range(0,len(series.lables[0])):
				s = series.lables[0][a]
				x = series.convertValueToUnits(float(series.lablespos[0][a]),0) - len(s)*self.textwidth
				self.target.putObject(x,y,s)	
		else:
			axis = 1
			for a in range(0,len(series.lables[1])):
				s = series.lables[1][a]
				if side == 2:
					x = self.target.marginSize[2]-self.lableindent[0]-len(s)*self.textwidth
				else:
					x = self.target.marginSize[2]+self.lableindent[0]-len(s)*self.textwidth
					x += plotsize[0]
				y = series.convertValueToUnits(float(series.lables[1][a]),1) - self.textheight/2
				self.target.putObject(x,y,s)
		self.target.putCommand("normalsize")
	def drawNotchesBottom(self,series):
		self.drawNotchesSide(series,1)
	def drawNotchesLeft(self,series):
		self.drawNotchesSide(series,2)
	def drawNotchesSide(self,series,side):
		plotsize = self.target.plotSize()
		if side in [0,1]:
			y = self.target.marginSize[1]
			if side == 0:
				y+=plotsize[1]
			x = series.convertValueToUnits(float(series.lablespos[0][0]),0)
			dx = series.convertValueToUnits(float(series.lablespos[0][1]),0)-x
			n = len(series.lablespos[0])
			if side == 1: line = self.target.getLine(0,1,self.notchlength)
			else: line = self.target.getLine(0,-1,self.notchlength)
			self.target.multiputObject(x,y,dx,0,n,line)
		elif side in [2,3]:
			y = series.convertValueToUnits(float(series.lablespos[1][0]),1)
			dy = (series.convertValueToUnits(float(series.lablespos[1][1]),1))-y
			n = len(series.lablespos[1])
			x = self.target.marginSize[2]
			if side == 2:
				line = self.target.getLine(1,0,self.notchlength)
			else:
				x+=plotsize[0]
				line = self.target.getLine(-1,0,self.notchlength)
			self.target.multiputObject(x,y,0,dy,n,line)
	def drawMinorNotchesBottom(self,series,notches):
		self.drawMinorNotchesSide(series,notches,1)
	def drawMinorNotchesLeft(self,series,notches):
		self.drawMinorNotchesSide(series,notches,2)
	def drawMinorNotchesSide(self,series,notches,side):
		plotsize = self.target.plotSize()
		self.target.putCommand("linethickness{0.02mm}")
		if notches == 0:
			if side < 3: a = 0
			else: a = 1
			notches = series.numberOfMinorNotches(a)
		if side in [0,1]:
			x = series.convertValueToUnits(float(series.lablespos[0][0]),0)
			dx = series.convertValueToUnits(float(series.lablespos[0][1]),0)-x
			dx = dx/(notches+1)
			n = (len(series.lablespos[0])-1)*(notches+1)
			y = self.target.marginSize[1]
			if side == 1:
				line = self.target.getLine(0,1,self.minornotchlength)
			else:
				y+=plotsize[1]
				line = self.target.getLine(0,-1,self.minornotchlength)
			self.target.multiputObject(x,y,dx,0,n,line)
		if side in [2,3]:
			y = series.convertValueToUnits(float(series.lablespos[1][0]),1)
			dy = (series.convertValueToUnits(float(series.lablespos[1][1]),1))-y
			dy = dy/(notches+1)
			n = (len(series.lablespos[1])-1)*(notches+1)
			x = self.target.marginSize[2]
			if side == 2:
				line = self.target.getLine(1,0,self.minornotchlength)
			else:
				x += plotsize[0]
				line = self.target.getLine(-1,0,self.minornotchlength)
			self.target.multiputObject(x,y,0,dy,n,line)
		self.target.putCommand("thinlines")	
	def drawMajorGridDirection(self,series,direction):
		plotsize = self.target.plotSize()
		if direction == 0:
			y = series.convertValueToUnits(float(series.lablespos[1][0]),1)
			dy = (series.convertValueToUnits(float(series.lablespos[1][1]),1))-y
			n = len(series.lablespos[1])
			x = self.target.marginSize[2]
			line = self.target.getLine(1,0,plotsize[0])
			self.target.multiputObject(x,y,0,dy,n,line)
		elif direction == 1:
			x = series.convertValueToUnits(float(series.lablespos[0][0]),0)
			dx = (series.convertValueToUnits(float(series.lablespos[0][1]),0))-x
			n = len(series.lablespos[0])
			y = self.target.marginSize[1]
			line = self.target.getLine(0,1,plotsize[1])
			self.target.multiputObject(x,y,dx,0,n,line)
	def drawMinorGridDirection(self,series,notches,direction):
		self.target.putCommand("linethickness{0.02mm}")
		if notches == 0:
			notches = series.numberOfMinorNotches(direction)
		y = series.convertValueToUnits(float(series.lablespos[1][0]),1)
		dy = (series.convertValueToUnits(float(series.lablespos[1][1]),1))-y
		dy = dy/(notches+1)
		n = (len(series.lablespos[1])-1)*(notches+1)
		x = self.target.marginSize[2]
		line = self.target.getLine(1,0,self.target.plotSize()[0])
		self.target.multiputObject(x,y,0,dy,n,line)
		self.target.putCommand("thinlines")
	def drawAxisTitleBottom(self,series):
		if not len(series.units) == 0:
			s = series.title + " ($" + series.units + "$)"
		else:
			s = series.title
		y = self.target.marginSize[1]-self.lableindent[1]-3*self.textheight
		x = self.target.marginSize[2]+float(self.target.plotSize()[0])/2
		x-= len(s)*self.textwidth
		self.target.putObject(x,y,s)
	def drawAxisTitleLeft(self,series):
		if not len(series.units) == 0:
			s = series.title + " ($" + series.units + "$)"
		else:
			s = series.title
		x = self.target.marginSize[2]-2*self.lableindent[0]
		lablelengths = []
		for a in series.lables[1]:
			lablelengths.append(len(a))
		x -= max(lablelengths)*self.textwidth + self.textheight
		y = self.target.marginSize[1]+float(self.target.plotSize()[1])/2
		y-= len(s)*self.textwidth
		s = self.target.getRotatedText(s)
		self.target.putObject(x,y,s)
	def AutoPlotScatterXY(self,x,y):
		self.drawPlotAreaBorder()
		self.drawGraphBorder()
		#self.drawBottomAndLeftPlotArea()
		self.drawXYScatter(x,y,"dot")
		self.drawLablesLeft(y)
		self.drawLablesBottom(x)
		self.drawNotchesLeft(y)
		self.drawMinorNotchesLeft(y,0)
		self.drawNotchesBottom(x)
		self.drawMinorNotchesBottom(x,0)
		self.drawAxisTitleBottom(x)
		self.drawAxisTitleLeft(y)
		#self.drawConnectingLineXYSortedAxis(x,y,0)
		#self.drawConnectingCurvedLineXYSortedAxis(x,y,0)
		#self.drawConnectingLineXY(x,y)
