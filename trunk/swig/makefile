#This is a makefile for swig from c++ or c to python.
#Take an example:
#1. code example.c, example.h(if necessary) and example.i
#2. swig -python example.i (generate example_wrap.c or example_wrap.cxx)
#3. compile example.c and example_wrap.c
#4. link example.o and example_wrap.o to _example.so

CTARGETS = _example.so
CPPTARGETS = _graph.so _list.so
CPPWRAP = graph_wrap.cc list_wrap.cc

C_COMPILER = gcc
CPP_COMPILER = g++

INCLUDE = -I/usr/include/python2.3

CFLAGS =  
CPPFLAGS = 

LINKFLAGS = -shared

.SUFFIXES:	.i	.cc	.c	.o	.so	_wrap.o


all:	$(CTARGETS) $(CPPTARGETS)

example_wrap.c:	%_wrap.c:	%.i
	swig -python $<

$(CPPWRAP):	%_wrap.cc:	%.i
	swig -c++ -python -o $@ $<

%_wrap.o:	%_wrap.c
	$(C_COMPILER) $(INCLUDE) $(CFLAGS) -c $< -o $@
	
%_wrap.o:	%_wrap.cc
	$(CPP_COMPILER) $(INCLUDE) $(CPPFLAGS) -c $< -o $@
	
.c.o:
	$(C_COMPILER) $(INCLUDE) $(CFLAGS) -c $< -o $@

.cc.o:
	$(CPP_COMPILER) $(INCLUDE) $(CPPFLAGS) -c $< -o $@

$(CPPTARGETS):	_%.so:	%.o %_wrap.o
	$(CPP_COMPILER) $(LINKFLAGS) $^ -o $@


$(CTARGETS):	_%.so:	%.o %_wrap.o
	$(C_COMPILER) $(LINKFLAGS) $^ -o $@



clean:
	-rm  -f *.o *.pyc *.so *_wrap.c *_wrap.cc
