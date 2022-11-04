#functions
from flask import flash
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ["math"]

def error(msg,back="/"):
	return "<html>"+msg+'\n<a href=\"'+back+'\">назад</a></html>'
	return redirect(back)



def errlog(something):
	with open("error.log","a",encoding="UTF-8") as f:f.write(str(something)+"\n")