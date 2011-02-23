#!/usr/bin/env python
"""
Parallel Hello World
"""

from mpi4py import MPI
import sys, os

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()
comm = MPI.COMM_WORLD

if rank == 0:
   data = {'a': 7, 'b': 3.14}
   sys.stdout.write(
    "data sending out from 0: %s. process %d of %d on %s.\n" 
    % (data, rank, size, name))
   comm.isend(data, dest=1, tag=11)
elif rank == 1:
   data = comm.recv(source=0, tag=11)
   sys.stdout.write(
    "data received from 0: %s. process %d of %d on %s.\n" 
    % (data, rank, size, name))
   import subprocess
   """
   # 2011-2-21 os.system() always works
   os.system('ls ./ -l')
   os.system('date')
   os.system('sleep 3|cat|cat')
   os.system('date')
   os.system('sleep 3|cat|cat')
   os.system('date')
   """
   # 2011-2-21 Below would only run when "-mca mpi_leave_pinned 1" is set for mpiexec.
   p0 = subprocess.Popen('ls ./', shell=True, stdin=None, stderr=sys.stderr, stdout=sys.stderr)
   #print os.waitpid(p0.pid, 0)[1]
   stdout_content, stderr_content = p0.communicate()
   print stdout_content
   print stderr_content


sys.stdout.write(
    "Hello, World! I am process %d of %d on %s.\n" 
    % (rank, size, name))
