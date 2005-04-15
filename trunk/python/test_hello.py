#!/usr/bin/env python
"""
04-15-05

test hello.so(boost::python)

"""

import hello
hello.set_module_and_type('Numeric', 'ArrayType')
instance = hello.World("Hi.")
dc={1:'NA',2:'123'}
from Numeric import *
ar = array([[1,2],[3,4]])
br = hello.exercise(ar)
result = instance.return_keys(dc,2,ar)
