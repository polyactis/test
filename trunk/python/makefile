#a makefile for Boost.Python

BoostPythonExt	= hello.so
IncludeDir	= -I/usr/include/python2.3
BoostPythonLib	= -lboost_python

ExtFlags	= -shared -fPIC
CxxFlags	= -O2

CxxCompiler	= g++

all:	$(BoostPythonExt)

.cc.o:
	$(CxxCompiler) $(CxxFlags) $(IncludeDir) -c $< -o $@

$(BoostPythonExt):	%.so:	%.o
	$(CxxCompiler) $(CxxFlags) $(ExtFlags) $(BoostPythonLib) $< -o $@

clean:
	-rm -f *.o $(BoostPythonExt)
