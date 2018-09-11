#!/usr/bin/python

#import common code and the json lib
import common, json
#create new common object so we can access common code
c =  common.common()
#get settings from the database
settings = c.get_settings()
#return settings in JSON format for front-end
print("Content-type: application/json\n")
print(json.dumps(settings, default=str))
