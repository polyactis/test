#!/usr/bin/env python

from Pegasus.DAX3 import *
import sys
import os

if len(sys.argv) != 3:
	print "Usage: %s PEGASUS_HOME SITE" % (sys.argv[0])
	sys.exit(1)

pegasus_home = sys.argv[1]
site_handler = sys.argv[2]
#2011.11.16
if site_handler!='condorpool':	#other sites need the initial input to be from "local", where it knows how to transfer.
	input_site_handler = 'local'
else:
	input_site_handler = site_handler
# Create a abstract dag
diamond = ADAG("whatever")
namespace='diamond'
version=1.0
memoryForSmallJob=5
memoryForLargeJob=7000

# Add input file to the DAX-level replica catalog
a = File("f.a")
a.addPFN(PFN("file://" + os.getcwd() + "/f.a", input_site_handler))
diamond.addFile(a)
	
# Add executables to the DAX-level replica catalog
# In this case the binary is keg, which is shipped with Pegasus, so we use
# the remote PEGASUS_HOME to build the path.
e_preprocess = Executable(namespace=namespace, name="preprocess", version=version, os="linux", arch="x86_64", installed=True)
e_preprocess.addPFN(PFN("file://" + pegasus_home + "/bin/keg", site_handler))
diamond.addExecutable(e_preprocess)
	
e_findrange = Executable(namespace=namespace, name="findrange", version=version, os="linux", arch="x86_64", installed=True)
e_findrange.addPFN(PFN("file://" + pegasus_home + "/bin/keg", site_handler))
diamond.addExecutable(e_findrange)
	
e_analyze = Executable(namespace=namespace, name="analyze", version=version, os="linux", arch="x86_64", installed=True)
e_analyze.addPFN(PFN("file://" + pegasus_home + "/bin/keg", site_handler))
diamond.addExecutable(e_analyze)

env = Executable(namespace=namespace, name="env", version=version, os="linux", arch="x86_64", installed=True)
env.addPFN(PFN("file:///usr/bin/env", site_handler))
diamond.addExecutable(env)


# Add a preprocess job
preprocess = Job(namespace=namespace, name=e_preprocess.name, version=version)
b1 = File("f.b1")
b2 = File("f.b2")
preprocess.addArguments("-a preprocess","-T30","-i",a,"-o",b1,b2)	#3600 is in seconds
preprocess.uses(a, link=Link.INPUT, transfer=True, register=True)
preprocess.uses(b1, link=Link.OUTPUT, transfer=True, register=True)
preprocess.uses(b2, link=Link.OUTPUT, transfer=True, register=True)
preprocess.addProfile(Profile(Namespace.CONDOR, key="request_cpus", value="3"))
preprocess.addProfile(Profile(Namespace.CONDOR, key="request_memory", value="%s"%(memoryForLargeJob)))
preprocess.addProfile(Profile(Namespace.CONDOR, key="request_disk", value="1024"))
#preprocess.addProfile(Profile(Namespace.CONDOR, key="requirements", value="(memory>=%s)"%7000))
preprocess.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="65"))	#65 is in minutes
#preprocess.addProfile(Profile(Namespace.GLOBUS, key="max_time", value="75"))
#preprocess.addProfile(Profile(Namespace.GLOBUS, key="max_cpu_time", value="70"))
preprocess.addProfile(Profile(Namespace.GLOBUS, key="minmemory", value="100"))
#preprocess.addProfile(Profile(Namespace.GLOBUS, key="count", value="4"))
#preprocess.addProfile(Profile(Namespace.GLOBUS, key="jobtype", value="multi"))
diamond.addJob(preprocess)


# Add left Findrange job
frl = Job(namespace=namespace, name=e_findrange.name, version=version)
c1 = File("f.c1")
frl.addArguments("-a findrange","-T60","-i",b1,"-o",c1)
frl.uses(b1, link=Link.INPUT)
frl.uses(c1, link=Link.OUTPUT)
frl.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="65"))
frl.addProfile(Profile(Namespace.CONDOR, key="request_cpus", value="1"))
frl.addProfile(Profile(Namespace.CONDOR, key="request_memory", value="%s"%(memoryForSmallJob)))
frl.addProfile(Profile(Namespace.CONDOR, key="request_disk", value="1024"))
#frl.addProfile(Profile(Namespace.CONDOR, key="requirements", value="(memory>=%s)"%500))
diamond.addJob(frl)

