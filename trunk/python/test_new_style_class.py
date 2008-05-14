#!/usr/bin/env python
"""
2008-05-09
	test new-style class, staticmethod, classmethod
"""
class classa(object):
	name = 'haha'
	def __init__(self, debug):
		self.debug = int(debug)
		self.func4(1,2)
	
	def func4(cls, a, b):
		print 'from func4:', a,b, cls
		
	func4 = classmethod(func4)
	
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

"""
05/09/08
	block below from http://users.rcn.com/python/download/Descriptor.htm
"""
class RevealAccess(object):
	"""
	05/09/08
		from http://users.rcn.com/python/download/Descriptor.htm
	A data descriptor that sets and returns values
	   normally and prints a message logging their access.
	"""
	
	def __init__(self, initval=None, name='var'):
		self.val = initval
		self.name = name
	
	def __get__(self, obj, objtype):
		print 'Retrieving', self.name
		return self.val
	
	def __set__(self, obj, val):
		print 'Updating' , self.name
		self.val = val

class MyClass(object):
	x = RevealAccess(10, 'var "x"')
	y = 5

m = MyClass()
print "isinstance(m, MyClass): ",isinstance(m, MyClass)
print m.x
m.x = 20
print m.x
print m.y

class C(object):
	def getx(self): return self.__x
	def setx(self, value): self.__x = value
	def delx(self): del self.__x
	x = property(getx, setx, delx, "I'm the 'x' property.")

c = C()
#print c.x
c.x = 10
print c.x
c.setx(10)
print c.x
