from bottle import route, run, template, request, response, view, redirect
from datetime import datetime
#displays home page
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
#sanitizes input and saves new entry and redirects the user
@route('/new_entry',method="POST")
def new_entry():
	text = request.params["entry"]
	if len(text)>140 or len(text)==0:
		redirect("/")
		return
	username = request.params["username"]
	text = text.replace("\t", " ")
	username = username.replace("\t", " ")
	text = text.replace("\n", " ")
	username = username.replace("\n", " ")
	write_entry(username, text, str(datetime.now()))
	redirect("/")
#saves user input
def write_entry(username, text, datetime):
	line = "%s\t%s\t%s\n"%(datetime, username, text)
	f=open("entry.tsv", "a")
	f.write(line)
	f.close()
#shows login page
@route('/login')
@view("login.html")
def login():
	return dict(error="")
#checks for login and password
@route('/login', method="POST")
@view("login.html")
def do_login():
	username = request.params["username"]
	password = request.params["password"]
	f=open("users.tsv", "r")
	users=f.read().split("\n")
	users.pop()
	for line in users:
		result = line.split("\t")
		file_username=result[0]
		file_password=result[1]
		if file_username==username: 
			if file_password==password:
					response.set_cookie('username', username)
					redirect("/")
	return dict(error="Invalid username or password")

run(host='0.0.0.0', port=8080, debug=True, reloader=True)