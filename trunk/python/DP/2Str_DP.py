#!/usr/bin/python

from numarray import *

class DP:
	'''
	Dynamic Programming algorithm: given 2 strings, get the optimal alignment.
	
	'''
	def __init__(self, arg1, arg2):
		self.string1 =  arg1
		self.string2 = arg2
		self.a_string1 = []
		self.a_string2 = []
		self.match = 2
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
		
		
if __name__ == '__main__':
	import sys
	instance = DP(sys.argv[1], sys.argv[2])
	instance.score()
	print instance.score_matrix
	print instance.trace_matrix
	print ''.join(instance.a_string1)
	print ''.join(instance.a_string2)
