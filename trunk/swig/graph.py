# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _graph

def _swig_setattr(self,class_type,name,value):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    self.__dict__[name] = value

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


GENE_CUT_OFF = _graph.GENE_CUT_OFF
JK_CUT_OFF = _graph.JK_CUT_OFF
COR_CUT_OFF = _graph.COR_CUT_OFF
class graph_construct(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, graph_construct, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, graph_construct, name)
    def __repr__(self):
        return "<C graph_construct instance at %s>" % (self.this,)
    def __init__(self, *args):
        _swig_setattr(self, graph_construct, 'this', _graph.new_graph_construct(*args))
        _swig_setattr(self, graph_construct, 'thisown', 1)
    def __del__(self, destroy=_graph.delete_graph_construct):
        try:
            if self.thisown: destroy(self)
        except: pass
    def cor_array_readin(*args): return _graph.graph_construct_cor_array_readin(*args)
    def general_split(*args): return _graph.graph_construct_general_split(*args)
    def input(*args): return _graph.graph_construct_input(*args)
    def edge_construct(*args): return _graph.graph_construct_edge_construct(*args)
    def output(*args): return _graph.graph_construct_output(*args)
    def cor(*args): return _graph.graph_construct_cor(*args)
    def bv_or(*args): return _graph.graph_construct_bv_or(*args)
    def bv_count(*args): return _graph.graph_construct_bv_count(*args)
    def split(*args): return _graph.graph_construct_split(*args)

class graph_constructPtr(graph_construct):
    def __init__(self, this):
        _swig_setattr(self, graph_construct, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, graph_construct, 'thisown', 0)
        _swig_setattr(self, graph_construct,self.__class__,graph_construct)
_graph.graph_construct_swigregister(graph_constructPtr)


