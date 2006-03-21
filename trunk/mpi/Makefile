#a makefile for mpi

Target	= hello
CxxCompiler	= mpicxx

all:	$(Target)

.cc.o:
	-$(CxxCompiler) $(CxxFlags) -c $< -o $@

$(Target):	%:	%.o
	-$(CxxCompiler) $(CxxFlags) $< -o $@

clean:
	-rm -f *.o $(Target)
