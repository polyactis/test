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


"""
10-03-05
	size is already in p_gene_table, no more mcl_table linking
"""
def cluster_id_size_list_from_p_gene_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	set_to_return = Set()
	from codense.common import db_connect, form_schema_tables
	import psycopg, sys, os
	schema_instance = form_schema_tables(input_fname, acc_cut_off=0.6)
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("DECLARE crs CURSOR FOR select mcl_id, cluster_size_cut_off from %s"%schema_instance.p_gene_table)
		#distinct is not necessary, because set_to_return will judge it
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	ls_to_return = []
	counter = 0
	while rows:
		for row in rows:
			mcl_id = row[0]
			if mcl_id not in set_to_return:
				set_to_return.add(mcl_id)
				ls_to_return.append(row)
			counter += 1
		sys.stderr.write('%s%s'%('\x08'*20, counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
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


"""
10-03-05
	good_cluster_table is ready, so directly get cluster information from there, not gene_p_table
"""
def cluster_id_size_list_from_good_cl_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	from codense.common import db_connect, form_schema_tables
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	schema_instance = form_schema_tables(input_fname, acc_cut_off=0.6)
	curs.execute("select mcl_id,array_upper(vertex_set,1) from %s "%schema_instance.good_cluster_table)
		#size in good_cluster_table is a bug, so still use array_upper()
	rows = curs.fetchall()
	ls_to_return = []
	for row in rows:
		mcl_id = row[0]
		ls_to_return.append(row)
	return ls_to_return

"""
10-03-05
	the most orginal data before prediction
"""
def cluster_id_size_list_from_mcl_table(input_fname, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	from codense.common import db_connect, form_schema_tables
	import psycopg, sys,os
	conn, curs = db_connect(hostname, dbname, schema)
	schema_instance = form_schema_tables(input_fname, acc_cut_off=0.6)
	curs.execute("DECLARE crs CURSOR FOR select mcl_id,array_upper(vertex_set,1) from %s "%schema_instance.mcl_table)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	ls_to_return = []
	counter = 0
	while rows:
		for row in rows:
			mcl_id = row[0]
			ls_to_return.append(row)
			counter += 1
		sys.stderr.write('%s%s'%('\x08'*20, counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
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
12-01-05
	use form_schema_tables()
12-23-05
	add more tables
"""
def remove_tables(input_fname, lm_bit, acc_cut_off=0.6, hostname='zhoudb', dbname='graphdb', schema='sc_new_38', commit=0):
	import sys,os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from codense.common import db_connect, form_schema_tables
	schema_instance = form_schema_tables(input_fname, acc_cut_off, lm_bit)
	table_list = [schema_instance.mcl_table, schema_instance.splat_table,  schema_instance.pattern_table, \
		schema_instance.p_gene_table, schema_instance.gene_p_table,\
		schema_instance.lm_table, schema_instance.good_cluster_table, schema_instance.cluster_bs_table]
	import psycopg, sys
	conn, curs = db_connect(hostname, dbname, schema)
	for table in table_list:
		try:
			sys.stderr.write("Deleting table %s"%table)
			curs.execute("drop table %s"%table)
			sys.stderr.write('.\n')
			if commit:
				curs.execute("end")
		except:
			try:
				conn, curs = db_connect(hostname, dbname, schema)
				sys.stderr.write("Deleting view %s"%table)
				curs.execute("drop view %s"%table)
				sys.stderr.write('.\n')
				if commit:
					curs.execute("end")
			except:
				print "\tError in deleting %s.  %s"%(table, repr(sys.exc_info()[0]))
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
	return None	#10-03-05 avoid r.hist() throw chunks of data to the screen
	
def hist_plot_list(input_list):
	from rpy import r
	r.hist(input_list,main='histogram',xlab='something',ylab='freq')
	return None

#11-27-05
def plot_ls(input_list):
	from rpy import r
	x_list = range(len(input_list))
	r.plot(x_list, input_list, main='plot',xlab='index',ylab='value', type='b')
	return None

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

"""
09-15-05
	write the gene incidence matrix
09-26-05
	This part has been ported to DrawGenePresenceMatrix.py
"""
def gene_no_set_from_one_file(filename):
	import csv
	from sets import Set
	gene_id_set = Set()
	reader = csv.reader(file(filename), delimiter='\t')
	for row in reader:
		gene_id_set.add(row[0])
	del reader
	return gene_id_set

def write_gene_incidence_matrix(dir, output_dir, hostname='zhoudb', dbname='graphdb', schema='hs_fim_138'):
	import sys, os, csv
	sys.path += [os.path.join(os.path.expanduser('~/script/annot/bin'))]
	from codense.common import db_connect, get_gene_id2gene_no
	from graph.complete_cor_vector import complete_cor_vector
	from sets import Set
	complete_cor_vector_instance = complete_cor_vector()
	
	(conn, curs) =  db_connect(hostname, dbname)
	gene_id2no = get_gene_id2gene_no(curs, schema)
	gene_id_list = list(gene_id2no.keys())
	
	final_outputfname = os.path.join(output_dir, '%s.gim'%schema)
	label_fname = os.path.join(output_dir, '%s_0'%final_outputfname)
	of = open(label_fname, 'w')
	for gene_id in gene_id_list:
		of.write('%s\n'%gene_id)
	del of
	
	files = os.listdir(dir)
	files = complete_cor_vector_instance.files_sort(files)
	sys.stderr.write("\tTotally, %d files to be processed.\n"%len(files))
	
	for i in range(len(files)):
		f = files[i]
		print f
		f_path = os.path.join(dir, f)
		gene_id_set = gene_no_set_from_one_file(f_path)
		
		#write the gene incidence to the output_fname
		output_fname = os.path.join(output_dir, '%s_%s'%(final_outputfname, i+1))
		of = open(output_fname, 'w')
		for gene_id in gene_id_list:
			if gene_id in gene_id_set:
				of.write('1\n')
			else:
				of.write('0\n')
		del of
	complete_cor_vector_instance.collect_and_merge_output(final_outputfname, len(files))	#collect_and_merge_output will use 0 to len(files)

"""
09-23-05
	convert the incidence matrix into a jpeg file
09-26-05
	This part has been ported to DrawGenePresenceMatrix.py
10-31-05 ported to codense/common.py
"""
import Image, ImageDraw
def get_char_dimension():
	im = Image.new('RGB', (50,50))
	draw = ImageDraw.Draw(im)
	char_dimension = draw.textsize('a')
	del im, draw
	return char_dimension


def get_text_region(text, dimension, rotate=1):
	text_im = Image.new('RGB', dimension, (255,255,255))
	text_draw = ImageDraw.Draw(text_im)
	text_draw.text((0,0), text, fill=(0,0,255))
	box = (0,0,dimension[0], dimension[1])
	text_reg = text_im.crop(box)
	if rotate:
		text_reg = text_reg.transpose(Image.ROTATE_90)	#90 is anti-clockwise
	return text_reg


def draw_incidence_matrix(input_fname, output_fname):
	import csv, Image, ImageDraw, os
	ylength_output = os.popen('wc %s'%input_fname)
	ylength_output = ylength_output.read()
	ylength = int(ylength_output.split()[0])
	
	xlength_output = os.popen('%s %s'%(os.path.expanduser('~/script/shell/count_columns.py'), input_fname))
	xlength_output = xlength_output.read()
	xlength = int(xlength_output.split()[-1])-1	#the first column is gene id
	
	char_width, char_height = get_char_dimension()
	text_dimension = (char_height, char_width*len(repr(xlength)))
	
	reader = csv.reader(open(input_fname,'r'), delimiter='\t')
	im = Image.new('RGB',(xlength*text_dimension[0],ylength+text_dimension[1]),(255,255,255))
	draw = ImageDraw.Draw(im)
	
	for i in range(xlength):	#write the text to a region and rotate anti-clockwise and paste it back
		text_region = get_text_region(repr(i+1), (text_dimension[1], text_dimension[0]))	#text_dimension reverse because rotate
		box = (i*text_dimension[0], 0, (i+1)*text_dimension[0], text_dimension[1])
		im.paste(text_region, box)
	
	y_offset = text_dimension[1]
	for row in reader:
		for i in range(len(row)-1):	#skip the first gene id
			index = i+1
			if row[index]=='1':
				draw.rectangle((i*text_dimension[0], y_offset, index*text_dimension[0], y_offset), fill=(0,255,0))
		y_offset += 1
	del reader
	im.save(output_fname)
	del im

"""
09-26-05
	construct the cor_fname and sig_fname of a schema derived from and old schema
09-26-05
	NOTE: this function has a bug, cor_vector or sig_vector files are using haiyan's gene_index, it's
	different from schema to schema. This function ignores it.
"""
import os
def cor_sig_subset(old_datasets_mapping, new_datasets_mapping, old_schema, old_support, new_schema, \
	new_support, dir=os.path.expanduser('~/bin/hhu_clustering/data/input/')):
	import csv, Numeric, sys
	from sets import Set
	#construct the set of new datasets
	sys.stderr.write("Getting the new_datasets_set.\n")
	reader = csv.reader(file(new_datasets_mapping), delimiter='\t')
	new_datasets_set = Set()
	for row in reader:
		new_datasets_set.add(row[0])
	del reader
	
	#the index list records what we want	
	sys.stderr.write("Getting the dataset_no_ls.\n")
	reader = csv.reader(file(old_datasets_mapping), delimiter='\t')
	dataset_no_ls = [0, 1]	#0 and 1 correspond to gene_id1 and gene_id2 in cor_fname or sig_fname
	dataset_no = 1
	for row in reader:
		if row[0] in new_datasets_set:
			dataset_no_ls.append(dataset_no+1)
		dataset_no += 1
	del reader
	#start
	sys.stderr.write("Start...\n")
	old_cor_file = os.path.join(dir, '%s_%s.cor_vector'%(old_schema, old_support))
	old_sig_file = os.path.join(dir, '%s_%s.sig_vector'%(old_schema, old_support))
	new_cor_file = os.path.join(dir, '%s_%s.cor_vector'%(new_schema, new_support))
	new_sig_file = os.path.join(dir, '%s_%s.sig_vector'%(new_schema, new_support))
	reader1 = csv.reader(file(old_cor_file), delimiter='\t')
	reader2 = csv.reader(file(old_sig_file), delimiter='\t')
	writer1 = csv.writer(open(new_cor_file, 'w'), delimiter='\t')
	writer2 = csv.writer(open(new_sig_file, 'w'), delimiter='\t')
	for row1 in reader1:
		row2 = reader2.next()
		row1 = map(int, row1)	#Numeric.take is for numeric list
		row2 = map(int, row2)
		new_row1 = Numeric.take(row1, dataset_no_ls)
		new_row2 = Numeric.take(row2, dataset_no_ls)
		new_sig_vector = map(int, new_row2[2:])
		if sum(new_sig_vector)>=new_support:	#meet the new min support
			writer1.writerow(new_row1)
			writer2.writerow(new_row2)
	del reader1, reader2, writer1, writer2

"""
09-26-05
	draw a function vs condition 2D map
10-31-05 ported to DrawMaps.py
"""
def draw_function_map(good_cluster_table, output_fname, hostname='zhoudb', dbname='graphdb', schema='mm_fim_97'):
	import sys, os, Image, ImageDraw
	sys.path += [os.path.join(os.path.expanduser('~/script/annot/bin'))]
	from codense.common import db_connect, get_go_no2name
	from sets import Set
	from MpiFromDatasetSignatureToPattern import encodeOccurrenceBv, decodeOccurrenceToBv, decodeOccurrence
	(conn, curs) =  db_connect(hostname, dbname)
	no_of_datasets = 0
	go_no2name = get_go_no2name(curs, schema)
	
	go_no2recurrence_cluster_id = {}
	curs.execute("DECLARE crs CURSOR FOR SELECT mcl_id, recurrence_array, go_no_list from %s"\
		%good_cluster_table)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	while rows:
		for row in rows:
			mcl_id, recurrence_array, go_no_list = row
			recurrence_array = recurrence_array[1:-1].split(',')
			recurrence_array = map(int, recurrence_array)
			if no_of_datasets == 0:
				no_of_datasets = len(recurrence_array)
			go_no_list = go_no_list[1:-1].split(',')
			go_no_list = map(int, go_no_list)
			for go_no in go_no_list:
				if go_no not in go_no2recurrence_cluster_id:
					go_no2recurrence_cluster_id[go_no] = [encodeOccurrenceBv(recurrence_array), Set([mcl_id])]	#use Set() because mcl_id has duplicates due to different p-values
				else:
					go_no2recurrence_cluster_id[go_no][0] = go_no2recurrence_cluster_id[go_no][0] | encodeOccurrenceBv(recurrence_array)
					go_no2recurrence_cluster_id[go_no][1].add(mcl_id)
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	
	recurrence_go_no_rec_array_cluster_id_ls = []
	for go_no in go_no2recurrence_cluster_id:
		encoded_recurrence, mcl_id_set = go_no2recurrence_cluster_id[go_no]
		recurrence_array = decodeOccurrence(encoded_recurrence)	#not binary vector
		recurrence = len(recurrence_array)
		recurrence_go_no_rec_array_cluster_id_ls.append([recurrence, go_no, recurrence_array, mcl_id_set])
	
	recurrence_go_no_rec_array_cluster_id_ls.sort()
	
	char_width, char_height = get_char_dimension()
	no_of_functions = len(recurrence_go_no_rec_array_cluster_id_ls)
	dataset_no_length = len(repr(no_of_datasets))
	function_name_length = 40	#truncate if exceed
	dataset_no_dimension = (char_width*dataset_no_length, char_height)	#one is not rotated, one is rotated
	no_of_clusters_dimension = (char_width*7, char_height)	#will rotate
	function_name_dimension = (char_width*function_name_length, char_height)	#will rotate
	
	x_offset0 = 0
	x_offset1 = dataset_no_dimension[0]
	y_offset0 = 0
	y_offset1 = function_name_dimension[0]
	y_offset2 = y_offset1 + no_of_datasets*dataset_no_dimension[1]
	y_offset3 = y_offset2 + dataset_no_dimension[0]
	whole_dimension = (x_offset1+no_of_functions*char_height, \
		y_offset3+no_of_clusters_dimension[0])
	
	im = Image.new('RGB',(whole_dimension[0],whole_dimension[1]),(255,255,255))
	draw = ImageDraw.Draw(im)
	#dataset_no section
	for i in range(no_of_datasets):
		text_region = get_text_region(repr(i+1), dataset_no_dimension, rotate=0)	#no rotate
		box = (x_offset0, y_offset1+i*dataset_no_dimension[1], x_offset1, y_offset1+(i+1)*dataset_no_dimension[1])
		im.paste(text_region, box)
	#
	for i in range(len(recurrence_go_no_rec_array_cluster_id_ls)):
		recurrence, go_no, recurrence_array, mcl_id_set = recurrence_go_no_rec_array_cluster_id_ls[i]
		x_offset_left = x_offset1+i*function_name_dimension[1]
		x_offset_right = x_offset1+(i+1)*function_name_dimension[1]
		#function_name
		go_name = go_no2name[go_no]
		if len(go_name)>function_name_length:
			go_name = go_name[:function_name_length]
		text_region = get_text_region(go_name, function_name_dimension)	#rotate
		box = (x_offset_left, y_offset0, x_offset_right, y_offset1)
		im.paste(text_region, box)
		#
		for dataset_no in recurrence_array:
			draw.rectangle((x_offset_left, y_offset1+(dataset_no-1)*dataset_no_dimension[1], x_offset_right, y_offset1+dataset_no*dataset_no_dimension[1]), fill=(0,255,0))
		
		text_region = get_text_region(repr(recurrence), dataset_no_dimension)	#rotate
		box = (x_offset_left, y_offset2, x_offset_right, y_offset3)
		im.paste(text_region, box)
		
		text_region = get_text_region(repr(len(mcl_id_set)), no_of_clusters_dimension)	#rotate
		box = (x_offset_left, y_offset3, x_offset_right, whole_dimension[1])
		im.paste(text_region, box)
	im.save(output_fname)
	del im		

"""
09-26-05
	transform TF information (gene_ids and tf_names) into Darwin format	
09-28-05
       goes to Schema2Darwin.py
"""
def tf_darwin_format(cluster_bs_table, good_cluster_table, ofname, hostname='zhoudb', dbname='graphdb', schema='mm_fim_97'):
	import sys, os, csv
	sys.path += [os.path.join(os.path.expanduser('~/script/annot/bin'))]
	from codense.common import db_connect, get_gene_no2gene_id, get_mt_no2tf_name, get_mcl_id2tf_set, dict_map
	conn, curs = db_connect(hostname, dbname, schema)
	gene_no2id = get_gene_no2gene_id(curs)
	mt_no2tf_name = get_mt_no2tf_name()
	mcl_id2tf_set = get_mcl_id2tf_set(curs, cluster_bs_table, mt_no2tf_name)
	
	of = open(ofname, 'w')
	of.write('r:=[\n')
	curs.execute("DECLARE crs CURSOR FOR select mcl_id, vertex_set from %s"%good_cluster_table)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	while rows:
		for row in rows:
			mcl_id, vertex_set = row
			if mcl_id in mcl_id2tf_set:
				vertex_set = vertex_set[1:-1].split(',')
				vertex_set = map(int, vertex_set)
				vertex_set = dict_map(gene_no2id, vertex_set)
				tf_list = list(mcl_id2tf_set[mcl_id])
				tf_list = map(list, tf_list)	#first transform to list, so will have []
				for i in range(len(tf_list)):
					tf_list[i] = map(list, tf_list[i])	#one tf_list[i] is (tf_name_tuple, ratio_tuple)
				tf_list = map(repr, tf_list)	#second transform inner list to string
				row = [repr(vertex_set)] + tf_list
				of.write('[%s],\n'%(','.join(row)))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	of.write('[]]:\n')	#add the last blank list
	del of

"""
09-27-05
	construct edge_table of new_schema from old_schema's. After some datasets of old_schema
	are deleted, new_schema retains the remaining datasets order.
"""
def index_take(ls, index_list):
	ls_to_return = []
	for index in index_list:
		ls_to_return.append(ls[index])
	return ls_to_return


def edge_table_from_old_schema(old_datasets_mapping, new_datasets_mapping, old_schema, new_schema, new_support, \
	hostname='zhoudb', dbname='graphdb', edge_table='edge_cor_vector', commit=0):
	import csv, sys, os
	from sets import Set
	sys.path += [os.path.join(os.path.expanduser('~/script/annot/bin'))]
	from codense.common import db_connect, get_gene_no2gene_id, get_gene_id2gene_no, dict_map
	conn, curs = db_connect(hostname, dbname)
	old_gene_no2id = get_gene_no2gene_id(curs, old_schema)
	new_gene_id2no = get_gene_id2gene_no(curs, new_schema)
	#construct the set of new datasets
	sys.stderr.write("Getting the new_datasets_set.\n")
	reader = csv.reader(file(new_datasets_mapping), delimiter='\t')
	new_datasets_set = Set()
	for row in reader:
		new_datasets_set.add(row[0])
	del reader
	
	#the index list records what we want	
	sys.stderr.write("Getting the index_list.\n")
	reader = csv.reader(file(old_datasets_mapping), delimiter='\t')
	index_list = []
	index = 0
	for row in reader:
		if row[0] in new_datasets_set:
			index_list.append(index)
		index += 1
	del reader
	print "index_list is ",index_list
	#start
	sys.stderr.write("Start...\n")
	curs.execute("DECLARE crs CURSOR FOR SELECT edge_name, cor_vector, sig_vector from %s.%s"%\
		(old_schema, edge_table))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 0
	insert_counter = 0
	while rows:
		for row in rows:
			edge_name, cor_vector, sig_vector = row
			edge_name = edge_name[1:-1].split(',')
			edge_name = map(int, edge_name)
			gene_id_tuple = dict_map(old_gene_no2id, edge_name)
			if gene_id_tuple[0] in new_gene_id2no and gene_id_tuple[1] in new_gene_id2no:
				cor_vector = cor_vector[1:-1].split(',')
				sig_vector = sig_vector[1:-1].split(',')
				new_cor_vector = index_take(cor_vector, index_list)
				new_sig_vector = index_take(sig_vector, index_list)
				new_sig_vector_int_form = map(int, new_sig_vector)
				if sum(new_sig_vector_int_form)>=new_support:
					gene_no1 = new_gene_id2no[gene_id_tuple[0]]
					gene_no2 = new_gene_id2no[gene_id_tuple[1]]
					if gene_no1<gene_no2:
						edge_name = '{%s,%s}'%(gene_no1, gene_no2)
					else:
						edge_name = '{%s,%s}'%(gene_no2, gene_no1)
					curs.execute("insert into %s.%s(edge_name, cor_vector, sig_vector) \
						values ('%s', '{%s}', '{%s}')"%\
						(new_schema, edge_table, edge_name, ','.join(new_cor_vector), ','.join(new_sig_vector)))
					insert_counter += 1
			counter += 1
		sys.stderr.write("%s%s\t%s"%('\0x08'*20,counter, insert_counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	if commit:
		conn.commit()
		conn, curs = db_connect(hostname, dbname, new_schema)
		curs.execute("create index %s_edge_name_idx on %s(edge_name)"%(edge_table, edge_table))
		conn.commit()

"""
10-06-05
	get mcl_id2accuracy, independent version of class MpiPredictionFilter's.
10-24-05
	get it from MpiPredictionFilter
"""
def get_mcl_id2accuracy(p_gene_table, is_correct_type=2, hostname='zhoudb', dbname='graphdb', schema='hs_fim_40'):
	import csv, sys, os
	from sets import Set
	sys.path += [os.path.join(os.path.expanduser('~/script/annot/bin'))]
	from codense.common import db_connect
	from MpiPredictionFilter import prediction_attributes
	conn, curs = db_connect(hostname, dbname, schema)
	crs_sentence = 'DECLARE crs CURSOR FOR SELECT p.p_gene_id, p.gene_no, p.go_no, p.is_correct, p.is_correct_l1, \
				p.is_correct_lca, p.avg_p_value, p.no_of_clusters, p.cluster_array, p.p_value_cut_off, p.recurrence_cut_off, \
				p.connectivity_cut_off, p.cluster_size_cut_off, p.unknown_cut_off, p.depth_cut_off, p.mcl_id, p.lca_list, \
				p.vertex_gradient, p.edge_gradient from %s p'%(p_gene_table)
	"""
	crs_sentence = 'DECLARE crs CURSOR FOR SELECT p_gene_id, gene_no, go_no, is_correct, is_correct_l1, \
			is_correct_lca, avg_p_value, no_of_clusters, cluster_array, p_value_cut_off, recurrence_cut_off, \
			connectivity_cut_off, cluster_size_cut_off, unknown_cut_off, depth_cut_off, mcl_id, lca_list  \
			from %s'%p_gene_table
	"""
	curs.execute("%s"%crs_sentence)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 0
	mcl_id2accuracy = {}
	while rows:
		for row in rows:
			prediction_attr_instance = prediction_attributes(row)
			if prediction_attr_instance.mcl_id not in mcl_id2accuracy:
				mcl_id2accuracy[prediction_attr_instance.mcl_id]  = []
			mcl_id2accuracy[prediction_attr_instance.mcl_id].append(prediction_attr_instance.is_correct_dict[is_correct_type])
			
			counter += 1
		sys.stderr.write("%s%s"%('\x08'*20, counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")
	for mcl_id, is_correct_ls in mcl_id2accuracy.iteritems():
		only_one_ls = map((lambda x: int(x>=1)), is_correct_ls)	#10-12-05 only correct(1) predictions are counted as 1
		one_or_zero_ls = map((lambda x: int(x>=0)), is_correct_ls)	#10-12-05 only correct(1) or wrong(0) are counted as 1, -1 is discarded
		if sum(one_or_zero_ls)==0:	#10-16-05	avoid the sum to be zero
			mcl_id2accuracy[mcl_id]=0
		else:
			accuracy = sum(only_one_ls)/float(sum(one_or_zero_ls))	#10-12-05 sum the one_or_zero_ls
			mcl_id2accuracy[mcl_id] = accuracy
	sys.stderr.write(" %s clusters. Done.\n"%len(mcl_id2accuracy))
	return mcl_id2accuracy

def return_mcl_id_list_given_acc_range(mcl_id2accuracy, min_acc, max_acc):
	mcl_id_list = []
	for mcl_id, accuracy in mcl_id2accuracy.iteritems():
		if accuracy>=min_acc and accuracy<=max_acc:
			mcl_id_list.append(mcl_id)
	return mcl_id_list

"""
10-24-05
"""
def partition_mcl_id_into_gaps_based_on_accuracy(mcl_id2accuracy):
	mcl_id_gap_list = []
	for i in range(10):
		mcl_id_gap_list.append([])
	for mcl_id, accuracy in mcl_id2accuracy.iteritems():
		if accuracy>=0.0 and accuracy<0.1:
			mcl_id_gap_list[0].append(mcl_id)
		elif accuracy>=0.1 and accuracy<0.2:
			mcl_id_gap_list[1].append(mcl_id)
		elif accuracy>=0.2 and accuracy<0.3:
			mcl_id_gap_list[2].append(mcl_id)
		elif accuracy>=0.3 and accuracy<0.4:
			mcl_id_gap_list[3].append(mcl_id)
		elif accuracy>=0.4 and accuracy<0.5:
			mcl_id_gap_list[4].append(mcl_id)
		elif accuracy>=0.5 and accuracy<0.6:
			mcl_id_gap_list[5].append(mcl_id)
		elif accuracy>=0.6 and accuracy<0.7:
			mcl_id_gap_list[6].append(mcl_id)
		elif accuracy>=0.7 and accuracy<0.8:
			mcl_id_gap_list[7].append(mcl_id)
		elif accuracy>=0.8 and accuracy<0.9:
			mcl_id_gap_list[8].append(mcl_id)
		elif accuracy>=0.9 and accuracy<=1.0:
			mcl_id_gap_list[9].append(mcl_id)
	return mcl_id_gap_list

"""
10-24-05
"""
def	get_mcl_id2gradient_score_list(p_gene_table, hostname='zhoudb', dbname='graphdb', schema='hs_fim_40'):
	import csv, sys, os
	sys.path += [os.path.join(os.path.expanduser('~/script/annot/bin'))]
	from codense.common import db_connect
	from MpiPredictionFilter import prediction_attributes
	conn, curs = db_connect(hostname, dbname, schema)
	crs_sentence = 'DECLARE crs CURSOR FOR SELECT p.p_gene_id, p.gene_no, p.go_no, p.is_correct, p.is_correct_l1, \
				p.is_correct_lca, p.avg_p_value, p.no_of_clusters, p.cluster_array, p.p_value_cut_off, p.recurrence_cut_off, \
				p.connectivity_cut_off, p.cluster_size_cut_off, p.unknown_cut_off, p.depth_cut_off, p.mcl_id, p.lca_list, \
				p.vertex_gradient, p.edge_gradient from %s p'%(p_gene_table)
	"""
	crs_sentence = 'DECLARE crs CURSOR FOR SELECT p_gene_id, gene_no, go_no, is_correct, is_correct_l1, \
			is_correct_lca, avg_p_value, no_of_clusters, cluster_array, p_value_cut_off, recurrence_cut_off, \
			connectivity_cut_off, cluster_size_cut_off, unknown_cut_off, depth_cut_off, mcl_id, lca_list  \
			from %s'%p_gene_table
	"""
	curs.execute("%s"%crs_sentence)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 0
	mcl_id2gradient_score_list = {}
	while rows:
		for row in rows:
			prediction_attr_instance = prediction_attributes(row)
			if prediction_attr_instance.mcl_id not in mcl_id2gradient_score_list:
				mcl_id2gradient_score_list[prediction_attr_instance.mcl_id]  = []
			mcl_id2gradient_score_list[prediction_attr_instance.mcl_id].append(prediction_attr_instance.p_value_cut_off)
			
			counter += 1
		sys.stderr.write("%s%s"%('\x08'*20, counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")
	sys.stderr.write(" %s clusters. Done.\n"%len(mcl_id2gradient_score_list))
	return mcl_id2gradient_score_list

"""
10-24-05 for a certain accuracy range, see the distribution of the gradient scores
"""
def partition_gradient_score_based_on_cluster_accuracy(mcl_id2gradient_score_list, mcl_id2accuracy):
	gradient_score_list_gap_list = []
	for i in range(10):
		gradient_score_list_gap_list.append([])
	for mcl_id, gradient_score_list in mcl_id2gradient_score_list.iteritems():
		accuracy = mcl_id2accuracy[mcl_id]
		if accuracy>=0.0 and accuracy<0.1:
			gradient_score_list_gap_list[0] += gradient_score_list
		elif accuracy>=0.1 and accuracy<0.2:
			gradient_score_list_gap_list[1] += gradient_score_list
		elif accuracy>=0.2 and accuracy<0.3:
			gradient_score_list_gap_list[2] += gradient_score_list
		elif accuracy>=0.3 and accuracy<0.4:
			gradient_score_list_gap_list[3] += gradient_score_list
		elif accuracy>=0.4 and accuracy<0.5:
			gradient_score_list_gap_list[4] += gradient_score_list
		elif accuracy>=0.5 and accuracy<0.6:
			gradient_score_list_gap_list[5] += gradient_score_list
		elif accuracy>=0.6 and accuracy<0.7:
			gradient_score_list_gap_list[6] += gradient_score_list
		elif accuracy>=0.7 and accuracy<0.8:
			gradient_score_list_gap_list[7] += gradient_score_list
		elif accuracy>=0.8 and accuracy<0.9:
			gradient_score_list_gap_list[8] += gradient_score_list
		elif accuracy>=0.9 and accuracy<=1.0:
			gradient_score_list_gap_list[9] += gradient_score_list
	return gradient_score_list_gap_list

def get_gene_set_given_mcl_id_ls(mcl_id_list, input_fname, acc_cut_off=0.6, hostname='zhoudb', dbname='graphdb', schema='hs_fim_40'):
	import csv, sys, os
	from sets import Set
	sys.path += [os.path.join(os.path.expanduser('~/script/annot/bin'))]
	from codense.common import db_connect, form_schema_tables
	conn, curs = db_connect(hostname, dbname, schema)
	schema_instance = form_schema_tables(input_fname, acc_cut_off)
	gene_set = Set()
	mcl_id_set = Set(mcl_id_list)
	curs.execute("DECLARE crs CURSOR FOR select mcl_id, vertex_set from %s"%schema_instance.mcl_table)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	while rows:
		for row in rows:
			mcl_id, vertex_set = row
			if mcl_id in mcl_id_set:
				vertex_set = vertex_set[1:-1].split(',')
				vertex_set = map(int, vertex_set)
				gene_set |= Set(vertex_set)
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	return gene_set

"""
10-14-05
"""
def p_gene_id_set_from_gene_p_table(gene_p_table, hostname='zhoudb', dbname='graphdb', schema='sc_new_38'):
	from sets import Set
	p_gene_id_set = Set()
	from codense.common import db_connect
	import psycopg
	conn, curs = db_connect(hostname, dbname, schema)
	curs.execute("select p_gene_id from %s"%gene_p_table)
	rows = curs.fetchall()
	for row in rows:
		p_gene_id = row[0]
		p_gene_id_set.add(p_gene_id)
	return p_gene_id_set

"""
10-17-05
	choose predictions given a p_gene_id_set
"""
def p_gene_table_transfer_given_p_gene_id_set(old_p_gene_table, new_p_gene_table, p_gene_id_set, hostname='zhoudb', dbname='graphdb', schema='hs_fim_40'):
	from sets import Set
	import sys, os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from codense.common import db_connect, p_gene_id_set_from_gene_p_table
	from MpiPredictionFilter import MpiPredictionFilter, prediction_attributes
	conn, curs = db_connect(hostname, dbname, schema)
	MpiPredictionFilter_instance = MpiPredictionFilter()
	MpiPredictionFilter_instance.createGeneTable(curs, new_p_gene_table)
	crs_sentence = "DECLARE crs CURSOR FOR SELECT p.p_gene_id, p.gene_no, p.go_no, p.is_correct, p.is_correct_l1, \
		p.is_correct_lca, p.avg_p_value, p.no_of_clusters, p.cluster_array, p.p_value_cut_off, p.recurrence_cut_off, \
		p.connectivity_cut_off, p.cluster_size_cut_off, p.unknown_cut_off, p.depth_cut_off, p.mcl_id, p.lca_list, p.vertex_gradient,\
		p.edge_gradient, 'vertex_set', 'edge_set', 'd_matrix', 'recurrence_array' \
		from %s p"%(old_p_gene_table)
	curs.execute("%s"%(crs_sentence))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 0
	while rows:
		for row in rows:
			p_attr_instance = prediction_attributes(row, type=3)
			counter += 1
			if p_attr_instance.p_gene_id in p_gene_id_set:
				MpiPredictionFilter_instance.submit_to_p_gene_table(curs, new_p_gene_table, p_attr_instance)
		sys.stderr.write("%s%s"%('\x08'*20, counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute("end")
	del conn, curs

"""
10-30-05
	step 1: find_low_density_pattern()
		low_density_pattern: no_of_edges = no_of_vertices-1
	step 2: filter_low_density_pattern()
		one d_row in d_matrix should be = range(no_of_vertices)
"""
def find_low_density_pattern(curs, good_cluster_table, schema='hs_fim_92'):
	import sys,os
	from sets import Set
	curs.execute("set search_path to %s"%schema)
	curs.execute("DECLARE crs CURSOR FOR SELECT mcl_id, recurrence, connectivity, \
		size, go_no_list from %s"%good_cluster_table)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	ls_to_return = []
	counter = 0
	real_counter =0
	while rows:
		for row in rows:
			mcl_id, recurrence, connectivity, size, go_no_list = row
			go_no_list = go_no_list[1:-1].split(',')
			go_no_list = map(int, go_no_list)
			go_no_set = Set(go_no_list)
			no_of_edges = connectivity*size*(size-1)/2	#this is a float
			if (size-no_of_edges-1) <0.001 and (size-no_of_edges-1)> -0.001:
				ls_to_return.append([recurrence, size, mcl_id, go_no_set])
				real_counter += 1
			counter += 1
		sys.stderr.write("%s%s/%s"%('\x08'*20, counter, real_counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")
	ls_to_return.sort()
	return ls_to_return

def filter_low_density_pattern(input_ls, pattern_table, schema='scfim30'):
	import sys,os
	curs.execute("set search_path to %s"%schema)
	ls_to_return = []
	for row in input_ls:
		recurrence, size, mcl_id, go_no_set = row
		curs.execute("select d_matrix from %s where id=%s"%(pattern_table, mcl_id))
		rows = curs.fetchall()
		d_matrix = rows[0][0]
		d_matrix = d_matrix[2:-2].split('},{')
		d_row_for_line_pattern = range(size)
		for d_row in d_matrix:
			d_row = d_row.split(',')
			d_row = map(int, d_row)
			d_row.sort()
			if d_row == d_row_for_line_pattern:
				ls_to_return.append(row)
	return ls_to_return

"""
10-30-05 try to find a pattern with >=2 distinct function centers
	patterns_with_multiple_functions() is step 1.
	filter_patterns_with_m_functions() is step 2.
"""
def patterns_with_multiple_functions(curs, good_cluster_table, schema='scfim30'):
	import sys,os
	from sets import Set
	curs.execute("set search_path to %s"%schema)
	curs.execute("DECLARE crs CURSOR FOR SELECT mcl_id, connectivity, \
		size, go_no_list from %s"%good_cluster_table)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	ls_to_return = []
	counter = 0
	real_counter =0
	while rows:
		for row in rows:
			mcl_id, connectivity, size, go_no_list = row
			go_no_list = go_no_list[1:-1].split(',')
			go_no_list = map(int, go_no_list)
			go_no_set = Set(go_no_list)
			if len(go_no_set)>=2 and size>12:	#
				ls_to_return.append(row)
				real_counter += 1
			counter += 1
		sys.stderr.write("%s%s/%s"%('\x08'*20, counter, real_counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")
	return ls_to_return

"""
any two go_no doesn't share word
"""
def filter_ls_above(input_ls, curs, schema='scfim30'):
	from sets import Set
	import sys, os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from codense.common import get_go_no2name
	go_no2name = get_go_no2name(curs)
	go_no2split_name_set = {}
	for go_no, name in go_no2name.iteritems():
		split_name_set = Set(name.split())
		go_no2split_name_set[go_no] = split_name_set
	
	ls_to_return = []
	for row in input_ls:
		mcl_id, connectivity, size, go_no_list = row
		go_no_list = go_no_list[1:-1].split(',')
		go_no_list = map(int, go_no_list)
		go_no_set = Set(go_no_list)
		go_no_list = list(go_no_set)
		to_break = 0
		for i in range(len(go_no_list)):
			for j in range(i, len(go_no_list)):
				if len(go_no2split_name_set[go_no_list[i]]&go_no2split_name_set[go_no_list[j]])==0:
					ls_to_return.append([mcl_id, connectivity, size, go_no_set])
					to_break = 1
					break
			if to_break == 1:
				break
	return ls_to_return
	
"""
all go_nos don't share word
"""

def filter_ls_above_2(input_ls, curs, max_bad=1, schema='scfim30'):
	from sets import Set
	import sys, os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from codense.common import get_go_no2name
	go_no2name = get_go_no2name(curs)
	go_no2split_name_set = {}
	for go_no, name in go_no2name.iteritems():
		split_name_set = Set(name.split())
		go_no2split_name_set[go_no] = split_name_set
	
	ls_to_return = []
	for row in input_ls:
		mcl_id, connectivity, size, go_no_list = row
		go_no_list = go_no_list[1:-1].split(',')
		go_no_list = map(int, go_no_list)
		go_no_set = Set(go_no_list)
		go_no_list = list(go_no_set)
		to_break = 0
		bad = 0
		for i in range(len(go_no_list)):
			for j in range(i, len(go_no_list)):
				if len(go_no2split_name_set[go_no_list[i]]&go_no2split_name_set[go_no_list[j]])>0:
					bad += 1
		if bad <=max_bad and len(go_no_set)>=2+max_bad:
			ls_to_return.append([mcl_id, connectivity, size, go_no_set])
	return ls_to_return
	
def filter_by_size(input_ls, min_size, max_size):
	ls_to_return = []
	for row in input_ls:
		mcl_id, connectivity, size, go_no_list = row
		if size>=min_size and size<=max_size:
			ls_to_return.append(row)
	return ls_to_return

def filter_by_function_not(input_ls, given_go_no_set):
	ls_to_return = []
	for row in input_ls:
		mcl_id, connectivity, size, go_no_set = row
		if len(given_go_no_set&go_no_set)==0:
			ls_to_return.append(row)
	return ls_to_return

def filter_by_function_in(input_ls, given_go_no_set):
	ls_to_return = []
	for row in input_ls:
		mcl_id, connectivity, size, go_no_set = row
		if given_go_no_set&go_no_set==given_go_no_set:
			ls_to_return.append(row)
	return ls_to_return

"""
10-31-05 parse the altsplice files and output id:no_of_splicing_events
"""
def altsplice_parse(input_fname, output_fname):
	import sys, os
	sys.path += [os.path.expanduser('~/script/transfac/src')]
	from transfacdb import fasta_block_iterator
	import cStringIO
	inf = open(input_fname,'r')
	outf = open(output_fname, 'w')
	iter = fasta_block_iterator(inf)
	for block in iter:
		block = cStringIO.StringIO(block)
		header_line = block.readline()
		ensembl_id = header_line[1:-1]
		no_of_splicing_events = 0
		for line in block:
			if line[:6] == 'Class ':
				no_of_splicing_events += 1
			else:
				break
		outf.write('%s\t%s\n'%(ensembl_id, no_of_splicing_events))
	del inf, outf

"""
10-31-05 parse the ensembl embl format files and get the mapping between ensembl_id and EntrezGene
	embl_ft_block_iterator
	get_ensembl_id2EntrezGene()
"""
class embl_ft_block_iterator:
	'''
	10-31-05 embl format FT block iterator.(similar to fasta_block_iterator)
		1. begin with 'FT'
		2. the first line of the block, position 5 contains gene, mRNA, CDS or misc_RNA
	'''
	def __init__(self, inf):
		self.inf = inf
		self.block = ''
		self.previous_line = ''
	def __iter__(self):
		return self
	def next(self):
		self.read()
		return self.block
	def read(self):
		self.block = self.previous_line	#don't forget the starting line
		for line in self.inf:
			if line[:2] == 'FT':
				feature_key = line[5:]
				if feature_key.find('gene')==0 or feature_key.find('mRNA')==0 or \
					feature_key.find('CDS')==0 or feature_key.find('misc_RNA')==0:
					self.previous_line = line
					if self.block:	#not the first time
						break
					else:	#first time to read the file, block is still empty
						self.block += line
				else:
					self.block += line
		if self.block==self.previous_line:
			raise StopIteration

def get_ensembl_id2EntrezGene(input_dir, output_fname):
	import sys, os, gzip, cStringIO
	files = os.listdir(input_dir)
	outf = open(output_fname, 'w')
	sys.stderr.write("\tTotally, %d files to be processed.\n"%len(files))
	for f in files:
		pathname = os.path.join(input_dir, f)
		sys.stderr.write("%d/%d:\t%s\n"%(files.index(f)+1,len(files),f))
		inf = gzip.open(pathname,'r')
		iter = embl_ft_block_iterator(inf)
		for block in iter:
			ensembl_id = ''
			block = cStringIO.StringIO(block)
			block.readline()	#discard firstline
			for line in block:
				qualifier_line = line[21:]
				if qualifier_line.find('/gene=')==0:	#eg: /gene=ENSMUSG00000069462 or /gene="ENSMUSG00000069462"
					ensembl_id = qualifier_line[6:-1]	#discard the newline
					#when it's 'gene' FT, there's no '"'
					if ensembl_id[0]=='"':
						ensembl_id = ensembl_id[1:]
					if ensembl_id[-1] == '"':
						ensembl_id = ensembl_id[:-1]
				if ensembl_id and qualifier_line.find('/db_xref="EntrezGene:')==0:	#eg: /db_xref="EntrezGene:385528"\n
					EntrezGene_id = qualifier_line[21:-2]	#discard the new line and double quote
					outf.write('%s\t%s\n'%(ensembl_id, EntrezGene_id))
		del inf
	del outf

"""
11-01-05 filter cluster_bs_table
"""
def filter_cluster_bs_table(curs, cluster_bs_table, output_table, top_number, commit=0):
	import sys,os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from TF_functions import hq_add
	from heapq import heappush, heappop, heapreplace
	
	score_id_hq = []
	mcl_id_no_of_bs2frequency = {}
	curs.execute("DECLARE crs CURSOR FOR select id,score,mcl_id,array_upper(bs_no_list,1)  from %s where \
		score_type=1"%(cluster_bs_table))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 1
	while rows:
		for row in rows:
			id, score, mcl_id, no_of_bs = row
			key = (mcl_id, no_of_bs)
			if key not in mcl_id_no_of_bs2frequency:
				mcl_id_no_of_bs2frequency[key] = 0
			mcl_id_no_of_bs2frequency[key] += 1
			if mcl_id_no_of_bs2frequency[key]<=2: #just take top 2 for each type and each mcl_id
				hq_add(score_id_hq, [-score, id, mcl_id], top_number)	#WATCH: min_heap, minus ahead
			counter += 1
		sys.stderr.write("%s%s"%('\x08'*20, counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")
	
	curs.execute("create table %s(\
		id	serial primary key,\
		cluster_bs_id	integer,\
		mcl_id integer)"%(output_table))
	
	while score_id_hq:
		score, id, mcl_id = heappop(score_id_hq)
		score = -score
		curs.execute("insert into %s(cluster_bs_id, mcl_id) values(%s, %s)"%(output_table, id, mcl_id))
	if commit:
		curs.execute("end")

"""
11-01-05 get the average no_of_events (alternative splicing) for each no_of_p_funcs2gene_set.
"""
def pleiotropy2as(picklefile, gene_no2no_of_events):
	import cPickle
	no_of_p_funcs2gene_set = cPickle.load(open(picklefile))
	no_of_p_funcs2avg_events = {}
	max_no_of_p_funcs = 0
	for no_of_p_funcs, gene_set in no_of_p_funcs2gene_set.iteritems():
		if no_of_p_funcs>max_no_of_p_funcs:
			max_no_of_p_funcs = no_of_p_funcs
		events_ls = []
		for gene_no in gene_set:
			if gene_no in gene_no2no_of_events:
				events_ls.append(gene_no2no_of_events[gene_no])
			else:
				events_ls.append(1)
		avg_events = sum(events_ls)/float(len(events_ls))
		no_of_p_funcs2avg_events[no_of_p_funcs] = avg_events
	
	avg_events_vs_no_of_p_funcs = [0]*max_no_of_p_funcs
	for no_of_p_funcs, avg_events in no_of_p_funcs2avg_events.iteritems():
		avg_events_vs_no_of_p_funcs[no_of_p_funcs-1] = avg_events
	return avg_events_vs_no_of_p_funcs

"""
11-29-05 learn from Kopelman2005, using Fraction AS
"""
def pleiotropy2fraction_as(picklefile, gene_no2no_of_events):
	import cPickle
	no_of_p_funcs2gene_set = cPickle.load(open(picklefile))
	no_of_p_funcs2fraction_as = {}
	max_no_of_p_funcs = 0
	for no_of_p_funcs, gene_set in no_of_p_funcs2gene_set.iteritems():
		if no_of_p_funcs>max_no_of_p_funcs:
			max_no_of_p_funcs = no_of_p_funcs
		no_of_genes_with_as = 0
		for gene_no in gene_set:
			if gene_no in gene_no2no_of_events:
				if gene_no2no_of_events[gene_no]>=2:	#more than one is counted as having AS
					no_of_genes_with_as += 1
		no_of_p_funcs2fraction_as[no_of_p_funcs] = float(no_of_genes_with_as)/len(gene_set)
	#convert to a histogram-like list
	fraction_as_vs_no_of_p_funcs = [0]*max_no_of_p_funcs
	for no_of_p_funcs, fraction_as in no_of_p_funcs2fraction_as.iteritems():
		fraction_as_vs_no_of_p_funcs[no_of_p_funcs-1] = fraction_as
	return fraction_as_vs_no_of_p_funcs
	


"""
11-02-05 find patterns from good_cluster_table given a go_no_set and output them
"""
def find_patterns_given_go_no_set(curs, schema_instance, given_go_no_set, pic_output_dir):
	import sys, os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from sets import Set
	from codense.common import get_gene_no2gene_id, get_gene_no2go_no
	from cluster_info import cluster_info	#transform vertex_set and edge_set into subgraph
	from codense.common import system_call, graphDotOutput
	
	gene_no2gene_id = get_gene_no2gene_id(curs)
	gene_no2go_no = get_gene_no2go_no(curs)
	
	cluster_info_instance = cluster_info()
	
	curs.execute("DECLARE crs CURSOR FOR select mcl_id, go_no_list from %s"%schema_instance.good_cluster_table)
	curs.execute("fetch 10000 from crs")
	rows = curs.fetchall()
	counter = 0
	real_counter = 0
	while rows:
		for row in rows:
			mcl_id, go_no_list = row
			go_no_list = go_no_list[1:-1].split(',')
			go_no_list = map(int, go_no_list)
			go_no_set = Set(go_no_list)
			join_go_no_set = go_no_set&given_go_no_set
			if join_go_no_set:
				curs.execute("select vertex_set, edge_set from %s where id=%s"%(schema_instance.pattern_table,mcl_id))
				rows = curs.fetchall()
				
				#draw graph
				vertex_set, edge_set = rows[0]
				vertex_set = vertex_set[1:-1].split(',')
				vertex_set = map(int, vertex_set)
				edge_set = edge_set[2:-2].split('},{')
				for i in range(len(edge_set)):
					edge_set[i] = edge_set[i].split(',')
					edge_set[i] = map(int, edge_set[i])
				#following copied from GuiAnalyzer.py
				for go_no in join_go_no_set:
					subgraph = cluster_info_instance.graph_from_node_edge_set(vertex_set, edge_set)
					graphSrcFname = '/tmp/GuiAnalyzer.dot'
					graphFname = os.path.join(pic_output_dir, '%s_%s.png'%(go_no, mcl_id))
					graphSrcF = open(graphSrcFname, 'w')
					graphDotOutput(graphSrcF, subgraph, gene_no2gene_id, gene_no2go_no, \
						function=go_no, weighted=0)
					graphSrcF.close()
					plot_type_command='neato -Goverlap=false'
					commandline = '%s -Tpng %s -o %s'%(plot_type_command, graphSrcFname, graphFname)
					system_call(commandline)
				real_counter += 1
				
			counter += 1
		sys.stderr.write("%s%s/%s"%('\x08'*20, counter, real_counter))
		curs.execute("fetch 10000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")

"""
11-16-05
	to confirm Fei's hypergeometric p-value on two clusters. See his 11/14/05 email.
"""
def get_gene_no_set_from_fei_file(input_fname):
	import csv
	from sets import Set
	reader = csv.reader(open(input_fname))
	gene_no_set = Set()
	for row in reader:
		gene_no = int(row[0])
		gene_no_set.add(gene_no)
	return gene_no_set
	
def get_go_no2gene_no_set_from_fei_file(input_fname, gene_no_set):
	from sets import Set
	inf = open(input_fname)
	#skip the first line
	inf.readline()
	import csv
	reader = csv.reader(inf, delimiter=';')
	go_no2gene_no_set = {}
	gene_no2go_no_set = {}
	for row in reader:
		gene_no, go_no = row
		gene_no = int(gene_no)
		if gene_no in gene_no_set:
			if go_no not in go_no2gene_no_set:
				go_no2gene_no_set[go_no]  = Set()
			go_no2gene_no_set[go_no].add(gene_no)
			if gene_no not in gene_no2go_no_set:
				gene_no2go_no_set[gene_no] = Set()
			gene_no2go_no_set[gene_no].add(go_no)
	del reader, inf
	return go_no2gene_no_set, gene_no2go_no_set

def cal_all_p_values(vertex_list, no_of_total_genes, go_no2gene_no_set, gene_no2go_no_set, debug=0):
	from sets import Set
	from rpy import r
	local_go_no2no_of_genes = {}
	for vertex in vertex_list:
		for go_no in gene_no2go_no_set[vertex]:
			if go_no not in local_go_no2no_of_genes:
				local_go_no2no_of_genes[go_no] = 0
			local_go_no2no_of_genes[go_no] += 1
	
	p_value_go_no_list = []
	cluster_size = len(vertex_list)
	for go_no, no_of_genes in local_go_no2no_of_genes.iteritems():
		x = no_of_genes
		m = len(go_no2gene_no_set[go_no])
		n = no_of_total_genes - m	#11-18-05 fix a bug here
		k = cluster_size
		
		if debug:
			print "x",x
			print "m",m
			print "n",n
			print "k", k
		
		p_value = r.phyper(x-1,m,n,k,lower_tail = r.FALSE)
		p_value_go_no_list.append([p_value, go_no])
	return p_value_go_no_list
	
	

"""
11-16-05
"""
def output_ls_in_stx_table_format(ls, row_length):
	"""
	one dimension
	"""
	row_delimiter =  '|'+'-'*row_length+'|'
	print row_delimiter
	for item in ls:
		print '|' + item.ljust(row_length) + '|'
		print row_delimiter

def output_2d_ls_in_stx_table_format(ls, row_length_ls):
	row_delimiter =  '|'+'-'*row_length_ls[0]+'|'+'-'*row_length_ls[1]+'|'
	print row_delimiter
	for item in ls:
		print '|' + item[0].ljust(row_length_ls[0]) + '|' + repr(item[1]).ljust(row_length_ls[1]) + '|'
		print row_delimiter

"""
11-19-05
"""
def get_unknown_gene_set_from_p_gene_table_vg_1(curs, p_gene_table):
	from sets import Set
	curs.execute("DECLARE crs CURSOR FOR select gene_no from %s where vertex_gradient=1 \
		and is_correct_lca=-1"%(p_gene_table))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	gene_set = Set()
	while rows:
		for row in rows:
			gene_set.add(row[0])
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute('close crs')
	return gene_set

def unknown_gene_set_from_gene_p_table(curs, p_gene_table, gene_p_table):
	from sets import Set
	from codense.common import db_connect
	gene_set = Set()
	#first get all good p_gene_id's
	curs.execute("DECLARE crs CURSOR FOR select p_gene_id from %s"%gene_p_table)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	p_gene_id_set  = Set()
	counter  =0
	while rows:
		for  row in rows:
			p_gene_id_set.add(row[0])
			counter += 1
		sys.stderr.write('%s%s'%('\x08'*20,counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute('close crs')
	
	curs.execute("DECLARE crs CURSOR FOR select p.p_gene_id, p.gene_no,p.is_correct_lca from %s p"%\
		(p_gene_table))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 0
	while rows:
		for row in rows:
			p_gene_id, gene_no, is_correct_lca= row
			if p_gene_id in p_gene_id_set and is_correct_lca==-1:
				gene_set.add(gene_no)
			counter += 1
		sys.stderr.write('%s%s'%('\x08'*20,counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute('close crs')
	
	return gene_set
"""
11-27-05
"""
def get_gene2freq_from_prediction_pair2freq(prediction_pair2freq):
	gene2freq = {}
	for prediction_pair, freq in prediction_pair2freq.iteritems():
		gene_no, go_no = prediction_pair
		if gene_no not in gene2freq:
			gene2freq[gene_no] = 0
		if freq>gene2freq[gene_no]:
			gene2freq[gene_no] = freq
	return gene2freq

"""
11-29-05
	get ensembl_id2no_of_promoters from Kim2005 supplemental table S4
"""
def get_ensembl_id2no_of_promoters(input_fname):
	import csv
	ensembl_id2no_of_promoters = {}
	reader = csv.reader(open(input_fname), delimiter='\t')
	#skip the 1st and 2nd line
	reader.next()
	reader.next()
	for row in reader:
		ensembl_id = row[0]
		dot_index = ensembl_id.find('.')
		if dot_index!=-1:
			ensembl_id = ensembl_id[:dot_index]
		no_of_promoters = int(row[2])
		ensembl_id2no_of_promoters[ensembl_id] = no_of_promoters
	del reader
	
	#output
	output_f = open('/tmp/ensembl_id2no_of_promoters', 'w')
	for ensembl_id, no_of_promoters in ensembl_id2no_of_promoters.iteritems():
		output_f.write('%s\t%s\n'%(ensembl_id, no_of_promoters))
	del output_f
	return ensembl_id2no_of_promoters

"""
12-04-05
"""
def cal_multi_fraction(ls):
	multi_number = sum(ls[1:])
	return float(multi_number)/sum(ls)

"""
12-06-05
"""
def get_gene_no2rank(gene_no_dict):
	value_gene_no_ls = []
	for gene_no, value in gene_no_dict.iteritems():
		value_gene_no_ls.append([value, gene_no])
	value_gene_no_ls.sort()
	
	
"""
12-06-05
"""
def filter_fim_output(input_fname, output_fname, min_support, max_support):
	inf = open(input_fname, 'r')
	outf = open(output_fname, 'w')
	for line in inf:
		row = line.split()
		if len(row)>=min_support and len(row)<=max_support:
			outf.write('%s'%line)
	del inf, outf


"""
12-07-05
import sys, os
sys.path += [os.path.expanduser('~/script/annot/bin')]
from codense.common import fill_edge2encodedOccurrence, db_connect
hostname='zhoudb'
dbname='graphdb'
schema='scfim30'
conn, curs = db_connect(hostname, dbname, schema)
edge2encodedOccurrence, no_of_datasets = fill_edge2encodedOccurrence(curs, 0, 500)
"""
def get_occurrent_dataset_ls(recurrence_array):
	occurrent_dataset_ls = []
	for i in range(len(recurrence_array)):
		if recurrence_array[i] == 1.0:
			occurrent_dataset_ls.append(i)	#starts from 0
	return occurrent_dataset_ls
	

def cal_original_density(curs, pattern_table, edge2encodedOccurrence, no_of_datasets, \
	min_density, max_density, edge_table='edge_cor_vector'):
	import sys, os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from MpiFromDatasetSignatureToPattern import decodeOccurrenceToBv
	curs.execute("DECLARE crs CURSOR FOR SELECT id, vertex_set, connectivity, recurrence_array from %s"%(pattern_table))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 0
	real_counter = 0
	real_counter2 = 0
	density_ls = []
	while rows:
		for row in rows:
			id, vertex_set, connectivity, recurrence_array = row
			if connectivity>=min_density and connectivity<=max_density:
				vertex_set = vertex_set[1:-1].split(',')
				vertex_set = map(int, vertex_set)
				no_of_nodes = len(vertex_set)
				recurrence_array = recurrence_array[1:-1].split(',')
				recurrence_array = map(float, recurrence_array)
				#only the on datasets, starting from 0
				occurrent_dataset_ls = get_occurrent_dataset_ls(recurrence_array)
				
				no_of_edges_vector = [0]*no_of_datasets
				for i in range(no_of_nodes):
					for j in range(i+1, no_of_nodes):
						edge_tuple = (vertex_set[i], vertex_set[j])
						if edge_tuple in edge2encodedOccurrence:
							sig_vector = decodeOccurrenceToBv(edge2encodedOccurrence[edge_tuple], no_of_datasets)
							for k in occurrent_dataset_ls:	#only the on datasets
								if sig_vector[k] == 1:
									no_of_edges_vector[k] += 1
				#calculate the density in each original dataset, only the on datasets
				total_low = 1
				for i in occurrent_dataset_ls:
					original_density = no_of_edges_vector[i]*2.0/(no_of_nodes*(no_of_nodes-1))	#WATCH 2.0(float)
					if original_density>=0.5:	#not all original_density is low
						total_low = 0
					density_ls.append(original_density)
				real_counter += 1
				if total_low:
					real_counter2 += 1
			counter += 1
		sys.stderr.write("%s%s\t%s\t%s"%('\x08'*30, counter, real_counter, real_counter2))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")
	return density_ls

"""
12-12-05
"""
def get_gene_no2no_of_functions_from_picklefile(picklefile):
	sys.stderr.write('Getting gene_no2no_of_functions from picklefile...')
	import cPickle
	no_of_p_funcs2gene_set = cPickle.load(open(picklefile))
	gene_no2no_of_functions = {}
	for no_of_p_funcs, gene_set in no_of_p_funcs2gene_set.iteritems():
		for gene_no in gene_set:
			gene_no2no_of_functions[gene_no] = no_of_p_funcs
	sys.stderr.write("Done.\n")
	return gene_no2no_of_functions


"""
12-12-05
"""
def get_avg_no_of_functions_vs_gene_age(gene_no2no_of_functions, gene_no2ca_depth):
	sys.stderr.write('Getting avg_no_of_functions_vs_gene_age...')
	ca_depth2no_of_functions_ls = {}
	for gene_no, ca_depth in gene_no2ca_depth.iteritems():
		if gene_no in gene_no2no_of_functions:
			if ca_depth not in ca_depth2no_of_functions_ls:
				ca_depth2no_of_functions_ls[ca_depth] = []
			ca_depth2no_of_functions_ls[ca_depth].append(gene_no2no_of_functions[gene_no])
	ca_depth_ls = []
	avg_no_of_functions_ls = []
	no_of_genes_ls = []
	for ca_depth, no_of_functions_ls in ca_depth2no_of_functions_ls.iteritems():
		ca_depth_ls.append(ca_depth)
		avg_no_of_functions_ls.append(sum(no_of_functions_ls)/float(len(no_of_functions_ls)))
		no_of_genes_ls.append(len(no_of_functions_ls))
	sys.stderr.write("Done.\n")
	return ca_depth_ls, avg_no_of_functions_ls, no_of_genes_ls

"""
12-14-05
	consider the family_size
"""
def get_avg_no_of_functions_vs_gene_age_considering_family_size(\
	gene_no2no_of_functions, gene_no2ca_depth, gene_no2family_size):
	sys.stderr.write('Getting avg_no_of_functions_vs_gene_age...')
	ca_depth2no_of_functions_ls = {}
	print
	for gene_no, ca_depth in gene_no2ca_depth.iteritems():
		if gene_no not in gene_no2family_size or gene_no2family_size[gene_no]<5:
			continue
		if gene_no in gene_no2no_of_functions:
			if ca_depth not in ca_depth2no_of_functions_ls:
				ca_depth2no_of_functions_ls[ca_depth] = []
			print ca_depth, gene_no
			ca_depth2no_of_functions_ls[ca_depth].append(gene_no2no_of_functions[gene_no])
	ca_depth_ls = []
	avg_no_of_functions_ls = []
	no_of_genes_ls = []
	for ca_depth, no_of_functions_ls in ca_depth2no_of_functions_ls.iteritems():
		ca_depth_ls.append(ca_depth)
		avg_no_of_functions_ls.append(sum(no_of_functions_ls)/float(len(no_of_functions_ls)))
		no_of_genes_ls.append(len(no_of_functions_ls))
	sys.stderr.write("Done.\n")
	return ca_depth_ls, avg_no_of_functions_ls, no_of_genes_ls

"""
12-12-05
"""
def gene_set_from_file(input_fname):
	import csv
	from sets import Set
	reader = csv.reader(open(input_fname), delimiter='\t')
	gene_set = Set()
	for row in reader:
		gene_set.add(int(row[2]))
	return gene_set

def find_pattern_within_gene_set(curs, good_cluster_table, gene_set):
	curs.execute("DECLARE gs_crs CURSOR FOR SELECT mcl_id, vertex_set from %s"%(good_cluster_table))
	curs.execute("fetch 1000 from gs_crs")
	rows = curs.fetchall()
	while rows:
		for row in rows:
			mcl_id, vertex_set = row
			vertex_set = vertex_set[1:-1].split(',')
			vertex_set = map(int, vertex_set)
			all_within_gene_set = 1
			for gene_no in vertex_set:
				if gene_no not in gene_set:
					all_within_gene_set = 0
			if all_within_gene_set:
				print "mcl_id:",mcl_id
		curs.execute("fetch 1000 from gs_crs")
		rows = curs.fetchall()
	
"""
12-12-05
	to draw recurrence vs connectivity
"""
def rec_con_return(curs, good_cluster_table):
	curs.execute("DECLARE gs_crs CURSOR FOR SELECT recurrence, connectivity from %s"%(good_cluster_table))
	curs.execute("fetch 1000 from gs_crs")
	rows = curs.fetchall()
	recurrence_ls = []
	connectivity_ls = []
	while rows:
		for row in rows:
			recurrence_ls.append(row[0])
			connectivity_ls.append(row[1])
		curs.execute("fetch 1000 from gs_crs")
		rows = curs.fetchall()
	return recurrence_ls, connectivity_ls


"""
12-16-05
	convert schema harbison2004 into 1+14 files for Jasmine
"""
def harbison2004toFiles(curs, output_dir):
	import os, sys
	from sets import Set
	import csv
	#get tf2target_gene_condition
	curs.execute("select b.mt_id, g.gene_symbol, b.comment from gene.gene g, harbison2004.binding_site b\
		where b.prom_id = g.gene_id")
	rows = curs.fetchall()
	tf2target_gene_condition = {}
	condition_set = Set()
	for row in rows:
		tf_name, gene_symbol, condition = row
		if tf_name not in tf2target_gene_condition:
			tf2target_gene_condition[tf_name] = []
		tf2target_gene_condition[tf_name].append((gene_symbol, condition))
		condition_set.add(condition)
	#sort tf2target_gene_condition into tf_target_gene_condition_ls
	tf_target_gene_condition_ls = []
	for tf, target_gene_condition_ls in tf2target_gene_condition.iteritems():
		tf_target_gene_condition_ls.append((tf, target_gene_condition_ls))
	tf_target_gene_condition_ls.sort()
	
	#prepare output files
	condition2file_handler = {}
	for condition in condition_set:
		filename = os.path.join(output_dir, 'yeast_%s.regulatory'%condition)
		condition2file_handler[condition] = csv.writer(open(filename, 'w'), delimiter='\t')
	ensemble_filename = os.path.join(output_dir, 'yeast.regulatory')
	ensemble_file = csv.writer(open(ensemble_filename, 'w'), delimiter='\t')
	#write out
	for tf, target_gene_condition_ls in tf_target_gene_condition_ls:
		condition2target_gene_ls = {}
		ensemble_gene_set = Set()
		for target_gene, condition in target_gene_condition_ls:
			if condition not in condition2target_gene_ls:
				condition2target_gene_ls[condition] = []
			condition2target_gene_ls[condition].append(target_gene)
			ensemble_gene_set.add(target_gene)
		ensemble_gene_ls  = list(ensemble_gene_set)
		ensemble_gene_ls.sort()
		ensemble_file.writerow([tf] + ensemble_gene_ls)
		for condition, target_gene_ls in condition2target_gene_ls.iteritems():
			target_gene_ls.sort()
			condition2file_handler[condition].writerow([tf] + target_gene_ls)
	#close all files
	del ensemble_file
	del condition2file_handler


"""
12-24-05
"""
def transform_hs_geo_tissue2pairwise_table(input_fname, output_fname):
	import csv
	reader = csv.reader(open(input_fname, 'r'), delimiter ='\t')
	writer = csv.writer(open(output_fname, 'w'), delimiter ='\t')
	for row in reader:
		tissue = row[0]
		for dataset_id in row[1:]:
			if dataset_id:	#not empty, plain csv file generated by excel has blank fields
				writer.writerow([dataset_id, tissue])
	del writer, reader

"""
12-24-05
"""
def draw_summary_graph_edge_frequency(input_fname, output_fname):
	import csv
	from rpy import r
	reader = csv.reader(open(input_fname, 'r'), delimiter=' ')
	edge_frequency_ls = []
	for row in reader:
		if row[0] == 'e':
			frequency = int(row[3])
			edge_frequency_ls.append(frequency)
	del reader
	r.png(output_fname)
	r.hist(edge_frequency_ls, main='histogram',xlab='edge frequency',ylab='no of edges', labels=r.TRUE)
	r.dev_off()
	return edge_frequency_ls

"""
12-24-05
similar to above, but from sig_vector, because summary graph is missing
"""
def draw_summary_graph_edge_frequency_from_sig_vector_file(input_fname, output_fname):
	import csv
	from rpy import r
	reader = csv.reader(open(input_fname, 'r'), delimiter='\t')
	edge_frequency_ls = []
	for row in reader:
		recurrence_array = row[2:]
		recurrence_array = map(int, recurrence_array)
		frequency = sum(recurrence_array)
		edge_frequency_ls.append(frequency)
	del reader
	r.png(output_fname)
	r.hist(edge_frequency_ls, main='histogram',xlab='edge frequency',ylab='no of edges', labels=r.TRUE)
	r.dev_off()
	return edge_frequency_ls

"""
12-24-05
"""
def draw_hist_lowest_correlation(input_dir, output_fname):
	import os, csv, sys
	from rpy import r
	files = os.listdir(input_dir)
	files.sort()
	sys.stderr.write("\tTotally, %d files to be processed.\n"%len(files))
	lowest_cor_dataset_id_ls = []
	for i in range(len(files)):
		f = files[i]
		print f
		f_path = os.path.join(input_dir, f)
		reader = csv.reader(open(f_path, 'r') ,delimiter='\t')
		for row in reader:	#in case some file have nothing at all.
			if row[0] == 'e':	#just the 1st correlation line (lowest), no more
				lowest_cor_dataset_id_ls.append([float(row[3]), f])
				break
		del reader
	lowest_cor_ls = [row[0] for row in lowest_cor_dataset_id_ls]
	if lowest_cor_ls:
		r.png(output_fname)
		r.hist(lowest_cor_ls, main='histogram',xlab='lowest correlation',ylab='frequency', labels=r.TRUE)
		r.dev_off()
	return lowest_cor_dataset_id_ls

"""
12-25-05
"""
def draw_hist_correlation(input_dir, output_dir):
	import os, csv, sys
	from rpy import r
	if not os.path.isdir(output_dir):
		os.makedirs(output_dir)
	files = os.listdir(input_dir)
	files.sort()
	sys.stderr.write("\tTotally, %d files to be processed.\n"%len(files))
	for i in range(len(files)):
		f = files[i]
		print f
		f_path = os.path.join(input_dir, f)
		reader = csv.reader(open(f_path, 'r') ,delimiter='\t')
		cor_list = []
		for row in reader:
			if row[0] == 't':
				continue
			elif row[0] == 'e':
				cor_list.append(float(row[3]))
		del reader
		if cor_list:
			output_fname = os.path.join(output_dir, '%s.png'%f)
			r.png(output_fname)
			r.hist(cor_list, main='histogram',xlab='correlation',ylab='frequency')
			r.dev_off()
	return None

"""
01-02-06
	type:
		1 fim_closed
		2 closet
"""
def count_no_of_edges_from_fim_input(fim_input_fname, type=1):
	import csv, sys
	if type==1:
		delimiter_char = '\t'
	elif type==2:
		delimiter_char = ' '
	
	reader = csv.reader(open(fim_input_fname, 'r'), delimiter=delimiter_char)
	dataset_no2no_of_edges = {}
	counter = 0
	for row in reader:
		if type==2:
			row.pop(0)	#for closet+, the 1st entry is no of items
		for dataset_no in row:
			if dataset_no not in dataset_no2no_of_edges:
				dataset_no2no_of_edges[dataset_no] = 0
			dataset_no2no_of_edges[dataset_no] += 1
		counter += 1
		if counter%100000 == 0:
			sys.stderr.write("%s%s"%('\x08'*20, counter))
	del reader
	
	no_of_edges_dataset_no_ls = []
	for dataset_no, no_of_edges in dataset_no2no_of_edges.iteritems():
		no_of_edges_dataset_no_ls.append([no_of_edges, dataset_no])
	return no_of_edges_dataset_no_ls

"""
01-05-06
	[0,1,0,1] => [2,4]
"""
def binary_vector2numeric_vector(binary_vector):
	numeric_vector = []
	for i in range(len(binary_vector)):
		if binary_vector[i] == 1:
			numeric_vector.append(i+1)
	return numeric_vector

"""
01-14-06
	parse http://wombat.gnf.org/downloads/U133A%20with%20AP%20calls.zip
	return the probe_id's that can't be linked to EntrezGene_id
"""
def transform_gnf_ap_call2gene_id2tissue(input_fname, output_fname, organism, platform_id=None):
	import sys,os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from codense.common import db_connect, get_probe_id2gene_id_list
	hostname='zhoudb'
	dbname='graphdb'
	conn, curs = db_connect(hostname, dbname)
	#get probe_id2gene_id_list
	probe_id2gene_id_list = get_probe_id2gene_id_list(curs, organism, platform_id)
	from MpiFromDatasetSignatureToPattern import encodeOccurrence, decodeOccurrence
	import csv, re
	reader = csv.reader(open(input_fname, 'r'), delimiter='\t')
	#construct number2tissue
	number2tissue = {}
	header_row = reader.next()
	p_tissue = re.compile(r'\w+?_(?P<tissue>.*)_Detection')	#discard .*_Signal,
		#first ? is used to do non-greedy match
	for i in range(2, len(header_row), 2):
		tissue = p_tissue.search(header_row[i]).group('tissue').strip()	#strip() to remove blanks
		number2tissue[i/2] = tissue	# .*_Detection's index is 2, 4, 6, 8... (from 0)
	print number2tissue
	#construct gene_id2encoded_tissue_vector
	gene_id2encoded_tissue_vector = {}
	unknown_probe_id_list = []
	for row in reader:
		probe_id = row[0]
		if probe_id not in probe_id2gene_id_list:	#unknown probe
			unknown_probe_id_list.append(probe_id)
			continue
		tissue_vector = []
		for i in range(2, len(row), 2):
			if row[i] == 'P':
				tissue_vector.append(i/2)
		if tissue_vector:	#it could be empty
			for gene_id in probe_id2gene_id_list[probe_id]:
				if gene_id not in gene_id2encoded_tissue_vector:
					gene_id2encoded_tissue_vector[gene_id] = 0	#0 means this gene doesn't have any tissue associated
				gene_id2encoded_tissue_vector[gene_id] |= encodeOccurrence(tissue_vector)
	
	del reader
	#output
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	for gene_id, encoded_tissue_vector in gene_id2encoded_tissue_vector.iteritems():
		tissue_vector = decodeOccurrence(encoded_tissue_vector)
		for number in tissue_vector:
			writer.writerow([gene_id, number2tissue[number]])
	del writer
	
	return unknown_probe_id_list

"""
01-15-06
	to show what GC_percentage looks like in fasta-format sequence files
"""
def draw_GC_percentage_plot(input_dir, output_fname):
	import os, sys, fileinput
	from rpy import r
	files = os.listdir(input_dir)
	files.sort()
	sys.stderr.write("\tTotally, %d files to be processed.\n"%len(files))
	GC_percentage_list = []
	for i in range(len(files)):
		f = files[i]
		print f
		f_path = os.path.join(input_dir, f)
		inf = open(f_path, 'r')
		for line in inf:
			if line[0]=='>':
				continue
			no_of_GC = 0
			for letter in line[:-1]:	#discard the \n
				if letter=='C' or letter=='G':
					no_of_GC += 1
			if len(line[:-1])>100:	#if it's <=100, don't count it
				GC_percentage_list.append(float(no_of_GC)/len(line[:-1]))
		del inf
	if len(GC_percentage_list)>10:
		r.png(output_fname)
		r.hist(GC_percentage_list, main='histogram',xlab='GC_percentage',ylab='frequency')
		r.dev_off()
	return GC_percentage_list

"""
01-16-06
01-18-06
	updated version see transfac/src/AnalyzeTRANSFACHits.py
"""
def get_mt_id_gc_perc2no_of_random_hits(curs, matrix2no_of_random_hits_table='transfac.matrix2no_of_random_hits'):
	sys.stderr.write("Getting mt_id_gc_perc2no_of_random_hits...\n")
	curs.execute("DECLARE crs CURSOR FOR select mt_id, gc_perc, no_of_hits\
		from %s"%matrix2no_of_random_hits_table)
	curs.execute("fetch 10000 from crs")
	rows = curs.fetchall()
	mt_id_gc_perc2no_of_random_hits = {}
	counter = 0
	while rows:
		for row in rows:
			mt_id, gc_perc, no_of_hits = row
			key = (mt_id, gc_perc)
			if key not in mt_id_gc_perc2no_of_random_hits:
				mt_id_gc_perc2no_of_random_hits[key] = []
			mt_id_gc_perc2no_of_random_hits[key].append(no_of_hits)
			counter += 1
		if counter%5000 == 0:
			sys.stderr.write("%s%s"%('\x08'*20, counter))
		curs.execute("fetch 10000 from crs")
		rows = curs.fetchall()
		
	for mt_id in mt_id_gc_perc2no_of_random_hits:
			mt_id_gc_perc2no_of_random_hits[mt_id].sort()
	sys.stderr.write("Done.\n")
	return mt_id_gc_perc2no_of_random_hits
	
"""
01-18-06
"""
def count_ATCG(sequence):
	dc = {'A':0, 'T':0, 'C':0, 'G':0}
	for letter in sequence:
		dc[letter.upper()] += 1
	return dc

"""
01-19-06
"""
def find_edge_frequency_of_all_good_clusters(curs, good_cluster_table, pattern_table):
	import os, sys
	#sys.path.insert(0, os.path.join(os.path.expanduser('~/script/annot/bin')))
	from Schema2Darwin import pattern_darwin_format
	from sets import Set
	
	sys.stderr.write("Getting all edges...\n")
	pattern_darwin_format_instance = pattern_darwin_format(acc_cut_off=0)
	mcl_id_set = pattern_darwin_format_instance.get_mcl_id_set_from_good_cluster_table(curs, good_cluster_table)
	edge_tuple_set = Set()
	for mcl_id in mcl_id_set:
		curs.execute("select edge_set from %s where id=%s"%(pattern_table, mcl_id))
		rows = curs.fetchall()
		edge_set = rows[0][0]
		edge_set = edge_set[2:-2].split('},{')
		for edge in edge_set:
			edge = edge.split(',')
			edge_tuple = (int(edge[0]), int(edge[1]))
			if edge_tuple not in edge_tuple_set:
				edge_tuple_set.add(edge_tuple)
	sys.stderr.write("Done getting %s edges.\n"%len(edge_tuple_set))
	
	sys.stderr.write("Getting frequency of all edges...\n")
	edge_frequency_ls = []
	counter = 0
	for edge_tuple in edge_tuple_set:
		curs.execute("select sig_vector from edge_cor_vector where edge_name='{%s, %s}'"%(edge_tuple[0], edge_tuple[1]))
		rows = curs.fetchall()
		sig_vector = rows[0][0][1:-1].split(',')
		sig_vector = map(int, sig_vector)
		edge_frequency_ls.append(sum(sig_vector))
		counter += 1
		if counter%5000 ==0:
			sys.stderr.write("%s%s"%('\x08'*15, counter))
	sys.stderr.write("Done getting edge frequency.\n")
	
	frequency2occurrence = {}
	for frequency in edge_frequency_ls:
		if frequency not in frequency2occurrence:
			frequency2occurrence[frequency] = 0
		frequency2occurrence[frequency] += 1
	
	return frequency2occurrence


"""
01-19-06
	input_fname is output of AnalyzeTRANSFACHits.py (*.data)
"""
def draw_p_value_distri_for_each_matrix(input_fname, output_dir):
	import os, sys, csv
	
	sys.stderr.write("Reading p-values...\n")
	mt_id2p_value_list = {}
	reader = csv.reader(open(input_fname, 'r'), delimiter='\t')
	counter = 0
	for row in reader:
		seq_id, sequence_length, mt_id, gc_perc, no_of_hits, pvalue = row
		if mt_id not in mt_id2p_value_list:
			mt_id2p_value_list[mt_id] = []
		mt_id2p_value_list[mt_id].append(float(pvalue))
		counter += 1
		if counter%50000 ==0:
			sys.stderr.write("%s%s"%('\x08'*15, counter))
	sys.stderr.write("Done.\n")
	
	from rpy import r
	if not os.path.isdir(output_dir):
		os.makedirs(output_dir)
	for mt_id, p_value_list in mt_id2p_value_list.iteritems():
		figure_name = '%s.pvalue_hist.png'%mt_id
		print "Drawing", figure_name
		figure_name = os.path.join(output_dir, figure_name)
		r.png(figure_name)
		r.hist(p_value_list, main=mt_id, xlab='pvalue', ylab='frequency')
		r.dev_off()
	

"""
01-26-06
	generate all combinations of base-frequency(A,T,C,G)
	use the backtrack algorithm from Skiena1997
	
	NOTE:
		1. float is fuzzy, not precise for boolean operator > or == or >
		2. correct way to generate candidate set is very important and tricky
"""
def generate_ATCG_combinations():
	import copy
	candidate_frequency_ls = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95] 	#candidate_frequency_ls for all
	candidate_frequency_set_ls= [0]*5	#place to store s1, s2, s3, s4, s5
	candidate_frequency_set_ls[0] = copy.deepcopy(candidate_frequency_ls)
	return_ls = []
	k = 0
	four_frequency_ls = [0] *4
	divide_functor = lambda x: x/100.0	#divide those integers
	while k>=0:
		while len(candidate_frequency_set_ls[k])>0:
			a = candidate_frequency_set_ls[k].pop(0)
			four_frequency_ls[k] = a
			one_combination = copy.deepcopy(four_frequency_ls[:k+1])	#only from 0 to k
			if sum(one_combination)==100 and len(one_combination)==4:	#got one
				#float_one_combination = map(divide_functor, one_combination)
				return_ls.append(copy.deepcopy(one_combination))
			k += 1	#advance
			remaining_max_value = 100 - sum(one_combination)	#this is the biggest value next candidate set could have
			sk = []	#next candidate set
			#generate a candidate set, tricky
			for i in range(10):
				if candidate_frequency_ls[i] == remaining_max_value and k==3:	#the 4th frequency allows '=='
					sk.append(candidate_frequency_ls[i])
				elif candidate_frequency_ls[i]>=remaining_max_value:
					continue
				elif k<3:	#if k ==3(last digit), those smaller elements shall not be included.
					sk.append(candidate_frequency_ls[i])
			candidate_frequency_set_ls[k] = copy.deepcopy(sk)
		k -= 1	#backtrack
	return return_ls


"""
01-26-06
	ATCG_combination_ls is generated by generate_ATCG_combinations()
"""
def submit_jobs_for_TRANSFAC_on_random_sequence(ATCG_combination_ls, job_prefix, \
	starting_number=0, job_dir='~/qjob'):
	import os
	job_dir = os.path.expanduser(job_dir)
	
	for one_combination in ATCG_combination_ls:
		job_fname = os.path.join(job_dir, '%s_%s'%(job_prefix, starting_number))
		of = open(job_fname, 'w')
		of.write('#!/bin/sh\n')
		of.write('#PBS -q cmb -j oe -S /bin/bash\n')
		of.write('#PBS -l walltime=200:00:00\n')
		of.write('#PBS -d /home/rcf-14/yuhuang/qjob_output\n')
		#of.write('#PBS -k eo\n')
		of.write('#PBS -l nodes=3:myri:ppn=4\n')
		of.write('source ~/.bash_profile\n')
		of.write('date\n')
		A_percentage = '%2.2f'%(one_combination[0]*0.1)
		T_percentage = '%2.2f'%(one_combination[1]*0.1)
		G_percentage = '%2.2f'%(one_combination[3]*0.1)	#WATCH index is 3
		sequence_dir = '~/transfac/random_a%s_t%s_g%s'%(one_combination[0], one_combination[1], one_combination[3])
		transfac_dir = '%s_out'%sequence_dir
		"""
		random_sequence_generator_commandline = \
			'~/script/transfac/src/RandomSequenceGenerator.py -o %s -a %s -t %s -g %s'%\
			(sequence_dir, A_percentage, T_percentage, G_percentage)
		of.write('echo COMMANDLINE: %s\n'%random_sequence_generator_commandline)
		of.write('%s\n'%random_sequence_generator_commandline)
		of.write('date\n')
		"""
		
		#codes below need parallel directives
		batch_match_commandline = \
			'~/script/shell/batch_match.py $PBS_NODEFILE %s %s ~/script/transfac/data/match_data/vertebrates_m0_8_c0_85_highQual.match.prf'%\
			(sequence_dir, transfac_dir)
		of.write('echo COMMANDLINE: %s\n'%batch_match_commandline)
		of.write('%s\n'%batch_match_commandline)
		of.write('date\n')
		
		starting_number += 1
		
		"""
		#01-26-06 codes below doesn't work well, submitted job disregard #PBS directives
		qsub_output = os.system('qsub %s'%job_fname)
		print "job_fname:", job_fname
		print "qsub_output:", qsub_output
		"""
		

"""
01-30-06
"""
def find_edges_given_dataset_signature(input_fname, dataset_signature):
	from MpiFromDatasetSignatureToPattern import encodeOccurrenceBv, encodeOccurrence
	import csv
	reader = csv.reader(open(input_fname), delimiter='\t')
	counter = 0
	real_counter = 0
	encoded_dataset_signature = encodeOccurrence(dataset_signature)
	freq2edge_list = {}
	for row in reader:
		gene_id1 = int(row[0])
		gene_id2 = int(row[1])
		sig_vector = row[2:]
		sig_vector = map(int, sig_vector)
		encoded_recurrence = encodeOccurrenceBv(sig_vector)
		if (encoded_recurrence&encoded_dataset_signature) == encoded_dataset_signature:
			frequency = sum(sig_vector)
			if frequency not in freq2edge_list:
				freq2edge_list[frequency] = []
			freq2edge_list[frequency].append((gene_id1, gene_id2))
			real_counter += 1
		counter += 1
		if counter%20000 == 0:
			sys.stderr.write("%s%s\t%s"%('\x08'*20, counter, real_counter))
	del reader
	sys.stderr.write("%s%s\t%s\n"%('\x08'*20, counter, real_counter))
	return freq2edge_list
	
"""
03-30-06
"""
def output_edge_sig_vector_given_dataset_signature(input_fname, output_fname, dataset_signature, min_support, max_support):
	from MpiFromDatasetSignatureToPattern import encodeOccurrenceBv, encodeOccurrence
	import csv
	reader = csv.reader(open(input_fname), delimiter='\t')
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	counter = 0
	real_counter = 0
	encoded_dataset_signature = encodeOccurrence(dataset_signature)
	for row in reader:
		gene_id1 = int(row[0])
		gene_id2 = int(row[1])
		sig_vector = row[2:]
		sig_vector = map(int, sig_vector)
		encoded_recurrence = encodeOccurrenceBv(sig_vector)
		if sum(sig_vector)>=min_support and sum(sig_vector) <= max_support:
			if (encoded_recurrence&encoded_dataset_signature) == encoded_dataset_signature:
				writer.writerow(row)
				real_counter += 1
		counter += 1
		if counter%20000 == 0:
			sys.stderr.write("%s%s\t%s"%('\x08'*20, counter, real_counter))
	del reader, writer
	sys.stderr.write("%s%s\t%s\n"%('\x08'*20, counter, real_counter))
	
"""
01-30-06
"""
def get_gene_no2go_no_given_level(curs, schema=None, go_table='go', level=4):
	sys.stderr.write("Getting gene_no2go_no...")
	if schema:
		curs.execute("set search_path to %s"%schema)
	
	gene_no2go_no = {}
	
	curs.execute("select go_no, gene_array from %s where depth=%s"%(go_table, level))
	rows = curs.fetchall()
	for row in rows:
		go_no = row[0]
		gene_list = row[1][1:-1].split(',')
		for gene_no in gene_list:
			gene_no = int(gene_no)
			if gene_no not in gene_no2go_no:
				gene_no2go_no[gene_no] = []
			gene_no2go_no[gene_no].append(go_no)
	sys.stderr.write("Done\n")
	return gene_no2go_no

"""
01-30-06
"""
def calculate_function_pair_perc(edge_list, gene_no2go_no, go_no2name):
	function_pair2counter = {}
	for edge in edge_list:
		if edge[0] not in gene_no2go_no:
			go_no_list1 = [0]
		else:
			go_no_list1 = gene_no2go_no[edge[0]]
		if edge[1] not in gene_no2go_no:
			go_no_list2 = [0]
		else:
			go_no_list2 = gene_no2go_no[edge[1]]
		for go_no1 in go_no_list1:
			for go_no2 in go_no_list2:
				if go_no1<go_no2:
					function_pair = (go_no1, go_no2)
				else:
					function_pair = (go_no2, go_no1)
				if function_pair not in function_pair2counter:
					function_pair2counter[function_pair] = 0.0
				function_pair2counter[function_pair] += 1
	function_pair2perc = {}
	for function_pair,counter in function_pair2counter.iteritems():
		function_pair2perc[function_pair] = counter/len(edge_list)
	return function_pair2perc
	""""
	perc_function_pair_list = []
	for function_pair, counter in function_pair2counter.iteritems():
		perc = counter/float(len(edge_list))
		function_pair = (go_no2name[function_pair[0]], go_no2name[function_pair[1]])
		perc_function_pair_list.append([perc, function_pair])
	perc_function_pair_list.sort()
	return perc_function_pair_list
	"""

"""
01-30-06
	go_no2name is not used
"""
def calculate_function2perc(edge_list, gene_no2go_no, go_no2name):
	function2perc = {}
	from sets import Set
	gene_set = Set()
	for edge in edge_list:
		gene_set.add(edge[0])
		gene_set.add(edge[1])
	for gene_no in gene_set:
		if gene_no not in gene_no2go_no:
			go_no_list = [0]
		else:
			go_no_list = gene_no2go_no[gene_no]
		for go_no in go_no_list:
			if go_no not in function2perc:
				function2perc[go_no] = 0.0
			function2perc[go_no] += 1
	for function, counter in function2perc.iteritems():
		function2perc[function] = counter/len(gene_set)
	return function2perc

"""
01-30-06
	correlation of two value lists from two dictionaries
"""
def cal_correlation_between_2_function_pair2counter(function_pair2counter_1, function_pair2counter_2):
	from sets import Set
	function_pair_set = Set(function_pair2counter_1.keys()+function_pair2counter_2.keys())
	perc_list1 = []
	perc_list2 = []
	for function_pair in function_pair_set:
		if function_pair in function_pair2counter_1:
			perc_list1.append(function_pair2counter_1[function_pair])
		else:
			perc_list1.append(0)
		if function_pair in function_pair2counter_2:
			perc_list2.append(function_pair2counter_2[function_pair])
		else:
			perc_list2.append(0)
	from rpy import r
	return r.cor(perc_list1, perc_list2)

"""
01-30-06
	use calculate_function_pair_perc() and cal_correlation_between_2_function_pair2counter()
	
"""
def cal_function_pair2counter_correlation_curve(freq2edge_list, center_frequency, gene_no2go_no, go_no2name, \
	dc_function=calculate_function_pair_perc):
	center_edge_list =freq2edge_list[center_frequency]
	center_function_pair2perc = dc_function(center_edge_list, gene_no2go_no, go_no2name)
	freq2correlation = {}
	for frequency, edge_list in freq2edge_list.iteritems():
		function_pair2perc = dc_function(edge_list, gene_no2go_no, go_no2name)
		freq2correlation[frequency] = cal_correlation_between_2_function_pair2counter(center_function_pair2perc, function_pair2perc)
	frequency_list = freq2correlation.keys()
	frequency_list.sort()
	import sys
	correlation_list = []
	for frequency in frequency_list:
		sys.stdout.write("\t%s:%s"%(frequency, freq2correlation[frequency]))
		correlation_list.append(freq2correlation[frequency])
	print
	return frequency_list, correlation_list
	


"""
02-03-06
	filter patterns based on recurrence*connectivity

"""
def filter_patterns_with_rec_conn(input_fname, output_fname, rec_conn_cutoff=2.5, debug=0):
	import csv
	reader = csv.reader(open(input_fname, 'r'), delimiter='\t')
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	counter = 0
	real_counter = 0
	for row in reader:
		vertex_list, edge_list, recurrence_array, d_matrix = row
		no_of_vertices = len(vertex_list[1:-1].split(','))
		no_of_edges = len(edge_list[2:-2].split('], ['))
		connectivity = 2*float(no_of_edges)/((no_of_vertices-1)*no_of_vertices)
		recurrence_array = recurrence_array[1:-1].split(', ')
		recurrence = 0.0
		for i in range(len(recurrence_array)):
			if recurrence_array[i] == '1.0':
				recurrence += 1
		if debug:
			print row
		if recurrence*connectivity>=rec_conn_cutoff:
			if debug:
				print "recurrence*connectivity:", recurrence*connectivity
				break
			writer.writerow(row)
			real_counter += 1
		counter += 1
		if counter%5000==0:
			sys.stderr.write("%s%s\t%s"%('\x08'*20, counter, real_counter))
	sys.stderr.write("%s%s\t%s\n"%('\x08'*20, counter, real_counter))
	del reader, writer

"""
03-03-06
"""
def rec_con_percentile(input_fname, debug=0):
	import csv
	reader = csv.reader(open(input_fname, 'r'), delimiter='\t')
	counter = 0
	rec_con_list = []
	for row in reader:
		vertex_list, edge_list, recurrence_array, d_matrix = row
		no_of_vertices = len(vertex_list[1:-1].split(','))
		no_of_edges = len(edge_list[2:-2].split('], ['))
		connectivity = 2*float(no_of_edges)/((no_of_vertices-1)*no_of_vertices)
		recurrence_array = recurrence_array[1:-1].split(', ')
		recurrence = 0.0
		for i in range(len(recurrence_array)):
			if recurrence_array[i] == '1.0':
				recurrence += 1
		rec_con_list.append(connectivity*recurrence)
		counter += 1
		if counter%5000==0:
			sys.stderr.write("%s%s"%('\x08'*20, counter))
	sys.stderr.write("%s%s\n"%('\x08'*20, counter))
	del reader
	
	rec_con_list.sort()
	print "1%:", rec_con_list[int(counter*0.01)]
	print "3%:", rec_con_list[int(counter*0.03)]
	print "5%:", rec_con_list[int(counter*0.05)]
	return rec_con_list

"""
02-04-06
	input_fname is output type=2 of go_informative_node.py
"""
def node_dependency(input_fname, output_fname):
	import csv
	from sets import Set
	reader = csv.reader(open(input_fname, 'r'), delimiter='\t')
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	go_id2gene_set = {}
	for row in reader:
		go_id, name = row[0], row[1]
		gene_no_set = row[2:]
		gene_no_set = map(int, gene_no_set)
		go_id2gene_set[go_id] = Set(gene_no_set)
	go_id_list = go_id2gene_set.keys()
	for i in range(len(go_id_list)):
		for j in range(i+1, len(go_id_list)):
			go_id1 = go_id_list[i]
			go_id2 = go_id_list[j]
			gene_no_set1 = go_id2gene_set[go_id1]
			gene_no_set2 = go_id2gene_set[go_id2]
			length_join = float(len(gene_no_set1&gene_no_set2))
			prob_in2given1 = length_join/len(gene_no_set1)
			prob_in1given2 = length_join/len(gene_no_set2)
			writer.writerow([go_id1, go_id2, prob_in2given1, prob_in1given2])
	del reader, writer


"""
04-16-06
	input_fname is output type=2 of go_informative_node.py
	three classifications
	1. one node is mostly included by another node (includee)
	2. one node is the includer
	3. one node is neither
"""
def classify_go_informative_nodes_based_on_dependency(input_fname, prob_cutoff=0.2):
	from sets import Set
	import csv
	reader = csv.reader(open(input_fname, 'r'), delimiter='\t')
	go_id2gene_set = {}
	for row in reader:
		go_id, name = row[0], row[1]
		gene_no_set = row[2:]
		gene_no_set = map(int, gene_no_set)
		go_id2gene_set[go_id] = Set(gene_no_set)
	
	go_id_list = go_id2gene_set.keys()
	includee_set = Set()
	includer_set = Set()
	for i in range(len(go_id_list)):
		for j in range(i+1, len(go_id_list)):
			go_id1 = go_id_list[i]
			go_id2 = go_id_list[j]
			gene_no_set1 = go_id2gene_set[go_id1]
			gene_no_set2 = go_id2gene_set[go_id2]
			length_join = float(len(gene_no_set1&gene_no_set2))
			prob_in2given1 = length_join/len(gene_no_set1)
			prob_in1given2 = length_join/len(gene_no_set2)
			if prob_in2given1>=prob_cutoff:
				includee_set.add(go_id1)
			elif prob_in1given2>=prob_cutoff:
				includer_set.add(go_id1)
			if prob_in1given2>=prob_cutoff:
				includee_set.add(go_id2)
			elif prob_in2given1>=prob_cutoff:
				includer_set.add(go_id2)
	del reader
	includer_set = includer_set - includee_set
	others = Set(go_id_list) - (includee_set|includer_set)
	return includee_set, includer_set, others

"""
04-16-06
	read go_no2accuracy dictionary from haifeng's R output, format like below:
[1] 1
   
     FALSE   TRUE
  0 131693  10906
  1  19727   9749
[1] "\n"
[1] 2
   
    FALSE  TRUE
  0 63307  7300
  1 10899 10029
[1] "\n"
...
"""
def get_go_no2accuracy_from_haifeng_R_output(input_fname):
	go_no2accuracy = {}
	inf = open(input_fname)
	for line in inf:
		row = line.split()
		if line[:3]=='  0':
			no_of_false_positives = float(row[-1])
		elif line[:3] == '  1':
			no_of_true_positives = float(row[-1])
			accuracy = no_of_true_positives/(no_of_true_positives+no_of_false_positives)
			go_no = len(go_no2accuracy)+1
			print "go_no", go_no, "no_of_false_positives", no_of_false_positives, "no_of_true_positives", no_of_true_positives, "accuracy", accuracy
			go_no2accuracy[go_no] = [no_of_true_positives, no_of_false_positives]
	del inf
	return go_no2accuracy



"""
02-14-06
02-21-06
	add vertex_set
"""
def compare_graphs(seed_gph_fname, other_gph_fname_list):
	sys.stderr.write("Reading seed graph...")
	from sets import Set
	import csv
	reader = csv.reader(open(seed_gph_fname, 'r'), delimiter='\t')
	edge_dict = {}
	vertex_set = Set()
	for row in reader:
		if row[0] == 'e':
			edge_tuple = (int(row[1]), int(row[2]))
			if edge_tuple[0]>edge_tuple[1]:
				edge_tuple = (edge_tuple[1], edge_tuple[0])
			edge_dict[edge_tuple] = 1
			vertex_set.add(edge_tuple[0])
			vertex_set.add(edge_tuple[1])
	del reader
	sys.stderr.write("done.\n")
	
	sys.stderr.write("start to compare with other graphs...\n")
	for input_fname in other_gph_fname_list:
		print '\t' + input_fname
		reader = csv.reader(open(input_fname, 'r'), delimiter='\t')
		no_of_overlapping_edges = 0
		no_of_total_edges = 0
		local_vertex_set = Set()
		for row in reader:
			if row[0] == 'e':
				edge_tuple = (int(row[1]), int(row[2]))
				if edge_tuple[0]>edge_tuple[1]:
					edge_tuple = (edge_tuple[1], edge_tuple[0])
				if edge_tuple in edge_dict:
					edge_dict[edge_tuple] += 1
					no_of_overlapping_edges += 1
				no_of_total_edges += 1
				local_vertex_set.add(edge_tuple[0])
				local_vertex_set.add(edge_tuple[1])
		vertex_overlapping_ratio = len(local_vertex_set&vertex_set)/float(len(local_vertex_set|vertex_set))
		edge_overlapping_ratio = float(no_of_overlapping_edges)/(len(edge_dict) + no_of_total_edges - no_of_overlapping_edges)
		print '\t overlapping ratio: %s(edge), %s(vertex)'%(edge_overlapping_ratio, vertex_overlapping_ratio)
		del reader
	sys.stderr.write("done.\n")
	
	return edge_dict


"""
02-19-06
"""
def convert_bfs2darwin(input_fname, output_fname):
	import os, sys
	inf = open(input_fname, 'r')
	outf = open(output_fname, 'w')
	outf.write('r:=[\n')
	for line in inf:
		row = line[:-1].split('\t')
		outf.write('[%s],\n'%(', '.join(row[:3])))
	outf.write('[]]:\n')
	del inf, outf

"""
02-24-06
"""
def function_homogeneity_of_summary_graph_edges(input_fname, curs, schema):
	from sets import Set
	import csv
	sys.stderr.write("Getting gene_no2go_no_set(only known)...")
	gene_no2go_no_set = {}
	curs.execute("select go_no, gene_array from %s.go where go_no!=0"%schema)
	rows = curs.fetchall()
	for row in rows:
		go_no, gene_array = row
		gene_array = gene_array[1:-1].split(',')
		gene_array = map(int, gene_array)
		for gene_no in gene_array:
			if gene_no not in gene_no2go_no_set:
				gene_no2go_no_set[gene_no] = Set()
			gene_no2go_no_set[gene_no].add(go_no)
	sys.stderr.write("Done.\n")
	
	
	sys.stderr.write("Reading edges...")
	edge_freq2similarity_ls = {}
	reader = csv.reader(open(input_fname), delimiter=' ')
	for row in reader:
		if row[0] == 'e':
			gene_no1 = int(row[1])
			gene_no2 = int(row[2])
			frequency = int(row[3])
			if (gene_no1 in gene_no2go_no_set) and (gene_no2 in gene_no2go_no_set):
				similarity = float(len(gene_no2go_no_set[gene_no1]&gene_no2go_no_set[gene_no2]))/len(gene_no2go_no_set[gene_no1]|gene_no2go_no_set[gene_no2])
				if frequency not in edge_freq2similarity_ls:
					edge_freq2similarity_ls[frequency] = []
				edge_freq2similarity_ls[frequency].append(similarity)
	sys.stderr.write("Done.\n")
	
	from rpy import r
	from MA import average
	freq_list = edge_freq2similarity_ls.keys()
	freq_list.sort()
	avg_similarity_list = []
	no_of_entries_list = []
	for frequency in freq_list:
		print "frequency", frequency
		avg_similarity = average(edge_freq2similarity_ls[frequency])
		avg_similarity_list.append(avg_similarity)
		no_of_entries_list.append(len(edge_freq2similarity_ls[frequency]))
		print "\tnumber of entries", len(edge_freq2similarity_ls[frequency])
		print "\taverage similarity", avg_similarity
		print "\tvariance", r.var(edge_freq2similarity_ls[frequency])
	
	return edge_freq2similarity_ls, freq_list, avg_similarity_list, no_of_entries_list

"""
2006-12-07
	This function inspects how function similarity is related to the recurrence of an edge

	input_fname is the output of haifeng's sigvector.sh
	go_fname is the output of go_informative_node.py in haifeng_annot
"""
def function_homogeneity_of_sig_vector_edges(input_fname, go_fname):
	from sets import Set
	import csv
	sys.stderr.write("Getting gene_no2go_no_set(only known)...")
	gene_no2go_no_set = {}
	f = open(go_fname)
	f.readline() #remove title line
	for line in f:
		row = map(int,line.strip().split())	#gene_no, is_known, go_bit1, go_bit2, ...
		if row[1]==1:	#known gene
			gene_no2go_no_set[row[0]] = Set()
			for i in range(2, len(row)):
				if row[i] == 1:
					gene_no2go_no_set[row[0]].add(i-1)	#i-1 starts from 1
	del f
	sys.stderr.write("Done.\n")
	
	sys.stderr.write("Reading edges...")
	edge_freq2similarity_ls = {}
	reader = csv.reader(open(input_fname), delimiter='\t')
	for row in reader:
		row = map(int, row)
		gene_no1 = row[0]
		gene_no2 = row[1]
		frequency = sum(row[2:])
		if (gene_no1 in gene_no2go_no_set) and (gene_no2 in gene_no2go_no_set):
			similarity = float(len(gene_no2go_no_set[gene_no1]&gene_no2go_no_set[gene_no2]))/len(gene_no2go_no_set[gene_no1]|gene_no2go_no_set[gene_no2])
			if frequency not in edge_freq2similarity_ls:
				edge_freq2similarity_ls[frequency] = []
			#if len(edge_freq2similarity_ls[frequency])<=1e6:	#2006-12-08 add an upper limit
			edge_freq2similarity_ls[frequency].append(similarity)
	sys.stderr.write("Done.\n")
	return edge_freq2similarity_ls

"""
2006-12-11
	draw a plot between frequency and average similarity returned by function above
		if no of edges with that frequency is less than 100, ignore it
	output_fname is just a prefix. no 'png', 'eps', 'svg' suffices
"""
def plot_edge_function_homogeneity(edge_freq2similarity_ls, output_fname, edge_freq_threshold=100, barchart=0):
	from rpy import r
	from MA import average
	freq_list = edge_freq2similarity_ls.keys()
	freq_list.sort()
	avg_similarity_list = []
	sd_of_avg_similarity_list = []
	no_of_entries_list = []
	for frequency in freq_list:
		print "frequency", frequency
		avg_similarity = average(edge_freq2similarity_ls[frequency])
		avg_similarity_list.append(avg_similarity)
		sd_of_avg_similarity = r.sd(edge_freq2similarity_ls[frequency])
		sd_of_avg_similarity_list.append(sd_of_avg_similarity)
		no_of_entries_list.append(len(edge_freq2similarity_ls[frequency]))
		
		print "\tnumber of entries", len(edge_freq2similarity_ls[frequency])
		print "\taverage similarity", avg_similarity
		print "\tstandard deviation", sd_of_avg_similarity
	import matplotlib; matplotlib.use("Agg")
	import pylab
	pylab.clf()
	pylab.xlabel("edge frequency")
	pylab.ylabel("average similarity")
	truncated_index = len(no_of_entries_list)
	for i in range(len(no_of_entries_list)):
		if no_of_entries_list[i]<edge_freq_threshold:
			truncated_index = i
			break
	#[:i] is 0, 1, ... , i-1
	if barchart:
		ind = pylab.arange(truncated_index)	# the x locations for the groups, arange() ensures that ind+width could work
		#range() can't work for ind+width
		width = 0.35	# the width of the bars
		pylab.bar(ind, avg_similarity_list[:truncated_index], width, yerr=sd_of_avg_similarity_list[:truncated_index])
		pylab.xticks(ind+width/2, map(repr, freq_list[:truncated_index]))	#tick's type must be string or text or something.
		pylab.xlim(-width,len(ind))
	else:
		pylab.plot(freq_list[:truncated_index], avg_similarity_list[:truncated_index], '-o')
	pylab.savefig('%s.png'%output_fname, dpi=200)
	pylab.savefig('%s.eps'%output_fname, dpi=200)
	pylab.savefig('%s.svg'%output_fname, dpi=200)


"""
02-28-06
	for Math505b
"""
def factorial(x):
	value = 1
	for i in range(x):
		value = value*(i+1)
	return value

def prob(N, lambda_mu):
	import math
	value = 0.0
	for i in range(N+1):
		value += math.pow(lambda_mu, i)/factorial(i)
	value = (math.pow(lambda_mu, i)/factorial(i))/value
	return value

"""
04-02-06
	filter haifeng's patterns
04-06-06
	fix the wrong format haifeng used
"""
def filter_haifeng_pattern(full_fname, rdup_fname, output_fname):
	import csv
	full_reader = csv.reader(open(full_fname), delimiter='\t')
	rdup_reader = csv.reader(open(rdup_fname), delimiter='\t')
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	for row in full_reader:
		rdup_row = rdup_reader.next()
		row_needed = int(rdup_row[1])
		if row_needed:
			vertex_set, edge_set, recurrence_array = row
			vertex_set = vertex_set[1:]	#04-03-06 haifeng put [] around the whole row
			edge_set = edge_set.replace('], [', '), (')
			writer.writerow([vertex_set, edge_set])
	del full_reader, rdup_reader, writer

"""
#04-11-06
"""
def construct_local_tf_no2gene_no_set(vertex_set, gene_no2bs_no_set):
	from sets import Set
	local_tf_no2gene_no_set = {}
	for gene_no in vertex_set:
		if gene_no in gene_no2bs_no_set:
			for tf_no in gene_no2bs_no_set[gene_no]:
				if tf_no not in local_tf_no2gene_no_set:
					local_tf_no2gene_no_set[tf_no] = Set()
				local_tf_no2gene_no_set[tf_no].add(gene_no)
	return local_tf_no2gene_no_set
	

def find_patterns_with_distinct_TF_layout(curs, pattern_table, min_gene_ratio=0.3, max_tf_overlapping_ratio=0.1):
	from MpiClusterBsStat import MpiClusterBsStat
	MpiClusterBsStat_instance = MpiClusterBsStat()
	gene_no2bs_no_block = MpiClusterBsStat_instance.get_gene_no2bs_no_block(curs)
	gene_no2bs_no_set, bs_no2gene_no_set = MpiClusterBsStat_instance.construct_two_dicts(1,	gene_no2bs_no_block)
	curs.execute("DECLARE crs CURSOR FOR SELECT id, vertex_set from %s"%(pattern_table))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	counter = 0
	while rows:
		for row in rows:
			id, vertex_set = row
			vertex_set = vertex_set[1:-1].split(',')
			vertex_set = map(int, vertex_set)
			no_of_genes = len(vertex_set)
			local_tf_no2gene_no_set = construct_local_tf_no2gene_no_set(vertex_set, gene_no2bs_no_set)
			no_of_genes_tf_no_ls = []
			for tf_no in local_tf_no2gene_no_set:
				no_of_genes_tf_no_ls.append([len(local_tf_no2gene_no_set[tf_no]), tf_no])
			if len(no_of_genes_tf_no_ls)>0:
				no_of_genes_tf_no_ls.sort()
				max_no_of_genes, max_tf_no = no_of_genes_tf_no_ls[0]
				if max_no_of_genes>=min_gene_ratio*no_of_genes:
					for i in range(1, len(no_of_genes_tf_no_ls)):
						no_of_genes_of_tf_no, tf_no = no_of_genes_tf_no_ls[i]
						overlapping_no_of_genes = len(local_tf_no2gene_no_set[tf_no]&local_tf_no2gene_no_set[max_tf_no])
						if no_of_genes_of_tf_no>=min_gene_ratio*no_of_genes and overlapping_no_of_genes<=max_tf_overlapping_ratio*no_of_genes:
							print "pattern id", id
							print "max_tf_no %s, gene_no_set: %s"%(max_tf_no, repr(local_tf_no2gene_no_set[max_tf_no]))
							print "tf_no: %s, gene_no_set: %s"%(tf_no, repr(local_tf_no2gene_no_set[tf_no]))
						break
			counter += 1
		sys.stderr.write("%s%s"%('\x08'*20, counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")
	curs.execute("close crs0")


"""
04-13-06
	transform go_informative_node.py's output (t=1) plus other unknown genes from schema's gene table
	into haifeng's input for his function prediction scheme
"""
def transform_informative_node_output_format(informative_node_fname, curs, schema, output_fname):
	import csv
	informative_node_reader = csv.reader(open(informative_node_fname, 'r'), delimiter='\t')
	gene_id2go_id_list = {}
	from sets import Set
	go_id_set = Set()
	for row in informative_node_reader:
		go_id, go_name, gene_id = row
		if gene_id not in gene_id2go_id_list:
			gene_id2go_id_list[gene_id] = []
		gene_id2go_id_list[gene_id].append(go_id)
		go_id_set.add(go_id)
	del informative_node_reader
	#get the go_id2column_index
	go_id_list = list(go_id_set)
	go_id_list.sort()
	go_id2column_index = {}
	for i in range(len(go_id_list)):
		go_id2column_index[go_id_list[i]] = i
	
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	go_id_list.insert(0, '')
	go_id_list.insert(0, '')
	writer.writerow(go_id_list)
	
	for gene_id in gene_id2go_id_list:
		go_id_incidence_list = [0]*len(go_id2column_index)
		for go_id in gene_id2go_id_list[gene_id]:
			go_id_incidence_list[go_id2column_index[go_id]] = 1
		writer.writerow([gene_id, 1]+go_id_incidence_list)
	
	#unknown genes
	from codense.common import get_gene_id2gene_no
	gene_id2gene_no = get_gene_id2gene_no(curs, schema)
	
	for gene_id in gene_id2gene_no:
		if gene_id not in gene_id2go_id_list:
			writer.writerow([gene_id, 0] + [0]*len(go_id2column_index))
	del writer



#05-31-06
def haifeng_datasets2my_datasets(haifeng_fname, mapping_fname, output_fname):
	import csv
	haifeng_f_reader = csv.reader(open(haifeng_fname, 'r'))
	mapping_f_reader = csv.reader(open(mapping_fname, 'r'), delimiter='\t')
	outf = open(output_fname, 'w')
	haifeng_dataset_fname2my_fname = {}
	for row in mapping_f_reader:
		my_fname, haifeng_dataset_fname = row
		haifeng_dataset_fname2my_fname[haifeng_dataset_fname] = my_fname
	
	for row in haifeng_f_reader:
		outf.write('%s\n'%haifeng_dataset_fname2my_fname[row[0]])
	
	del haifeng_f_reader, mapping_f_reader, outf


"""
06-05-06
	below are for inspecting TF association in clusters
"""
def get_gene_id2mt_no_set(tax_id, hostname='zhoudb', dbname='graphdb', schema='graph', table='gene_id2mt_no'):
	sys.stderr.write("Getting gene_id2mt_no_set...")
	gene_id2mt_no_set = {}
	(conn, curs) =  db_connect(hostname, dbname, schema)
	curs.execute("select gene_id, mt_no from %s where tax_id=%s"%(table, tax_id))
	rows = curs.fetchall()
	from sets import Set
	for row in rows:
		gene_id, mt_no = row
		gene_id = int(gene_id)
		if gene_id not in gene_id2mt_no_set:
			gene_id2mt_no_set[gene_id] = Set()
		gene_id2mt_no_set[gene_id].add(mt_no)
	del conn, curs
	sys.stderr.write("Done\n")
	return gene_id2mt_no_set

from sets import Set

def get_mt_no2gene_id_set(gene_id2mt_no_set, vertex_set):
	mt_no2gene_id_set = {}
	for gene_id in vertex_set:
		if gene_id in gene_id2mt_no_set:
			for mt_no in gene_id2mt_no_set[gene_id]:
				if mt_no not in mt_no2gene_id_set:
					mt_no2gene_id_set[mt_no] = Set()
				mt_no2gene_id_set[mt_no].add(gene_id)
	return mt_no2gene_id_set


def draw_pattern_tf_info(curs, pattern_table, condition, gene_id2mt_no_set, min_asso_number=5):
	import networkx as nx
	import pylab
	curs.execute("DECLARE crs CURSOR FOR select id, edge_set from %s where %s"%(pattern_table, condition))
	curs.execute("fetch 100 from crs")
	rows = curs.fetchall()
	while rows:
		for row in rows:
			id, edge_set = row
			g = nx.Graph()
			edge_set = edge_set[2:-2].split('},{')
			for edge in edge_set:
				edge = edge.split(',')
				edge = map(int, edge)
				g.add_edge(edge[0], edge[1])
			mt_no2gene_id_set = get_mt_no2gene_id_set(gene_id2mt_no_set, g.nodes())
			print "pattern id:", id
			pos = nx.spring_layout(g)
			for mt_no in mt_no2gene_id_set:
				asso_number = len(mt_no2gene_id_set[mt_no])
				print "\tmt_no:", mt_no, "asso_number:", asso_number
				if asso_number<min_asso_number:
					continue
				color_list = []
				for v in g:
					if v in mt_no2gene_id_set[mt_no]:
						color_list.append(10)
					else:
						color_list.append(1)
				nx.draw(g, pos, node_color=pylab.array(color_list), with_labels=False)
				pylab.title("pattern id: %s mt_no: %s with %s genes"%(id, mt_no, asso_number))
				pylab.show()
				cond = raw_input("continue?")
				if cond=='n' or cond=='N':
					break
			cond = raw_input("continue?")
			if cond=='n' or cond=='N':
				break
		cond = raw_input("continue?")
		if cond=='n' or cond=='N':
			break
		curs.execute("fetch 100 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")


"""
2006-08-22
	for Jasmine's collaborator, Mike West's request
"""
def get_E2F_Y_target_list(input_fname):
	"""
	2006-08-23
		add co_factor
	"""
	import string
	inf = open(input_fname)
	E2F_Y_target_list = []
	for line in inf:
		if line[0] == 'Y':
			co_factor = line[:-1].split(' = ')[1]
			co_factor = co_factor.strip()
		elif line[0] == 'A':
			target_ls = line[:-1].split(' = ')[1]
			target_ls = target_ls.split(', ')
			target_ls = map(string.strip, target_ls)
			E2F_Y_target_list.append([co_factor, target_ls])
	del inf
	return E2F_Y_target_list


def calculate_overlapping_E2F_Y_target_list(curs, pattern_table, E2F_Y_target_list, \
		gene_symbol2gene_id, gene_id2gene_symbol, output_fname, threshold=4, left_cutoff=0.4, right_cutoff=0.4):
	"""
	2006-08-23
		take patterns whose overlapping_ratio_left is 1.0
	"""
	sys.stderr.write("Calculating overlapping_E2F_Y_target_set_list...\n")
	from sets import Set
	from codense.common import dict_map
	import csv
	#writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	#header = ['overlapping_ratio', 'overlapping_ratio_left(pattern)', 'overlapping_ratio_right(target_set)', \
	#	'no_of_overlappings', 'pattern_id', 'target_set id']
	#writer.writerow(header)
	curs.execute("DECLARE crs CURSOR FOR select id, vertex_set \
		from %s"%(pattern_table))
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	no_of_hits = 0
	counter = 0
	target_ls_index2sub_patterns = {}
	while rows:
		for row in rows:
			id = row[0]
			vertex_ls = row[1][1:-1].split(',')
			vertex_ls = map(int, vertex_ls)
			vertex_set = Set(vertex_ls)
			for i in  range(len(E2F_Y_target_list)):
				co_factor,  target_ls = E2F_Y_target_list[i]
				target_ls_gene_id = dict_map(gene_symbol2gene_id, target_ls)
				target_set = Set(target_ls_gene_id)
				no_of_overlappings = len(vertex_set & target_set)
				"""
				print target_set
				print vertex_set
				print no_of_overlappings
				break
				"""
				overlapping_ratio = float(no_of_overlappings)/len(vertex_set|target_set)
				overlapping_ratio_left = float(no_of_overlappings)/len(vertex_set)
				overlapping_ratio_right = float(no_of_overlappings)/len(target_set)
				#if no_of_overlappings >= threshold and overlapping_ratio_left>=left_cutoff and overlapping_ratio_right>=right_cutoff:
				if overlapping_ratio_left==1.0:
					no_of_hits += 1
					if i not in target_ls_index2sub_patterns:
						target_ls_index2sub_patterns[i] = []
					target_ls_index2sub_patterns[i].append([id, vertex_ls])
					#writer.writerow([overlapping_ratio, overlapping_ratio_left, overlapping_ratio_right, no_of_overlappings, id, i])
			counter+= 1
			#break
			if counter%1000==0:
				sys.stderr.write("%s%s/%s"%('\x08'*20, counter, no_of_hits))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
		#break
	curs.execute("close crs")
	outf = open(output_fname, 'w')
	for target_ls_index in target_ls_index2sub_patterns:
		co_factor,  target_ls = E2F_Y_target_list[target_ls_index]
		outf.write('Y = %s\n'%co_factor)
		outf.write('A = %s\n'%(', '.join(target_ls)))
		for id, vertex_ls in target_ls_index2sub_patterns[target_ls_index]:
			outf.write('P(%s) = %s\n'%(id, ', '.join(dict_map(gene_id2gene_symbol, vertex_ls))))
		outf.write('\n')
	del outf
	sys.stderr.write("Done.\n")


def wrap_E2F_functions(input_fname, curs, pattern_table, \
		output_fname, tax_id=9606, threshold=4, left_cutoff=0.4, right_cutoff=0.4):
	""" 
	2006-08-23
		wrap functions above together
	"""
	from codense.common import get_gene_id2gene_symbol, get_gene_symbol2gene_id
	gene_symbol2gene_id = get_gene_symbol2gene_id(curs, tax_id)
	gene_id2gene_symbol = get_gene_id2gene_symbol(curs, tax_id)
	E2F_Y_target_list = get_E2F_Y_target_list(input_fname)
	calculate_overlapping_E2F_Y_target_list(curs, pattern_table, E2F_Y_target_list, \
		gene_symbol2gene_id, gene_id2gene_symbol, output_fname)


"""
2006-08-24
	get the relationship between (predicted times) vs accuracy
2006-08-31
	read the output of parse_haifeng_markov()
"""
def plot_prediction_times_vs_accuracy(input_fname, output_fname, prediction_times_threshold=6, known_or_unknown_type=1):
	#get data from haifeng's pred.sh output file, like human.100.known1.2
	inf = open(input_fname, 'r')
	prediction2prediction_times = {}
	for line in inf:
		row =  line[:-1].split()
		gene_id, pattern_id, go_id, is_known, is_correct, markov_score, p_value = row
		#row = tuple(map(int, row))	#format of row: gene_no, go_no, is_correct
		gene_id = int(gene_id)
		is_known = int(is_known)
		is_correct = int(is_correct)
		if is_known==known_or_unknown_type:
			row = (gene_id, go_id, is_correct)
			if row not in prediction2prediction_times:
				prediction2prediction_times[row] = 0
			prediction2prediction_times[row] += 1
	del inf
	#get the equal_count range
	import rpy
	rpy.r.library('lattice')
	rpy.set_default_mode(rpy.NO_CONVERSION)
	prediction_times_equal_count_object = rpy.r.equal_count(prediction2prediction_times.values())
	rpy.set_default_mode(rpy.BASIC_CONVERSION)
	prediction_times_range_list = rpy.r.levels(prediction_times_equal_count_object)
	prediction_times_range_list = map(tuple, prediction_times_range_list)
	print "prediction_times range:", prediction_times_range_list
	
	#put predictions into different ranges
	#count predictions over a prediction_times_threshold
	prediction_times_range2stat = {}
	prediction_times_is_correct_ls = []
	no_of_right_predictions = 0
	no_of_total_predictions = 0
	from sets import Set
	genes_predicted_set = Set()
	
	for prediction_tuple, prediction_times in prediction2prediction_times.iteritems():
		prediction_times_is_correct_ls.append([prediction_times, prediction_tuple[-1]])
		for prediction_times_range in prediction_times_range_list:
			if prediction_times>=prediction_times_range[0] and prediction_times<=prediction_times_range[1]:
				if prediction_times_range not in prediction_times_range2stat:
					prediction_times_range2stat[prediction_times_range] = [0, 0]
				prediction_times_range2stat[prediction_times_range][prediction_tuple[-1]] += 1
		if prediction_times>=prediction_times_threshold:
			no_of_right_predictions += prediction_tuple[-1]
			no_of_total_predictions += 1
			genes_predicted_set.add(prediction_tuple[0])
	
	accuracy = no_of_right_predictions/float(no_of_total_predictions)
	print "prediction_times_threshold: %s, #genes: %s, #right predictions: %s, #total predictions: %s, accuracy: %s\n"\
		%(prediction_times_threshold, len(genes_predicted_set), no_of_right_predictions, no_of_total_predictions, accuracy)
	"""
	#also count predictions over a prediction_times_threshold, not necessary anymore
	prediction_times_is_correct_ls.sort()
	import Numeric
	prediction_times_is_correct_array = Numeric.array(prediction_times_is_correct_ls)
	
	for i in range(len(prediction_times_is_correct_array)):
		if prediction_times_is_correct_array[i][0]>=prediction_times_threshold:
			no_of_right_predictions = sum(prediction_times_is_correct_array[i:, 1])
			no_of_total_predictions = len(prediction_times_is_correct_array[i:, 1])
			accuracy = no_of_right_predictions/float(no_of_total_predictions)
			print "prediction_times_threshold: %s, #right predictions: %s, #total predictions: %s, accuracy: %s\n"%(prediction_times_threshold,\
				no_of_right_predictions, no_of_total_predictions, accuracy)
			break
	print prediction_times_range2stat
	"""
	
	#draw the plot
	
	#import rpy
	#rpy.r.png(output_fname)
	import pylab
	prediction_times_list = []
	accuracy_list = []
	for prediction_times_range, wrong_correct_tuple in prediction_times_range2stat.iteritems():
		prediction_times_list.append(sum(prediction_times_range)/2.0)
		accuracy_list.append(float(wrong_correct_tuple[1])/sum(wrong_correct_tuple))
	#rpy.r.plot(prediction_times_list, accuracy_list, xlab='prediction_times', ylab='accuracy', type='p')
	#rpy.r.dev_off()
	pylab.xlabel("prediction times")
	pylab.ylabel("accuracy")
	import os
	pylab.title(os.path.basename(input_fname))
	pylab.plot(prediction_times_list, accuracy_list, 'bo')
	pylab.show()
	return genes_predicted_set


"""
2006-08-29
	parse haifeng's markov.py's output file and output 
"""
def parse_haifeng_markov(markov_output_fname, go_fname, output_fname, score_cutoff, p_value_cut_off=0.01):
	sys.stderr.write("Getting go_index2id...")
	import Numeric as numpy
	go_inf = open(go_fname)
	go_id_line = go_inf.readline()
	go_id_list = go_id_line.split()
	del go_inf
	no_of_gos = len(go_id_list)
	go_index2id = dict(zip(range(no_of_gos), go_id_list))
	sys.stderr.write("Done.\n")
	
	import csv
	reader = csv.reader(open(markov_output_fname), delimiter='\t')
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	sys.stderr.write("Reading %s...\n"%markov_output_fname)
	counter = 0
	no_of_hits = 0
	for row in reader:
		pattern_id, unknown_percentage, no_of_vertices, no_of_edges, avg_degree, density, supports, vertex_id, \
		is_known, unknown_neighbor_perc, degree, no_of_neighbors = row[:12]
		go_binary_list = row[12:12+no_of_gos*1]
		m1_list = row[12+no_of_gos*1:12+no_of_gos*2]
		p_value_list =row[12+no_of_gos*2:12+no_of_gos*3]
		"""
		m0_list = row[12+no_of_gos*2:12+no_of_gos*3]
		mu_list = row[12+no_of_gos*3:12+no_of_gos*4]
		p_value_list = row[12+no_of_gos*4:12+no_of_gos*5]
		"""
		m1_list = map(float, m1_list)
		p_value_list = map(float, p_value_list)
		
		go_index_with_highest_score = numpy.argmax(m1_list)
		
		counter += 1
		#for i in range(no_of_gos):
		i = go_index_with_highest_score
		if p_value_list[i]<p_value_cut_off and m1_list[i]>0 and m1_list[i]>score_cutoff:
			writer.writerow([vertex_id, pattern_id, go_index2id[i], is_known, go_binary_list[i], m1_list[i], p_value_list[i]])
			no_of_hits += 1
		if counter%1000==0:
			sys.stderr.write('%s\t%s\t%s'%('\x08'*20, counter, no_of_hits))
	sys.stderr.write('%s\t%s\t%s\n'%('\x08'*20, counter, no_of_hits))
	
	del reader, writer
	sys.stderr.write("Done.\n")
	

"""
2006-08-31
"""
def masked_prom_seq2db(curs, input_dir, prom_seq_table='transfac.prom_seq', need_commit = 0):
	sys.stderr.write("Submitting masked prom_seq ...\n")
	sys.path.insert(0, os.path.join(os.path.expanduser('~/script/transfac/src')))
	from transfacdb import fasta_block_iterator
	import cStringIO
	for input_fname in os.listdir(input_dir):
		if input_fname.find('masked')==-1:
			continue
		print input_fname
		input_fname = os.path.join(input_dir, input_fname)
		inf = open(input_fname)
		iter = fasta_block_iterator(inf)
		block_no = 0
		curs.execute("begin")
		for block in iter:
			block = cStringIO.StringIO(block)
			header_line = block.readline()
			id = header_line[1:-1]	#no need to convert it to integer
			sequence = ''
			for line in block:
				sequence += line[:-1]
			curs.execute("update %s set masked_seq='%s' where id=%s"%(prom_seq_table, sequence, id))
			block_no += 1
			if block_no%500==0:
				sys.stderr.write('%s%s'%('\x08'*20, block_no))
		if need_commit:
			curs.execute("end")
		del inf, iter
	sys.stderr.write('%s%s'%('\x08'*20, block_no))
	sys.stderr.write("Done.\n")
	

"""
2006-09-05
	codes below are trying to compare the histograms of correlations 
		of edges which are within one node, between this node and other nodes,
		and edges totally outside
"""
def get_go_id2gene_set(go_fname):
	sys.stderr.write("Getting go_id2gene_set...")
	import csv
	from sets import Set
	reader = csv.reader(open(go_fname), delimiter='\t')
	go_id2gene_set = {}
	for row in reader:
		go_id, go_name, gene_id = row
		gene_id = int(gene_id)
		if go_id not in go_id2gene_set:
			go_id2gene_set[go_id] = Set()
		go_id2gene_set[go_id].add(gene_id)
	del reader
	sys.stderr.write("Done.\n")
	return go_id2gene_set

def get_gene_pair_cor_list(cor_fname):
	sys.stderr.write("Getting gene_pair_cor_list...")
	import csv
	reader = csv.reader(open(cor_fname), delimiter='\t')
	reader.next()	#skip the first line
	gene_pair_cor_list = []
	for row in reader:
		edge_tag, gene_id1, gene_id2, cor= row
		gene_id1 = int(gene_id1)
		gene_id2 = int(gene_id2)
		cor = float(cor)
		gene_pair_cor_list.append([gene_id1, gene_id2, cor])
	del reader
	sys.stderr.write("Done.\n")
	return gene_pair_cor_list

def go_correlation_coherence(cor_fname, go_fname, output_dir):
	"""
	2006-09-06
		use subplot() to separate three histograms
	"""
	import os, sys
	import pylab
	import matplotlib
	matplotlib.use('Agg') 
	go_id2gene_set = get_go_id2gene_set(go_fname)
	gene_pair_cor_list = get_gene_pair_cor_list(cor_fname)
	counter = 0
	for go_id, gene_set in go_id2gene_set.iteritems():
		intra_cor_list = []
		inter_cor_list = []
		extra_cor_list = []
		for row in gene_pair_cor_list:
			gene_id1, gene_id2, cor= row
			if (gene_id1 in gene_set) and (gene_id2 in gene_set):
				intra_cor_list.append(cor)
			elif (gene_id1 in gene_set) and (gene_id2 not in gene_set):
				inter_cor_list.append(cor)
			elif (gene_id1 not in gene_set) and (gene_id2 in gene_set):
				inter_cor_list.append(cor)
			elif (gene_id1 not in gene_set) and (gene_id2 not in gene_set):
				extra_cor_list.append(cor)
		counter += 1
		pylab.figure(counter)
		
		pylab.subplot(311)
		pylab.title('Intra node')
		if intra_cor_list:
			pylab.hist(intra_cor_list)
		
		pylab.subplot(312)
		pylab.title('inter node')
		if inter_cor_list:
			pylab.hist(inter_cor_list)
		
		pylab.subplot(313)
		pylab.title('extra node')
		if extra_cor_list:
			pylab.hist(extra_cor_list)
		pylab.xlabel('go_id: %s'%go_id)
		fig_fname = '%s_go_id_%s.png'%(cor_fname, go_id)
		print fig_fname
		pylab.savefig(os.path.join(output_dir,fig_fname))


def tss_cds_distance_histogram(curs, tax_id=9606, entrezgene_mapping_table='sequence.entrezgene_mapping', \
		annot_assembly_table = 'sequence.annot_assembly'):
	"""
	2006-09-14
		check how far between TSS and CDS
	2006-09-19
		fix a bug about the strand
		
	"""
	from codense.common import pg_1d_array2python_ls
	sys.stderr.write("Getting getting tss and cds info from database...\n")
	curs.execute("DECLARE crs CURSOR FOR SELECT e.gene_id,  e.mrna_start, e.mrna_stop, e.cds_start, e.cds_stop, e.strand\
		from %s e where e.tax_id=%s"%(entrezgene_mapping_table, tax_id))
	curs.execute("fetch 10000 from crs")
	rows = curs.fetchall()
	counter = 0
	distance_ls = []
	no_of_faraways = 0
	while rows:
		for row in rows:
			gene_id, mrna_start, mrna_stop, cds_start, cds_stop, strand = row
			mrna_loc_ls = []
			cds_loc_ls = []
			if mrna_start and mrna_stop and cds_start and cds_stop:
				mrna_start = pg_1d_array2python_ls(mrna_start, int)
				mrna_stop = pg_1d_array2python_ls(mrna_stop, int)
				for i in range(len(mrna_start)):
					mrna_loc_ls.append([mrna_start[i],mrna_stop[i]])
				cds_start = pg_1d_array2python_ls(cds_start, int)
				cds_stop = pg_1d_array2python_ls(cds_stop, int)
				for i in range(len(cds_start)):
					cds_loc_ls.append([cds_start[i],cds_stop[i]])
				mrna_loc_ls.sort()
				cds_loc_ls.sort()
				if strand=='1':	#plus strand
					distance =  abs(mrna_loc_ls[0][0] - cds_loc_ls[0][0])
				elif strand=='-1':	#minus strand
					distance =  abs(mrna_loc_ls[-1][0] - cds_loc_ls[-1][0])
				else:	#ignore genes with no strand info, some are not real genes
					continue
				if distance<=10000:
					distance_ls.append(distance)
				else:
					no_of_faraways +=1
			counter += 1
		sys.stderr.write("%s\t%s"%('\x08'*20, counter))
		curs.execute("fetch 10000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")
	print "no_of_faraways", no_of_faraways
	sys.stderr.write("Done.\n")
	import pylab
	pylab.hist(distance_ls)
	pylab.show()


"""
2006-09-17
	list comparison based on  a specified location
"""
def list_compare(x, y, k):
	if x[k]>y[k]:
		return 1
	elif x[k]==y[k]:
		return 0
	else: # x<y
		return -1

def get_mcl_id2occurrent_dataset_ls(curs, pattern_table, occurrence_cutoff=0.8):
	"""
	2006-09-21
		for next function, printTF2pattern2geneInfo()
	"""
	from codense.common import pg_1d_array2python_ls
	sys.stderr.write("Getting mcl_id2occurrent_dataset_ls from %s..."%pattern_table)
	curs.execute("DECLARE crs1 CURSOR FOR SELECT id, recurrence_array from %s"%\
		(pattern_table))
	curs.execute("fetch 2000 from crs1")
	rows = curs.fetchall()
	counter = 0
	mcl_id2occurrent_dataset_ls = {}
	lambda_cut = lambda x: int(x>=occurrence_cutoff)
	while rows:
		for row in rows:
			id, recurrence_array = row
			recurrence_array = pg_1d_array2python_ls(recurrence_array, float)
			recurrence_array = map(lambda_cut, recurrence_array)
			occurrent_dataset_ls = []
			for i in range(len(recurrence_array)):
				if recurrence_array[i] == 1:
					occurrent_dataset_ls.append(i+1)
			mcl_id2occurrent_dataset_ls[id] = occurrent_dataset_ls
			counter += 1
		sys.stderr.write("%s\t%s"%('\x08'*20, counter))
		curs.execute("fetch 2000 from crs1")
		rows = curs.fetchall()
	curs.execute("close crs1")
	sys.stderr.write("Done.\n")
	return mcl_id2occurrent_dataset_ls


def printTF2pattern2geneInfo(curs, cluster_bs_table, mt_no2tf_name, output_fname, \
	mcl_id2occurrent_dataset_ls, no_of_bs_nos=1):
	"""
	2006-09-17
		print out a global picture of TF vs gene pattern information
	2006-09-19
		add no_of_bs_nos
	2006-09-21
		add mcl_id2occurrent_dataset_ls
		
		call list_compare() above
	"""
	from codense.common import pg_1d_array2python_ls
	sys.stderr.write("Getting TF2pattern2geneInfo from database...\n")
	curs.execute("DECLARE crs0 CURSOR FOR SELECT mcl_id, core_vertex_ls, bs_no_list, gene_no_list from %s"%\
		(cluster_bs_table))
	curs.execute("fetch 2000 from crs0")
	rows = curs.fetchall()
	counter = 0
	tf2data = {}	#key is tf, value is a list, [#patterns, gene2freq]
	while rows:
		for row in rows:
			mcl_id, core_vertex_ls, bs_no_list, gene_no_list = row
			core_vertex_ls = pg_1d_array2python_ls(core_vertex_ls, int)
			bs_no_list = pg_1d_array2python_ls(bs_no_list, int)
			gene_no_list = pg_1d_array2python_ls(gene_no_list, int)
			if len(bs_no_list)==no_of_bs_nos:
				bs_no_list.sort()
				key = tuple(bs_no_list)
				if key not in tf2data:
					tf2data[key] = [0, {}, {}]
				tf2data[key][0] += 1
				for gene_no in gene_no_list:
					if gene_no not in tf2data[key][1]:
						tf2data[key][1][gene_no] = 0
					tf2data[key][1][gene_no] += 1
				for dataset_no in mcl_id2occurrent_dataset_ls[mcl_id]:
					if dataset_no not in tf2data[key][2]:
						tf2data[key][2][dataset_no] = 0
					tf2data[key][2][dataset_no] += 1
				counter += 1
		sys.stderr.write("%s\t%s"%('\x08'*20, counter))
		curs.execute("fetch 2000 from crs0")
		rows = curs.fetchall()
	curs.execute("close crs0")
	sys.stderr.write("Done.\n")
	
	sys.stderr.write("Outputting data...")
	tf_data_list = []
	for tf, data in tf2data.iteritems():
		gene_no2freq = data[1]
		dataset_no2freq = data[2]
		lambda_divid = lambda x: float(x)/data[0]
		freq_list = map(lambda_divid, gene_no2freq.values())
		no_of_genes = len(gene_no2freq)
		avg_freq_per_pattern = sum(freq_list)/float(no_of_genes)
		
		dataset_freq_list = map(lambda_divid, dataset_no2freq.values())
		no_of_datasets = len(dataset_freq_list)
		avg_dataset_freq_per_pattern = sum(dataset_freq_list)/float(no_of_datasets)
		tf_data_list.append([tf, data[0], avg_freq_per_pattern, no_of_genes, avg_dataset_freq_per_pattern, no_of_datasets])
	
	lambda_list_cmp = lambda x, y: list_compare(x, y, 1)	#compare the list based on 2nd position(#patterns)
	tf_data_list.sort(lambda_list_cmp)
	tf_data_list.reverse()
	
	from codense.common import dict_map
	import csv
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	header_row = ['TF name', 'no_of_patterns', 'gene freq', 'no_of_genes', 'dataset freq', 'no_of_datasets']
	writer.writerow(header_row)
	for row in tf_data_list:
		row[0] = dict_map(mt_no2tf_name, row[0])
		writer.writerow(row)
		#outf.write('%s\t%s\t%s\t%s\t%s\t%s\n'%(','.join(tf_list), row[1], row[2], row[3], row[4], row[5]))
	del writer
	sys.stderr.write("Done.\n")
	
"""
2006-09-21
	a wrap-up for functions above
"""
def run_printTF2pattern2geneInfo(curs, cluster_bs_table, output_fname, \
	pattern_table, occurrence_cutoff=0.8, no_of_bs_nos=1, tax_id=9606):
	from codense.common import get_gene_id2gene_symbol
	gene_id2gene_symbol = get_gene_id2gene_symbol(curs, tax_id)
	mcl_id2occurrent_dataset_ls = get_mcl_id2occurrent_dataset_ls(curs, pattern_table, occurrence_cutoff)
	printTF2pattern2geneInfo(curs, cluster_bs_table, gene_id2gene_symbol, output_fname, \
		mcl_id2occurrent_dataset_ls, no_of_bs_nos)

"""
2006-10-03
	different from the get_gene_symbol2gene_id() of common.py, due to the table name
	BUG in common.py's version
"""
def upper_case_gene_symbol2gene_id(curs, tax_id, table='gene.gene'):
	sys.stderr.write("Getting gene_symbol2gene_id...")
	gene_symbol2gene_id = {}
	curs.execute("select gene_id, gene_symbol from %s where tax_id=%s"%(table, tax_id))
	rows = curs.fetchall()
	for row in rows:
		gene_symbol2gene_id[row[1].upper()] = row[0]
	sys.stderr.write("Done.\n")
	return gene_symbol2gene_id

"""
2006-10-08
	Table gene_symbol2id contains all reverse-mapping information, including aliases, synonyms, etc.
	Multiple names could lead to same gene_id. 2728 out of 90768 human genes(3%) have this problem.
	
	One way to solve this problem is checking the real gene_symbol2gene_id table. 
"""
def get_upper_case_gene_name2gene_id(curs, tax_id, table='gene.gene_symbol2id'):
	sys.stderr.write("Getting upper_case gene_symbol2gene_id...")
	gene_symbol2gene_id = {}
	curs.execute("select gene_id, gene_symbol from gene.gene where tax_id=%s"%(tax_id))
	rows = curs.fetchall()
	for row in rows:
		gene_symbol2gene_id[row[1].upper()] = row[0]
	sys.stderr.write("Done.\n")
	
	sys.stderr.write("Getting upper_case gene_symbol2gene_id_list...")
	gene_symbol2gene_id_list = {}
	curs.execute("select gene_id, gene_symbol from %s where tax_id=%s"%(table, tax_id))
	rows = curs.fetchall()
	for row in rows:
		gene_id, gene_symbol = row
		gene_symbol = gene_symbol.upper()
		if gene_symbol not in gene_symbol2gene_id_list:
			gene_symbol2gene_id_list[gene_symbol] = []
		gene_symbol2gene_id_list[gene_symbol].append(gene_id)
	sys.stderr.write("Done.\n")
	
	sys.stderr.write("Making gene_name2gene_id...")
	gene_name2gene_id = {}
	for gene_symbol, gene_id_list in gene_symbol2gene_id_list.iteritems():
		if len(gene_id_list)==1:
			gene_name2gene_id[gene_symbol] = gene_id_list[0]
		elif gene_symbol in gene_symbol2gene_id:	#take the orthodox one
			gene_name2gene_id[gene_symbol] = gene_symbol2gene_id[gene_symbol]
	sys.stderr.write("Done.\n")
	return gene_name2gene_id

"""
2006-10-03
"""
def Wei2006_data_to_db(curs, input_fname, target_table='graph.tf_mapping', tf_name='TP53', \
	tax_id=9606, gene_symbol2gene_id=None, paper_name='Wei2006', \
	comment='replace multiple spaces with one space and cut the 3rd column'):
	
	mt_no = gene_symbol2gene_id.get(tf_name.upper())
	if not mt_no:
		print "%s not found in gene_symbol2gene_id"%tf_name
		return
	inf = open(input_fname)
	curs.execute("begin")
	for line in inf:
		gene_symbol = line[:-1]
		gene_id = gene_symbol2gene_id.get(gene_symbol.upper())
		if gene_id:
			curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
				(target_table, gene_id, mt_no, tax_id, paper_name, comment))
	del inf
	curs.execute("end")
	
def Lee2006_data_to_db(curs, input_fname, target_table='graph.tf_mapping', tf_name='SUZ12', \
	tax_id=9606, gene_symbol2gene_id=None, paper_name='Lee2006', \
	comment='1st column of table s8'):
	
	mt_no = gene_symbol2gene_id.get(tf_name.upper())
	if not mt_no:
		print "%s not found in gene_symbol2gene_id"%tf_name
		return
	inf = open(input_fname)
	curs.execute("begin")
	for line in inf:
		gene_id = line[:-1]
		if gene_id:
			curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
				(target_table, gene_id, mt_no, tax_id, paper_name, comment))
	del inf
	curs.execute("end")

def Boyer2005_data_to_db(curs, input_fname, target_table='graph.tf_mapping', tf_name_list=['POU5F1', 'SOX2', 'NANOG', 'E2F4'], \
	tax_id=9606, gene_symbol2gene_id=None, paper_name='Boyer2005', \
	comment='read the csv format of the xls'):
	#POU5F1 is OCT4
	import csv
	reader = csv.reader(open(input_fname), delimiter='\t')
	#skip the first 4 lines
	for i in range(4):
		reader.next()
	
	curs.execute("begin")
	for row in reader:
		gene_symbol, oct4_flag, sox2_flag, nanog_flag, e2f4_flag, expressed_flag = row
		gene_id = gene_symbol2gene_id.get(gene_symbol.upper())
		tf_flag_list = [oct4_flag, sox2_flag, nanog_flag, e2f4_flag]
		if gene_id:
			for i in range(len(tf_flag_list)):
				if tf_flag_list[i] != '-':
					mt_no = gene_symbol2gene_id.get(tf_name_list[i].upper())
					curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
						(target_table, gene_id, mt_no, tax_id, paper_name, comment))
	curs.execute("end")
	del reader

def Odom2006_data_to_db(curs, input_fname, target_table='graph.tf_mapping', \
	tf_name_list=['FOXA2', 'TCF1', 'HNF4A', 'ONECUT1', 'CREB1',  'USF1'], \
	tax_id=9606, gene_symbol2gene_id=None, paper_name='Odom2006', \
	comment='read the csv format of the xls', acc_file='/usr/local/research_data/ncbi/gene/gene2accession'):
	
	#FOXA2 is HNF3B, TCF1 is HNF1A, ONECUT1 is HNF6
	
	sys.path.insert(0, os.path.join(os.path.expanduser('~/script/microarray/bin')))
	from sets import Set
	tax_id_set = Set([tax_id])
	from MdbId2GeneId import MdbId2GeneId
	MdbId2GeneId_instance = MdbId2GeneId()
	acc2gene_id = MdbId2GeneId_instance.setup_acc2gene_id(acc_file, tax_id_set)
	
	reader = csv.reader(open(input_fname), delimiter='\t')
	#skip the first line
	reader.next()
	
	curs.execute("begin")
	for row in reader:
		refseq_acc, flag1, flag2, flag3, flag4, flag5, flag6 = row
		key = (refseq_acc.upper(), tax_id)
		if key in acc2gene_id:
			tf_flag_list = [flag1, flag2, flag3, flag4, flag5, flag6]
			if len(acc2gene_id[key])==1:
				gene_id = acc2gene_id[key][0]
				for i in range(len(tf_flag_list)):
					if tf_flag_list[i] == '1':
						mt_no = gene_symbol2gene_id.get(tf_name_list[i].upper())
						curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
							(target_table, gene_id, mt_no, tax_id, paper_name, comment))
	curs.execute("end")
	del reader

def Cam2004_data_to_db(curs, input_fname, target_table='graph.tf_mapping', tf_name_list=['E2F4', 'RBL2'], \
	tax_id=9606, gene_symbol2gene_id=None, paper_name='Cam2004', \
	comment='read the csv format of the xls, p-value<=0.005', p_value_cut_off=0.005):
	#RBL2 is p130
	reader = csv.reader(open(input_fname), delimiter='\t')
	#skip the first 3 lines
	for i in range(3):
		reader.next()
	
	curs.execute("begin")
	for row in reader:
		gene_symbol = row[0]
		locuslink = row[1]
		index_range_e2f4 = [2,6,10]
		e2f4_p_value_list = []
		for i in index_range_e2f4:
			if row[i]:
				e2f4_p_value_list.append(row[i])
		e2f4_p_value_list = map(float, e2f4_p_value_list)
		index_range_p130 = [4,8,12]
		p130_p_value_list = []
		for i in index_range_p130:
			if row[i]:
				p130_p_value_list.append(row[i])
		p130_p_value_list = map(float, p130_p_value_list)
		gene_id = gene_symbol2gene_id.get(gene_symbol.upper())
		if gene_id:
			tag_e2f4 = 0
			for p_value in e2f4_p_value_list:
				if p_value<=p_value_cut_off:
					tag_e2f4 = 1
			tag_p130 = 0
			for p_value in p130_p_value_list:
				if p_value<=p_value_cut_off:
					tag_p130 = 1
			if tag_e2f4==1:
				mt_no = gene_symbol2gene_id.get(tf_name_list[0].upper())
				curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
					(target_table, gene_id, mt_no, tax_id, paper_name, comment))
			if tag_p130==1:
				mt_no = gene_symbol2gene_id.get(tf_name_list[1].upper())
				curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
					(target_table, gene_id, mt_no, tax_id, paper_name, comment))
	curs.execute("end")
	del reader

def Cam2004_data_to_db_NRF1(curs, input_fname, target_table='graph.tf_mapping', tf_name='NRF1', \
	tax_id=9606, gene_symbol2gene_id=None, paper_name='Cam2004', \
	comment='csv format of xls, NRF1'):
	
	mt_no = gene_symbol2gene_id.get(tf_name.upper())
	if not mt_no:
		print "%s not found in gene_symbol2gene_id"%tf_name
		return
	reader = csv.reader(open(input_fname), delimiter='\t')
	#skip one line
	reader.next()
	curs.execute("begin")
	for row in reader:
		gene_symbol = row[0]
		gene_id = gene_symbol2gene_id.get(gene_symbol.upper())
		if gene_id:
			curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
				(target_table, gene_id, mt_no, tax_id, paper_name, comment))
	curs.execute("end")
	del reader


def Schreiber2006_data_to_db_E2F4(curs, input_fname, target_table='graph.tf_mapping', tf_name='E2F4', \
	tax_id=9606, gene_symbol2gene_id=None, paper_name='Schreiber2006', \
	comment='Table 4, E2F4 target, unstimulated U937 cells'):
	
	mt_no = gene_symbol2gene_id.get(tf_name.upper())
	if not mt_no:
		print "%s not found in gene_symbol2gene_id"%tf_name
		return
	inf = open(input_fname)
	curs.execute("begin")
	for line in inf:
		gene_symbol = line[:-1]
		gene_id = gene_symbol2gene_id.get(gene_symbol.upper())
		if gene_id:
			curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
				(target_table, gene_id, mt_no, tax_id, paper_name, comment))
	del inf
	curs.execute("end")

"""
2006-10-09
"""
def Palomero2006_data_to_db(curs, input_fname, target_table='graph.tf_mapping', tf_name_list=['TAL1', 'TCF3', 'TCF12'], \
	tax_id=9606, gene_symbol2gene_id=None, paper_name='Palomero2006', \
	comment='TableS2, hand-copy from the pdf format'):
	#TCF3 is E2A, TCF12 is HEB
	import csv
	reader = csv.reader(open(input_fname), delimiter='\t')
	#skip the first line
	reader.next()
	
	curs.execute("begin")
	for row in reader:
		gene_symbol, flag1, flag2, flag3 = row
		if gene_symbol:	#skip the blank lines
			gene_id = gene_symbol2gene_id.get(gene_symbol.upper())
			tf_flag_list = [flag1, flag2, flag3]
			if gene_id:
				for i in range(len(tf_flag_list)):
					if tf_flag_list[i] == '1':
						mt_no = gene_symbol2gene_id.get(tf_name_list[i].upper())
						curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
							(target_table, gene_id, mt_no, tax_id, paper_name, comment))
	curs.execute("end")
	del reader

def Schreiber2006_binding_data_to_db(curs, input_fname, target_table='graph.tf_mapping', \
	tf_name_list=['RELA', 'REL', 'RELB', 'NFKB1', 'FKBP4'], \
	tax_id=9606, gene_symbol2gene_id=None, paper_name='Schreiber2006', \
	comment='', p_value_threshold=0.01):
	#RELA is p65, NFKB1 is p50, REL is c-Rel, FKBP4 is p52
	import csv
	reader = csv.reader(open(input_fname), delimiter='\t')
	#skip the first 2 lines
	reader.next()
	reader.next()
	
	curs.execute("begin")
	for row in reader:
		gene_symbol = row[0]
		no_LPS_p_value_list = row[1:6]
		with_LPS_p_value_list = row[7:12]
		rpolII_binding_ratio_list = row[14:16]
		if gene_symbol:	#skip the blank lines
			gene_id = gene_symbol2gene_id.get(gene_symbol.upper())
			if gene_id:
				for i in range(len(no_LPS_p_value_list)):	#without LPS
					if no_LPS_p_value_list[i] and no_LPS_p_value_list[i]!=' ':
						p_value = float(no_LPS_p_value_list[i])
						if p_value<=p_value_threshold:
							mt_no = gene_symbol2gene_id.get(tf_name_list[i].upper())
							if rpolII_binding_ratio_list[0]:	#if the ratio under no LPS is available
								comment = 'pvalue=%s, LPS=0, RPolII_ratio=%s'%(p_value, rpolII_binding_ratio_list[0])
							else:
								comment = 'pvalue=%s, LPS=0, RPolII_ratio=NA'%(p_value)
							curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
								(target_table, gene_id, mt_no, tax_id, paper_name, comment))
				for i in range(len(with_LPS_p_value_list)):	#with LPS
					if with_LPS_p_value_list[i] and with_LPS_p_value_list[i]!=' ':
						p_value = float(with_LPS_p_value_list[i])
						if p_value<=p_value_threshold:
							mt_no = gene_symbol2gene_id.get(tf_name_list[i].upper())
							if rpolII_binding_ratio_list[1]:	#if the ratio under LPS is available
								comment = 'pvalue=%s, LPS=1, RPolII_ratio=%s'%(p_value, rpolII_binding_ratio_list[1])
							else:
								comment = 'pvalue=%s, LPS=1, RPolII_ratio=NA'%(p_value)
							curs.execute("insert into %s(gene_id, mt_no, tax_id, paper, comment) values('%s', %s, %s, '%s', '%s')"%\
								(target_table, gene_id, mt_no, tax_id, paper_name, comment))
	curs.execute("end")
	del reader

"""
2006-10-03
	see how much overlapping between computational and experiments' hits
"""

def get_mt_no2gene_id_set(curs, tf_mapping_table, gene_id_set):
	from sets import Set
	sys.stderr.write("Getting mt_no2gene_id_set from %s"%tf_mapping_table)
	curs.execute("select gene_id, mt_no from %s"%tf_mapping_table)
	rows = curs.fetchall()
	mt_no2gene_id_set = {}
	for row in rows:
		gene_id, mt_no = row
		if gene_id in gene_id_set:
			if mt_no not in mt_no2gene_id_set:
				mt_no2gene_id_set[mt_no] = Set()
			mt_no2gene_id_set[mt_no].add(gene_id)
	sys.stderr.write("Done.\n")
	return mt_no2gene_id_set

def draw_pie_chart(figure_no, fracs, output_fname, mt_symbol, labels= ['comp', 'both', 'expt'], explode=(0, 0.05, 0)):
	import matplotlib
	matplotlib.use("Agg")
	import pylab
	# make a square figure and axes
	pylab.figure(figure_no, figsize=(8,8))
	#ax = axes([0.1, 0.1, 0.8, 0.8])
	#labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
	#fracs = [15,30,45, 10]
	#explode=(0, 0.05, 0, 0)
	pylab.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
	pylab.title('overlapping of  %s targets'%mt_symbol, bbox={'facecolor':0.8, 'pad':5})
	pylab.savefig(output_fname)
	#show()

def draw_pie_charts_of_overlapping_tf_targets(curs, gene_table, output_dir, gene_id2gene_symbol,\
	comp_tf_mapping_table='graph.gene_id2mt_no', expt_tf_mapping_table='graph.tf_mapping'):
	import os,sys
	sys.stderr.write("Getting gene_id set from %s"%gene_table)
	curs.execute("select gene_id from %s"%gene_table)
	from sets import Set
	gene_id_set = Set()
	rows = curs.fetchall()
	for row in rows:
		gene_id_set.add(row[0])
	sys.stderr.write("Done.\n")
	
	comp_mt_no2gene_id_set = get_mt_no2gene_id_set(curs, comp_tf_mapping_table, gene_id_set)
	expt_mt_no2gene_id_set = get_mt_no2gene_id_set(curs, expt_tf_mapping_table, gene_id_set)
	
	comp_mt_no_set = Set(comp_mt_no2gene_id_set.keys())
	expt_mt_no_set = Set(expt_mt_no2gene_id_set.keys())
	overlapping_mt_no_set = comp_mt_no_set&expt_mt_no_set
	sys.stderr.write("Drawing...\n")
	if not os.path.isdir(output_dir):
		os.makedirs(output_dir)
	figure_no = 2
	for mt_no in overlapping_mt_no_set:
		mt_symbol = gene_id2gene_symbol.get(mt_no)
		if mt_symbol:
			print mt_symbol
			comp_only_set = comp_mt_no2gene_id_set[mt_no] - expt_mt_no2gene_id_set[mt_no]
			expt_only_set = expt_mt_no2gene_id_set[mt_no] - comp_mt_no2gene_id_set[mt_no]
			common_set = comp_mt_no2gene_id_set[mt_no] & expt_mt_no2gene_id_set[mt_no]
			total_length = len(comp_only_set) + len(expt_only_set) + len(common_set)
			total_length = float(total_length)
			fracs = [len(comp_only_set)/total_length, len(expt_only_set)/total_length, len(common_set)/total_length]
			output_fname = os.path.join(output_dir, '%s_pie.png'%mt_symbol)
			draw_pie_chart(figure_no, fracs, output_fname, '%s, %s genes'%(mt_symbol, int(total_length)) )
			figure_no += 1
	sys.stderr.write("Done.\n")

	
"""
2006-10-22
	draw some histograms of haifeng's prediction output(p-value, m1_score)
2006-10-31
	draw histograms of all attributes
2006-10-31
	each entry of prediction_data has three columns
	consider unknown data as a third color
	fix a bug
"""
def inspect_prediction_data_m1_score_and_p_value(input_fname, output_dir):
	import csv, numarray, math
	import matplotlib; matplotlib.use("Agg")
	import pylab
	reader = csv.reader(open(input_fname), delimiter='\t')
	prediction_data = [[[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []]]	#[[[],[]]]*7 doens't work. It'll link all five lists.
	#7 entries corresponding to 7 attributes. For each attribute, index 0 is wrong, index 1 is correct, index 2(-1) is unknown
	counter = 0
	for row in reader:
		pattern_id, unknown_percentage, no_of_vertices, no_of_edges, avg_degree, density, supports, vertex_id, \
			is_known, unknown_neighbor_perc, degree, no_of_neighbors = row[:12]
		no_of_gos = len(row[12:])/3
		go_binary_list = row[12:12+no_of_gos*1]
		m1_list = row[12+no_of_gos*1:12+no_of_gos*2]
		p_value_list =row[12+no_of_gos*2:12+no_of_gos*3]
		
		m1_list = map(float, m1_list)
		p_value_list = map(float, p_value_list)
		go_index_with_max_m1_score = numarray.argmax(m1_list)
		m1_score = m1_list[go_index_with_max_m1_score]
		p_value = p_value_list[go_index_with_max_m1_score]
		if p_value==0:
			log_p_value = 50
		else:
			log_p_value = -math.log(p_value)
		
		row = [log_p_value, m1_score, float(supports), float(density), int(no_of_vertices), float(avg_degree), float(unknown_percentage)]
		is_correct = int(go_binary_list[go_index_with_max_m1_score])
		if is_known=='0':	#2006-10-31
			is_correct=-1
		for i in range(len(row)):	#disregard the 1st entry, is_correct
			prediction_data[i][is_correct].append(row[i])
		
		counter+=1
		if counter%2000==0:
			sys.stderr.write("%s%s"%('\x08'*20, counter))
	sys.stderr.write("%s%s\n"%('\x08'*20, counter))
	del reader
	
	if not os.path.isdir(output_dir):
		os.makedirs(output_dir)
	property_label_list = ['p_value', 'm1_score', 'recurrence', 'density', 'cluster_size', 'avg_degree', 'unknown_ratio']
	for i in range(len(property_label_list)):
		histogram_fname = os.path.join(output_dir, 'histogram_%s'%(property_label_list[i]))
		draw_two_color_histogram(prediction_data[i], property_label_list[i], histogram_fname)


def inspect_recurrence_size_scatter(curs, pattern_table):
	import pylab
	curs.execute("DECLARE crs CURSOR for select no_of_vertices, connectivity, recurrence_array from %s"%pattern_table)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	recurrence_ls = []
	size_ls = []
	counter = 0
	while rows:
		for row in rows:
			no_of_vertices, connectivity, recurrence_array = row
			recurrence_array = recurrence_array[1:-1].split(',')
			recurrence_array = map((lambda x: int(float(x)>=0.8)), recurrence_array)
			recurrence = sum(recurrence_array)
			recurrence_ls.append(recurrence)
			size_ls.append(connectivity)
			counter += 1
		sys.stderr.write("%s%s"%('\x08'*20, counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")
	pylab.scatter(size_ls, recurrence_ls, alpha=0.5)
	pylab.show()
	
"""
2006-10-22
	input_fname is output of MpiMarkov.py
"""
def tryRandomForest(input_fname):
	import csv, numarray, math
	reader = csv.reader(open(input_fname), delimiter='\t')
	counter = 0
	real_counter = 0
	known_data = []
	for row in reader:
		pattern_id, unknown_percentage, no_of_vertices, no_of_edges, avg_degree, density, supports, vertex_id, \
			is_known, unknown_neighbor_perc, degree, no_of_neighbors = row[:12]
		no_of_gos = len(row[12:])/3
		go_binary_list = row[12:12+no_of_gos*1]
		m1_list = row[12+no_of_gos*1:12+no_of_gos*2]
		p_value_list =row[12+no_of_gos*2:12+no_of_gos*3]
		if is_known=='1':
			m1_list = map(float, m1_list)
			p_value_list = map(float, p_value_list)
			go_index_with_max_m1_score = numarray.argmax(m1_list)
			p_value = p_value_list[go_index_with_max_m1_score]
			if p_value<1:	#filter out some entries
				#log_p_value = -math.log(p_value)
				is_correct = int(go_binary_list[go_index_with_max_m1_score])
				data_row = [p_value, float(supports), float(density),\
					int(no_of_vertices), m1_list[go_index_with_max_m1_score], is_correct]
				known_data.append(data_row)
				real_counter += 1
		counter += 1
		if counter%5000==0:
			sys.stderr.write("%s%s\t%s"%('\x08'*20, counter, real_counter))
	sys.stderr.write("%s%s\t%s\n"%('\x08'*20, counter, real_counter))
	del reader
	known_data = numarray.array(known_data)
	from rpart_prediction import rpart_prediction
	rpart_prediction_instance = rpart_prediction(debug=1)
	fit_model = rpart_prediction_instance.randomForest_fit(known_data, [0], rpart_prediction_instance.bit_string)
	known_pred = rpart_prediction_instance.randomForest_predict(fit_model, known_data)
	fit_model_py = fit_model.as_py(BASIC_CONVERSION)
	print rpart_prediction_instance.cal_accuracy(known_data,  fit_model_py['predicted'], pred_type=1)
	print self.cal_accuracy(known_data, known_pred, pred_type=2)
	

"""
2006-10-23
	convert MpiMarkov.py's output to R data frame input in order to draw scatter matrix
"""
def convert_prediction_data_to_R(input_fname, output_fname):
	import csv, numarray, math
	reader = csv.reader(open(input_fname), delimiter='\t')
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	counter = 0
	header_row = ['recurrence', 'size', 'density', 'm1_score', 'p_value']
	writer.writerow(header_row)
	for row in reader:
		pattern_id, unknown_percentage, no_of_vertices, no_of_edges, avg_degree, density, supports, vertex_id, \
			is_known, unknown_neighbor_perc, degree, no_of_neighbors = row[:12]
		no_of_gos = len(row[12:])/3
		go_binary_list = row[12:12+no_of_gos*1]
		m1_list = row[12+no_of_gos*1:12+no_of_gos*2]
		p_value_list =row[12+no_of_gos*2:12+no_of_gos*3]
		m1_list = map(float, m1_list)
		p_value_list = map(float, p_value_list)
		go_index_with_max_m1_score = numarray.argmax(m1_list)
		p_value = p_value_list[go_index_with_max_m1_score]
		is_correct = int(go_binary_list[go_index_with_max_m1_score])
		row = [int(supports), int(no_of_vertices), float(density), m1_list[go_index_with_max_m1_score], p_value]
		writer.writerow(row)
		counter += 1
		if counter%5000==0:
			sys.stderr.write("%s%s"%('\x08'*20, counter))
	sys.stderr.write("%s%s\n"%('\x08'*20, counter))
	del reader, writer

"""
2006-10-23
"""
def extract_go_with_max_score_from_prediction_data(input_fname, output_fname):
	import csv, numarray, math
	reader = csv.reader(open(input_fname), delimiter='\t')
	writer = csv.writer(open(output_fname, 'w'), delimiter='\t')
	counter = 0
	header_row = ['gene_no', 'pattern_id', 'go_index', 'is_correct', 'recurrence', 'size', 'density', 'm1_score', 'p_value']
	writer.writerow(header_row)
	for row in reader:
		pattern_id, unknown_percentage, no_of_vertices, no_of_edges, avg_degree, density, supports, vertex_id, \
			is_known, unknown_neighbor_perc, degree, no_of_neighbors = row[:12]
		no_of_gos = len(row[12:])/3
		go_binary_list = row[12:12+no_of_gos*1]
		m1_list = row[12+no_of_gos*1:12+no_of_gos*2]
		p_value_list =row[12+no_of_gos*2:12+no_of_gos*3]
		m1_list = map(float, m1_list)
		p_value_list = map(float, p_value_list)
		go_index_with_max_m1_score = numarray.argmax(m1_list)
		p_value = p_value_list[go_index_with_max_m1_score]
		is_correct = int(go_binary_list[go_index_with_max_m1_score])
		row = [vertex_id, pattern_id, go_index_with_max_m1_score, go_binary_list[go_index_with_max_m1_score], \
			int(supports), int(no_of_vertices), float(density), m1_list[go_index_with_max_m1_score], p_value]
		writer.writerow(row)
		counter += 1
		if counter%5000==0:
			sys.stderr.write("%s%s"%('\x08'*20, counter))
	sys.stderr.write("%s%s\n"%('\x08'*20, counter))
	del reader, writer

"""
2006-10-23
"""
def inspect_all_patterns_edge_freq(curs, pattern_table, edge_freq_hist_output_fname):
	import matplotlib; matplotlib.use("Agg")
	import pylab, networkx
	curs.execute("DECLARE crs CURSOR for select edge_set from %s"%pattern_table)
	curs.execute("fetch 5000 from crs")
	rows = curs.fetchall()
	g = networkx.XGraph()
	counter = 0
	while rows:
		for row in rows:
			edge_set = row[0]
			edge_set = edge_set[2:-2].split('},{')
			for edge in edge_set:
				edge = edge.split(',')
				edge = map(int, edge)
				if g.has_edge(edge):
					freq = g.get_edge(edge[0], edge[1]) + 1
					g.add_edge(edge[0], edge[1], freq)
				else:
					g.add_edge(edge[0], edge[1], 1)
			counter += 1
		sys.stderr.write("%s%s"%('\x08'*20, counter))
		curs.execute("fetch 5000 from crs")
		rows = curs.fetchall()
	curs.execute("close crs")
	print
	edge_frequency_ls = []
	for e in g.edges_iter():
		edge_frequency_ls.append(e[2])
	pylab.figure()
	pylab.xlabel("edge frequency (from %s patterns)"%counter)
	pylab.title("histogram of edge freq from %s"%pattern_table)
	pylab.hist(edge_frequency_ls, 500, alpha=0.5)
	pylab.savefig(edge_freq_hist_output_fname)
	pylab.clf()
	print "%s nodes"%g.number_of_nodes()
	print "%s edges"%g.number_of_edges()
	return g

"""
2006-10-26
	draw some histograms of p_gene table(p-value, m1_score)
2006-10-31
	look at more attributes than m1_score and p_value
	call draw_two_color_histogram()
"""
def inspect_p_gene_table_m1_score_and_p_value(curs, p_gene_table, output_dir):
	import csv, numarray, math
	import matplotlib; matplotlib.use("Agg")
	import pylab
	curs.execute("DECLARE crs1 CURSOR FOR SELECT is_correct, avg_p_value, edge_gradient, recurrence_cut_off, \
			connectivity_cut_off, cluster_size_cut_off, vertex_gradient, unknown_cut_off from %s"%p_gene_table)
	curs.execute("fetch 5000 from crs1")
	rows = curs.fetchall()
	prediction_data = [[[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []], [[], [], []]]	#[[[],[]]]*7 doens't work. It'll link all five lists.
	#7 entries corresponding to 7 attributes. For each attribute, index 0 is wrong, index 1 is correct, index 2 is unknown
	counter = 0
	while rows:
		for row in rows:
			is_correct, p_value, m1_score, recurrence, connectivity, cluster_size, avg_degree, unknown_ratio = row
			if p_value==0:
				log_p_value = 50
			else:
				log_p_value = -math.log(p_value)
			row = [log_p_value, m1_score, recurrence, connectivity, cluster_size, avg_degree, unknown_ratio]
			for i in range(len(row)):	#disregard the 1st entry, is_correct
				prediction_data[i][is_correct].append(row[i])
			counter+=1
		curs.execute("fetch 5000 from crs1")
		rows = curs.fetchall()
		sys.stderr.write("%s%s"%('\x08'*20, counter))
	sys.stderr.write("%s%s\n"%('\x08'*20, counter))
	curs.execute("close crs1")
	
	if not os.path.isdir(output_dir):
		os.makedirs(output_dir)
	property_label_list = ['p_value', 'm1_score', 'recurrence', 'density', 'cluster_size', 'avg_degree', 'unknown_ratio']
	for i in range(len(property_label_list)):
		histogram_fname = os.path.join(output_dir, 'histogram_%s'%(property_label_list[i]))
		draw_two_color_histogram(prediction_data[i], property_label_list[i], histogram_fname)

"""
2006-10-26
	convert p_gene_table to R data frame input in order to draw scatter matrix
"""
def convert_p_gene_table_to_R(curs, p_gene_table, output_fname):
	import csv, numarray, math
	outf = open(output_fname, 'w')
	counter = 0
	row = ['recurrence', 'size', 'density', 'm1_score', 'p_value']
	outf.write("%s\t%s\t%s\t%s\t%s\n"%(row[0], row[1], row[2], row[3], row[4]))
	#writer.writerow(header_row)
	curs.execute("DECLARE crs1 CURSOR FOR SELECT recurrence_cut_off, cluster_size_cut_off, connectivity_cut_off, edge_gradient,\
		avg_p_value from %s"%p_gene_table)
	curs.execute("fetch 5000 from crs1")
	rows = curs.fetchall()
	while rows:
		for row in rows:
			outf.write("%s\t%s\t%s\t%s\t%s\n"%(row[0], row[1], row[2], row[3], row[4]))
			#writer.writerow(row)
			counter += 1
		curs.execute("fetch 5000 from crs1")
		rows = curs.fetchall()
		sys.stderr.write("%s%s"%('\x08'*20, counter))
	sys.stderr.write("%s%s\n"%('\x08'*20, counter))
	curs.execute("close crs1")
	#del writer
	del outf

"""
2006-10-27
"""
def draw_two_color_scatter_plot(x_data, y_data, x_label, y_label, output_fname):
	sys.stderr.write("Drawing scatter plot %s vs %s ..."%(x_label, y_label))
	"""
	x_max = max(max(x_data[0]), max(x_data[1]))
	x_min = min(min(x_data[0]), min(x_data[1]))
	x_extra = (x_max - x_min)*0.1
	y_max = max(max(y_data[0]), max(y_data[1]))
	y_min = min(min(y_data[0]), min(y_data[1]))
	y_extra = (y_max-y_min)*0.1
	"""
	import matplotlib; matplotlib.use("Agg")
	import pylab
	pylab.figure()
	pylab.xlabel(x_label)
	pylab.ylabel(y_label)
	"""
	pylab.xlim(x_min-x_extra, x_max+x_extra)
	pylab.ylim(y_min-y_extra, y_max+y_extra)
	"""
	pylab.scatter(x_data[1], y_data[1], 10, alpha=0, edgecolor='w', facecolor='w')	#just leave a ghost
	pylab.scatter(x_data[0], y_data[0], 10, alpha=0.3, edgecolor='w')
	pylab.savefig(output_fname)
	pylab.clf()
	
	pylab.figure()
	pylab.xlabel(x_label)
	pylab.ylabel(y_label)
	"""
	pylab.xlim(x_min-x_extra, x_max+x_extra)
	pylab.ylim(y_min-y_extra, y_max+y_extra)
	"""
	pylab.scatter(x_data[0], y_data[0], 10, alpha=0, edgecolor='w')	#just leave a ghost
	pylab.scatter(x_data[1], y_data[1], 10, c='r', alpha=0.3, edgecolor='w')
	new_output_fname = '%s2'%output_fname
	pylab.savefig(new_output_fname)
	pylab.clf()
	
	sys.stderr.write("done.\n")

def draw_two_color_histogram(data, label, output_fname):
	"""
	2006-10-31
		add a histogram for the 3rd entry of data if present
	"""
	sys.stderr.write("Drawing histogram %s ..."%label)
	import matplotlib; matplotlib.use("Agg")
	import pylab
	pylab.figure()
	pylab.xlabel(label)
	pylab.hist(data[0], 100, normed=1, alpha=0.4)
	pylab.hist(data[1], 100, normed=1, alpha=0.4, facecolor='r', edgecolor='r')
	if len(data)==3	#2006-10-31
		if len(data[2])>5:
		pylab.hist(data[2], 100, normed=1, alpha=0.4, facecolor='g', edgecolor='g')
	pylab.savefig(output_fname)
	pylab.clf()
	sys.stderr.write("done.\n")

def inspect_patterns_in_prediction_data_by_pylab(input_fname, output_dir):
	"""
	2006-10-31
		fix a bug, is_known=0 should be excluded
	"""
	import csv, numarray, math
	reader = csv.reader(open(input_fname), delimiter='\t')
	counter = 0
	pattern_id2properties = {}
	for row in reader:
		pattern_id, unknown_percentage, no_of_vertices, no_of_edges, avg_degree, density, supports, vertex_id, \
			is_known, unknown_neighbor_perc, degree, no_of_neighbors = row[:12]
		no_of_gos = len(row[12:])/3
		go_binary_list = row[12:12+no_of_gos*1]
		m1_list = row[12+no_of_gos*1:12+no_of_gos*2]
		p_value_list =row[12+no_of_gos*2:12+no_of_gos*3]
		m1_list = map(float, m1_list)
		p_value_list = map(float, p_value_list)
		go_index_with_max_m1_score = numarray.argmax(m1_list)
		p_value = p_value_list[go_index_with_max_m1_score]
		is_correct = int(go_binary_list[go_index_with_max_m1_score])
		if is_known=='1':	#2006-10-31
			if pattern_id not in pattern_id2properties:
				pattern_id2properties[pattern_id] = [0.0, 0.0, int(supports), int(no_of_vertices), float(density), float(avg_degree), \
					float(unknown_percentage)]	#the first two 0,0 are for #wrong, #correct respectively
			pattern_id2properties[pattern_id][is_correct]+=1
		
		counter += 1
		if counter%5000==0:
			sys.stderr.write("%s%s"%('\x08'*20, counter))
	sys.stderr.write("%s%s\n"%('\x08'*20, counter))
	del reader
	#import pdb
	prediction_data = [[[], []], [[], []], [[], []], [[], []], [[], []]]	#[[[],[]]]*5 doens't work. It'll link all five lists.
	for pattern_id, properties in pattern_id2properties.iteritems():
		#pdb.set_trace()
		correct_ratio = float(properties[1])/(properties[0]+properties[1])
		if correct_ratio ==1:
			logit = 100
		else:
			logit = correct_ratio/(1-correct_ratio)
		which_category = int(logit>1)
		for i in range(5):
			prediction_data[i][which_category].append(properties[i+2])
	if not os.path.isdir(output_dir):
		os.makedirs(output_dir)
	property_label_list = ['recurrence', 'size', 'density', 'avg_degree', 'unknown_ratio']
	for i in range(5):
		histogram_fname = os.path.join(output_dir, 'histogram_%s'%(property_label_list[i]))
		draw_two_color_histogram(prediction_data[i], property_label_list[i], histogram_fname)
		for j in range(i+1, 5):
			scatter_plot_fname = os.path.join(output_dir, 'scatterplot_%s_%s'%(property_label_list[i], property_label_list[j]))
			draw_two_color_scatter_plot(prediction_data[i], prediction_data[j], property_label_list[i], property_label_list[j], scatter_plot_fname)


"""
2006-11-19
"""
def get_dataset_no2description(curs, schema=None):
	if schema:
		curs.execute("set search_path to %s"%schema)
	dataset_no2description = {}
	curs.execute("select dataset_no, dataset_id, title from dataset_no2id_geo_view")
	rows = curs.fetchall()
	for row in rows:
		dataset_no, dataset_id, title = row
		dataset_no2description[dataset_no] = '%s, %s'%(dataset_id, title)
	curs.execute("select dataset_no, dataset_id, category, subcategory, experimenter from dataset_no2id_smd_view")
	rows = curs.fetchall()
	for row in rows:
		dataset_no, dataset_id, category, subcategory, experimenter = row
		dataset_no2description[dataset_no] = '%s, %s, %s, %s'%(dataset_id, category, subcategory, experimenter)
	return dataset_no2description

def display_pattern_condition(curs, mcl_id, pattern_table, dataset_no2description):
	from codense.common import pg_1d_array2python_ls
	curs.execute("select recurrence_array from %s where id=%s"%(pattern_table, mcl_id))
	rows = curs.fetchall()
	recurrence_array = rows[0][0]
	recurrence_array = pg_1d_array2python_ls(recurrence_array, float)
	occurrence_cutoff_func = lambda x: int(x>=0.8)
	recurrence_array = map(occurrence_cutoff_func, recurrence_array)
	for i in range(len(recurrence_array)):
		if recurrence_array[i] == 1:
			print i+1, dataset_no2description[i+1]

"""
2006-12-11
	pattern_table could be a good_cluster_table
"""
def draw_connectivity_histogram_of_table(curs, pattern_table, output_fname):
	sys.stderr.write("Getting connectivity_ls ...\n")
	connectivity_ls = []
	curs.execute("DECLARE crs0 CURSOR for select connectivity from %s"%pattern_table)
	counter = 0
	curs.execute("fetch 1000 from crs0")
	rows = curs.fetchall()
	while rows:
		for row in rows:
			connectivity_ls.append(row[0])
			counter += 1
		sys.stderr.write("%s%s"%('\x08'*30, counter))
		curs.execute("fetch 1000 from crs0")
		rows = curs.fetchall()
	curs.execute("close crs0")
	sys.stderr.write("Done.\n")
	
	import matplotlib; matplotlib.use("Agg")
	import pylab
	pylab.clf()
	pylab.title('histogram of connectivity of patterns')
	pylab.xlabel('connectivity')
	pylab.hist(connectivity_ls, 40, normed=1, alpha=0.4)
	pylab.savefig('%s.png'%output_fname, dpi=200)
	pylab.savefig('%s.eps'%output_fname, dpi=200)
	pylab.savefig('%s.svg'%output_fname, dpi=200)

"""
2006-12-17
"""
def get_genes_pred_certain_function(curs, go_no, p_gene_table, gene_p_table, pattern_table, bs_no_table_list):
	

#01-03-06 for easy console
import sys, os, math
bit_number = math.log(sys.maxint)/math.log(2)
if bit_number>40:       #64bit
	sys.path.insert(0, os.path.expanduser('~/lib64/python'))
	sys.path.insert(0, os.path.join(os.path.expanduser('~/script64/annot/bin')))
else:   #32bit
	sys.path.insert(0, os.path.expanduser('~/lib/python'))
	sys.path.insert(0, os.path.join(os.path.expanduser('~/script/annot/bin')))

sys.path.insert(0, os.path.join(os.path.expanduser('~/script/test/python')))
from codense.common import db_connect, form_schema_tables
hostname='zhoudb'
dbname='graphdb'
conn, curs = db_connect(hostname, dbname)

if __name__ == '__main__':
	
	import sys,os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from codense.common import db_connect, form_schema_tables
	hostname='zhoudb'
	dbname='graphdb'
	conn, curs = db_connect(hostname, dbname)
	masked_prom_seq2db(curs, '/home/cmb-01/yuhuang/transfac/prom_seq_mm_masked', 'transfac.prom_seq', need_commit = 1)
	
	#### following codes find patterns given go_no_list
	"""
	if len(sys.argv)==1:
		print "Usage: misc.py schema input_fname lm_bit acc_cut_off given_go_no_list pic_output_dir"
		sys.exit(0)
	schema, input_fname, lm_bit, acc_cut_off, given_go_no_list, pic_output_dir = sys.argv[1:]
	acc_cut_off = float(acc_cut_off)
	given_go_no_list = given_go_no_list.split(',')
	given_go_no_list = map(int, given_go_no_list)
	from sets import Set
	given_go_no_set = Set(given_go_no_list)
	
	schema_instance = form_schema_tables(input_fname, acc_cut_off, lm_bit)
	conn, curs = db_connect(hostname, dbname, schema)
	find_patterns_given_go_no_set(curs, schema_instance, given_go_no_set, pic_output_dir)
	"""
	"""
	#11-02-05 following is to give pleiotropy overview(AS events)
	
	if len(sys.argv)==1:
		print "Usage: misc.py schema picklefile"
		print "\t investigate how alternative splicing or other stuff is correlated to multi-function."
		print
		print "Usage: misc.py schema input_fname lm_bit acc_cut_off type outputfname"
		print "\t type: 0(redundant), 1(non-redundant)"
		print "\t output no_of_genes vs no_of_functions into outputfname(picklefile)"
		print
		print "Usage: misc.py schema input_fname good_cluster_table"
		print "\t investigate patterns entirely from the gene-set from input_fname"
		print
		sys.exit(0)
	
	if len(sys.argv)==4:
		schema, input_fname, good_cluster_table =  sys.argv[1:5]
		conn, curs = db_connect(hostname, dbname, schema)
		gene_set = gene_set_from_file(input_fname)
		find_pattern_within_gene_set(curs, good_cluster_table, gene_set)
	
	if len(sys.argv)==3:
		schema, picklefile =  sys.argv[1:3]
		from codense.common import get_gene_no2no_of_events, get_gene_no2family_size
		conn, curs = db_connect(hostname, dbname, schema)
		
		#12-12-05 test gene_no2no_of_components
		#from codense.common import get_gene_no2no_of_components_given_gene_id_set, get_gene_id2gene_no
		#gene_id2gene_no = get_gene_id2gene_no(curs)
		#gene_no2no_of_components = get_gene_no2no_of_components_given_gene_id_set(curs, gene_id2gene_no, 'Saccharomyces cerevisiae')
		#gene_no2no_of_events = gene_no2no_of_components
		
		#12-12-05 test to see no_of_function2gene_age
		from codense.common import get_tg_tax_id2ca_depth, get_gene_id2ca_depth
		tg_tax_id2ca_depth = get_tg_tax_id2ca_depth(curs, 9606)
		gene_id2ca_depth = get_gene_id2ca_depth(curs, 9606, tg_tax_id2ca_depth)
		gene_no2no_of_functions = get_gene_no2no_of_functions_from_picklefile(picklefile)
		gene_no2family_size = get_gene_no2family_size(curs, 9606)	#12-14-05
		print get_avg_no_of_functions_vs_gene_age_considering_family_size(\
			gene_no2no_of_functions, gene_id2ca_depth, gene_no2family_size)
		
		#12-12-05 test get_gene_no2no_of_tfbs
		#from codense.common import get_gene_no2no_of_tfbs
		#gene_no2no_of_tfbs = get_gene_no2no_of_tfbs(curs, schema='harbison2004')
		#gene_no2no_of_events = gene_no2no_of_tfbs
		
		
		#11-30-05 try network topologies
		#from codense.common import get_gene_no2no_of_topologies
		#input_fname = 'hs_fim_92m5x25bfsdfl10q0_7gf1p0_0001'
		#lm_bit = '000001'
		#acc_cut_off  = 0.6
		#schema_instance = form_schema_tables(input_fname, acc_cut_off, lm_bit)
		#similarity_cutoff = float(sys.argv[3])
		#distance = int(sys.argv[4])
		#gene_no2no_of_events = get_gene_no2no_of_topologies(curs, schema_instance, similarity_cutoff, distance)
		
		#gene_no2no_of_events = get_gene_no2family_size(curs, 9606)	#11-29-05 try family size
		
		#11-29-05 try promoter
		#gene_no2no_of_events = get_gene_no2no_of_events(curs, ensembl2no_of_events_table='graph.ensembl_id2no_of_promoters')
		
		
		#gene_no2no_of_events = get_gene_no2no_of_events(curs, ensembl2no_of_events_table='graph.ensembl2no_of_events')
		#avg_events_vs_no_of_p_funcs = pleiotropy2fraction_as(picklefile, gene_no2no_of_events)
		#avg_events_vs_no_of_p_funcs = pleiotropy2as(picklefile, gene_no2no_of_events)
		#print avg_events_vs_no_of_p_funcs
	
	
	#11-01-05 following is used to filter cluster_bs_table
	
	if len(sys.argv)==1:
		print "Usage: misc.py schema input_fname lm_bit acc_cut_off top_number commit_bit"
		sys.exit(0)
	schema, input_fname, lm_bit, acc_cut_off, top_number, commit_bit = sys.argv[1:]
	acc_cut_off = float(acc_cut_off)
	top_number = int(top_number)
	commit_bit = int(commit_bit)
	schema_instance = form_schema_tables(input_fname, acc_cut_off, lm_bit)
	conn, curs = db_connect(hostname, dbname, schema)
	filter_cluster_bs_table(curs, schema_instance.cluster_bs_table, schema_instance.good_bs_table, top_number, commit_bit)
	
	
	###10-31-05 following is for global pleiotropy of one prediction setting
	
	import sys,os
	sys.path += [os.path.expanduser('~/script/annot/bin')]
	from codense.common import db_connect, p_gene_id_src_set_from_gene_p_table,\
		get_gene_no2p_go_no_set_given_p_gene_id_set, form_schema_tables, p_gene_id_set_from_gene_p_table
	hostname='zhoudb'
	dbname='graphdb'
	if len(sys.argv)==7:
		schema, input_fname, lm_bit, acc_cut_off, type, outputfname = sys.argv[1:]
		acc_cut_off = float(acc_cut_off)
		type = int(type)
		conn, curs = db_connect(hostname, dbname, schema)
		schema_instance = form_schema_tables(input_fname, acc_cut_off, lm_bit)
		if type==0:
			p_gene_id_src_set = p_gene_id_set_from_gene_p_table(curs, schema_instance.gene_p_table)
		else:
			p_gene_id_src_set = p_gene_id_src_set_from_gene_p_table(curs, 'gene_p_test') #schema_instance.gene_p_table)
		gene_no2p_go_no_set 	= get_gene_no2p_go_no_set_given_p_gene_id_set(curs, \
			schema_instance.p_gene_table, p_gene_id_src_set, report=1)
		
		
		#10-31-05 following is for histogram drawing
		no_of_genes_vs_no_of_p_funcs = []	#index is no_of_p_funcs, value is no_of_genes, like histogram
		for gene_no, p_go_no_set in gene_no2p_go_no_set.iteritems():
			no_of_p_funcs = len(p_go_no_set)
			current_length = len(no_of_genes_vs_no_of_p_funcs)
			if no_of_p_funcs>current_length:
				no_of_genes_vs_no_of_p_funcs += [0]*(no_of_p_funcs-current_length)
			no_of_genes_vs_no_of_p_funcs[no_of_p_funcs-1] += 1
		print no_of_genes_vs_no_of_p_funcs
		
		
		#following stuff dumps the object into a picklefile
		no_of_p_funcs2no_of_genes = {}
		for gene_no, p_go_no_set in gene_no2p_go_no_set.iteritems():
			no_of_p_funcs = len(p_go_no_set)
			if no_of_p_funcs not in no_of_p_funcs2no_of_genes:
				no_of_p_funcs2no_of_genes[no_of_p_funcs] = Set()
			no_of_p_funcs2no_of_genes[no_of_p_funcs].add(gene_no)
		import cPickle
		cPickle.dump(no_of_p_funcs2no_of_genes, open(outputfname, 'w'))
		"""
