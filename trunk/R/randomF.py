#!/usr/bin/env python
"""
03-16-06
	testing the randomF.r
"""

#read data
def read_data(input_fname):
	data = []
	import csv
	reader = csv.reader(open(input_fname, 'r'), delimiter='\t')
	reader.next()
	is_correct_list = []
	for row in reader:
		p_value, recurrence, connectivity, cluster_size, gradient, gene_no, go_no, is_correct = row
		data.append([float(p_value), float(recurrence), float(connectivity), float(cluster_size), float(gradient), int(gene_no), int(go_no), int(is_correct)])
	del reader
	return data, is_correct_list

known_fname = '/tmp/hs_fim_92m5x25bfsdfl10q0_7gf1.known'
unknown_fname = '/tmp/hs_fim_92m5x25bfsdfl10q0_7gf1.unknown'

known_data, known_is_correct_list = read_data(known_fname)
unknown_data, unknown_is_correct_list = read_data(unknown_fname)

from numarray import array
from rpy import r, set_default_mode,NO_CONVERSION,BASIC_CONVERSION
set_default_mode(NO_CONVERSION)
#pack data into data_frame
known_data = array(known_data)
known_data_frame = r.as_data_frame({"p_value":known_data[:,0], "recurrence":known_data[:,1], "connectivity":known_data[:,2], \
	"cluster_size":known_data[:,3], "gradient":known_data[:,4]})
unknown_data = array(unknown_data)
unknown_data_frame = r.as_data_frame({"p_value":unknown_data[:,0], "recurrence":unknown_data[:,1], "connectivity":unknown_data[:,2], \
	"cluster_size":unknown_data[:,3], "gradient":unknown_data[:,4]})
#start to call randomF.r to run randomForest
r.library('randomForest')
r.source('randomF.r')
#rf_model still needs to be in pure R object
rf_model = r.randomF(known_data_frame, known_data[:,-1])

set_default_mode(BASIC_CONVERSION)
unknown_pred = r.predictRandomF(rf_model, unknown_data_frame)

rf_model= rf_model.as_py(BASIC_CONVERSION)
print rf_model.keys()
print rf_model['confusion']
