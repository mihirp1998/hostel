from __future__ import print_function
from sqlalchemy import create_engine

from app import app
from flask import render_template,request,send_from_directory,send_file,Response
import PIL
# import lsh.lshparser as lshparser
import pandas as pd
import numpy as np
import warnings
from flask import make_response, redirect,jsonify
from functools import wraps, update_wrapper
import MySQLdb
from werkzeug.exceptions import HTTPException, NotFound
import sys
from werkzeug import secure_filename

cur = None
roomno,name,block,idno,key,table,chair,misc = None,None,None,None,None,None,None,None

@app.route("/answer", methods=['GET', 'POST'])
def predict():
	if request.method == 'POST':
		train_batch,train_label_batch,test_batch,test_label_batch = getData()
		cost,ans = sess.run([loss,a2],feed_dict={xP:X_test,yP:Y_test})

	else:
		print ('no post')
	return render_template('result_page.html',tables=[final_result.to_html()],thequery=printquery, 
										synonymquery=synonymquery, val=val, val1=val1)


@app.route('/uploader', methods = [ 'POST'])
def upload_file():
	global headVal,bodyVal,m
	global check
	try:
		f = request.files['file']
		print(type(f))
		f.save(secure_filename('./file.csv'))
		engine = create_engine("mysql://hostel:hostel123@localhost/hostel")
		con = engine.connect()
		# df = pd.DataFrame.from_csv('./file.csv')
		df = pd.DataFrame.from_csv('./file.csv',index_col=None)
		df.columns = ['id','name','Room_No','Block']
		df.to_sql('Student',con,if_exists='append',index= False)
		return render_template('insertExcel.html',article='<p>File Uploaded</p>')
	except Exception as e:
		print(e)
		check = False
		return render_template('insertExcel.html',article='<p>Reupload! File Not Uploaded</p>')
@app.route('/uploadD', methods = [ 'POST'])
def delete_file():
	global headVal,bodyVal,m
	global check
	try:
		f = request.files['file']
		print(type(f))
		f.save(secure_filename('./file.csv'))
		df = pd.DataFrame.from_csv('./file.csv',index_col=None)
		removeIds = df.transpose().values.tolist()[0]
		print(removeIds)
		removeIds = [str(i) for i in removeIds]
		db,cur = connectDb()
		cur.execute("update Student set status = 'E' where id in %s", [removeIds])
		db.commit()
		db.close()
		# df = pd.DataFrame.from_csv('./file.csv')

		return render_template('deleteExcel.html',article='<p>File Uploaded</p>')
	except Exception as e:
		print(e)
		check = False
		return render_template('deleteExcel.html',article='<p>Reupload! File Not Uploaded</p>')		


@app.route("/getInfo", methods=['POST','GET'])
def  getInfo():
	global cur,roomno,name,block,idno,key,table,chair,misc
	print("Info Sent")
	db,cur = connectDb()
	idno = request.args['name']
	cur.execute("select * from Student where id = %s", [idno])
	for row in cur.fetchall():
		roomno = row[2]
		name = row[1]
		block = row[3]
		key = row[4]
		table = row[5]
		chair = row[6]
		misc = row[7]

	db.close()	
	print(idno)
	return 'Success'

@app.route("/nextInfo")
def  nextInfo():
	print(name,roomno,block,idno)
	return render_template('display.html',name=name,room=roomno,block=block,id=idno,keyl= key,tablel=table,chairl=chair,miscl=misc)	

@app.route("/dataSave",methods=["POST","GET"])
def dataSave():
	print("hello")
	db,cur = connectDb()
	r = request.form['r']
	i = request.form['i']
	b = request.form['b']
	k = request.form['k']
	t = request.form['t']
	c = request.form['c']
	m = request.form['m']
	print("data",r,b,i,k,t,c,m)
	cur.execute("UPDATE Student SET  Room_No= %s, Block= %s, keyl = %s,tablel = %s, chairl = %s, misc = %s  WHERE id = %s;",[r,b,k,t,c,m,i])
	db.commit()
	result_set = cur.fetchall()
	print(result_set)
	print(request.form,"no",request.data)
	db.close()
	return "Success"	

