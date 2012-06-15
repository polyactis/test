#!/usr/bin/env python

import sys, os, math
sys.path.insert(0, os.path.expanduser('~/lib/python'))
sys.path.insert(0, os.path.join(os.path.expanduser('~/script')))

def testVerticalSurface():
	import pylab, numpy
	pylab.clf()
	
	no_of_phenotypes = 5
	x, y = numpy.mgrid[0:2*no_of_phenotypes:1, 0:10:1]	#added a gap of 1 column between two phenotypes. one phenotype occupies two rows & two columns.
	
	
	#remove the gap in x & y
	needed_index_ls = [0,5]
	#for i in [0, 5]:
	#	for j in xrange(no_of_phenotypes):
	#		needed_index_ls.append(no_of_phenotypes*i+j)
	#for i in range(0, no_of_phenotypes):
	#	needed_index_ls.append(2*i)
		#needed_index_ls.append(3*i+1)
		#y[3*i+1][1]=2
	x = x[:, needed_index_ls]
	y = y[:, needed_index_ls]
	
	enrichment_matrix = numpy.ones(x.shape, numpy.float)
	enrichment_matrix[:,:] =10
	enrichment_matrix[0,0]=3
	
	from enthought.mayavi import mlab
	mlab.clf()
	from pymodule.yh_mayavi import customBarchart
	bar = customBarchart(x, y , enrichment_matrix, y_scale=4.5, opacity=1, mode='cube', color=(0,1,0), scale_factor=1.0, x_scale=0.9)
	"""
	#mlab.ylabel("KW")
	#mlab.xlabel("Emma")
	#mlab.zlabel("Enrichment Ratio")
	from pymodule.DrawMatrix import get_font 
	font = get_font()
	
	for i in range(len(xlabel_ls)):
		label = xlabel_ls[i]
		char_width, char_height = font.getsize(label)	#W is the the biggest(widest)
		
		mlab.text(2*i, 0, label, z=0, width=char_width/1500.)	#min(0.0075*len(label), 0.04))
	
	"""
	s = numpy.zeros(x.shape, numpy.int)
	#s[0,1]=0.5
	surf = mlab.surf(x, y, s, opacity=0.6, extent=[-1, 2*no_of_phenotypes, -1, 10, 0.0,0.0])
	mlab.show()
	
if __name__ == '__main__':
	testVerticalSurface()