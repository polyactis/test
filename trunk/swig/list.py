# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _list

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


class List(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, List, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, List, name)
    def __repr__(self):
        return "<C List instance at %s>" % (self.this,)
    def __init__(self, *args):
        _swig_setattr(self, List, 'this', _list.new_List(*args))
        _swig_setattr(self, List, 'thisown', 1)
    def __del__(self, destroy=_list.delete_List):
        try:
            if self.thisown: destroy(self)
        except: pass
    __swig_setmethods__["length"] = _list.List_length_set
    __swig_getmethods__["length"] = _list.List_length_get
    if _newclass:length = property(_list.List_length_get, _list.List_length_set)

class ListPtr(List):
    def __init__(self, this):
        _swig_setattr(self, List, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, List, 'thisown', 0)
        _swig_setattr(self, List,self.__class__,List)
_list.List_swigregister(ListPtr)


