# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
#
# This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

import hashlib
import logging
import os
import time
from socket import gethostbyname

import gtk
from twisted.internet import reactor

import deluge.component as component
from deluge.common import resource_filename
from deluge.configmanager import ConfigManager, get_config_dir
from deluge.error import AuthenticationRequired, BadLoginError, IncompatibleClient
from deluge.ui.client import Client, client
from deluge.ui.common import get_localhost_auth
from deluge.ui.gtkui.common import get_deluge_icon, get_logo
from deluge.ui.gtkui.dialogs import AuthenticationDialog, ErrorDialog

log = logging.getLogger(__name__)


    
class AddAccount(component.Component):
    def __init__(self):
        component.Component.__init__(self, "AddAccount")
        self.builder = gtk.Builder()
        # The base dialog
        #######################################################################
        read = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/loggedinusrs.txt", 'r')
        i = 0
        for line in read:
            i = i + 1
            if i%2 == 0:
                lvl = line.rstrip('\n')
                accesslevel = lvl
            else:
                usrname = line.rstrip('\n')
        read.close
        filepath = "/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/ui/gtkui/glade/" + str(accesslevel)     
        self.builder.add_from_file(filepath+"/add_account_dialog.ui")#deluge.common.resource_filename(
            #"deluge.ui.gtkui", os.path.join("glade", "add_torrent_dialog.ui")
        
		######################################################################################
        #self.builder.connect_signals(Handler())
        
        self.dialog = self.builder.get_object("add_account_dialog")
    def show(self):
        #if component.get("AddAccount").is_on_active_workspace():
        #self.dialog.set_transient_for(component.get("AddAccount").window)
        #else:
            #self.dialog.set_transient_for(None)
            
        self.builder.connect_signals({
            # Torrent Menu                                                                                                                       
            "on_create_user_clicked": self.on_create_user_clicked,
            "on_button_close_clicked": self.on_button_close_clicked
        })
        
        #window = builder.get_object("window1")
        #window.show_all()


        self.dialog.present()
        gtk.main()

        return None

    def on_create_user_clicked(self, widget):
    
		username = self.builder.get_object('account_name').get_text()
		pass1 = self.builder.get_object('password_field1').get_text()
		pass2 = self.builder.get_object('password_field2').get_text()
		statusbar = self.builder.get_object('addUsersSatusbar')
		
		if len(pass1) > 8:
		
			print "username: " + username
			print "pass1: " + pass1
			print "pass2: " + pass2

		    

			hash_object = hashlib.md5(bytes(pass1))
			hash_pass = hash_object.hexdigest()
		
			if pass1 == pass2:
				fin = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/hashes.txt", 'a')
				fin.write(username +':' + hash_pass + ':' +  self.builder.get_object("combobox1").get_active_text().lower()  + '\n')
				fin.close()
				name = username + " has been created"
				statusbar.push(0, name) 

			self.builder.get_object("add_account_dialog").response(gtk.RESPONSE_CLOSE)
		else:
			statusbar.push(0, "password must be at leat 8 characters")
        
    def on_button_close_clicked(self, widget):
        pass
        

    
