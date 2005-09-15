#!/usr/bin/env python
"""
04-27-05
	miscellaneous functions used in python's interactive mode
"""
import psycopg, sys
from sets import Set

from Numeric import array,transpose
import csv

def take_list(source_list,index_list):
	"""
	04-27-05
		functions like Numeric.take, but work on list
	"""
	new_list = []
	for i in index_list:
		new_list.append(source_list[i])
	return new_list

def return_seed_array(curs, edge_id_list, col_index_list):
	"""
	04-27-05
		return the edge correlation matrix
	"""
	cor_2d_list, sig_2d_list = get_edge_vector_by_id(curs, edge_id_list)
	cor_2d_array = Numeric.array(cor_2d_list)
	seed_array = Numeric.take(cor_2d_array, col_index_list,1)
	return seed_array
	return new_list

def return_seed_array2(curs, edge_id_list, col_index_list):
	"""
	04-27-05
		return the edge significance-flag matrix
	"""
	cor_2d_list, sig_2d_list = get_edge_vector_by_id(curs, edge_id_list)
	cor_2d_array = Numeric.array(sig_2d_list)
	seed_array = Numeric.take(cor_2d_array, col_index_list,1)
	return seed_array

#04-27-05	the 54 dataset description
dataset_description = ['rosetta_mcb','rosetta_science','2,3,8,3 perception of external stimulus','2,4,3,1 cell cycle control',\
'2,4,6,2,3 organelle organization and biogenesis','2,4,6,3,2 cell wall organization and biogenesis',\
'2,4,6,5,2,2,2,2,1 chromatin modeling','2,4,11,4 ion homeostasis','2,4,13,11,49,6 protein biosynthesis',\
'2,4,13,14,57,5 protein degradation','2,4,13,23,14 steroid metabolism',\
'2,4,13,26 nucleobase, nucleoside, nucleotide and nucleic acid metabolism',\
'2,4,13,31,2,13 protein amino acid phosphorylation','2,4,13,33 protein metabolism and modification',\
'2,4,16,23 protein transport','2,6,10,2,1,3 pseudohyphal growth','ume6-deleted diploids','ume6-deleted diploids',\
'ume6-deleted diploids','ume6-deleted diploids','chitin synthesis in wildtype BY4741 and mutant fks1',\
'Wild type and sgs1 null yeast,DNA damaging agent methyl methanesulfonate (MMS)','Cell-cycle,Alpha factor block-release',\
'Drug_treatment,Diamide','Metals, Zinc','Mutants, YPD-stationary-phase','Mutants, heat shock','Mutants, osmotic',\
'ORF-INT Enrichment, Chromatin distribution','Phosphate, Nutrient limitation','Cell-cycle, Elutriation',\
'RNA coimmunoprecipitation, Identify Target Genes','RNA coimmunoprecipitation, RNA localization',\
'Sporulation, Transcription Factors','Starvation, YPD-stationary-phase','Stress, H2O2','Stress, Heat steady',\
'Stress, Heat-shock','Stress, Heat-shock','Stress, MD','Cell-cycle, Forkheads','tress, Nitrogen-starvation',\
'Transcript size, RNA','Transcription, Cell-cycle factors','Transcription, swi_snf','calcium, Time course',\
'evolution, DNA','salt treatment, Time course','Cell-cycle, cdc15','Chemical effects, DTT','Chromatin IP, Cell-cycle factors',\
'Chromatin IP, SIR Proteins','DNA damage, Gamma radiation','DNA damage, MMS']


def transposed_matrix(filename):
	"""
	04-29-05
	"""
	list_2d = []
	reader = csv.reader(open(filename,'r'),delimiter='\t')
	reader.next()	#ignore the first line
	for row in reader:
		ls = []
		for item in row:
			if item=='NA':
				ls.append(1.1)
			else:
				ls.append(float(item))
		
		list_2d.append(ls)
	matrix = array(list_2d)
	m1 = transpose(matrix)
	return m1

def output_transposed_matrix(filename, m1):
	"""
	04-29-05
	"""
	writer = csv.writer(open(filename,'w'),delimiter='\t')
	for i in range(m1.shape[0]):
		ls = [i]
		for item in m1[i]:
			if item==1.1:
				ls.append('NA')
			else:
				ls.append(item)
		writer.writerow(ls)
	del writer


def db_connect(hostname, dbname, schema=None):
	"""
	02-28-05
		establish database connection, return (conn, curs).
		copied from CrackSplat.py
	03-08-05
		parameter schema is optional
	"""
	import psycopg
	conn = psycopg.connect('host=%s dbname=%s'%(hostname, dbname))
	curs = conn.cursor()
	if schema:
		curs.execute("set search_path to %s"%schema)
	return (conn, curs)

def get_gene_no2go_no(curs, schema=None, gene_table='gene'):
	"""
	03-09-05
		get the gene_no2go_no
	"""
	sys.stderr.write("Getting gene_no2go_no...")
	if schema:
		curs.execute("set search_path to %s"%schema)
	
	gene_no2go_no = {}
	
	curs.execute("select gene_no,go_functions from %s"%gene_table)
	rows = curs.fetchall()
	for row in rows:
		gene_no2go_no[row[0]] = []
		go_functions_list = row[1][1:-1].split(',')
		for go_no in go_functions_list:
			gene_no2go_no[row[0]].append(int(go_no))
	sys.stderr.write("Done\n")
	return gene_no2go_no


def get_go_no2depth(curs, schema=None, table='go'):
	"""
	03-14-05
		get the go_no2depth
	"""
	sys.stderr.write("Getting go_no2depth...")
	if schema:
		curs.execute("set search_path to %s"%schema)
	go_no2depth = {}
	curs.execute("select go_no, depth from %s"%table)
	rows = curs.fetchall()
	for row in rows:
		go_no2depth[row[0]] = row[1]
	sys.stderr.write("Done\n")
	return go_no2depth


