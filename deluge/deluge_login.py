import hashlib
import gtk
import pygtk
import os
#login builder
builder = gtk.Builder() 
#loggedin
loggedin = False
accesslevel = ''
message = "hello"
attempts = 0

class Handler:
	def onDeleteWindow(self, *args):
		gtk.main_quit(*args)
	def onButtonPressed(self,button):
		usrname = builder.get_object('entry2')
		psswrd = builder.get_object('entry1')
		textBox = builder.get_object('statusbar1')
		lgin(usrname,psswrd)
		textBox.push(0,message)
	def on_Enter(self,button):
		usrname = builder.get_object('entry2')
		psswrd = builder.get_object('entry1')
		textBox = builder.get_object('statusbar1')
		lgin(usrname,psswrd)
		textBox.push(0,message)

def lgin(usr,pwd):
	#make global variabls
	global accesslevel
	global loggedin
	global message
	global attempts
	
	if (attempts < 5):
		#create hashed username and password
		enteredPassword = hashlib.md5(str.encode(pwd.get_text()))
		enteredUsername = usr.get_text()
	
		#open username and password file
		loginFile = open("hashes.txt", 'r')
	
		#check for matching username and password
		for line in loginFile:
			up = line.split(":")
			username = up[0]
		
			password = up[1]
			if (str(username)) == enteredUsername:
				if (str(password)) == enteredPassword.hexdigest():
					accesslevel = str(up[2])
					loggedin = True
					break
		#if matching username and password then open deluge
		if loggedin:
			message = "Welcome " + usr.get_text()
			t = open("loggedinusrs.txt", 'w')
			t.write(usr.get_text())
			t.write("\n")
			t.write(accesslevel)
			t.close
			gtk.main_quit()
		else:
			message = "Invalid username or password"
			attempts = attempts + 1
	
	else:
		message = "out of attempts"
	

def login():
    builder.add_from_file("login_menu.ui")
    builder.connect_signals(Handler())
    window = builder.get_object("window1")
    window.show_all()    
    gtk.main()

if __name__ == "__main__":
	login()
	print("yo")
	os.system("deluge")
