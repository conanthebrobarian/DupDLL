import re, sys, subprocess, StringIO
procmodlist = []
modlist = []
curproc = ""

if len(sys.argv) == 2:
	tskoutput = open(sys.argv[1], "r")
elif len(sys.argv) > 2:
	print "Usage: run on its own to detect duplicate DLLs on host machine"
	print "Run with a tasklist /m output to detect duplicate DLLs in file"
else:
	proc = subprocess.Popen("tasklist /m", stdout=subprocess.PIPE, shell=True)
	(tstr, terr) = proc.communicate()
	tskoutput = StringIO.StringIO(tstr)
	
#loop over header
#for x in range(1,4):
#		tskoutput.readline()	
	
m = re.compile("^[a-zA-Z0-9]")

for x in tskoutput:
	if m.match(x):
		modlist.sort()
		if curproc != "":
			procmodlist.append((curproc, modlist))
		curproc = x.split()[0]
		modlist = []
		#loop through csv with a process on the same line
		for y in x.split(","):
			try:
				modlist.append(y.split()[-1])
			except:
				True
	else:
		for y in x.split(","):
			try:
				modlist.append(y.split()[-1])
			except:
				True

procmodlist.sort()
for x in procmodlist:
	dllstr = ""
	for y in x[1]:
		if y == dllstr:
			print "Duplicate DLL detected in " + x[0] + " : " + y
		dllstr = y
