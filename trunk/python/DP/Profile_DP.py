#!/usr/bin/python

from numarray import *
import Numeric

'''
This is an implementation for Math578a hwk's No.4 problem.
The difference from the normal profile multiple alignment is:
1. profile initation based on two closest sequences
2. profile will grow step by step
'''

class Profile_DP:
	def __init__(self):
		#self.seqs = arg1
		self.aligned_seqs = Numeric.sarray(['attgccatt','atggccatt'])
		self.match = 2
		self.mismatch = -1
		self.indel = -2
		self.MultipleAlign_score = 0
		self.a_string1 = []
		self.a_string2 = []
		
	def score_matrix_init(self, matrix):
		for i in range(1, matrix.shape[0]):
			matrix[i,0] = i * self.indel
		for i in range(1, matrix.shape[1]):
			matrix[0,i] = i * self.indel

	def trace_matrix_init(self, matrix):
		for i in range(1, matrix.shape[0]):
			matrix[i,0] = 1
		for i in range(1, matrix.shape[1]):
			matrix[0,i] = -1

	def build_profile(self):
		NoPositions = self.aligned_seqs.shape[1]
		NoSeqs = self.aligned_seqs.shape[0]
		self.profile = zeros( (5,NoPositions) , type = Float32)

		for i in range(NoPositions):
			Noofa = float(0)
			Nooft = float(0)
			Noofc = float(0)
			Noofg = float(0)
			Noof_ = float(0)
			for j in range(NoSeqs):
				if self.aligned_seqs[j,i].tostring().lower() == 'a':
					Noofa = Noofa + 1
				if self.aligned_seqs[j,i].tostring().lower() == 't':
					Nooft = Nooft + 1
				if self.aligned_seqs[j,i].tostring().lower() == 'c':
					Noofc = Noofc + 1
				if self.aligned_seqs[j,i].tostring().lower() == 'g':
					Noofg = Noofg + 1
				if self.aligned_seqs[j,i].tostring().lower() == '-':
					Noof_ = Noof_ + 1
					
			self.profile[0,i] = Noofa / NoSeqs
			self.profile[1,i] = Nooft / NoSeqs
			self.profile[2,i] = Noofc / NoSeqs
			self.profile[3,i] = Noofg / NoSeqs
			self.profile[4,i] = Noof_ / NoSeqs


	def SumOfPairs(self):
		self.MultipleAlign_score = 0
		NoSeqs = self.aligned_seqs.shape[0]
		NoPositions = self.aligned_seqs.shape[1]
		for i in range( NoSeqs):
			for j in range(i+1, NoSeqs):
				seq1 = self.aligned_seqs[i]
				seq2 = self.aligned_seqs[j]
				for k in range(NoPositions):
					self.MultipleAlign_score = self.MultipleAlign_score + self.distance(seq1[k],seq2[k])
				
	def profile_distance(self, p ,s):
		return p[0]*self.distance('a',s) + p[1]* self.distance('t',s) + p[2]* self.distance('c', s) + p[3]*self.distance('g',s) + p[4]*self.distance('-',s)
		
	def distance(self, a, b):
		if a == '-' and b == '-':
			return 0
		if a == '-' or b == '-':
			return self.indel
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
			self.a_string1.append(self.aligned_seqs[:,i-1].tostring())
			self.a_string2.append(self.seq[j-1])
		if self.trace_matrix[i,j] == 1:
			self.trace(i-1,j)
			self.a_string1.append(self.aligned_seqs[:,i-1].tostring())
			self.a_string2.append('-')
		if self.trace_matrix[i,j] == -1:
			self.trace(i,j-1)
			self.a_string1.append('-')
			self.a_string2.append(self.seq[j-1])
	
	def profile_score(self, seq):
		self.seq = seq
		self.score_matrix = zeros((self.profile.shape[1]+1,len(seq)+1))
		self.score_matrix_init(self.score_matrix)
		self.trace_matrix = zeros((self.profile.shape[1]+1,len(seq)+1))
		self.trace_matrix_init(self.trace_matrix)
		
		for i in range(1, self.score_matrix.shape[0]):
			for j in range(1, self.score_matrix.shape[1]):
				m_array = array([self.score_matrix[i-1, j-1] + self.profile_distance(self.profile[:,i-1], self.seq[j-1]),
													self.score_matrix[i-1, j] + self.indel,
													self.score_matrix[i, j-1] + self.indel])
				self.score_matrix[i][j] = m_array.max()
				index_max = m_array.argmax()
				if index_max ==2 :
					self.trace_matrix[i][j] = -1
				else:
					self.trace_matrix[i][j] = index_max
					
		self.a_string1 = []
		self.a_string2 = []
		self.trace(self.trace_matrix.shape[0]-1, self.trace_matrix.shape[1]-1)
		return self.score_matrix


def batch(instance, seq):
	instance.build_profile()
	instance.profile_score(seq)
	print instance.profile
	print instance.score_matrix
	print instance.trace_matrix
	print instance.a_string1
	print instance.a_string2

if __name__ == '__main__':
	import sys
	instance = Profile_DP()
	instance.build_profile()
	instance.profile_score('atcttctt')
	instance.SumOfPairs()
	
	print instance.profile
	print instance.score_matrix
	print instance.trace_matrix
	print instance.a_string1
	print instance.a_string2
	print instance.MultipleAlign_score
