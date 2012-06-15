#a makefile for Boost.Graph

Target	= first custom_syntax multiple_sources option_groups options_description real regex response_file
GslLib	= -lboost_program_options
CxxFlags	= -O2
CxxCompiler	= g++

all:	$(Target)

.cc.o:
	- $(CxxCompiler) $(CxxFlags) -c $< -o $@

$(Target):	%:	%.o
	- $(CxxCompiler) $(CxxFlags) $(GslLib) $< -o $@

clean:
	-rm -f *.o $(Target)
