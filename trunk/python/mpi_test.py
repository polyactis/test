#!/usr/bin/env mpipython
#2007-01-20 test the problem incurred by rpy under parallel environment
#basically, the popen() or stderr causes the communication 
import sys, os, math
bit_number = math.log(sys.maxint)/math.log(2)
if bit_number>40:       #64bit
	sys.path.insert(0, os.path.expanduser('~/lib64/python'))
	sys.path.insert(0, os.path.join(os.path.expanduser('~/script64/annot/bin')))
	binary_path = os.path.expanduser('~/script64/haifeng_annot/bin')
else:   #32bit
	sys.path.insert(0, os.path.expanduser('~/lib/python'))
	sys.path.insert(0, os.path.join(os.path.expanduser('~/script/annot/bin')))
	binary_path = os.path.expanduser('~/script/haifeng_annot/bin')
import getopt, csv, cPickle, re
from Scientific import MPI
from codense.common import system_call, mpi_synchronize, output_node, input_node,\
	computing_node
import Numeric as numpy
from sets import Set

hostname = os.popen('hostname').read().strip()
if hostname in ['soma-desktop', 'dl403k-1']:
	import rpy_options
	rpy_options.rpy_options['RHOME']='/usr/lib/R'
	if hostname=='soma-desktop':
		rpy_options.rpy_options['RVERSION']='2.3.1'
	elif hostname=='dl403k-1':
		rpy_options.rpy_options['RVERSION']='2.4.0'
from rpy import r
if sys.version_info[:2] < (2, 3):       #python2.2 or lower needs some extra
        from python2_3 import *


from Scientific import MPI
import sys, cPickle	#10-15-05 cPickle is used to serialize objects
from Numeric import Float, array, Int, zeros

communicator = MPI.world.duplicate()
sys.stdout.write("Re rank: %s, hostname: %s\n"%(communicator.rank, hostname))

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

sys.stdout.flush()
sys.stderr.flush()
communicator.barrier()

if communicator.rank==0:
	for i in range(1, communicator.size):
		ls = [i]*5
		ls_pickle = cPickle.dumps(ls,-1)
		communicator.send(ls_pickle,i,0)
else:
	data, source, tag = communicator.receiveString(0, None)
	ls = cPickle.loads(data)
	print "No.",communicator.rank,"got",ls
