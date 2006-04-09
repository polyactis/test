#!/usr/bin/env python
"""
Usage:	SimulateIntegral.py

Option:
	-n ...,	number of monte carlo's, 20(default)
	-s ...,	no_of_samplings for each monte carlo, 1e5(default)
	-y ...,	type of method, 1(plain MC), 2(control variate)
	-b,	enable debug flag
	-r,	enable report flag
	-h
	
Examples:


Description:
	Use simulation to solve integrals. \int_{0}^{1}sin(1/x)^2 dx
"""
import sys, os, math, random, getopt, MLab

class SimulateIntegral:
	def __init__(self, no_of_monte_carlos=20, no_of_samplings=100000, type=1, debug=0, report=0):
		self.no_of_monte_carlos = no_of_monte_carlos
		self.no_of_samplings = no_of_samplings
		self.type = int(type)
		self.debug = int(debug)
		self.report = int(report)
		
		self.mc_method_dict = {1: self.plain_simulate,
			2: self.control_variate}
		
	def plain_simulate(self, no_of_monte_carlos, no_of_samplings, debug, report):
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
	
	def control_variate(self, no_of_monte_carlos, no_of_samplings, debug, report):
		"""
		04-09-06 use beta(1,1) as a control variate, beta(1,1) and uniform(0,1)
			have same mean, 1/2.
			It turns out to be impossible, the only distribution correlated to uniform is uniform iteself
		"""
		pass
	
	def run(self):
		self.mc_method_dict[self.type](no_of_monte_carlos, no_of_samplings, debug, report)
		
		

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print __doc__
		sys.exit(2)
		
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hn:s:t:br", ["help"])
	except:
		print __doc__
		sys.exit(2)
	no_of_monte_carlos = 20
	no_of_samplings = int(1e5)
	type = 1
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
		elif opt in ("-t",):
			type = int(arg)
		elif opt in ("-b",):
			debug = 1
		elif opt in ("-r",):
			report = 1
	if no_of_monte_carlos and no_of_samplings:
		instance = SimulateIntegral(no_of_monte_carlos, no_of_samplings, type, debug, report)
		instance.run()
	else:
		print __doc__
		sys.exit(2)
