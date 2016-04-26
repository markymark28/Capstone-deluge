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


    
class EditAccount(component.Component):
    def __init__(self):
        component.Component.__init__(self, "EditAccount")
        self.gtkui_config = ConfigManager("gtkui.conf")
        self.running = False
        
        
    def show(self):
        #if component.get("AddAccount").is_on_active_workspace():
        #self.dialog.set_transient_for(component.get("AddAccount").window)
        #else:
            #self.dialog.set_transient_for(None)
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
        self.builder.add_from_file(filepath+"/edit_account_dialog.ui")#deluge.common.resource_filename(
            #"deluge.ui.gtkui", os.path.join("glade", "add_torrent_dialog.ui")
        
        self.dialog = self.builder.get_object("edit_account_dialog")
            
        self.builder.connect_signals({
            # Torrent Menu                                                                                                                       
            "on_create_user_clicked": self.on_create_user_clicked,
            "on_button_close_clicked": self.on_button_close_clicked
        })
        
        #window = builder.get_object("window1")
        #window.show_all()
        fin = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/ui/gtkui/pass.txt", 'r')
        accountname = fin.read()
        accountname = accountname.strip()
        self.builder.get_object("account_name").set_text(accountname)


        self.dialog.present()

        return None

    def on_create_user_clicked(self, widget):

        fin = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/ui/gtkui/pass.txt", 'r')
        accountname = fin.read()
        accountname = accountname.strip()
        
        fin = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/hashes.txt", 'r')
        lines = fin.read()
        fin.close()

        pass1 = self.builder.get_object('password_field1').get_text()                                                                                
        pass2 = self.builder.get_object('password_field2').get_text() 
        
        statusbar = self.builder.get_object('editUserStatusbar')  
        
        if pass1 == pass2 and len(pass1) >= 16:
            fout = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/hashes.txt", 'w')
            lines = lines.split("\n")
            for line in lines:
                if len(line) is not 0:
                    line = line.strip()
                    line = line.split(':')
                    if line[0] != accountname:
                        fout.write(line[0] + ':' + line[1] +  ":" + line[2] + "\n")
                    else:
                        hash_object = hashlib.sha1(bytes(pass1))
                        hash_pass = hash_object.hexdigest()
                        fout.write(accountname + ':' + hash_pass + ":" + self.builder.get_object("combobox1").get_active_text().lower() + '\n')
        else:
             if pass1 != pass2:
                 #print
                 statusbar.push(0,"Passwords do not match")
             elif len(pass1) < 16 or len(pass2) < 16:
                 #print
                 statusbar.push(0,"Length must be at least 16 characters")
        fout.close()
        


        '''
        username = self.builder.get_object('account_name').get_text()
        pass1 = self.builder.get_object('password_field1').get_text()
        pass2 = self.builder.get_object('password_field2').get_text()

        print "username: " + username
        print "pass1: " + pass1
        print "pass2: " + pass2

        
        if pass1 == pass2:
            fin = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/ui/gtkui/test_accounts.txt", 'a')
            fin.write(username +'\t' + "operator"  + '\n')
            fin.close()
        '''
        #print self.builder.get_object("combobox1").get_active_text()
        self.builder.get_object("edit_account_dialog").response(gtk.RESPONSE_CLOSE)
        self.builder.get_object("edit_account_dialog").destroy()

        
    def on_button_close_clicked(self, widget):
        pass
        

    
