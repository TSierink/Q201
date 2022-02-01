#!/bin/bash
END=120
for i in $(seq 0 $END);
do 
    echo $i
    until netqasm simulate --formalism=dm --network-config-file ../yamlfolder/network$i.yaml | grep "fidelities" >> ../results_epl.txt;
    do 
        :
    done; 
done