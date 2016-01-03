def compare(a,b):
	aa=a.split("-")
	bb=b.split("-")
	ta=[]
	tb=[]
	for aaa in aa:
		ta.append(int(aaa))
	for bbb in bb:
		tb.append(int(bbb))
	for i in range(len(ta)):
		if ta[i]<tb[i]:
			return False
		if ta[i]>tb[i]:
			return True



print (compare("12-5463","12-7879"))