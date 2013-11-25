from bottle import route, run, template, request, response, view, redirect
from datetime import datetime

@route('/')
@view("home.html")
def home():
	f=open("entry.tsv", "a+")
	f.seek(0, 0)
	entries=f.read().split("\n")
	entries.pop()
	entries.reverse()
	entries_dicts = []
	for line in entries:
		result = line.split("\t")
		entry=dict(datetime=result[0], username=result[1], entry=result[2])
		entries_dicts.append(entry)

	return dict (entries = entries_dicts)

@route('/new_entry',method="POST")
def new_entry():
	f=open("entry.tsv", "a")
	line = "%s\t%s\t%s\n"%(str(datetime.now()), request.params["username"], request.params["entry"])
	f.write(line)
	redirect("/")


run(host='0.0.0.0', port=8080, debug=True, reloader=True)