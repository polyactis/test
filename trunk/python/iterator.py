#!/usr/bin/env python

class xml_block_iterator:
	'''looping over a big file, generate xml block'''
	def __init__(self, inf):
		self.inf = inf
		self.xml_block = ''
	def __iter__(self):
		return self		
	def next(self):
		self.read()
		return self.xml_block
	def read(self):
		self.xml_block = ''
		line = self.inf.readline()
		while line.find('</BlastOutput>') !=0:
			if line == '':
				raise StopIteration
				break
			if line.find('<!DOCTYPE')!=0:
				self.xml_block += line
			line = self.inf.readline()
		self.xml_block += line
	
class Reverse:
    "Iterator for looping over a sequence backwards"
    def __init__(self, data):
        self.data = data
        self.index = len(data)
    def __iter__(self):
        return self
    def next(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]

if __name__ == '__main__':
	import sys
	f_hanler = open(sys.argv[1], 'r')
	iter =  xml_block_iterator(f_hanler)
	for block in iter:
		print block
	'''
	block = iter.next()
	while block:
		print block[:10]
		block = iter.next()
	'''
