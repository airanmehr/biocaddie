#!/usr/bin/env python
import re
import sys
from optparse import OptionParser
from collections import defaultdict
import pickle
# import pprint
from dbModule import DBFactoryMesh as lite;
import sqlite3;

usage = "usage: prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option('-s', '--source', dest='source',
              	help="source txt file to get mesh terms")
parser.add_option('-d', '--database', dest='db', default='mesh_test.db',
                help="database for sqlite3 connect")
parser.add_option('-t', '--table1', dest='table1', default='article_mesh',
                help="table name to insert mesh header for each article")
# parser.add_option('-T', '--table2', dest='table2', default='header_entry',
#                 help="table name to upsert entry terms for each mesh header")
(options, args) = parser.parse_args()

article_mesh = defaultdict(list)
header_entry = defaultdict(list)

pattern_pid = re.compile('PMID- ')
pattern_mesh = re.compile('MH  - ')

f = open(options.source,'r')
for line in f:
	# empty lines separate each medline article, first line always pmid
	if pattern_pid.match(line):
		pmid = line[6:-1]
	if (pattern_mesh.match(line)):
		entry_terms = line[6:-1].split('/')
		# print(secondary)
		header = entry_terms.pop(0)
		# print(mesh_terms)
		article_mesh[pmid].append(header)
		# print('pmid: ',pmid, 'with header', article_mesh[pmid])
		header_entry[header].append(entry_terms)
f.close()

# for key,value in article_mesh.iteritems():
# 	print(key, value)

# remove duplicate entry terms associated with header & unnest entry terms
for key in header_entry:
	temp = [item for sublist in header_entry[key] for item in sublist]
	header_entry[key] = list(set(temp))
	# print(key, list(header_entry[key]))

with lite.dbConnectorMesh(options.db) as db_conn:
    db_conn.saveInformation(article_mesh, options.table1);
    # db_conn.upsert(header_entry, options.table2);
pass;

fp = open('header_entry.pkl','ab')
pickle.dump(header_entry, fp)
fp.close()