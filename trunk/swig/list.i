%module list
%{
#include "list.h"
%}
%include "cstring.i"
%cstring_bounded_mutable(char* my_name, 1024);
%cstring_bounded_mutable(char* m_name, 1024);
%include "list.h"
