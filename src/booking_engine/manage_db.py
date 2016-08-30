from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import sys, time
import MySQLdb
import server_setting.settings

def execute_query(query, db_name):
	db = connect_db(db_name)
	cursor = db.cursor()
	cursor.execute(query)
	columns = cursor.description 
	result = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
	return result

# def execute_query_single_row(query):
# 	db = connect_db()
# 	cursor = db.cursor()
# 	cursor.execute(query)
# 	columns = cursor.description
# 	result = {}
# 	value = cursor.fetchone()
# 	for i in range (0, len(columns)):
# 		result[columns[i][0]] = value[i]
# 	return result

# def execute_query_result(query):
# 	db = connect_db()
# 	cursor = db.cursor()
# 	cursor.execute(query)
# 	result = cursor.fetchall()
# 	return result

def connect_db(db_name):
	return MySQLdb.connect(user=server_setting.settings.DATABASES[db_name]['USER'], db=server_setting.settings.DATABASES[db_name]['NAME'], passwd=server_setting.settings.DATABASES[db_name]['PASSWORD'], host=server_setting.settings.DATABASES[db_name]['HOST'])