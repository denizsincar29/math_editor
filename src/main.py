from funx import *
from urllib.parse import quote,unquote
from flask import Flask,render_template,request,flash,redirect, url_for
from sf import secure_filename
from glob import glob
from math2html import mathprocess
import sys
# import tgbot
# from tgbot import bot
import os
dir=""
if sys.platform!="win32":dir="/home/denizsincar29/mysite/"
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/math"
app.config['MAX_CONTENT_LENGTH']=1024*1024*4

@app.route("/",methods=["GET","POST"])
def mainsite():
	if request.method=="POST" and 'file' in request.files:
		file = request.files['file']
		if file.filename == '':return error("error. no selected file")
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(dir+"math/"+filename)
			return redirect("/math/"+filename)
		else:return error("cannot upload this")
	math=glob(dir+"math/*.math")

	math.sort(key=os.path.getmtime)
	math=[i.replace("math/","").replace(".math","").replace("math\\","").replace(dir,"") for i in math][::-1]
	tmplate=render_template('math.html', math=math,edit=False)
	return tmplate

#view edit list
@app.route("/edit/")
def edit():
	math=glob(dir+"math/*.math")
	math=[i.replace(".math","").replace("math\\","").replace(dir,"") for i in math]
	tmplate=render_template('math.html', math=math,edit=True)
	return tmplate

#view math
@app.route("/math/<mname>/")
def viewmath(mname):
	mname=unquote(mname)
	with open(dir+"math/"+mname,encoding="UTF-8") as f:return mathprocess(f.read(),mname.replace(".math",""))

#math as it is
@app.route("/mathraw/<mname>/")
def mathraw(mname):
	mname=unquote(mname)
	with open(dir+"math/"+mname,encoding="UTF-8") as f:return f.read()


#edit a math (depricated)
@app.route("/edt/<mname>/",methods=["POST"])
def editmath(mname):
	mname=unquote(mname)
	if request.method=="POST":
		headers = {"Content-Type": "text/plain","Accept":"text/plain"}
		towrite=request.data.decode(encoding="UTF-8")
		if towrite=="":return ""
		with open(dir+"math/"+mname,"w",encoding="UTF-8") as f:f.write(towrite)
		return mathprocess(towrite,mname.replace(".math",""),ed=...)

@app.route("/body/<mname>")
def body(mname):
	mname=unquote(mname)
	with open(dir+"math/"+mname,encoding="UTF-8") as f:return mathprocess(f.read(),mname.replace(".math",""),ed=...)


@app.route("/create/<newfile>")
def createfile(newfile):
	errlog([newfile, unquote(newfile)])
	newfile=unquote(newfile)
	newfile=secure_filename(newfile+".math")
	errlog(newfile)
	with open(dir+"math/"+newfile,"w",encoding="UTF-8") as f:f.write("файл пустой")
	return redirect("/math/"+newfile)


@app.route("/del/<mname>/")
def delmath(mname):
	mname=unquote(mname)
	os.remove(dir+"math/"+mname)
	return error("файл удалён")

if sys.platform=="win32":app.run("0.0.0.0",80)