class get_edge_data:
	"""
	06-03-05
		see annot/MpiTightClust.py for updated version.
	"""
	def __init__(self, hostname='zhoudb', dbname='graphdb', schema=None):
		self.hostname = hostname
		self.dbname = dbname
		self.schema = schema
		self.gene_no2go_no = {}
		self.go_no2edge_matrix_data = {}
	
	def run(self):
		import psycopg
		import sys
		conn,curs = db_connect(psycopg, self.hostname, self.dbname,self.schema)
		
		self.gene_no2go_no = self.prepare_gene_no2go_no(curs)
		self.get_function_edge_matrix_data(curs)
		
		for go_no, edge_data in self.go_no2edge_matrix_data.iteritems():
			self.edge_data_output(go_no, edge_data)
		
		
	def get_function_edge_matrix_data(self, curs, edge_table='edge_cor_vector'):
		"""
		04-15-05
			
		"""
		sys.stderr.write("Getting edge matrix for all functions...\n")
		curs.execute("DECLARE crs CURSOR FOR select edge_id,edge_name,cor_vector \
			from %s"%(edge_table))
		
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
		counter = 0
		while rows:
			for row in rows:
				self._get_function_edge_matrix_data(row)
				counter +=1
			sys.stderr.write('%s%s'%('\x08'*20, counter))
			curs.execute("fetch 5000 from crs")
			rows = curs.fetchall()
		sys.stderr.write("Done\n")


	def _get_function_edge_matrix_data(self, row):
		"""
		04-11-05
		"""
		edge_id = row[0]
		edge = row[1][1:-1].split(',')
		edge = map(int, edge)
		for go_no in self.return_common_go_no_of_edge(edge):
			if go_no not in self.go_no2edge_matrix_data:
				self.go_no2edge_matrix_data[go_no] = [[go_no]]	#later expanded in pop_edge_data_of_one_function()
					#to be packaged into a Numeric array
			self.go_no2edge_matrix_data[go_no].append([edge_id]+self.return_edge_vector(row[2]))
	
	def return_common_go_no_of_edge(self, edge):
		"""
		04-15-05
			return common go_no's shared by an edge.
		"""
		gene_no1, gene_no2 = edge
		common_go_no_set = self.gene_no2go_no[gene_no1] & self.gene_no2go_no[gene_no2]
		return common_go_no_set
	
	def return_edge_vector(self, edge_vector_string):
		"""
		04-16-05
			parse the edge_vector_string fetched from database,
			handle the NA issues, replace them with random numbers for Cheng2000's biclustering
		"""
		edge_vector = []
		for item in edge_vector_string[1:-1].split(','):
			if item=='1.1':	#1.1 is 'NA', convention because of haiyan's copath
				edge_vector.append('NA')	#don't use (-800,800)
			else:
				edge_vector.append(float(item))
		return edge_vector
	
	def prepare_gene_no2go_no(self, curs):
		"""
		04-15-05
			different from get_gene_no2go_no, the value is a set.
		04-27-05
			only depth ==5
		"""
		sys.stderr.write("Preparing gene_no2go_no...")
		#from codense.common import get_gene_no2go_no, get_go_no2depth
		go_no2depth = get_go_no2depth(curs)
		gene_no2go_no = get_gene_no2go_no(curs)
		gene_no2go_no_set = {}
		for gene_no,go_no_list in gene_no2go_no.iteritems():
			gene_no2go_no_set[gene_no] = Set()
			for go_no in go_no_list:
				if go_no2depth[go_no] == 5:
					gene_no2go_no_set[gene_no].add(go_no)
		sys.stderr.write("Done.\n")
		return gene_no2go_no_set
	
	def edge_data_output(self, go_no, edge_data):
		"""
		04-27-05
			output edge data to investigate separately
		"""
		filename = 'edge_data_%s'%go_no
		file = open(filename, 'w')
		writer = csv.writer(file, delimiter='\t')
		for row in edge_data:
			writer.writerow(row)
		del writer
		file.close()

def return_gene_set_list(dir):
	import sys, os, csv
	from sets import Set
	files = os.listdir(dir)
	files.sort()
	sys.stderr.write("\tTotally, %d files to be processed.\n"%len(files))
	gene_set_list = []
	for f in files:
		local_gene_set = Set()
		print f
		#sys.stderr.write("%d/%d:\t%s\n"%(files.index(f)+1,len(files),f))
		f_path = os.path.join(dir, f)
		reader = csv.reader(file(f_path), delimiter='\t')
		for row in reader:
			local_gene_set.add(row[0])
		gene_set_list.append(local_gene_set)
		del reader
	return gene_set_list

def cal_set_intersection(gene_set_list, outfname):
	import sys, csv
	writer = csv.writer(open(outfname,'w'), delimiter='\t')
	counter = len(gene_set_list)
	for i in range(counter):
		ls = ['']*counter
		ls[i] = len(gene_set_list[i])
		for j in range(i+1, counter):
			ls[j] = len(gene_set_list[i]&gene_set_list[j])
		writer.writerow(ls)
	
def known_gene_percentage(gene_set, known_gene_dict):
	counter = 0
	for gene in gene_set:
		if gene in known_gene_dict:
			counter+=1
	
	print counter

"""
05-12-05
	the filename is fetched from NCBI GEO, which has an interface
	to let you get the GDS's given a platform_id
	
	The function parses the text file and get the GDS ids.
"""
def return_gds_list(filename):
	import re, os
	p_gds = re.compile(r'(GDS\d+)\ ')
	gds_list = []
	inf = open(filename, 'r')
	for line in inf:
		p_gds_result = p_gds.search(line)
		if p_gds_result:
			gds_list.append(p_gds_result.groups()[0])
	inf.close()
	return gds_list

"""
05-12-05
	get the dataset_ids from the database given a GPL id.
"""
def return_old_gpl_list(curs, gpl):
	curs.execute("select dataset_id from ds_stat where platform_id ='%s' and total_samples>=8"%(gpl))
	rows = curs.fetchall()
	old_gpl_list = []
	for row in rows:
		old_gpl_list.append(row[0])
	return old_gpl_list

