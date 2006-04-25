#!/usr/bin/env python
#04-24-06 (add comment, program written long time ago) how fast python is compared against c++(hello.cpp)
import sys
import math
for i in range(6000):
	for j in range(i,6000):
		math.sqrt(2.0)
sys.stdout.write("hello, I'm 8 today\n")
