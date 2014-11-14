#!/bin/bash

for i in {0..1}
do
	A="python mesh_db.py -s ../../../PubMed/MEDLINE/Medline_batch"
	C=".xml -d mesh.db -t article_mesh"
	run=$A$i$C
    echo $run
done