# Add right Findrange job
frr = Job(namespace=namespace, name=e_findrange.name, version=version)
c2 = File("f.c2")
frr.addArguments("-a findrange","-T60","-i",b2,"-o",c2)
frr.uses(b2, link=Link.INPUT, transfer=True, register=True)
frr.uses(c2, link=Link.OUTPUT, transfer=True, register=True)
frr.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="65"))
frr.addProfile(Profile(Namespace.CONDOR, key="request_cpus", value="1"))
frr.addProfile(Profile(Namespace.CONDOR, key="request_memory", value="%s"%(memoryForSmallJob)))
frr.addProfile(Profile(Namespace.CONDOR, key="request_disk", value="1024"))
#frr.addProfile(Profile(Namespace.CONDOR, key="requirements", value="(memory>=%s)"%memoryForSmallJob))
diamond.addJob(frr)

#2011.11.16 add 10 findrange jobs
for i in xrange(10):
	findrangeJob = Job(namespace=namespace, name=e_findrange.name, version=version)
	output = File("f.c%s"%i)
	findrangeJob.addArguments("-a findrange", "-T600", "-i", b2, "-o", output)
	findrangeJob.uses(b2, link=Link.INPUT, transfer=True, register=True)
	findrangeJob.uses(output, link=Link.OUTPUT, transfer=True, register=True)
	findrangeJob.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="650"))
	#findrangeJob.addProfile(Profile(Namespace.CONDOR, key="request_cpus", value="1"))
	#findrangeJob.addProfile(Profile(Namespace.CONDOR, key="request_memory", value="%s"%(memoryForSmallJob)))
	#findrangeJob.addProfile(Profile(Namespace.CONDOR, key="request_disk", value="1024"))
	#findrangeJob.addProfile(Profile(Namespace.CONDOR, key="requirements", value="(memory>=%s)"%memoryForSmallJob))
	diamond.addJob(findrangeJob)
	diamond.addDependency(Dependency(parent=preprocess, child=findrangeJob))

# Add Analyze job
analyzeJob = Job(namespace=namespace, name=e_analyze.name, version=version)
d = File("f.d")
analyzeJob.addArguments("-a analyze","-T60","-i",c1,c2,"-o",d)
analyzeJob.uses(c1, link=Link.INPUT, transfer=True, register=True)
analyzeJob.uses(c2, link=Link.INPUT, transfer=True, register=True)
analyzeJob.uses(d, link=Link.OUTPUT, transfer=True, register=True)
analyzeJob.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="650"))
analyzeJob.addProfile(Profile(Namespace.CONDOR, key="request_cpus", value="1"))
analyzeJob.addProfile(Profile(Namespace.CONDOR, key="request_memory", value="%s"%memoryForSmallJob))
analyzeJob.addProfile(Profile(Namespace.CONDOR, key="requirements", value="(memory>=%s)"%memoryForSmallJob))
#analyzeJob.addProfile(Profile(Namespace.GLOBUS, key="count", value="3"))
#analyzeJob.addProfile(Profile(Namespace.GLOBUS, key="jobtype", value="single"))
diamond.addJob(analyzeJob)

# Add env job
env_job = Job(namespace=namespace, name=env.name, version=version)
#env_out = File("env.out")
#env_job.addArguments(">", env_out)
#env_job.uses(env_out, link=Link.OUTPUT, transfer=True, register=True)
env_job.addProfile(Profile(Namespace.GLOBUS, key="maxwalltime", value="5"))
#env_job.addProfile(Profile(Namespace.CONDOR, key="request_cpus", value="1"))
#env_job.addProfile(Profile(Namespace.CONDOR, key="request_memory", value="%s"%memoryForSmallJob))
#env_job.addProfile(Profile(Namespace.CONDOR, key="request_disk", value="1024"))
#env_job.addProfile(Profile(Namespace.CONDOR, key="requirements", value="(memory>=%s)"%memoryForSmallJob))
diamond.addJob(env_job)

# Add control-flow dependencies
diamond.addDependency(Dependency(parent=preprocess, child=frl))
diamond.addDependency(Dependency(parent=preprocess, child=frr))
diamond.addDependency(Dependency(parent=frl, child=analyzeJob))
diamond.addDependency(Dependency(parent=frr, child=analyzeJob))

#2011-11-16 another way of specifying dependency
#diamond.depends(parent=preprocess, child=frl)
#diamond.depends(parent=preprocess, child=frr)
#diamond.depends(parent=frl, child=analyzeJob)
#diamond.depends(parent=frr, child=analyzeJob)

# Write the DAX to stdout
diamond.writeXML(sys.stdout)
