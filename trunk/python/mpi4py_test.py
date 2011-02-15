#!/usr/bin/env python
"""
Parallel Hello World
"""

from mpi4py import MPI
import sys

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


sys.stdout.write(
    "Hello, World! I am process %d of %d on %s.\n" 
    % (rank, size, name))
