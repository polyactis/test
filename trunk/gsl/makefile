gsl_lib		= -lgsl -lgslcblas
gsl_cxx_targets	= gsl_example gsl_eigen
cxx_flags	= -O2 -Wall
cxx_compiler	= g++
gsl_c_targets	= gsl_histo_example
c_flags		= -O2 -Wall
c_compiler	= gcc


all:	$(gsl_cxx_targets) $(gsl_c_targets)

$(gsl_cxx_targets):	%:	%.o
	$(cxx_compiler) $(cxx_flags) $(gsl_lib) $< -o $@

.cc.o:
	$(cxx_compiler) $(cxx_flags) -c $< -o $@

$(gsl_c_targets):	%:	%.o
	$(c_compiler) $(c_flags) $(gsl_lib) $< -o $@

.c.o:
	$(c_compiler) $(c_flags) -c $< -o $@

clean:
	-rm -f *.o $(gsl_cxx_targets) $(gsl_c_targets)
