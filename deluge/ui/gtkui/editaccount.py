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
        self.builder.add_from_file(filepath+"/edit_account.ui")#deluge.common.resource_filename(
            #"deluge.ui.gtkui", os.path.join("glade", "add_torrent_dialog.ui")
        
		######################################################################################
        self.dialog = self.builder.get_object("window1")
    def show(self):
        if component.get("MainWindow").is_on_active_workspace():
            self.dialog.set_transient_for(component.get("MainWindow").window)
        else:
            self.dialog.set_transient_for(None)

        self.dialog.present()

        return None

   
    
