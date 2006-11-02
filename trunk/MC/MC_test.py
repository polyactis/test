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
5: Problem5_1
6: Problem5_5
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

class Problem5_1 (unittest.TestCase):
	"""
	2006-10-31
		basic
		simulated anealing
		
		R code to get the maximum:
		f = function(x) { (cos(50*x)+sin(20*x))^2}
		optimize( f, l=0, u = 1, maximum=TRUE)
			or
		optim(0, f, l=0, u=1, control=list(fnscale=-100)
		
		The answer is x=0.379125, max(f)= 3.832543
	"""
	def setUp(self):
		print
		print "stochastic exploration to get maximum of (cos(50x)+sin(20x))^2"
		
	def test_basic(self, no_of_samples=1e6):
		import random, math
		f = -10	#initial value
		i = 0
		x_where_maxi_f = 0
		while i< no_of_samples:
			x = random.random()
			new_f = math.pow((math.cos(50*x)+math.sin(20*x)), 2)
			if new_f>f:
				f = new_f
				x_where_maxi_f = x
			i+=1
		print "x=%s, max(f)=%s"%(x_where_maxi_f, f)
	
	def f_function(self, x):
		return math.pow((math.cos(50*x)+math.sin(20*x)), 2)
	
	def test_simulated_annealing(self, neighbor_range = 0.25, no_of_samples=1e6):
		import matplotlib; matplotlib.use("Agg")
		import random, math, pylab
		t = 2
		x_where_maxi_f = 0	#initial x
		x_list = [x_where_maxi_f]
		f_list = [self.f_function(x_where_maxi_f)]
		while t< no_of_samples:
			u = random.uniform(max(x_where_maxi_f - neighbor_range, 0), min(x_where_maxi_f + neighbor_range, 1))
			t_i = 0.01/math.log(t)
			prob = min(math.exp( ( self.f_function(u) - self.f_function(x_where_maxi_f) )/t_i ), 1)
			random_prob = random.random()
			if random_prob<=prob:
				x_where_maxi_f = u
				x_list.append(x_where_maxi_f)
				f_list.append(self.f_function(x_where_maxi_f))
			
			t += 1
		max_f = self.f_function(x_where_maxi_f)
		print "x=%s, max(f)=%s"%(x_where_maxi_f, max_f)
		pylab.xlabel('Exploration')
		pylab.ylabel('Function value')
		pylab.plot(x_list, f_list, '-o')
		pylab.savefig('prob5_1_simulated_annealing.png')
		#pylab.show()

