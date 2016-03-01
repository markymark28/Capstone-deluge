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
        self.gtkui_config = ConfigManager("gtkui.conf")
        self.running = False

    # Component overrides
    def start(self):
        pass

    def stop(self):
        # Close this dialog when we are shutting down
        if self.running:
            self.add_account.response(gtk.RESPONSE_CLOSE)

    def shutdown(self):
        pass

    def __load_config(self):
        pass
    # Public methods
    def show(self):
        """
        Show the ConnectionManager dialog.
        """
        self.config = self.__load_config()
        # Get the gtk builder file for the connection manager
        self.builder = gtk.Builder()
        # The main dialog
        ###############################################################################
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
        self.builder.add_from_file(filepath+"/add_account.ui")#resource_filename(
            #"deluge.ui.gtkui", os.path.join("glade", "connection_manager.ui")
        #))
        # The add host dialog
               ##################################################################################
        self.window = component.get("MainWindow")

        # Setup the ConnectionManager dialog
        self.add_account = self.builder.get_object("add_account")
        self.add_account.set_transient_for(self.window.window)

        self.add_account.set_icon(get_deluge_icon())

        self.builder.get_object("image1").set_from_pixbuf(get_logo(32))

     

      

        # Connect the signals to the handlers
        self.builder.connect_signals(self)
 
        self.running = True
        # Trigger the on_selection_changed code and select the first host
        # if possible
        '''
        self.hostlist.get_selection().unselect_all()
        if len(self.liststore) > 0:
            self.hostlist.get_selection().select_path("0")
        '''
        # Run the dialog
        self.add_account.run()
        self.running = False

        # Save the toggle options
        
        self.add_account.destroy()
        del self.builder
        del self.window
        del self.add_account
    '''     
    def on_button_close_clicked(self, widget):
        self.account_manager.response(gtk.RESPONSE_CLOSE)

    def on_button_adduser_clicked(self, data):
        component.get("AddAccount").show()

        
    def on_button_edituser_clicked(self,widget):
        pass
    def on_button_adduser_clicked(self,widget):
        pass

    def on_button_removeuser_clicked(self,widget):
        pass
    '''
