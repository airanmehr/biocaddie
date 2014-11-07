#!/bin/bash

for (i=3; i<=100; i++); do
	A="python mbiocaddie/indexing/parser/main.py patternList ../../../PubMed/PMC_XML/PMC_batch"
	batch_num=$i
	C=".xml ../../../hctest.db"
	run = $A$batch_num$C
    echo $run
done