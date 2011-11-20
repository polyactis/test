#!/bin/bash

if test $# -lt 1 ; then
	echo "Please specify local or other site name as argument. Examples:"
	echo "  $0 TargetSite [InputSite] [CLUSTER_PEGASUS_HOME]"
	echo ""
	echo "	This script calls blackdiamond.py to generate a black diamond dag in xml."
	echo "	TargetSite is the site on which the dag would run."
	echo "	Default InputSite is local."
	echo "	CLUSTER_PEGASUS_HOME could be /u/home/eeskin/point/bin/pegasus or /home/cmb-03/mn/yuhuang/bin/pegasus depending on the site for hoffman2/uschpc. For local or condorpool, omit it so it's set to the default self-detected PEGASUS_HOME."
	exit 1
fi

TargetSite=$1
InputSite=$2
CLUSTER_PEGASUS_HOME=$3
# figure out where Pegasus is installed
export PEGASUS_HOME=`which pegasus-plan | sed 's/\/bin\/*pegasus-plan//'`
if [ "x$PEGASUS_HOME" = "x" ]; then
	echo "Unable to determine location of your Pegasus install"
	echo "Please make sure pegasus-plan is in your path"
	exit 1
fi 

echo PEGASUS_HOME: $PEGASUS_HOME

if [ "x$InputSite" = "x" ]; then
	InputSite="local"
fi 

if [ "x$CLUSTER_PEGASUS_HOME" = "x" ]; then
	CLUSTER_PEGASUS_HOME=$PEGASUS_HOME
fi 
# generate the input file
echo "This is sample input to KEG" >f.a
# generate the dax
export PYTHONPATH=$PYTHONPATH:$PEGASUS_HOME/lib/python
echo "./blackdiamond.py $CLUSTER_PEGASUS_HOME $InputSite $TargetSite \>blackdiamond.dax"
./blackdiamond.py $CLUSTER_PEGASUS_HOME $InputSite $TargetSite >blackdiamond.dax