@app.route("/generateCSV.csv")
def genCSV():
	global cur
	db,cur = connectDb()
	cur.execute("select id,name,Room_No,Block from Student where status='P';")
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
	summaryDf.to_csv('summary.csv')

	return send_file( '../summary.csv',mimetype="text/csv",as_attachment=True)

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    print(str(e))    
    return jsonify(error=str(e)), code	

@app.route("/getPassedTable", methods=['POST','GET'])
def getPassedTable():
	print("Table Rendered")
	df = getPassedTableSQL()	
	return jsonify(df)

@app.route("/getTable", methods=['POST','GET'])
def getTable():
	print("Table Rendered")
	df = getTableSQL()	
	return jsonify(df)

def connectDb():
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
	                     user="hostel",         # your username
	                     passwd="hostel123",  # your password
	                     db="hostel")        # name of the data base


	cur = db.cursor()
	return db,cur



def getPassedTableSQL():
	global cur
	db,cur = connectDb()
	cur.execute("select id,name,Room_No,Block from Student where status='E';")
	arr = []
	for row in cur.fetchall():
	    arr.append(list(row))
	df = pd.DataFrame(arr)
	df = df.transpose()
	val = df.values.tolist()
	db.close()
	return val

def getTableSQL():
	global cur
	db,cur = connectDb()
	cur.execute("select id,name,Room_No,Block from Student where status='P';")
	arr = []
	for row in cur.fetchall():
	    arr.append(list(row))
	df = pd.DataFrame(arr)
	df = df.transpose()
	val = df.values.tolist()
	db.close()
	return val




@app.route('/studentData.js')
def sendjs():
	return render_template('studentData.js')	

@app.route('/frontpage.css')
def sendcssa4():
	return send_from_directory('./static', 'frontpage.css')


@app.route('/homepage.css')
def sendcssa2():
	return send_from_directory('./static', 'homepage.css')


@app.route('/animate.css')
def sendcssa3():
	return send_from_directory('./static', 'animate.css')	

@app.route('/table.js')
def sendcssa1():
	return render_template('table.js',table="getTable")	

@app.route('/logo.png')
def sendpng():
	return send_from_directory('./static', 'logo.png')

@app.route('/jumbotron.jpg')
def sendpng1():
	return send_from_directory('./static', 'jumbotron.jpg')

@app.route('/passOut')
def passOut():
	return render_template('deleteExcel.html')

@app.route('/insertExcel')
def insertExcel():
	return render_template('insertExcel.html')

@app.route('/codropsicons.eot')
def sendFont():
	return send_from_directory('./static', 'codropsicons.eot')

@app.route('/codropsicons.svg')
def sendFont1():
	return send_from_directory('./static', "codropsicons.svg")

@app.route('/codropsicons.ttf')
def sendFont2():
	return send_from_directory('./static', "codropsicons.ttf")

@app.route('/component.css')
def sendcssa31():
	return send_from_directory('./static', 'component.css')

@app.route('/demo.css')
def sendcssa41():
	return send_from_directory('./static', 'demo.css')


@app.route('/normalize.css')
def sendcssa11():
	return send_from_directory('./static', 'normalize.css')	

@app.route('/codropsicons.woff')
def sendFont3():
	return send_from_directory('./static',  "codropsicons.woff")		

@app.route('/passout.js')
def sendpassoutjs():
	return render_template('table.js',table='getPassedTable')


@app.route('/signin.js')
def sendjqeury():
	return render_template('signin.js')

@app.route('/next')
def sendNext():
	return render_template('homepage.html',table="table.js")

@app.route('/getPassed')
def sendPassed():
	return render_template('homepage.html',table="passout.js")


@app.route('/jquery.js')
def sendJs():
	return render_template('jquery.js')

@app.route('/excel.css')
def sendExcelCss():
	return send_from_directory('./static','excel.css')	

@app.route('/cover.jpg')
def sendCoverjpg():
	return send_from_directory('./static','cover.jpg')	

@app.route('/excel.js')
def sendExcelJs():
	return render_template('excel.js')


@app.route('/')
def index():
	print('rendered')
	return render_template('front.html')
