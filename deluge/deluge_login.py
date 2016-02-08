import hashlib
import gtk
import pygtk
import os
#login builder
builder = gtk.Builder() 
#loggedin
loggedin = False
accesslevel = ''

class Handler:
	def onDeleteWindow(self, *args):
		gtk.main_quit(*args)
	def onButtonPressed(self,button):
		usrname = builder.get_object('entry2')
		psswrd = builder.get_object('entry1')
		lgin(usrname,psswrd)

def lgin(usr,pwd):
	#import pswd DB
	global accesslevel
	k = open("hashes.txt", 'r')
	tbl = {}
	i = 0
	for line in k:
		i = i + 1
		if i%2 == 0:
			lvl = line.rstrip('\n')
			accesslevel = lvl
			tbl[hsh] = lvl
		else:
			hsh = line.rstrip('\n')
	#import usrname DB
	d = open("usrnames.txt", 'r')
	usrlist = []
	
	for line in d:
		name = line.rstrip('\n')
		usrlist.append(name)
	
	#check for pswd md5hash
	hash_object = hashlib.md5(str.encode(pwd.get_text()))
	pwdkey = hash_object.hexdigest()
#	print(pwdkey)
	haspwd = tbl.has_key(pwdkey)
#	print(haspwd)
	
	#check for usrname md5hash
	hash_object2 = hashlib.md5(str.encode(usr.get_text()))
	usrkey = hash_object2.hexdigest()
#	print(usrkey)
	if usrlist.count(usrkey) > 0:
		hasusr = True
	else:
		hasusr = False
#	print(hasusr)

	if hasusr and haspwd:
		loggedin = True
		print("Welcome " + usr.get_text())
		t = open("loggedinusrs.txt", 'w')
		t.write(usr.get_text())
		t.write("\n")
		t.write(accesslevel)
		t.close
		gtk.main_quit()
	else:
		print("invalid login, try again")

def login():
    builder.add_from_file("login_menu.ui")#deluge.common.resource_filename("deluge.ui.gtkui", os.path.join("glade", "login_menu.ui")))
    builder.connect_signals(Handler())
    window = builder.get_object("window1")
    window.show_all()    
    gtk.main()

if __name__ == "__main__":
	login()
	print("yo")
	os.system("deluge")
