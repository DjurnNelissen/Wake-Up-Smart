#!/usr/bin/python

import sys
sys.path.insert(0, '../python')

import common, json, cgi

form = cgi.FieldStorage()
c = common.common()

for key in form.keys():
        variable = str(key)
        value = str(form.getvalue(variable))
        c.update_setting(variable, value)

c.close_database_connection()

print("Content-type: application/json\n")
print(json.dumps({'succes': True}, default=str))
