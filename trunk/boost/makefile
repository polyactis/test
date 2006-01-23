#a makefile for Boost.Graph

Target	= test_dynamic_bit_set
GslLib	= -lgsl -lgslcblas
CxxFlags	= -O2
CxxCompiler	= g++

all:	$(Target)

.cc.o:
	-$(CxxCompiler) $(CxxFlags) -c $< -o $@

$(Target):	%:	%.o
	-$(CxxCompiler) $(CxxFlags) $(GslLib) $< -o $@

clean:
	-rm -f *.o $(Target)
