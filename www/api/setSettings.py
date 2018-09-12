#!/usr/bin/python

import sys
sys.path.insert(0, '../python')

import common, json

c = common.common()


#print header
print("Content-type: application/json\n")
print(json.dumps({'succes': True}, default=str))
