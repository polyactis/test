#!/usr/bin/env python


import sys, time

class ProgressIndicator:
	"""
	A progress indicator intended for terminal output (relies on ^H).
	
	Indicator style, given as constructor argument, can be
	0: percentage; 1: bar; or 2: both. Default is 0.
	
	If using styles 1 or 2, an optional width argument
	for the bar portion can also be given (default 60).
	
	Example usage:
	# First emit whatever prefaces the indicator, if desired
	print " status:",
	sys.__stdout__.flush()
	# Create a new indicator
	p = ProgressIndicator(2)
	p.newIndicator()
	# With each iteration through a task, or as often as you want,
	# call updateProgress(), passing 2 numbers: amount completed,
	# and total amount to do.
	limit = 300000
	for i in range(limit):
	p.updateProgress(i, limit)
	print
	"""
	
	_style = 0  # 0=percent, 1=bar, 2=both
	_lasttime = int(time.time())
	_barwidth = 60
	_hashchar = '*'
		
	def __init__(self, style=0, width=60):
		if style:
			self._style = style
			if width is not None:
				self._barwidth = width
		return
		
	def newIndicator(self, style=None, width=None):
		"""
		Start a new indicator at 00%.
		Optional style and width arguments are same as constructor.
		"""
		if style is not None:
			self._style=style
		if self._style and width is not None:
			self._barwidth = width * (width > 3) or 3
		if self._style==0:
			print " 00%",
		elif self._style==1:
			print "|%s|" % (" " * (self._barwidth - 2)),
		elif self._style==2:
			print "|%s|  00%%" % (" " * (self._barwidth - 2)),
		sys.__stdout__.flush()
		return
	
	def reset(self):
		"""
		Reset an indicator that is being re-used after reaching 100%.
		"""
		if self._style==0:
			self._erasePercent()
		elif self._style==1:
			self._eraseBar()
		elif self._style==2:
			self._eraseBoth()
		self._lasttime = int(time.time()) - 1
		self.newIndicator()
		return
		
	def _erasePercent(self):
		print "\x08" * 5 + " " * 4 + "\x08" * 5,
		return
	
	def _eraseBar(self):
		print "\x08" * (self._barwidth + 2),
		return
	
	def _eraseBoth(self):
		print "\x08" * (self._barwidth + 7),
	
	def updateProgress(self, cur, limit):
		"""
		Update an existing indicator to reflect given progress.
		Arguments are amount completed so far, and total to do.
		For example, if 4 out of 30 have been completed, call
		updateProgress(4,30).
		"""
		currenttime = int(time.time())
		if cur+1 >= limit or currenttime > self._lasttime:
			if self._style==0:
				self._updateProgressPercent(cur, limit)
			elif self._style==1:
				self._updateProgressBar(cur, limit)
			elif self._style==2:
				self._updateProgressBoth(cur, limit)
			self._lasttime = currenttime
		return
		
	def _updateProgressPercent(self, cur, limit):
		pct = int((cur+1)*100/limit)
		print "%s%s%%" % ("\x08" * 5,
						  " " * (pct < 100) + "%02d" % pct,
						 ),
		sys.__stdout__.flush()
		return
	
	def _updateProgressBar(self, cur, limit):
		hashwidth = int(float(cur+1)/limit * (self._barwidth - 2))
		print "%s%s%s" % ("\x08" * (self._barwidth),
						  self._hashchar * hashwidth,
						  " " * (self._barwidth - hashwidth - 2) + "|"
						 ),
		sys.__stdout__.flush()
		return
	
	def _updateProgressBoth(self, cur, limit):
		hashwidth = int(float(cur+1)/limit * (self._barwidth - 2))
		pct = int((cur+1)*100/limit)
		print "%s%s%s %s%%" % ("\x08" * (self._barwidth + 5),
							   self._hashchar * hashwidth,
							   " " * (self._barwidth - hashwidth - 2) + "|",
							   " " * (pct < 100) + "%02d" % pct,
							  ),
		sys.__stdout__.flush()
		return
		


if __name__ == '__main__':
	limit = 500000
	
	# percent indicator
	print " status:",
	sys.__stdout__.flush()
	p = ProgressIndicator()
	p.newIndicator()
	for i in range(limit):
		p.updateProgress(i, limit)
	print
	
	# bar indicator
	print " status:",
	p.newIndicator(1, 60)
	for i in range(limit):
		p.updateProgress(i, limit)
	print
	# bar and percent indicators
	print " status:",
	sys.__stdout__.flush()
	p.newIndicator(2,60)
	for i in range(limit):
		p.updateProgress(i, limit)
	print
