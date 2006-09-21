#!/usr/bin/env python
""""
Usage: MC_test.py -y TestCaseType [OPTIONS]

Option:
	-y ..., --type=...	which test case should be invoked.
	-h, --help              show this help

Examples:
	MC_test.py -y 2

06-14-06
	Problems from Monte Carlo Statiscal Methods, 2nd Edition, Christian Robert, George Casella
1: Problem2_2
2: Problem2_3
3: Problem3_3
4: Problem3_15
"""
import sys, os, math
bit_number = math.log(sys.maxint)/math.log(2)
if bit_number>40:       #64bit
	sys.path.insert(0, os.path.expanduser('~/lib64/python'))
	sys.path.insert(0, os.path.join(os.path.expanduser('~/script64/annot/bin')))
else:   #32bit
	sys.path.insert(0, os.path.expanduser('~/lib/python'))
	sys.path.insert(0, os.path.join(os.path.expanduser('~/script/annot/bin')))
import unittest, os, sys, getopt, csv

class Problem2_2(unittest.TestCase):
	def test_GenerateBinomial(self, no_of_samples=10000, size=25, prob=0.2):
		import rpy, random, pylab
		#generate the list of prob(X<=x)
		cdf_list = []
		for i in range(size+1):
			mass_prob = rpy.r.choose(size, i)*math.pow(prob, i)*math.pow((1-prob), size-i)
			if len(cdf_list)==0:
				cdf_list.append(mass_prob)
			else:
				cumulative_prob = mass_prob + cdf_list[-1]
				cdf_list.append(cumulative_prob)
		#start the sampling
		sample_list = []
		for i in range(no_of_samples):
			u = random.random()
			for j in range(size+1):
				if cdf_list[j]>u:
					break
			sample_list.append(j)
		
		pylab.hist(sample_list, 26)
		pylab.title("binomial generator via inverse")
		pylab.show()
		
		sample_list = rpy.r.rbinom(no_of_samples, size, prob)
		pylab.hist(sample_list, 26)
		pylab.title("R binomial generator")
		pylab.show()
	
	def test_DrawMassFunction(self, size=25, prob=0.2):
		import rpy, pylab
		cdf_list = []
		for i in range(size+1):
			mass_prob = rpy.r.choose(size, i)*math.pow(prob, i)*math.pow((1-prob), size-i)
			cdf_list.append(mass_prob)
		pylab.plot(cdf_list, 'o-')
		pylab.show()

class Problem2_3(unittest.TestCase):
	def test_NormalByCauchyAcceptReject(self, no_of_samples=10000):
		import rpy, math, random, pylab
		sample_list = []
		M = math.pi/(math.sqrt(2*math.pi)) +0.1 #"+0.1" makes it a little bit less efficient, but keeps the density around 0 normal
		for i in range(no_of_samples):
			cauchy_sample = rpy.r.rcauchy(1)
			u = random.random()
			normal_mass = rpy.r.dnorm(cauchy_sample)
			cauchy_mass = 1/(math.pi*(1+cauchy_sample*cauchy_sample))
			if u<= normal_mass/(M*cauchy_mass):
				sample_list.append(cauchy_sample)
		accept_ratio = len(sample_list)/float(no_of_samples)
		print "accept ratio is %s"%(accept_ratio)
		n, bins, patches = pylab.hist(sample_list, 100, normed=1)
		pylab.title("Normal via cauchy, accept_ratio:%s"%accept_ratio)
		y = pylab.normpdf( bins, 0, 1)
		l = pylab.plot(bins, y, 'ro-', linewidth=2)
		pylab.show()

class Problem3_3(unittest.TestCase):
	"""
	2006-09-13
	2006-09-20 change no_of_samples from 10e7 to 1e7
	"""
	def test_pro3_3_part_a(self, no_of_samples=1e7):
		print
		t_value = 2.5
		print "Get normal probability P(Z>%s) via Monte Carlo sums"%t_value
		import rpy
		print 'P(x>%s) from R is %s'%(t_value, rpy.r.pnorm(t_value, lower_tail=rpy.r.FALSE))
		import random, sys
		cum_sum = 0.0
		i = 0
		prev_no_of_simulations = 1
		while i <no_of_samples:
			random_gauss = random.gauss(0,1)
			cum_sum += int(random_gauss>t_value)
			i += 1
			if i/float(prev_no_of_simulations)==10:
				prev_no_of_simulations = i
				print i, cum_sum/i

class Problem3_15(unittest.TestCase):
	"""
	2006-09-20
		importance sampling with exponential distribution
	"""
	def test_pro3_15(self, no_of_samples=1e7):
		print
		t_value = 2.5
		print "Importance sampling of normal probability P(Z>%s) via exponential distribution"%t_value
		import rpy
		print 'P(x>%s) from R is %s'%(t_value, rpy.r.pnorm(t_value, lower_tail=rpy.r.FALSE))
		import random, sys, math
		cum_sum = 0.0
		i = 0
		prev_no_of_simulations = 1
		lmbd =1	#10 is bad, 1 and 0.1 is ok.
		while i <no_of_samples:
			random_exp = random.expovariate(lmbd)
			cum_sum += int(random_exp>t_value)/(lmbd*math.sqrt(2*math.pi))*math.exp(-random_exp*random_exp/2 + lmbd*random_exp)	#simplify the ratio by one exp()
			i += 1
			if i/float(prev_no_of_simulations)==10:
				prev_no_of_simulations = i
				print i, cum_sum/i

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print __doc__
		sys.exit(2)
	
	long_options_list = ["help", "type="]
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hy:", long_options_list)
	except:
		print __doc__
		sys.exit(2)
	
	TestCaseDict = {1:Problem2_2,
		2:Problem2_3,
		3:Problem3_3,
		4:Problem3_15}
	type = 0
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print __doc__
			sys.exit(2)
		elif opt in ("-y", "--type"):
			type = int(arg)
			
	if type:
		suite = unittest.TestSuite()
		"""
		add one by one
		"""
		#suite.addTest(TestGeneStatPlot("test_return_distinct_functions"))
		#suite.addTest(TestGeneStatPlot("test_L1_match"))
		#suite.addTest(TestGeneStat("test__gene_stat_leave_one_out"))
		#suite.addTest(TestGeneStat("test_submit"))
		#suite.addTest(TestGeneStat("test_common_ancestor_deep_enough"))
		"""
		add all
		"""
		suite.addTest(unittest.makeSuite(TestCaseDict[type]))
		unittest.TextTestRunner(verbosity=2).run(suite)

	else:
		print __doc__
		sys.exit(2)
