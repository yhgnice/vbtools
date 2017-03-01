#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on '2017/2/22 17:38'

import MySQLdb


def getData():
	try:
		database = MySQLdb.connect(host='188.188.1.158', user='root', port=3306, passwd='lhb!@#$', db='aj2_gamedata_v2',
		                           charset='utf8')
		cursor = database.cursor()
		sql = "select f_id,f_name from t_goodmodel "
		cursor.execute(sql)
		result = cursor.fetchall()
		return result
		database.close()
	except Exception, e:
		print e


def WriteSql(data):
	Dlist = []
	for k,v in data:
		dsql = '''replace into t_goodmodel ({f_id}, {f_name});'''.format(f_id=k,f_name=(v).encode('utf-8'))
		print dsql
		
 
	# with open('t_goodmodel.txt', 'a') as f:
	# 	f.write(data)
	# 	f.write('\n')
	# 	f.close()


if __name__ == '__main__':
	sqldata = getData()
	WriteSql(sqldata)
 