# 2009-11-10 yh: makefile
CFLAGS	= -O3
CXXFLAGS	= -fPIC $(CFLAGS)
CXXCOMPILER = g++

all:	sort_vardata

sort_vardata:	sort_vardata.cpp
	-$(CXXCOMPILER) $(CXXFLAGS) -o $@ $<

clean:
	-rm sort_vardata