import os
import sys
import config.settings
import json
from dotenv import load_dotenv
load_dotenv()


# create settings object corresponding to specified env
APP_ENV = os.environ.get('APP_ENV', 'Prod')
_current = getattr(sys.modules['config.settings'], '{0}Config'.format(APP_ENV))


# copy attributes to the module for convenience
for atr in [f for f in dir(_current) if '__' not in f]:
	val = os.environ.get(atr, getattr(_current, atr))	# environment can override anything
	setattr(sys.modules[__name__], atr.upper(), val)


'''
	config.get("config_name") return real-time config from database
	config.config_name return cached config from database
'''

def parse_type(value, vtype):
	vtype = vtype if vtype else "str"
	try:
		if vtype == "int":
			value = int(value)
		elif vtype == "str":
			value = str(value)
		elif vtype == "json":
			value = json.loads(value)
		elif vtype == "bool":
			value = True if (value == 'true' or value == "True" or (value != "0" and value != 0)) else False
	except:
		pass
	return value

def get(name):
	# Config in cache
	if hasattr(sys.modules[__name__], name.upper()):
		return getattr(sys.modules[__name__], name.upper())
	
	from db import db
	query_config = db.getOne('config', ['type', 'value'], ('name=%s OR name=%s', [name.upper(), name]))
	if not query_config or not hasattr(query_config, 'value'):
		raise Exception("Config not found.")
	
	value = parse_type(query_config.value, query_config.type)

	return value
	

