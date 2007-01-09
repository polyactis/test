#!/bin/sh
#2007-01-07


#batch diff the current version with all the old versions and see if the difference contains 'edge'
for line in `svn log -q Schema2Darwin.py`
do
	version=`echo $line |awk '/^r/ {print $1}'`
	echo $version
	if test -n $version
	then
		svn diff -$version Schema2Darwin.py |grep edge
	fi
done