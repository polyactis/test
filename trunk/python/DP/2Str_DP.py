#!/usr/bin/env python
"""
Usage: 2Str_DP.py [OPTIONS] Str1 Str2

Option:
	-o ...	OUTPUT_FILE
	-b, --debug	just test running the program, no daytime restriction
	-r, --report	report the progress (time before each query)
	-h, --help	show this help

Examples:
	2Str_DP.py GCATG GCATG

Description:
	Alignment of Str1 and Str2 through dynamic alignment.
	Get the polytope through exhaustive search.
	
"""

import sys, getopt, os
from numpy import *

class DP:
	'''
	Dynamic Programming algorithm: given 2 strings, get the optimal alignment.
	
	'''
	def __init__(self, arg1, arg2):
		self.string1 =  arg1
		self.string2 = arg2
		self.a_string1 = []
		self.a_string2 = []
		self.match = 1
		self.mismatch = -1
		self.indel = -2
		self.score_matrix = zeros((len(self.string1)+1,len(self.string2)+1))
		for i in range(1, self.score_matrix.shape[0]):
			self.score_matrix[i,0] = i * self.indel
		for i in range(1, self.score_matrix.shape[1]):
			self.score_matrix[0,i] = i * self.indel
		
		self.trace_matrix = zeros((len(self.string1)+1,len(self.string2)+1))
		for i in range(1, self.trace_matrix.shape[0]):
			self.trace_matrix[i,0] = 1
		for i in range(1, self.trace_matrix.shape[1]):
			self.trace_matrix[0,i] = -1

	def distance(self, a, b):
		if a.upper() == b.upper():
			return self.match
		else:
			return self.mismatch
	
	def trace(self, i, j):
		"""
		06-23-06
			-1 means from left, 1 means from up, 0 means from triangle
		"""
		if i < 0 or j < 0:
			return
		if i == 0 and j == 0 :
			return
		if self.trace_matrix[i,j] == 0:
			self.trace(i-1,j-1)
			self.a_string1.append(self.string1[i-1])
			self.a_string2.append(self.string2[j-1])
		if self.trace_matrix[i,j] == 1:
			self.trace(i-1,j)
			self.a_string1.append(self.string1[i-1])
			self.a_string2.append('-')
		if self.trace_matrix[i,j] == -1:
			self.trace(i,j-1)
			self.a_string1.append('-')
			self.a_string2.append(self.string2[j-1])
	
	def score(self):
		for i in range(1, self.score_matrix.shape[0]):
			for j in range(1, self.score_matrix.shape[1]):
				m_array = array([self.score_matrix[i-1, j-1] + self.distance(self.string1[i-1], self.string2[j-1]),
													self.score_matrix[i-1, j] + self.indel,
													self.score_matrix[i, j-1] + self.indel])
				self.score_matrix[i][j] = m_array.max()
				index_max = m_array.argmax()
				if index_max ==2 :
					self.trace_matrix[i][j] = -1
				else:
					self.trace_matrix[i][j] = index_max

		self.trace(self.trace_matrix.shape[0]-1, self.trace_matrix.shape[1]-1)
		return self.score_matrix
		
		
