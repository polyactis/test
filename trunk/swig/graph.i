%module graph
%{
#include "graph.h"
%}
%include "cstring.i"
%cstring_mutable(char * g_name);
%include "graph.h"
