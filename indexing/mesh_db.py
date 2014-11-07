#!/usr/bin/env python
import re
import sys
from optparse import OptionParser
import pprint
import DBFactoryMesh as lite;


usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option('-s', '--source', dest='source',
                  help="source txt file to get mesh terms")
parser.add_option('-d', '--database', dest='db', default='mesh_test.db',
                  help="database for sqlite3 connect")
parser.add_option('-t', '--table', dest='table', default='mesh_parse',
                  help="table name within database to insert mesh values for article")
(options, args) = parser.parse_args()

output = dict()
pattern = re.compile('MH  - ')

f = open(options.source,'r')

output['pmid'] = int(f.readline()[6:-1])
output['mesh_tags'] = []

for line in f:
	if (pattern.match(line)):
		secondary = line[6:-1].split('/')
		output['mesh_tags'].append([secondary.pop(0), secondary])
f.close()

# for key in output.keys():
	# pprint.pprint(output[key])

with lite.dbConnectorMesh(options.db) as db_conn:
    db_conn.saveInformation(output, options.table);
pass;