class Problem5_5(unittest.TestCase):
	"""
	2006-11-01
	
	Interesting model, it seems it either reaches full +1 or -1 matrix.
	"""
	def setUp(self):
		print
		print "simulated annealing for Ising model"
	
	def pick_one_node(self, grid_length = 10):
		import random
		return (random.randint(0, grid_length-1), random.randint(0, grid_length-1))
	
	def cal_neighbor_score(self, node_pos , sign_matrix, grid_length):		
		score = 0.0
		if node_pos[0]-1 >= 0:
			score += sign_matrix[node_pos[0]-1, node_pos[1]]
		if node_pos[0]+1 <= grid_length-1:
			score += sign_matrix[ node_pos[0]+1, node_pos[1]]
		if node_pos[1]-1 >= 0:
			score += sign_matrix[node_pos[0], node_pos[1]-1]
		if node_pos[1]+1 <= grid_length-1:
			score += sign_matrix[ node_pos[0], node_pos[1]+1]
		return score
	
	def cal_matrix_score(self, sign_matrix, grid_length):
		"""
		2006-11-02
			the calculation is (one-horizontal row, one-vertical row), alternating, total
			so, horizontal is n-1 edges with n rows; vertical is n edges with n-1 times
		"""
		matrix_score = 0.0
		for i in range(grid_length-1):	#the first horizontal row
			matrix_score += sign_matrix[0, i]*sign_matrix[0, i+1]
		for i in range(1, grid_length):
			matrix_score += sign_matrix[i-1, 0]*sign_matrix[i, 0]	#the first vertical edge
			for j in range(grid_length-1):
				matrix_score += sign_matrix[i, j]* sign_matrix[i, j+1]
				matrix_score += sign_matrix[i-1, j+1]*sign_matrix[i, j+1]
		return matrix_score
		
	def modify_matrix_score(self, sign_matrix, node_pos, grid_length):
		"""
		2006-11-02
			it's assumed, sign of node_pos is reversed.
			The calculation is a lot simplification.
				each edge score diff = new_sign*neighbor - old_sign*neighbor = -2*old_sign* neighbor
				total score diff = -2 * old_sign * (\sigma neighbors)
		"""
		delta_score = 0.0	#the new score of four edges -  the old score
		if node_pos[0]-1 >= 0:
			delta_score += sign_matrix[node_pos[0]-1, node_pos[1]]
		if node_pos[0]+1 <= grid_length-1:
			delta_score += sign_matrix[ node_pos[0]+1, node_pos[1]]
		if node_pos[1]-1 >= 0:
			delta_score += sign_matrix[node_pos[0], node_pos[1]-1]
		if node_pos[1]+1 <= grid_length-1:
			delta_score += sign_matrix[ node_pos[0], node_pos[1]+1]
		delta_score = -2*sign_matrix[ node_pos]*delta_score
		return delta_score
	
	def test_Ising_model(self, no_of_samples=1e5, grid_length = 10, beta=0.4):
		import matplotlib; matplotlib.use("Agg")
		import Numeric, random, math, pylab
		#sign_matrix = Numeric.ones(( grid_length, grid_length ))
		sign_matrix = Numeric.array( [[-1,-1,-1,-1,-1,-1,-1,-1,-1,1,],
			 [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,],
			 [-1,1,-1,-1,1,-1,-1,-1,1,-1,],
			 [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,],
			 [-1,-1,-1,1,-1,-1,-1,-1,-1,-1,],
			 [-1,-1,-1,1,-1,-1,-1,-1,-1,-1,],
			 [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,],
			 [-1,-1,-1,1,1,1,-1,-1,-1,-1,],
			 [1,-1,-1,-1,-1,-1,1,-1,-1,-1,],
			 [-1,1,-1,-1,-1,-1,-1,-1,-1,1,]])
		matrix_score = beta * self.cal_matrix_score(sign_matrix, grid_length)
		score_list = [ matrix_score]
		t = 2
		while t< no_of_samples:
			t_i = 1/math.log(t)
			picked_node = self.pick_one_node(grid_length)
			old_sign  = sign_matrix[ picked_node]
			
			score = 2*beta*self.cal_neighbor_score(picked_node, sign_matrix, grid_length)
			exp_score = math.exp(score)
			
			bernoulli_prob = exp_score/(1 + exp_score)
			random_prob = random.random()
			if random_prob<= bernoulli_prob:
				new_sign = 1
			else:
				new_sign = -1
			if new_sign != old_sign:
				delta_score = beta*self.modify_matrix_score(sign_matrix, picked_node, grid_length)
				annealing_prob = min(math.exp( delta_score/t_i ), 1)
				random_prob = random.random()
				if random_prob <= annealing_prob:
					sign_matrix[ picked_node] = new_sign	#changed after delta_score is got					
					matrix_score = matrix_score + delta_score
					score_list.append( matrix_score)
			t += 1
		print "matrix_score:", matrix_score
		print "matrix:"
		print sign_matrix
		pylab.xlabel('Iterations')
		pylab.ylabel('matrix score')
		pylab.plot(range(len(score_list)) , score_list, '-o')
		pylab.savefig('prob5_5_ising_model_score.png')
					
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
		4:Problem3_15,
		5: Problem5_1 ,
		6: Problem5_5}
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
