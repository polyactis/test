#!/usr/bin/env python
"""
Usage:	

Option:

	
Examples:


Description:

"""
import sys, os, math, random


no_of_samplings = 10000000
result = 0
for i in range(no_of_samplings):
	x = random.random()
	result += math.sin(1/x)*math.sin(1/x)

print result/no_of_samplings
