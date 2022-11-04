from urllib.parse import quote,unquote
from flask import render_template
def mathprocess(val,tit="Math",ed=False):
	br=True
	rval="" # return value
	orig=val
	val=val.replace("@ls","<ul>").replace("@le","</ul>").replace("@nls","<ol>").replace("@nle","</ol>").replace("@li","<li>")
	lines=val.replace("\r","").split("\n")
	print(len(lines),"lines")
	for i,line in enumerate(lines):
		nextline=""
		try:nextline=lines[i+1]
		except:pass
		br=True
		if line.startswith("#"):
			head="h"+str(line[0:6].count("#"))
			rval+="<"+head+">"+line.replace("#","")+"</"+head+">"
			continue
		if line.startswith("!"):
			rval+=render_template("iframe.html",cc=line.replace("!",""))
			continue
		if line.endswith("$$") or line.endswith(">") or nextline.startswith("$$") or nextline.startswith("<") or ("<ls>" in line+nextline) or ("<ol>" in line+nextline) or ("<li>" in line+nextline) or ("$$" in line+nextline):br=False
		rval+=line+("<br>" if br else "")+"\n"

	if ed==...:return render_template("justbody.html",body=rval)
	else:return render_template("mathfile.html",title=tit,rtitle=quote(tit),body=rval)
