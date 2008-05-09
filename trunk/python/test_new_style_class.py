#!/usr/bin/env python
"""
2008-05-09
	test new-style class, staticmethod, classmethod
"""
class classa(object):
	name = 'haha'
	def __init__(self, debug):
		self.debug = int(debug)
	def func2(self, a,b):
		print 'from func2: ', a,a,b,b
	
	def func0(a,b):
		print 'from func0:', a,b
	func0 = staticmethod(func0)
	
	def func3(cls, a, b):
		print 'from func3:', a,b, cls
		classa.func0(a,b)
		cls.func0(a,b)
		cls.func2(classa(0), a, b)	#TypeError: unbound method func2() must be called with classa instance as first argument (got str instance instead)
	func3 = classmethod(func3)
	
	def func1(a,b):
		print 'from func1:', a,b
		print classa.name
		#print self.debug	#no varible named as self
		#print classa.debug	#not initialized yet
		#classa.func2(a,b)	#doesn't work with normal class functions.
		classa.func3(a,b)
		#classa.func3(classa, a, b)	#TypeError: func3() takes exactly 3 arguments (4 given)
	func1 = staticmethod(func1)

classa.func1('a',2)
