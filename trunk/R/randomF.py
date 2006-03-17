"""
03-16-06
	testing the randomF.r
"""

#read data
known_data = []
import csv
reader = csv.reader(open('/tmp/hs_fim_92m5x25bfsdfl10q0_7gf1.known', 'r'), delimiter='\t')
reader.next()
is_correct_list = []
for row in reader:
	p_value, recurrence, connectivity, cluster_size, gradient, gene_no, go_no, is_correct = row
	known_data.append([float(p_value), float(recurrence), float(connectivity), float(cluster_size), float(gradient), int(gene_no), int(go_no)])
	is_correct_list.append(is_correct)

del reader

from numarray import array
from rpy import r, set_default_mode,NO_CONVERSION,BASIC_CONVERSION
set_default_mode(NO_CONVERSION)
#pack data into data_frame
known_data = array(known_data)
data_frame = r.as_data_frame({"p_value":known_data[:,0], "recurrence":known_data[:,1], "connectivity":known_data[:,2], \
		"cluster_size":known_data[:,3], "gradient":known_data[:,4]})

#start to call randomF.r to run randomForest
r.source('randomF.r')
set_default_mode(BASIC_CONVERSION)
rf_result = r.randomF(data_frame, is_correct_list)
print dir(rf_result)
print rf_result
