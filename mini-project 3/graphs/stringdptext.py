def stringdp(num,dp):
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
	if not "." in u:
		u+="."+"0"*dp
	if hasexp:
		u = u+"e"+m
	return u

#print stringdp(2,04)

def getdp(num):
	try:
		a = (str(num).split(".")[1])
		if "e" in a: return len(str(a).split("e")[0])
		else: return len(a)
	except IndexError:
		return 0

def scientificForm(num):
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
for a in [500304,0.0043,56.763,1.2,34,0.12]:
	print scientificForm(a)