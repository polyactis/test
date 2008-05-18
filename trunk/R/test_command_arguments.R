#!/usr/bin/env Rscript
#2008-05-17 test how to pass arguments to an R standalone program. $* stands for all the arguments on the shell commandline after $0
#R --vanilla --args $0 $* <<EOF

command_args = commandArgs()	#command_args starts with ["/usr/lib/R/bin/exec/R", "--vanilla", "--args"]
print(command_args)


#EOF below is optional
#EOF