%module list
%{
#include "list.h"
%}
%include "cstring.i"
%cstring_bounded_mutable(char* my_name, 1024);
%cstring_bounded_mutable(char* m_name, 1024);
%include "std_vector.i"
%include "std_string.i"
namespace std {
	%template(IntVector) vector<int>;
	%template(FloatVector) vector<float>;
	%template(DoubleVector) vector<double>;
	%template(StringVector) vector<string>;
}

%include "list.h"
