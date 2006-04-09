#!/usr/bin/env python
"""
Usage:	SimulateIntegral.py

Option:
	-n ...,	number of monte carlo's, 20(default)
	-s ...,	no_of_samplings for each monte carlo, 1e5(default)
	-b,	enable debug flag
	-r,	enable report flag
	-h
	
Examples:


Description:
	Use simulation to solve integrals. \int_{0}^{1}sin(1/x)^2 dx
"""
import sys, os, math, random, getopt, MLab

def plain_simulate(no_of_monte_carlos, no_of_samplings):
	result_ls = []
	for j in range(no_of_monte_carlos):
		result = 0
		for i in range(no_of_samplings):
			x = random.random()
			result += math.sin(1/x)*math.sin(1/x)
		result /= no_of_samplings
		print "%s: %s"%(j, result)
		result_ls.append(result)
	print "mean: %s, std: %s"%(MLab.mean(result_ls), MLab.std(result_ls))

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print __doc__
		sys.exit(2)
		
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hn:s:br", ["help"])
	except:
		print __doc__
		sys.exit(2)
	no_of_monte_carlos = 20
	no_of_samplings = int(1e5)
	debug = 0
	report = 0
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print __doc__
			sys.exit(2)
		elif opt in ("-n",):
			no_of_monte_carlos = int(arg)
		elif opt in ("-s",):
			no_of_samplings = int(arg)
		elif opt in ("-b",):
			debug = 1
		elif opt in ("-r",):
			report = 1
	if no_of_monte_carlos and no_of_samplings:
		plain_simulate(no_of_monte_carlos, no_of_samplings)
	else:
		print __doc__
		sys.exit(2)
