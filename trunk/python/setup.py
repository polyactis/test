#!/usr/bin/env python
"""
the build file for spam.c

"""
from distutils.core import setup, Extension

module1 = Extension('spam',
                    sources = ['spam.c'])

setup (name = 'spam',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