class calculate_polytope:
	def __init__(self, string1, string2, debug, report):
		self.string1 = string1
		self.string2 = string2
		self.debug = int(debug)
		self.report = int(report)
		
		#06-23-06, this is counts, not parameter score
		self.match = 0
		self.mismatch = 0
		self.indel = 0
		
		self.trace_matrix = zeros((len(self.string1)+1, len(self.string2)+1))
		for i in range(1, self.trace_matrix.shape[0]):
			self.trace_matrix[i,0] = 1
		for i in range(1, self.trace_matrix.shape[1]):
			self.trace_matrix[0,i] = -1
			
		self.summary2counts = {}
	
	def trace(self, i, j):
		"""
		06-23-06
			-1 means from left, 1 means from up, 0 means from triangle
		"""
		if self.debug:
			print "trace:", i, j
		if i < 0 or j < 0:
			return
		if i == 0 and j == 0 :
			return
		if self.trace_matrix[i,j] == 0:
			if self.debug:
				print "mismatch or match"
			if self.string1[i-1].upper() == self.string2[j-1].upper():
				self.match += 1
			else:
				self.mismatch += 1
			self.trace(i-1,j-1)
		elif self.trace_matrix[i,j] == 1:
			if self.debug:
				print "space 1"
			self.trace(i-1,j)
			self.indel+=1
		elif self.trace_matrix[i,j] == -1:
			if self.debug:
				print "space -1"
			self.trace(i,j-1)
			self.indel+=1
	
	def construct_candidate_directions(self, coord, len1, len2):
		if coord[0] == len1:
			candidate_directions = [(0,1)]
		elif coord[1] == len2:
			candidate_directions = [(1,0)]
		else:
			candidate_directions = [(0,1), (1,0), (1,1)]
		return candidate_directions
	
	def _calculate_polytope(self, coord_list, k, len1, len2):
		if self.debug:
			print "k:", k
		coord_row = 0
		coord_column = 0
		for i in range(k+1):	#from 0 to k
			coord_row += coord_list[i][0]
			coord_column += coord_list[i][1]
		
		if self.debug:
			print "coord_list:", coord_list
			print "coord:", coord_row, coord_column
		if coord_row ==5 and coord_column==5:
			#clear counts first
			self.match = 0
			self.mismatch = 0
			self.indel = 0
			self.trace(len1, len2)
			summary_triple = (self.match, self.mismatch, self.indel)
			if self.debug:
				print "summary_triple",summary_triple
			if summary_triple not in self.summary2counts:
				self.summary2counts[summary_triple] = 0
			self.summary2counts[summary_triple] += 1
		else:
			k += 1
			if self.debug:
				print "new k:", k
			candidate_directions = self.construct_candidate_directions((coord_row, coord_column), len1, len2)
			for candidate_direction in candidate_directions:
				coord_list[k] = candidate_direction
				coord = (coord_row +candidate_direction[0], coord_column +  candidate_direction[1])
				if self.debug:
					print "new coord:", coord
				if candidate_direction==(0,1):
					self.trace_matrix[coord[0], coord[1]] = -1
				elif candidate_direction == (1,0):
					self.trace_matrix[coord[0], coord[1]] = 1
				else:
					self.trace_matrix[coord[0], coord[1]] = 0
				if self.debug:
					print "trace_matrix:"
					print self.trace_matrix
				self._calculate_polytope(coord_list, k, len1, len2)
	
	def run(self):
		coord_list = [(0, 0)]*(len(self.string1)+len(self.string2)+1)
		k = 0
		self._calculate_polytope(coord_list, k, len(self.string1), len(self.string2))
		match_list = []
		mismatch_list = []
		indel_list = []
		for summary_triple in self.summary2counts:
			match_list.append(summary_triple[0])
			mismatch_list.append(summary_triple[1])
			indel_list.append(summary_triple[2])
			print summary_triple, self.summary2counts[summary_triple]
		print match_list
		print mismatch_list
		print indel_list
		print "total routes:", sum(self.summary2counts.values())



if __name__ == '__main__':
	if len(sys.argv) == 1:
		print __doc__
		sys.exit(2)
	
	long_options_list = []
	try:
		opts, args = getopt.getopt(sys.argv[1:], "o:brh", long_options_list)
	except:
		print __doc__
		sys.exit(2)
	
	output_fname = None
	debug = 0
	report = 0
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print __doc__
			sys.exit(2)
		elif opt in ("-o",):
			output_fname = arg
		elif opt in ("-b", "--debug"):
			debug = 1
		elif opt in ("-r", "--report"):
			report = 1
	
	if len(args)>0:
		instance = DP(args[0], args[1])
		instance.score()
		print instance.score_matrix
		print instance.trace_matrix
		print ''.join(instance.a_string1)
		print ''.join(instance.a_string2)

		instance = calculate_polytope(args[0], args[1], debug, report)
		instance.run()

	else:
		print __doc__
		sys.exit(2)
