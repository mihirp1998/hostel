from __future__ import print_function

from app import app
from flask import render_template,request,send_from_directory
import PIL
# import lsh.lshparser as lshparser
import pandas as pd
import warnings
from flask import make_response, redirect,jsonify
from functools import wraps, update_wrapper
import MySQLdb
from werkzeug.exceptions import HTTPException, NotFound
import sys

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


@app.route("/getInfo", methods=['POST','GET'])
def  getInfo():
	global cur,roomno,name,block,idno,key,table,chair,misc
	print("Info Sent")
	db,cur = connectDb()
	idno = request.args['name']
	cur.execute("select * from StudentInput where id = %s", [idno])
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
	a = request.form['a']
	b = request.form['b']
	print("data",r,b,a,i)
	cur.execute("UPDATE StudentInput SET  Room_No= %s, Block= %s, cost= %s WHERE id = %s;",[r,b,a,i])
	db.commit()
	result_set = cur.fetchall()
	print(result_set)
	print(request.form,"no",request.data)
	db.close()
	return "Success"	


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    print(str(e))    
    return jsonify(error=str(e)), code	


@app.route("/getTable", methods=['POST','GET'])
def getTable():
	print("Table Rendered")
	df = getTableSQL()	
	return jsonify(df)

def connectDb():
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
	                     user="root",         # your username
	                     passwd="helloworld",  # your password
	                     db="hostel")        # name of the data base


	cur = db.cursor()
	return db,cur

def getTableSQL():
	global cur
	db,cur = connectDb()
	cur.execute("select * from StudentInput;")
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
	return render_template('table.js')	

@app.route('/logo.png')
def sendpng():
	return send_from_directory('./static', 'logo.png')

@app.route('/jumbotron.jpg')
def sendpng1():
	return send_from_directory('./static', 'jumbotron.jpg')


@app.route('/signin.js')
def sendjqeury():
	return render_template('signin.js')

@app.route('/next')
def sendNext():
	return render_template('homepage.html')

@app.route('/jquery.js')
def sendJs():
	return render_template('jquery.js')


@app.route('/')
def index():
	print('rendered')
	return render_template('front.html')
