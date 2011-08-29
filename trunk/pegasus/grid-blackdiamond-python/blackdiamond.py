#!/usr/bin/env python

from Pegasus.DAX3 import *
import sys
import os

if len(sys.argv) != 2:
	print "Usage: %s PEGASUS_HOME" % (sys.argv[0])
	sys.exit(1)

# Create a abstract dag
diamond = ADAG("diamond")

# Add input file to the DAX-level replica catalog
a = File("f.a")
a.addPFN(PFN("file://" + os.getcwd() + "/f.a", "local"))
diamond.addFile(a)
	
# Add executables to the DAX-level replica catalog
# In this case the binary is keg, which is shipped with Pegasus, so we use
# the remote PEGASUS_HOME to build the path.
e_preprocess = Executable(namespace="diamond", name="preprocess", version="4.0", os="linux", arch="x86_64")
e_preprocess.addPFN(PFN("file://" + sys.argv[1] + "/bin/keg", "TestCluster"))
diamond.addExecutable(e_preprocess)
	
e_findrange = Executable(namespace="diamond", name="findrange", version="4.0", os="linux", arch="x86_64")
e_findrange.addPFN(PFN("file://" + sys.argv[1] + "/bin/keg", "TestCluster"))
diamond.addExecutable(e_findrange)
	
e_analyze = Executable(namespace="diamond", name="analyze", version="4.0", os="linux", arch="x86_64")
e_analyze.addPFN(PFN("file://" + sys.argv[1] + "/bin/keg", "TestCluster"))
diamond.addExecutable(e_analyze)

env = Executable(namespace="diamond", name="env", version="4.0", os="linux", arch="x86_64")
env.addPFN(PFN("file:///usr/bin/env", "TestCluster"))
diamond.addExecutable(env)

# Add a preprocess job
preprocess = Job(namespace="diamond", name="preprocess", version="4.0")
b1 = File("f.b1")
b2 = File("f.b2")
preprocess.addArguments("-a preprocess","-T60","-i",a,"-o",b1,b2)	#3600 is in seconds
preprocess.uses(a, link=Link.INPUT)
preprocess.uses(b1, link=Link.OUTPUT)
preprocess.uses(b2, link=Link.OUTPUT)
preprocess.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="65"))	#65 is in minutes
diamond.addJob(preprocess)

# Add left Findrange job
frl = Job(namespace="diamond", name="findrange", version="4.0")
c1 = File("f.c1")
frl.addArguments("-a findrange","-T60","-i",b1,"-o",c1)
frl.uses(b1, link=Link.INPUT)
frl.uses(c1, link=Link.OUTPUT)
frl.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="65"))
diamond.addJob(frl)

# Add right Findrange job
frr = Job(namespace="diamond", name="findrange", version="4.0")
c2 = File("f.c2")
frr.addArguments("-a findrange","-T60","-i",b2,"-o",c2)
frr.uses(b2, link=Link.INPUT)
frr.uses(c2, link=Link.OUTPUT)
frr.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="65"))
diamond.addJob(frr)

# Add Analyze job
analyze = Job(namespace="diamond", name="analyze", version="4.0")
d = File("f.d")
analyze.addArguments("-a analyze","-T600","-i",c1,c2,"-o",d)
analyze.uses(c1, link=Link.INPUT)
analyze.uses(c2, link=Link.INPUT)
analyze.uses(d, link=Link.OUTPUT, register=True)
analyze.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="650"))
diamond.addJob(analyze)

# Add env job
env_job = Job(namespace="diamond", name=env.name, version="4.0")
#env_out = File("env.out")
#env_job.addArguments(">", env_out)
#env_job.uses(env_out, link=Link.OUTPUT, register=True)
env_job.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="5"))
diamond.addJob(env_job)

# Add control-flow dependencies
diamond.addDependency(parent=preprocess, child=frl)
diamond.addDependency(parent=preprocess, child=frr)
diamond.addDependency(parent=frl, child=analyze)
diamond.addDependency(parent=frr, child=analyze)

# Write the DAX to stdout
diamond.writeXML(sys.stdout)



