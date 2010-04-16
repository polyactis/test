#!/usr/bin/env python

"""
2008-05-28 copied from collections_demo.py and line_collection.py, line_collection2.py
testing collections' picker events
"""
from pylab import *
from matplotlib.collections import LineCollection

def on_canvas_pick(event):
	print dir(event)
	import pdb
	pdb.set_trace()

def draw():
	# In order to efficiently plot many lines in a single set of axes,
	# Matplotlib has the ability to add the lines all at once. Here is a
	# simple example showing how it is done.
	N = 50
	x = arange(N)
	# Here are many sets of y to plot vs x
	ys = [x+i*10 for i in x]
	
	# We need to set the plot limits, the will not autoscale
	fig = gcf()
	ax = fig.add_subplot(2,1,1)
	#ax = axes()
	ax.set_xlim((amin(x),amax(x)))
	ax.set_ylim((amin(amin(ys)),amax(amax(ys))))
	
	# colors is sequence of rgba tuples
	# linestyle is a string or dash tuple. Legal string values are
	#		  solid|dashed|dashdot|dotted.  The dash tuple is (offset, onoffseq)
	#		  where onoffseq is an even length tuple of on and off ink in points.
	#		  If linestyle is omitted, 'solid' is used
	# See matplotlib.collections.LineCollection for more information
	line_segments = LineCollection([zip(x,y) for y in ys], # Make a sequence of x,y pairs
									linewidths	= (0.5,1,1.5,2),
									linestyle = 'solid', picker=True)
	line_segments.set_array(x)
	ax.add_collection(line_segments)
	fig.canvas.mpl_connect('pick_event', on_canvas_pick)
	axcb = fig.colorbar(line_segments)
	axcb.set_label('Line Number')
	ax.set_title('Line Collection with mapped colors')
	sci(line_segments) # This allows interactive changing of the colormap.
	
	ax = fig.add_subplot(2,1,2)
	ax.scatter(x,x, picker=True)
	
	
	show()

def draw2():
	import pylab as P
	from matplotlib import collections, axes, transforms
	from matplotlib.colors import colorConverter
	import matplotlib.numerix as N
	
	nverts = 50
	npts = 100
	
	# Make some spirals
	r = N.array(range(nverts))
	theta = N.array(range(nverts)) * (2*N.pi)/(nverts-1)
	xx = r * N.sin(theta)
	yy = r * N.cos(theta)
	spiral = zip(xx,yy)
	
	# Make some offsets
	xo = P.randn(npts)
	yo = P.randn(npts)
	xyo = zip(xo, yo)
	
	# Make a list of colors cycling through the rgbcmyk series.
	colors = [colorConverter.to_rgba(c) for c in ('r','g','b','c','y','m','k')]
	
	fig = P.figure()
	fig.canvas.mpl_connect('pick_event', on_canvas_pick)
	a = fig.add_subplot(2,1,1)
	col = collections.LineCollection([spiral], offsets=xyo,
									transOffset=a.transData, picker=True)
		# Note: the first argument to the collection initializer
		# must be a list of sequences of x,y tuples; we have only
		# one sequence, but we still have to put it in a list.
	a.add_collection(col, autolim=True)
		# autolim=True enables autoscaling.  For collections with
		# offsets like this, it is neither efficient nor accurate,
		# but it is good enough to generate a plot that you can use
		# as a starting point.  If you know beforehand the range of
		# x and y that you want to show, it is better to set them
		# explicitly, leave out the autolim kwarg (or set it to False),
		# and omit the 'a.autoscale_view()' call below.
	
	# Make a transform for the line segments such that their size is
	# given in points:
	trans = transforms.scale_transform(fig.dpi/transforms.Value(72.),
										fig.dpi/transforms.Value(72.))
	col.set_transform(trans)  # the points to pixels transform
	col.set_color(colors)
	
	a.autoscale_view()  # See comment above, after a.add_collection.
	a.set_title('LineCollection using offsets')
	
	
	# The same data as above, but fill the curves.
	
	a = fig.add_subplot(2,1,2)
	
	col = collections.PolyCollection([spiral], offsets=xyo,
									transOffset=a.transData)
	col._picker =True
	a.add_collection(col, autolim=True)
	trans = transforms.scale_transform(fig.dpi/transforms.Value(72.),
										fig.dpi/transforms.Value(72.))
	col.set_transform(trans)  # the points to pixels transform
	col.set_color(colors)
	
	
	a.autoscale_view()
	a.set_title('PolyCollection using offsets')
	P.show()

def drawArrow():
	"""
	2010-4-15
		test drawing arrow
	"""
	import pylab
	pylab.clf()
	arrow_params={'length_includes_head':True, 'shape':'right', \
		'head_starts_at_zero':True}
	
	pylab.arrow(0.1, 0.1, 0.8, 0.5, \
			fc='blue', ec='red', alpha=0.6, width=0.1, head_width=0.3, \
			head_length=0.2, **arrow_params)
	pylab.annotate("start",
			xy=(0.2, 0.2), xycoords='data',
			xytext=(0.8, 0.8), textcoords='data',
			arrowprops=dict(arrowstyle="->", color='b', 
							connectionstyle="arc3"),
			picker=True,)
	pylab.show()
	
def drawLegend():
	"""
	2010-4-15
		test legend
	"""
	import numpy as np
	import matplotlib.pyplot as plt
	
	a = np.arange(0,3,.02)
	b = np.arange(0,3,.02)
	c = np.exp(a)
	d = c[::-1]
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(a,c,'k--',a,d,'k:',a,c+d,'k')
	bbox_props = dict(boxstyle="round", fc="r", ec="0.5", alpha=0.5)	#2010-4-15 text()'s bbox argument value 
	leg = ax.legend(('Model length', 'Data length', 'Total message length'),
				'upper center', shadow=True)#, bbox=bbox_props)	#2010-4-15 legen() doesn't accept bbox argument. text() does. 
	ax.set_ylim([-1,20])
	ax.grid(False)
	ax.set_xlabel('Model complexity --->')
	ax.set_ylabel('Message length --->')
	ax.set_title('Minimum Message Length')
	
	ax.set_yticklabels([])
	ax.set_xticklabels([])
	
	# set some legend properties.  All the code below is optional.  The
	# defaults are usually sensible but if you need more control, this
	# shows you how
	
	# the matplotlib.patches.Rectangle instance surrounding the legend
	frame  = leg.get_frame()  
	frame.set_facecolor('0.80')	# set the frame face color to light gray
	frame.set_alpha(0.60)
	
	#bbox = leg.get_bbox_patch()	# 2010-4-15 get_bbox_patch() is only for text()
	
	# matplotlib.text.Text instances
	for t in leg.get_texts():
		t.set_fontsize('small')	# the legend text fontsize
	
	# matplotlib.lines.Line2D instances
	for l in leg.get_lines():
		l.set_linewidth(1.5)  # the legend line width
	plt.show()


if __name__ == '__main__':
	drawArrow()