#!/usr/bin/env mpipython
from Scientific import MPI
import Numeric, sys

communicator = MPI.world.duplicate()

print "I'm %s of %s"%(communicator.rank, communicator.size)

# Send and receive

if communicator.rank == 0:
	#check which one has the edge, if one has it, increment it.
	for dest in range(1,communicator.size):
		communicator.send("abs,abc", dest, dest)
		data, source, tag = communicator.receiveString(dest, None)
		print "%s received from %s, %s"%(communicator.rank, source, data)
	
	#if none has this edge, pick one which is still under memory threshold, add it to that one
	
	#tell each guy to output its memory and exit
	for dest in range(1, communicator.size):
		communicator.send("output", dest, dest)
		sys.stdout.flush()
		data, source, tag = communicator.receiveString(dest, None)
		if data=="Done":
			print "%s has finished its output"%(source)
	

else:
	while 1:
		data, source, tag = communicator.receiveString(0, None)
		if data=='increment':
			print "%s incremented"%(communicator.rank)
		elif data=="output":
			print "%s outputting..."%(communicator.rank)
			print "\toutputting..."
			#flush the file at last
			communicator.send("Done",0,0)
			sys.exit(0)
		elif data=="query":
			communicator.send("1",0,0)
		else:
			data.split(',')
			if data[0] == 'new':
				print "%s create an entry"%(communicator.rank)
			else:
				print "%s don't have %s"%(communicator.rank, data)
				communicator.send("NotFull", 0, 0)
