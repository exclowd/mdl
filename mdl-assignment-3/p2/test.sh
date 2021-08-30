#! /bin/bash

python q2.py > qp.pomdp
# cp q2.txt q2.pomdp
./pomdpsol qp.pomdp
./pomdpsim --simLen 1000 --simNum 100 --policy-file out.policy ./qp.pomdp