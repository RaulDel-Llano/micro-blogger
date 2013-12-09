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

	return dict (entries = entries_dicts, username = request.get_cookie("username"))

#sanitizes input and saves new entry and redirects the user
@route('/new_entry',method="POST")
def new_entry():
	text = request.params["entry"]
	if len(text)>140 or len(text)==0:
		redirect("/")
		return
	username = request.get_cookie("username")
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
					redirect('/')
	return dict(error="Invalid username or password")

#logout
@route('/logout', )
def logout():
	response.set_cookie('username', "")
	redirect('/')


#shows signup page
@route('/signup')
@view("signup.html")
def signup():
	return dict(error="")

#checks that username is not used and passwords match
@route('/signup', method="POST")
@view("signup.html")
def do_signup():
	username = request.params["username"]
	password = request.params["password"]
	retype_password = request.params["retype_password"]
	if username_taken(username):
		return dict(error="Username is already taken try again")
	if password != retype_password:
		return dict(error="Passwords don't match")
	"""if bad_password(password):
		return dict(error="bad password")"""
	write_user(username, password)
	response.set_cookie('username', username)
	redirect('/')

#checks if username is already taken
def username_taken(username):
	f=open("users.tsv", "r")
	users=f.read().split("\n")
	users.pop()
	for line in users:
		parts = line.split("\t")
		file_username=parts[0]
		if file_username == username:
			return True
	return False

#
def write_user(username, password):
	line = "%s\t%s\n"%(username, password)
	f=open("users.tsv", "a")
	f.write(line)
	f.close()



run(host='0.0.0.0', port=8080, debug=True, reloader=True)