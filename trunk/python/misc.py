"""
04-27-05
	miscellaneous functions used in python's interactive mode
"""


def take_list(source_list,index_list):
	"""
	04-27-05
		functions like Numeric.take, but work on list
	"""
	new_list = []
	for i in index_list:
		new_list.append(source_list[i])
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


from Numeric import array,transpose
import csv

def transposed_matrix(filename):
	"""
	04-29-05
	"""
	
	list_2d = []
	reader = csv.reader(open(filename,'r'),delimiter='\t')
	for row in reader:
		row = map(float,row)
		list_2d.append(row)
	matrix = array(list_2d[1:])
	m1 = transpose(matrix)
	return m1

def output_transposed_matrix(filename, m1):
	"""
	04-29-05
	"""
	writer = csv.writer(open(filename,'w'),delimiter='\t')
	for i in range(55):
		row = [i]+m1[i].tolist()
		writer.writerow(row)
	del writer
