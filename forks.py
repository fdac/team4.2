import os

numCores = 4
forkId = 0


for i in range(numCores):
	forkId = i
	if(os.fork() == 0):
		print "Process: " + str(forkId)
		break;
	#elif( i == numCores - 1):
	#	exit()

	
