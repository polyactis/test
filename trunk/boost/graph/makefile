#a makefile for Boost.Graph

GraphTarget	= bgl_test kevin-bacon quick_tour undirected connected_components file_dependencies subgraph johnson-eg
GslLib	= -lgsl -lgslcblas
CxxFlags	= -O2
CxxCompiler	= g++

all:	$(GraphTarget)

.cc.o:
	-$(CxxCompiler) $(CxxFlags) -c $< -o $@

$(GraphTarget):	%:	%.o
	-$(CxxCompiler) $(CxxFlags) $(GslLib) $< -o $@

clean:
	-rm -f *.o $(GraphTarget)
