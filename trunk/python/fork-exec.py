#!/usr/bin/env python
"""

03-19-05
	modeled after fork-exec.c in the test repositary

"""

import os, sys

print "Right before process duplicating..."

child_id = os.fork()
if child_id!=0:
	print "This is parent process: %s"%os.getpid()

else:
	print "This is child process: %s with parent id: %s"%(os.getpid(), os.getppid())
	#exec* family functions will replace the current child process. So the child process won't
	#run code after the if block.
	os.execvp("sh",["sh",'-c', 'ls /'])
	
wait_status = os.wait()

print "wait status is (pid,status): %s"%repr(wait_status)

if os.WIFEXITED(wait_status[1]):
	print "child process exits with exit code:%s"%os.WEXITSTATUS(wait_status[1])
else:
	print "child process exits abnormally"
	
print "done with main program"
