from pymongo import MongoClient
from config import *
import string, random, datetime

def getRandomToken(len = 10):
	pool = string.letters + string.digits
	return ''.join(random.choice(pool) for _ in xrange(len))

def getClient(host = MONGO_HOST):
	if host:
		client = MongoClient(host)
		return client
	return None

def getDatabase():
	client = getClient()
	return client.yazlo if client else None

def access_token_valid(access_token):
	if access_token is None:
		return False
	seconds_difference = (datetime.datetime.utcnow() - access_token["date_created"]).seconds
	if seconds_difference >= TOKEN_TIMEOUT:
		mainDB = getDatabase()
		if mainDB:
			mainDB.tokens.delete_one({"token": access_token["token"]})
		return False
	return True

def user_total_db(mainDB, access_token):
	databases = mainDB.databases.find({"author": access_token["author"]})
	return databases.count() if databases else 0

def user_total_tables(mainDB, db_id, access_token):
	tables = mainDB.tables.find({"author": access_token["author"], "database_id": db_id})
	return tables.count() if tables else 0