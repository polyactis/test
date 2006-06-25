#!/usr/bin/env python
"""
Usage: find_conserved_elements.py [OPTIONS] -o OUTPUT_FILE INPUT_FILES

Option:
	-o ...	OUTPUT_FILE
	-s ...	minimum number of species (4, default)
	-l ...	minimum length of the multiple alignment (20, default)
	-z,	input files are gzipped
	-b, --debug	just test running the program, no daytime restriction
	-r, --report	report the progress (time before each query)
	-h, --help	show this help

Examples:
	find_conserved_elements.py -o output -l 15 -z yh/*

Description:
	program to parse UCSC MAF(multiple alignment format) files and
	get the conserved(identity) segments
	
"""

import sys, getopt, os, csv, copy, gzip

class alignment_block_iterator:
	'''
	06-23-06
		alignment block iterator
	'''
	def __init__(self, inf):
		self.inf = inf
		self.block = []
		self.previous_line = ''
	def __iter__(self):
		return self
	def next(self):
		self.read()
		return self.block
	def read(self):
		self.block = []
		for line in self.inf:
			if line[0]=='a':
				self.previous_line = line
				if self.block:	#not the first time
					break
			elif line[0]=='s':
				self.block.append( line.split())
		if self.block == []:
			raise StopIteration

class find_conserved_elements:
	def __init__(self, input_files, output_fname, min_number_species, min_length, gzipped=0, debug=0, report=0):
		self.input_files = input_files
		self.output_fname = output_fname
		self.min_number_species = int(min_number_species)
		self.min_length = int(min_length)
		self.gzipped = int(gzipped)
		self.debug = int(debug)
		self.report = int(report)
	
	def parse_one_block(self, block, conserve_param2hits, min_number_species, min_length):
		"""
		06-24-06
			each element in block is like this
			
			['s', 'hg18.chr1', '1325', '29', '+', '247249719', 'GATTATAGGGAAACACCCGGA------------Gcatatgc']
		"""
		min_alignment_length = 0
		align_info_list = []
		seq_list = []
		number_of_species = len(block)
		if self.debug:
			print block
			print "number_of_species:", number_of_species
		
		if number_of_species <=min_number_species:
			return
		
		for alignment_info in block:
			alignment_size = int(alignment_info[3])
			if min_alignment_length==0:
				min_alignment_length= int(alignment_info[3])
			elif alignment_size<min_alignment_length:
				min_alignment_length=alignment_size
			if min_alignment_length<min_length:	#no need to continue analysis
				return
			align_info_list.append([alignment_info[1], int(alignment_info[2]), alignment_info[4]])	#seq location, starting, strand
			seq_list.append(alignment_info[6])
		
		alignment_length = len(seq_list[0])
		identity_length = 0
		
		for i in range(alignment_length):
			column_char = seq_list[0][i]
			is_column_identity = 1	#assume the column is identity
			if self.debug:
				print "%s column_char: %s"%(i, column_char)
			#go through all rows to see if it's identity
			for j in range(number_of_species):
				if self.debug:
					print "(%s,%s) char is %s"%(j, i, seq_list[j][i])
				if seq_list[j][i] != column_char:
					is_column_identity = 0
					if self.debug:
						print "not equal"
				if seq_list[j][i] == '-':
					is_column_identity = 0
					if self.debug:
						print "it's -"
				else:
					align_info_list[j][1] += 1	#advance one step
					if self.debug:
						print "not - advance"
			#based on whether it's identity, do more
			if is_column_identity==1:
				identity_length += 1
				if self.debug:
					print "column identity, identity_length:%s"%(identity_length)
			else:	#this column is not identity, reset the identity_length
				if identity_length>=min_length:
					align_info_list_copy = copy.deepcopy(align_info_list)
					for j in range(number_of_species):
						align_info_list_copy[j][1] -= identity_length	#No -1, because the starting in align_info_list_copy is pointing to the current non-identity
					key_pair = (number_of_species, identity_length)
					if self.debug:
						print "key_pair:", key_pair
						print "align_info_list_copy", align_info_list_copy
					if key_pair not in conserve_param2hits:
						conserve_param2hits[key_pair] = []
					conserve_param2hits[key_pair].append(align_info_list_copy)
				#finally, set identity to length 0
				identity_length = 0
			"""
			if self.debug:
				is_continue =raw_input("continue?(Y/n)")
				if is_continue == 'n':
					break
			"""
	
	def run(self):
		conserve_param2hits = {}
		sys.stderr.write("\tTotally, %d files to be processed.\n"%len(self.input_files))
		for fname in self.input_files:
			sys.stderr.write("%d/%d:\t%s\n"%(self.input_files.index(fname)+1,len(self.input_files), os.path.basename(fname)))
			if self.gzipped:
				inf = gzip.open(fname, 'r')
			else:
				inf = open(fname)
			iter = alignment_block_iterator(inf)
			for block in iter:
				self.parse_one_block(block, conserve_param2hits, self.min_number_species, self.min_length)
			del inf, iter
		
		writer   = csv.writer(open(self.output_fname, 'w'), delimiter='\t')
		for (key, value) in conserve_param2hits.iteritems():
			writer.writerow(list(key)+value)
		del writer

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print __doc__
		sys.exit(2)
	
	long_options_list = []
	try:
		opts, args = getopt.getopt(sys.argv[1:], "o:s:l:zbrh", long_options_list)
	except:
		print __doc__
		sys.exit(2)
	
	output_fname = None
	min_number_species = 4
	min_length = 20
	gzipped = 0
	debug = 0
	report = 0
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print __doc__
			sys.exit(2)
		elif opt in ("-z",):
			gzipped = 1
		elif opt in ("-o",):
			output_fname = arg
		elif opt in ("-s",):
			min_number_species = int(arg)
		elif opt in ("-l",):
			min_length = int(arg)
		elif opt in ("-b", "--debug"):
			debug = 1
		elif opt in ("-r", "--report"):
			report = 1
	
	if len(args)>0 and output_fname:
		instance = find_conserved_elements(args, output_fname, min_number_species, min_length, gzipped, debug, report)
		instance.run()
	else:
		print __doc__
		sys.exit(2)