"""
05-12-05
	output the gds_list in ftp url form to let wget automatically download all files
"""
def output_gds_url(gds_list, filename):
	outf = open(filename, 'w')
	url_prefix = 'ftp://anonymous:243242fa@ftp.ncbi.nih.gov/pub/geo/data/gds/soft_gz/'
	for gds in gds_list:
		line = '%s%s.soft.gz'%(url_prefix, gds)
		outf.write('%s\n'%line)
	outf.close()

"""
05-12-05
	output GDS's from mdb given  gds_id_list
"""
def output_gds_id_list(gds_id_list, output_dir, prefix):
	from microarraydb import microarraydb
	import os
	instance = microarraydb('mdb', 1)	#1 means normalization required
	for gds_id in gds_id_list:
		ofname = '%s_%s'%(prefix, gds_id)
		ofname = os.path.join(output_dir, ofname)
		instance.geo_single(gds_id, ofname)

"""
05-16-05
	
"""
def return_gene_no2is_correct_lca(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	gene_no2is_correct_lca = {}
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select p.p_gene_id, p.gene_no, p.is_correct_lca from %s p, %s g where g.p_gene_id=p.p_gene_id"%\
		(p_gene_table, gene_p_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no = row[1]
		is_correct_lca = row[2]
		if is_correct_lca==-1:
			continue
		if gene_no not in gene_no2is_correct_lca:
			gene_no2is_correct_lca[gene_no] = []
		gene_no2is_correct_lca[gene_no].append(is_correct_lca)
	return gene_no2is_correct_lca

def extra_gene_accuracy(gene_no2is_correct_lca_1, gene_no2is_correct_lca_2):
	from sets import Set
	gene_no_set1 = Set(gene_no2is_correct_lca_1.keys())
	gene_no_set2 = Set(gene_no2is_correct_lca_2.keys())
	
	extra_gene_set = gene_no_set2 - gene_no_set1
	is_correct_lca_list = []
	for gene in extra_gene_set:
		is_correct_lca_list += gene_no2is_correct_lca_2[gene]
	print "No of extra genes: %s"%len(extra_gene_set)
	print "Total predictions: %s"%len(is_correct_lca_list)
	print "Accuracy: %s"%(float(sum(is_correct_lca_list))/len(is_correct_lca_list))

"""
05-12-05
	additional GDS's

>>> Set(new_gpl81_list)-Set(old_gpl81_list)
Set(['GDS879', 'GDS857', 'GDS951', 'GDS717', 'GDS734', 'GDS912', 'GDS658', 'GDS739', 'GDS812', 'GDS679', 'GDS771', 'GDS773', 'GDS794', 'GDS684', 'GDS615', 'GDS614', 'GDS639', 'GDS638', 'GDS907', 'GDS782', 'GDS967', 'GDS788', 'GDS828', 'GDS640', 'GDS641', 'GDS681', 'GDS683', 'GDS648', 'GDS890', 'GDS604', 'GDS882', 'GDS605', 'GDS663', 'GDS660'])
>>> Set(new_gpl85_list)-Set(old_gpl85_list)
Set(['GDS965', 'GDS869', 'GDS769', 'GDS621', 'GDS778', 'GDS955', 'GDS956', 'GDS877', 'GDS599', 'GDS589', 'GDS872', 'GDS657', 'GDS656', 'GDS808', 'GDS654', 'GDS174', 'GDS598', 'GDS710', 'GDS765'])
>>> Set(new_gpl96_list)-Set(old_gpl96_list)
Set(['GDS834', 'GDS855', 'GDS690', 'GDS858', 'GDS737', 'GDS730', 'GDS914', 'GDS810', 'GDS916', 'GDS917', 'GDS738', 'GDS715', 'GDS686', 'GDS906', 'GDS962', 'GDS785', 'GDS901', 'GDS946', 'GDS826', 'GDS749', 'GDS748', 'GDS556', 'GDS760'])

"""

"""
05-16-05
	transform the cor_vector file (haiyan's copath input format) into the format similar to microarray datasets
	to do graph construction.
	use sig_fname to judge whether one edge meets the min_support
"""
def haiyan_cor_vector_file2graph_modeling_input(cor_fname, sig_fname, output_fname, min_support=6):
	import csv
	cor_reader = csv.reader(file(cor_fname), delimiter='\t')
	sig_reader = csv.reader(file(sig_fname), delimiter='\t')
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	cor_row = cor_reader.next()
	sig_row = sig_reader.next()
	while 1:
		edge_id = '%s_%s'%(cor_row[0], cor_row[1])	#concatenate the first two gene indices to form an edge
		ls = [edge_id]	#later write it to the output_fname
		sig_ls = sig_row[2:]
		sig_ls = map(int, sig_ls)
		support = sum(sig_ls)
		if support>min_support:
			for cor in cor_row[2:]:
				if cor=='1100':
					ls.append('NA')
				else:
					ls.append('%s'%(int(cor)*0.001))	#use string formatting to avoid too long points
			writer.writerow(ls)
		try:
			cor_row = cor_reader.next()
			sig_row = sig_reader.next()
		except StopIteration:
			break
	del writer

"""
05-17-05
	return the set of vertices covered by a mcl table
"""
def return_mcl_table_vertex_set(input_fname, schema):
	mcl_table = "mcl_%s"%input_fname
	hostname = 'zhoudb'
	dbname = 'graphdb'
	from codense.common import db_connect
	import psycopg, sys
	conn, curs = db_connect(hostname, dbname, schema)
	from sets import Set
	gene_no_set = Set()
	curs.execute("select vertex_set from %s"%mcl_table)
	curs.execute("DECLARE crs CURSOR FOR select vertex_set from %s"%(mcl_table))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 0
	while rows:
		for row in rows:
			vertex_set = row[0]
			vertex_list = vertex_set[1:-1].split(',')
			vertex_list = map(int, vertex_list)
			gene_no_set |= Set(vertex_list)
			counter+=1
		sys.stderr.write("%s%s"%("\x08"*20,counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	return gene_no_set

"""
05-18-05
"""
def gene_no_set_from_p_gene_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	gene_no_set = Set()
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select gene_no from %s"%\
		(p_gene_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no = row[0]
		gene_no_set.add(gene_no)
	return gene_no_set

"""
05-18-05
	not depend on curs,
"""
def get_gene_no2gene_id(hostname='zhoudb', dbname='graphdb', schema=None, table='gene'):
	from codense.common import db_connect
	import psycopg, sys
	conn, curs = db_connect(hostname, dbname, schema)
	sys.stderr.write("Getting gene_no2gene_id...")
	gene_no2gene_id = {}
	if schema:
		curs.execute("set search_path to %s"%schema)
	curs.execute("select gene_no, gene_id from %s"%table)
	rows = curs.fetchall()
	for row in rows:
		gene_no2gene_id[row[0]] = row[1]
	sys.stderr.write("Done\n")
	return gene_no2gene_id

"""
05-18-05
	
"""
def return_mcl_cluster_size_list(input_fname, hostname='zhoudb', dbname='graphdb', schema=None):
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg, sys
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select array_upper(vertex_set,1) from %s"%mcl_table)
	rows = curs.fetchall()
	cluster_size_list = []
	for row in rows:
		cluster_size_list.append(row[0])
	return cluster_size_list

"""
05-18-05
"""
def return_mcl_cluster_density_list(input_fname, hostname='zhoudb', dbname='graphdb', schema=None):
	splat_table = 'splat_%s'%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg, sys
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select s.connectivity from %s m, %s s where s.splat_id =m.splat_id"%(mcl_table, splat_table))
	rows = curs.fetchall()
	ls = []
	for row in rows:
		ls.append(row[0])
	return ls

"""
05-18-05
"""
def return_mcl_density_original_list(input_fname, hostname='zhoudb', dbname='graphdb', schema=None):
	splat_table = 'splat_%s'%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg, sys
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select connectivity_original from %s"%(mcl_table))
	rows = curs.fetchall()
	ls = []
	for row in rows:
		ls.append(row[0])
	return ls

"""
05-18-05
"""
def cluster_id_set_from_p_gene_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	set_to_return = Set()
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select mcl_id from %s"%\
		(p_gene_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no = row[0]
		set_to_return.add(gene_no)
	return set_to_return

def cluster_id_set_from_gene_p_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	set_to_return = Set()
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select p.mcl_id from %s p, %s g where p.p_gene_id=g.p_gene_id"%\
		(p_gene_table, gene_p_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no = row[0]
		set_to_return.add(gene_no)
	return set_to_return




def cluster_size_list_from_p_gene_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	set_to_return = Set()
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(ho65stname, dbname, schema)
	curs.execute("select distinct m.mcl_id,array_upper(m.vertex_set,1) from %s m, %s p where p.mcl_id=m.mcl_id"%\
		(mcl_table, p_gene_table))
	rows = curs.fetchall()
	ls_to_return = []
	for row in rows:
		mcl_id = row[0]
		if mcl_id not in set_to_return:
			set_to_return.add(mcl_id)
			ls_to_return.append(row[1])
	return ls_to_return

def cluster_size_list_from_gene_p_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	set_to_return = Set()
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select m.mcl_id,array_upper(m.vertex_set,1) from %s m, %s p, %s g where p.mcl_id=m.mcl_id and p.p_gene_id=g.p_gene_id"%\
		(mcl_table, p_gene_table, gene_p_table))
	rows = curs.fetchall()
	ls_to_return = []
	for row in rows:
		mcl_id = row[0]
		if mcl_id not in set_to_return:
			set_to_return.add(mcl_id)
			ls_to_return.append(row[1])
	return ls_to_return

def cluster_id_size_list_from_p_gene_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	set_to_return = Set()
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select m.mcl_id,array_upper(m.vertex_set,1) from %s m, %s p where p.mcl_id=m.mcl_id"%\
		(mcl_table, p_gene_table))
	rows = curs.fetchall()
	ls_to_return = []
	for row in rows:
		mcl_id = row[0]
		if mcl_id not in set_to_return:
			set_to_return.add(mcl_id)
			ls_to_return.append(row)
	return ls_to_return
"""
05-24-05
	not finished
"""

def return_edge_set_of_summary_graph(summary_gfile, cluster_edge_file, output_fname):
	import csv,sys
	summary_gf = open(summary_gfile,'r')
	from sets import Set
	edge_set = Set()
	
	cluster_edge_f = open(cluster_edge_file, 'r')
	of = open(output_fname,'w')
	edge_list = cluster_edge_f.readline()
	edge_list = edge_list[2:-3].split('},{')
	for i in range(len(edge_list)):
		edge_list[i]  = edge_list[i].split(',')
		edge_list[i] = map(int, edge_list[i])
	for line in summary_gf:
		if line[0]!='e':
			of.write(line)
		else:
			break
	for edge in edge_list:
		of.write('e %s %s 10\n'%(edge[0], edge[1]))
	of.close()
	
"""
05-18-05
	protein efetch xml handler
"""
from xml.sax import handler
from xml import sax
class efetch_handler(handler.ContentHandler):
	def __init__(self):
		handler.ContentHandler.__init__(self)
		self.GBSeq_comment = 0
		self.comment = ''
	def characters(self, s):
		if self.GBSeq_comment == 1:
			self.comment = s
	def startElement(self, name, attrs):
		if name == "GBSeq_comment":
			self.GBSeq_comment = 1
	def endElement(self, name):
		if name == "GBSeq_comment":
			self.GBSeq_comment = 0

"""
05-20-05
"""
def get_total_gene_id2no(hostname='zhoudb', dbname='graphdb', schema='graph', organism=None):
	from codense.common import db_connect
	import psycopg, sys
	conn, curs = db_connect(hostname, dbname, schema)
	sys.stderr.write("Getting gene_no2gene_id...")
	gene_id2no = {}
	if schema:
		curs.execute("set search_path to %s"%schema)
	curs.execute("select gene_id, gene_no from gene_id_to_no where organism='%s'"%organism)
	rows = curs.fetchall()
	for row in rows:
		gene_id2no[row[0]] = row[1]
	sys.stderr.write("Done\n")
	return gene_id2no

def gene_set_from_summary_graph(summary_gfile, min_support):
	import csv,sys
	from sets import Set
	summary_gf = open(summary_gfile,'r')
	reader = csv.reader(summary_gf, delimiter='\t')
	gene_no_set = Set()
	for row in reader:
		if row[0]=='e':
			gene_no1 = int(row[1])
			gene_no2 = int(row[2])
			#support = int(row[3])
			#if support >= min_support:
			gene_no_set.add(gene_no1)
			gene_no_set.add(gene_no2)
	del reader
	return gene_no_set


def no_of_edges_from_summary_graph_given_gene_set(summary_gfile, min_support, gene_set):
	import csv,sys
	from sets import Set
	summary_gf = open(summary_gfile,'r')
	reader = csv.reader(summary_gf, delimiter=' ')
	no_of_edges = 0
	for row in reader:
		if row[0]=='e':
			gene_no1 = int(row[1])
			gene_no2 = int(row[2])
			support = int(row[3])
			if support >= min_support and (gene_no1 in gene_set) and (gene_no2 in gene_set) :
				no_of_edges += 1
	del reader
	return no_of_edges

def output_graph_edge_from_matrix(matrix_file):
	import csv, sys
	reader = csv.reader(open(matrix_file,'r'), delimiter='\t')
	i=0
	graph_dict = {}
	for row in reader:
		row = map(int, row)
		for j in range(len(row)):
			if row[j]>0:
				if i<j:
					graph_dict[(i,j)]=row[j]
		i+=1
	for edge in graph_dict:
		print edge, graph_dict[edge]
	edge_list = graph_dict.keys()
	edge_list.sort()
	print edge_list

"""
05-24-05
	remove a series of tables based on the input_fname
"""
def remove_tables(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38', commit=0):
	splat_result_table = "splat_%s"%input_fname
	mcl_result_table = "mcl_%s"%input_fname
	cluster_stat_table = "cluster_%s"%input_fname
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	edge_input_fname = '%se'%input_fname
	e_splat_result_table = "splat_%s"%edge_input_fname
	e_mcl_result_table = "mcl_%s"%edge_input_fname
	e_cluster_stat_table = "cluster_%s"%edge_input_fname
	e_p_gene_table = "p_gene_%s_e5"%edge_input_fname
	e_gene_p_table = "gene_p_%s_e5_p01"%edge_input_fname
	
	old_cluster_stat_table = "cluster_stat_%s"%input_fname
	old_splat_result_table = "splat_result_%s"%input_fname
	old_mcl_result_table = "mcl_result_%s"%input_fname
	table_list = [splat_result_table, mcl_result_table, cluster_stat_table, p_gene_table, gene_p_table,\
		e_splat_result_table, e_mcl_result_table,e_cluster_stat_table, e_p_gene_table, e_gene_p_table, \
		old_cluster_stat_table, old_splat_result_table, old_mcl_result_table]
	from codense.common import db_connect
	import psycopg, sys
	conn, curs = db_connect(hostname, dbname, schema)
	for table in table_list:
		try:
			sys.stderr.write("Deleting %s...\n"%table)
			curs.execute("drop table %s"%table)
			if commit:
				curs.execute("end")
		except:
			print "Deleting %s error: %s"%(table, repr(sys.exc_info()[0]))
			conn, curs = db_connect(hostname, dbname, schema)

"""
05-24-05

"""
def gene_no2cluster_id_list_from_gene_p_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	gene_no2cluster_id_list = {}
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select p.gene_no,p.mcl_id from %s p, %s g where p.p_gene_id=g.p_gene_id"%\
		(p_gene_table, gene_p_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no = row[0]
		cluster_id = row[1]
		if gene_no not in gene_no2cluster_id_list:
			gene_no2cluster_id_list[gene_no] = []
		gene_no2cluster_id_list[gene_no].append(cluster_id)
	return gene_no2cluster_id_list

"""
06-21-05
"""
def gene_no2go_id_set_from_gene_p_given_gene_set(input_fname, gene_set, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	gene_no2go_id_list = {}
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select p.gene_no,go.go_id from %s p, go, %s g where p.p_gene_id=g.p_gene_id and go.go_no=p.go_no"%\
		(p_gene_table, gene_p_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no = row[0]
		go_id = row[1]
		if gene_no in gene_set:
			if gene_no not in gene_no2go_id_list:
				gene_no2go_id_list[gene_no] = Set()
			gene_no2go_id_list[gene_no].add(go_id)
	return gene_no2go_id_list

def gene_no_go_id_pair_from_gene_p_given_gene_set(input_fname, gene_set, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	gene_no2go_id_set = Set()
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select p.gene_no,go.go_id from %s p, %s g, go where p.p_gene_id=g.p_gene_id and go.go_no =p.go_no"%\
		(p_gene_table, gene_p_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no = row[0]
		go_id = row[1]
		if gene_no in gene_set:
			gene_no2go_id_set.add((gene_no,go_id))
	return gene_no2go_id_set
	
"""
06-26-05
"""
def go_id_set_from_gene_p_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	go_id_set = Set()
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select p.gene_no,go.go_id from %s p, %s g, go where p.p_gene_id=g.p_gene_id and go.go_no =p.go_no"%\
		(p_gene_table, gene_p_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no = row[0]
		go_id = row[1]
		go_id_set.add(go_id)
	return go_id_set

"""
06-27-05
"""
def gene_no2go_id_set_from_gene_p_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	gene_no2go_id_set = {}
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select p.gene_no,go.go_id from %s p, go, %s g where p.p_gene_id=g.p_gene_id and go.go_no=p.go_no"%\
		(p_gene_table, gene_p_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no = row[0]
		go_id = row[1]
		if gene_no not in gene_no2go_id_set:
			gene_no2go_id_set[gene_no] = Set()
		gene_no2go_id_set[gene_no].add(go_id)
	return gene_no2go_id_set

"""
05-25-05
	read in a graph(haiyan's edge format) and return a matrix and an edge_list
"""
def read_in_graph(input_fname):
	import csv
	edge_list = []
	no_of_vertices = 0
	vertex_dict = {}
	reader = csv.reader(open(input_fname,'r'),delimiter='\t')
	for row in reader:
		vertex1 = int(row[0])
		vertex2 = int(row[1])
		if vertex1 not in vertex_dict:
			vertex_dict[vertex1] = no_of_vertices
			no_of_vertices += 1
		if vertex2 not in vertex_dict:
			vertex_dict[vertex2] = no_of_vertices
			no_of_vertices += 1
		edge_list.append([vertex_dict[vertex1], vertex_dict[vertex2]])
	from Numeric import zeros
	graph_matrix = zeros((no_of_vertices, no_of_vertices))
	for edge in edge_list:
		graph_matrix[edge[0], edge[1]] = 1
		graph_matrix[edge[1], edge[0]] = 1
	del reader
	return (graph_matrix, edge_list)

"""
05-25-05
	transform an adjacency matrix to laplacian matrix
"""
def adjacency2laplacian(adjacency_matrix):
	from Numeric import zeros
	laplacian_matrix = zeros(adjacency_matrix.shape)
	for i in range(adjacency_matrix.shape[0]):
		degree = sum(adjacency_matrix[i, :])
		laplacian_matrix[i,i] = degree
		for j in range(adjacency_matrix.shape[1]):
			if adjacency_matrix[i,j] != 0:
				laplacian_matrix[i,j] = -1
	return laplacian_matrix

"""
05-25-05
	plot the graph in the planar form(see Dan Spielman's online tutorial)
"""
def plot_platnar_graph(laplacian_matrix, edge_list):
	from MLab import eig
	from rpy import r
	eigen_result = eig(laplacian_matrix)
	#eigen_result[0] is an array of eigenvalues
	#eigen_result[1] is an array of corresponding eigenvectors
	eigen_vector_2nd = eigen_result[1][argsort(eigen_result[0])[1]]	#the second minimum, but must be non-zero, the graph is connected
	eigen_vector_3rd = eigen_result[1][argsort(eigen_result[0])[2]]
	r.plot(list(eigen_vector_2nd),list(eigen_vector_3rd),xlab='',ylab='')
	for edge in edge_list:
		x_list = [eigen_vector_2nd[edge[0]], eigen_vector_2nd[edge[1]]]
		y_list = [eigen_vector_3rd[edge[0]], eigen_vector_3rd[edge[1]]]
		r.lines(x_list,y_list)
	
"""
05-25-05
	normalize a graph matrix, and I-(the normalized graph matrix) = laplacian matrix(normalized)
"""
def return_normalized_laplacian_matrix(graph_matrix):
	from Numeric import Float, dot, identity, diagonal
	graph_matrix = graph_matrix.astype(Float)
	laplacian_matrix = adjacency2laplacian(graph_matrix)
	D_1_2 = identity(laplacian_matrix.shape[0])*pow(diagonal(laplacian_matrix),-0.5)
	normalized_laplacian_matrix = identity(graph_matrix.shape[0])-dot(dot(D_1_2,graph_matrix),D_1_2)
	return normalized_laplacian_matrix

"""
05-27-05
	read in the 2nd-order graph constructed by netmine2nd given --out2nd
	and output it in a similar way to check_netmine2nd.py
	
	Please refer the same function in check_netmine2nd.py. This one is outdated.
"""
def read_2nd_order_graph(input_fname, output_fname):
	import csv
	reader = csv.reader(open(input_fname,'r'), delimiter='\t')
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	for row in reader:
		edge_list_2nd_order_graph = row[3]
		edge_list_2nd_order_graph = edge_list_2nd_order_graph[1:-2].split(';')
		for edge in edge_list_2nd_order_graph:
			edge = edge.split('-')
			edge.sort()
			writer.writerow(edge)
	del reader,writer

"""
06-07-05
	return the set of distinct datasets in all the results of tightClust.
"""

def return_distinct_datasets_set(input_fname):
	import csv
	from sets import Set
	ds_set = Set()
	reader = csv.reader(open(input_fname,'r'),delimiter='\t')
	for row in reader:
		ds_set |= Set(row)
	del reader
	return ds_set

"""
06-10-05
"""
def return_ds_set_list(input_fname):
	import csv
	from sets import Set
	ds_set_list = []
	reader = csv.reader(open(input_fname,'r'),delimiter=',')
	for row in reader:
		row = map(int, row)
		ds_set_list.append( Set(row))
	del reader
	return ds_set_list
"""
06-16-05
	read a graph(graph_modeling output format, or even simpler (without 'e')) and return
	the graph_dict, edge is in tuple form(smaller_id, bigger_id)
"""
def graph_dict_from_graph(input_fname):
	import csv
	graph_dict = {}
	reader = csv.reader(open(input_fname,'r'),delimiter='\t')
	reader.next()
	for row in reader:
		vertex1 = int(row[0])
		vertex2 = int(row[1])
		weight = row[2]
		if vertex1 < vertex2:
			edge_tuple = (vertex1,vertex2)
		else:
			edge_tuple = (vertex2, vertex1)
		graph_dict[edge_tuple] = weight
	del reader
	return graph_dict
"""
graph_modeling format (with 'e')
"""
def graph_dict_from_graph2(input_fname):
	import csv
	graph_dict = {}
	reader = csv.reader(open(input_fname,'r'),delimiter='\t')
	reader.next()
	for row in reader:
		vertex1 = int(row[1])
		vertex2 = int(row[2])
		weight = row[3]
		if vertex1 < vertex2:
			edge_tuple = (vertex1,vertex2)
		else:
			edge_tuple = (vertex2, vertex1)
		graph_dict[edge_tuple] = weight
	del reader
	return graph_dict

"""
06-23-05
	output 500 lines of a specified correlation
"""
def output_corTable(outfname, cor):
	import csv
	writer = csv.writer(open(outfname,'w'), delimiter='\t')
	for i in range(500):
		writer.writerow([i+1, cor])
	del writer
"""
06-27-05
"""
def return_gene_no_set_with_this_prediction(gene_no2go_id_set, go_id):
	from sets import Set
	gene_no_set = Set()
	for gene_no,go_id_set in gene_no2go_id_set.iteritems():
		if go_id in go_id_set:
			gene_no_set.add(gene_no)
	return gene_no_set

def return_gene_no_set_with_prediction_set(gene_no2go_id_set, go_id_set_given):
	from sets import Set
	gene_no_set = Set()
	for gene_no,go_id_set in gene_no2go_id_set.iteritems():
		intersection_set = go_id_set_given&go_id_set
		if len(intersection_set)>0:
			gene_no_set.add(gene_no)
	return gene_no_set


"""
07-06-05
"""
def recurrence_list_from_p_gene_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	set_to_return = Set()
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_p01"%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select distinct m.mcl_id,p.recurrence_cut_off from %s m, %s p where p.mcl_id=m.mcl_id"%\
		(mcl_table, p_gene_table))
	rows = curs.fetchall()
	ls_to_return = []
	for row in rows:
		mcl_id = row[0]
		if mcl_id not in set_to_return:
			set_to_return.add(mcl_id)
			ls_to_return.append(row[1])
	return ls_to_return


"""
07-27-05
"""
def subgraph_from_summary_graph_given_geneset(summary_gfile, gene_set, min_support):
	from graphlib import Graph
	import csv,sys
	from sets import Set
	graph = Graph.Graph()
	summary_gf = open(summary_gfile,'r')
	reader = csv.reader(summary_gf, delimiter=' ')
	for row in reader:
		if row[0]=='e':
			gene_no1 = int(row[1])
			gene_no2 = int(row[2])
			support = int(row[3])
			if support >= min_support and gene_no1 in gene_set and gene_no2 in gene_set:
				graph.add_node(gene_no1)
				graph.add_node(gene_no2)
				graph.add_edge(gene_no1, gene_no2, support)
	del reader
	return graph

"""
07-27-05
"""
def recurrence_list_from_gene_p_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	set_to_return = Set()
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_a60"%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select m.mcl_id,p.recurrence_cut_off from %s m, %s p, %s g where p.mcl_id=m.mcl_id and p.p_gene_id=g.p_gene_id"%\
		(mcl_table, p_gene_table, gene_p_table))
	rows = curs.fetchall()
	ls_to_return = []
	for row in rows:
		mcl_id = row[0]
		if mcl_id not in set_to_return:
			set_to_return.add(mcl_id)
			ls_to_return.append(row[1])
	return ls_to_return

"""
07-27-05
"""
def connectivity_list_from_gene_p_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	set_to_return = Set()
	splat_table = 'splat_%s'%input_fname
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_a60"%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select m.mcl_id,s.connectivity from %s m, %s p, %s g, %s s \
		where p.mcl_id=m.mcl_id and p.p_gene_id=g.p_gene_id and m.splat_id=s.splat_id"%\
		(mcl_table, p_gene_table, gene_p_table, splat_table))
	rows = curs.fetchall()
	ls_to_return = []
	for row in rows:
		mcl_id = row[0]
		if mcl_id not in set_to_return:
			set_to_return.add(mcl_id)
			ls_to_return.append(row[1])
	return ls_to_return

"""
07-27-05
"""
def rec_con_list_from_gene_p_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	set_to_return = Set()
	splat_table = 'splat_%s'%input_fname
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_a60"%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select m.mcl_id,p.recurrence_cut_off,s.connectivity from %s m, %s p, %s g, %s s \
		where p.mcl_id=m.mcl_id and p.p_gene_id=g.p_gene_id and m.splat_id=s.splat_id"%\
		(mcl_table, p_gene_table, gene_p_table, splat_table))
	rows = curs.fetchall()
	ls_to_return = []
	for row in rows:
		mcl_id = row[0]
		if mcl_id not in set_to_return:
			set_to_return.add(mcl_id)
			ls_to_return.append([row[1],row[2]])
	return ls_to_return

"""
07-28-05
"""
def plot_rec_con_list(rec_con_list):
	rec_list = [row[0] for row in rec_con_list]
	con_list = [row[1] for row in rec_con_list]
	from rpy import r
	r.plot(rec_list,con_list,main='con~rec',xlab='rec',ylab='con')

def hist_plot_rec_con_list(rec_con_list, which_column=0):
	rec_list = [row[which_column] for row in rec_con_list]
	from rpy import r
	r.hist(rec_list,main='histogram',xlab='something',ylab='freq')

"""
07-29-05
"""
def output_edge_data_for_fim(edge_table='edge_cor_vector', min_support=3, hostname='zhoudb', dbname='graphdb', schema='sc_new_38', debug=0):
	#connect to the database
	import sys, psycopg, os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from codense.common import db_connect
	conn, curs = db_connect(hostname, dbname, schema)
	
	#get the number of graphs in total
	curs.execute("select array_upper(sig_vector,1) from %s limit 1"%(edge_table))
	rows = curs.fetchall()
	no_of_files = int(rows[0][0])
	
	#create fname_list
	fname_list = []
	for i in range(no_of_files):
		fname_list.append('/tmp/graph%s'%i)
	
	#open a number of files
	fhandler_list = []
	for i in range(no_of_files):
		fhandler_list.append(open(fname_list[i], 'w'))
	
	sys.stderr.write("Getting edge matrix for all functions...\n")
	curs.execute("DECLARE crs CURSOR FOR select edge_id,sig_vector \
		from %s"%(edge_table))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 0
	while rows:
		for row in rows:
			edge_id = row[0]
			sig_vector = row[1][1:-1].split(',')
			sig_vector = map(int, sig_vector)
			if sum(sig_vector)>=min_support:
				for i in range(len(sig_vector)):
					if sig_vector[i]==1:
						fhandler_list[i].write('\t%s'%edge_id)
			counter +=1
		sys.stderr.write('%s%s'%('\x08'*20, counter))
		if debug:
			break
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	
	#append the newline
	for i in range(no_of_files):
		fhandler_list[i].write('\n')
		fhandler_list[i].close()
	
	os.system('rm /tmp/graph.fim_input')
	for i in range(len(fname_list)):
		os.system('cat %s >>/tmp/graph.fim_input'%fname_list[i])
	
	sys.stderr.write("Done\n")

"""
08-04-05
"""
def output_edge_data_fim_edge_oriented(edge_table='edge_cor_vector', min_support=3, max_support=200, hostname='zhoudb', dbname='graphdb', schema='sc_new_38', debug=0):
	#connect to the database
	import sys, psycopg, os, csv
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from codense.common import db_connect
	conn, curs = db_connect(hostname, dbname, schema)
	
	fname = "/tmp/%s.fim.input"%schema
	writer = csv.writer(open(fname,'w'),delimiter='\t')
	
	sys.stderr.write("Getting edge matrix for all functions...\n")
	curs.execute("DECLARE crs CURSOR FOR select edge_id,sig_vector \
		from %s"%(edge_table))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 0
	while rows:
		for row in rows:
			edge_id = row[0]
			sig_vector = row[1][1:-1].split(',')
			sig_vector = map(int, sig_vector)
			
			if sum(sig_vector)>=min_support and sum(sig_vector)<=max_support:
				new_row = []
				for i in range(len(sig_vector)):
					if sig_vector[i]==1:
						new_row.append(i+1)
				writer.writerow(new_row)
			counter +=1
		sys.stderr.write('%s%s'%('\x08'*20, counter))
		if debug:
			break
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	
	sys.stderr.write("Done\n")

"""
07-14-05
"""
def return_dc_from_file(filename):
	import csv
	reader = csv.reader(file(filename), delimiter='\t')
	dc = {}
	for row in reader:
		dc[row[0]] = int(row[1])
	return dc

"""
07-14-05
"""
def key_dif(dc1, dc2, max_no_cutoff, ratio_cutoff):
	from sets import Set
	s = Set(dc1.keys())|Set(dc2.keys())
	ls = []
	tuple_ls = []
	for item in s:
		no1 = dc1.get(item)
		no2 = dc2. get(item)
		if no1 == None:
			no1 = 0
		if no2 == None:
			no2 = 0
		no_diff = no1-no2
		max_no = max(no1, no2)
		if max_no>= max_no_cutoff and no_diff/float(max_no) >= ratio_cutoff:
			ls.append(item)
			tuple_ls.append((item,no1, no2))
	return ls, tuple_ls

"""
08-16-05
"""
def gene2go_no_from_gene_p_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	gene2go_no = {}
	splat_table = 'splat_%s'%input_fname
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_a60"%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select distinct p.gene_no,p.go_no from %s p, %s g \
		where p.p_gene_id=g.p_gene_id"%\
		(p_gene_table, gene_p_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no= row[0]
		go_no = row[1]
		if gene_no not in gene2go_no:
			gene2go_no[gene_no] = []
		gene2go_no[gene_no].append(go_no)
	return gene2go_no

def gene2go_no_from_gene_p_table2(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	gene2go_no = {}
	splat_table = 'splat_%s'%input_fname
	p_gene_table = "p_gene_%s_e5"%input_fname
	gene_p_table = "gene_p_%s_e5_a60"%input_fname
	mcl_table = 'mcl_%s'%input_fname
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select distinct p.gene_no,p.go_no from %s p, %s g \
		where p.p_gene_id=g.p_gene_id_src"%\
		(p_gene_table, gene_p_table))
	rows = curs.fetchall()
	for row in rows:
		gene_no= row[0]
		go_no = row[1]
		if gene_no not in gene2go_no:
			gene2go_no[gene_no] = []
		gene2go_no[gene_no].append(go_no)
	return gene2go_no	
"""
08-16-05
"""
def hist_plot_pleiotropy(gene2go_no, no_of_breaks):
	go_list = gene2go_no.values()
	freq_list = map(len, go_list)
	from rpy import r
	r.hist(freq_list,main='histogram',xlab='something',ylab='freq', breaks=no_of_breaks)
	print "total predictions :",sum(freq_list)

def count_genes(gene2go_no):
	freq2counter = {}
	for gene_no, go_no_list in gene2go_no.iteritems():
		frequency = len(go_no_list)
		if frequency not in freq2counter:
			freq2counter[frequency] = 0
		freq2counter[frequency] += 1
	return freq2counter

def hist_plot_pleiotropy_prob(gene2go_no, no_of_breaks):
	go_list = gene2go_no.values()
	freq_list = map(len, go_list)
	from rpy import r
	r.hist(freq_list,main='histogram',xlab='something',ylab='freq',breaks=no_of_breaks)
	print "total predictions :",sum(freq_list)
	return freq_list

"""
08-24-05
	to test whether a Numeric array is passed as a pointer or copied
"""
def fill_edge_matrix(edge_matrix):
	for i in range(edge_matrix.shape[0]):
		for j in range(edge_matrix.shape[1]):
			edge_matrix[i][j] = i*j

def append_list(ls):
	for i in range(10):
		ls.append([i]*10)


"""
08-28-05
	get a certain column data into a list, and draw a histogram
"""
def draw_one_column(inputfile, which_column, no_of_breaks, top_value=None):
	import csv
	reader = csv.reader(open(inputfile, 'r'), delimiter='\t')
	data = []
	for row in reader:
		value = float(row[which_column])
		if top_value:
			if value>=top_value:
				continue
		data.append(value)
	del reader
	from rpy import r
	r.hist(data, xlab='value',ylab='freq',main='hist', breaks=no_of_breaks)
	return data

"""
09-02-05
	a function to stop betweenness_centrality_clustering()
"""
def done(m_centrality, edge_desc, g):
	connectivity = g.num_edges()*2.0/(g.num_vertices()*(g.num_vertices()-1)/2)
	eim=g.get_edge_index_map()
	print "The edge is %s"%eim[edge_desc]
	print "its centrality is",m_centrality
	print "connectivity is ",connectivity
	vim = g.get_vertex_int_map("component")
	n_of_c = bgl.connected_components(g, vim)
	print "number of connected components is",n_of_c
	if n_of_c >=2:
		return True
	elif connectivity>=0.7:
		return True
	else:
		return False

if __name__ == '__main__':
	import sys
	instance = get_edge_data('zhoudb','graphdb', sys.argv[1])
	instance.run()
	#haiyan_cor_vector_file2graph_modeling_input(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
