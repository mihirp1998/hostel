import MySQLdb
import pandas as pd
import numpy as np
def hello():
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
	                     user="root",         # your username
	                     passwd="helloworld",  # your password
	                     db="hostel")        # name of the data base
	cur = db.cursor()
	cur.execute("select * from StudentInput;")
	arr = []
	for row in cur.fetchall():
	    arr.append(list(row))
	df = pd.DataFrame(arr)
	df.to_csv('sql.csv')
	df = df.transpose()
	val = df.values.tolist()
	# db.close()
	return db,cur
def connectDb():
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
	                     user="root",         # your username
	                     passwd="helloworld",  # your password
	                     db="hostel")        # name of the data base


	cur = db.cursor()
	return db,cur
def createCsv():
	global cur
	db,cur = connectDb()
	cur.execute("select id,name,Room_No,Block from StudentInput where status='P';")
	arr = []
	for row in cur.fetchall():
	    arr.append(list(row))
	df = pd.DataFrame(arr)	
	# return df
	allyear = ['Block','2011F', '2011H', '2012F', '2012H', '2013F', '2013H','2014F', '2014H', '2015F', '2015H', '2016F', '2016H', '2017F', '2017H']
	hyear = ['2011H', '2012H', '2013H', '2013H', '2014H', '2015H', '2016H', '2017H']
	fyear = ['2011F', '2012F', '2013F', '2013F', '2014F', '2015F', '2016F', '2017F']
	year =  ['2011', '2012', '2013', '2014', '2015', '2016', '2017']
	block = ['A','B','C','D','G']
	
	summaryDf = pd.DataFrame(np.zeros((len(block),len(allyear))),columns=allyear,index=block,dtype=np.int8)
	# summaryDf.iloc[:,0] = first_col
	for i in year:
		k = i + 'F'
		for j in range(len(block)):
			summaryDf.ix[j,k] = (df.iloc[:,0].str.contains(i) &  df.iloc[:,3].str.contains(block[j]) &  df.iloc[:,0].str.contains("A")).sum()

	for i in year:
		k = i + 'H'
		for j in range(len(block)):
			summaryDf.ix[j,k] = (df.iloc[:,0].str.contains(i) &  df.iloc[:,3].str.contains(block[j]) &  df.iloc[:,0].str.contains("H")).sum()
	summaryDf.loc["Total",:] = summaryDf.sum(axis=0)
	summaryDf.loc[:,"Total"] = summaryDf.sum(axis=1)
	return summaryDf
