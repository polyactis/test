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


def db_connect(psycopg, hostname, dbname, schema=None):
	"""
	02-28-05
		establish database connection, return (conn, curs).
		copied from CrackSplat.py
	03-08-05
		parameter schema is optional
	"""
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
	def __init__(self):
		self.gene_no2go_no = {}
		self.go_no2edge_matrix_data = {}
	
	def run(self):
		import psycopg
		import sys
		conn,curs = db_connect(psycopg, "zhoudb","graphdb","sc_54_6661")
		
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



if __name__ == '__main__':
	instance = get_edge_data()
	instance.run()
