#!/usr/bin/env python
import re
import sys
from optparse import OptionParser
from collections import defaultdict
import pickle
# import pprint
import DBFactoryMesh as lite;
import sqlite3;

usage = "usage: prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option('-s', '--source', dest='source',
              	help="pickle file to open")
parser.add_option('-d', '--database', dest='db', default='mesh_test.db',
                help="database for sqlite3 connect")
parser.add_option('-t', '--table1', dest='table1', default='header_entry',
                help="table name to upsert entry terms for each mesh header")
(options, args) = parser.parse_args()

header_entry = defaultdict(list)

pkl = open(options.source,'rb')
# pkl = pickle.load(f)
for i in range(975):
# for i in range(10):
	temp = pickle.load(pkl)
	if i % 10 == 0:
		print ('loading pickle...'+str(round(i/975.,2))+'%')
	for key,value in temp.iteritems():
		header_entry[key] = value
pkl.close()

with lite.dbConnectorMesh(options.db) as db_conn:
    # db_conn.saveInformation(article_mesh, options.table1);
    db_conn.upsert(header_entry, options.table1);
pass;


# remove duplicate entry terms associated with header & unnest entry terms
# for key in header_entry:
	# temp = [item for sublist in header_entry[key] for item in sublist]
	# header_entry[key] = list(set(temp))
	# print(key, header_entry[key])