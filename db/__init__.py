import os, sys, config
from simplemysql import SimpleMysql

'''
	Initate MYSQL Database
'''
def connect():
	return SimpleMysql(
		host=config.DB_HOST,
		db=config.DB_NAME,
		user=config.DB_USER,
		passwd=config.DB_PASS,
		keep_alive=True,  # try and reconnect timedout mysql connections?,
		autocommit=True,
	)

db = connect()