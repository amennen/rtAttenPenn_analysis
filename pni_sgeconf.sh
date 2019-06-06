#!/bin/bash

lists="q p hgrp prj e"
nonlists="conf sconf rqs c"

qconf -sconf >/dev/null 2>&1
(( ! $? == 0 )) && echo "not an SGE cluster, quitting." && exit 1

# configurations that are singletons, not lists
for i in $nonlists ; do
  qconf -s${i}
done

# get list members and iterate over them
for i in $lists ; do
  qconf -s${i}l
  m=$(qconf -s${i}l)
  for j in $m ; do
     echo "info for $j ..."
     qconf -s${i} ${j}
  done
done

# get some info about currently running stuff
qstat -F

