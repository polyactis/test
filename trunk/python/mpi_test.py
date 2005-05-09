#!/usr/bin/env mpipython
from Scientific import MPI
import sys
from Numeric import Float, array, Int, zeros

communicator = MPI.world.duplicate()

print "I'm %s of %s"%(communicator.rank, communicator.size)

# Send and receive

if communicator.rank == 0:
	"""
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
	"""
	for dest in range(1,communicator.size):
		float_dest = float(dest)
		ar = array([[1,3,2],[float_dest,float_dest+1,float_dest+2]])
		communicator.send(ar, dest, dest)
		data, source, tag = communicator.receiveString(dest, None)
		print "%s received from %s, %s"%(communicator.rank, source, data)

else:
	while 1:
		data, source, tag, count = communicator.receive(Float, 0, None)
		no_of_columns = data[1]	#it's encoded in the 2nd entry
		no_of_rows = count/no_of_columns
		data.shape = (no_of_rows, no_of_columns)
		
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
			print "%s received from %s: %s"%(communicator.rank, source, repr(data))
			communicator.send("%s got data"%communicator.rank, 0, 0)
			break
			"""
			data.split(',')
			if data[0] == 'new':
				print "%s create an entry"%(communicator.rank)
			else:
				print "%s don't have %s"%(communicator.rank, data)
				communicator.send("NotFull", 0, 0)
			"""
if communicator.rank==0:	
	data = array([[1,3,2.0],[4,5,6]])
else:
	data = zeros((2,3),Float)
communicator.broadcast(data, 0)

print "%s has data: %s"%(communicator.rank, repr(data))
