#!/bin/sh
# r = 5: batch of root sets for identities.py (output: ../results/identities_r5.txt)
PY=../../.venv/bin/python
for u in -1 2 -2 3 -3 1/2 -1/2 1/3 -1/3 4 -4 3/2 -3/2 2/3 -2/3 5 -5; do for d in 10 12; do $PY identities.py $d 5 1 $u; done; done
for u in 2 -2 1/2 -1/2 3 -3 1/3 -1/3; do for d in 10 12; do $PY identities.py $d 5 1 -1 $u; done; done
for d in 10 12; do $PY identities.py $d 5 1 2 3; $PY identities.py $d 5 1 2 4; $PY identities.py $d 5 1 2 1/2; $PY identities.py $d 5 1 -1 2 -2; $PY identities.py $d 5 1 -1 2 1/2; done
for q in 1,0,1 1,1,1 1,-1,1 -2,0,1 2,0,1 -1,-1,1 -3,0,1 3,0,1; do for d in 10 12 14; do $PY identities.py $d 5 $q; $PY identities.py $d 5 1 $q; $PY identities.py $d 5 1 -1 $q; done; done
for d in 10 12; do $PY identities.py $d 5 1 -1 1,1,1 1,-1,1; $PY identities.py $d 5 1 -1 1,0,1 1,1,1; $PY identities.py $d 5 1,0,1 1,1,1 1,-1,1; done
echo BATCH_DONE
