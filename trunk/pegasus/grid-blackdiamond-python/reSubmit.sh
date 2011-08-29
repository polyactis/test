#!/bin/sh

workdir=$1
pegasus-run -Dpegasus.user.properties=$workdir/pegasus*.properties --nodatabase $workdir
