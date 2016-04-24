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




class AccountManager(component.Component):
    def __init__(self):
        component.Component.__init__(self, "AccountManager")
        self.gtkui_config = ConfigManager("gtkui.conf")
        self.running = False
	
    # Component overrides
    def start(self):
        pass

    def stop(self):
        # Close this dialog when we are shutting down
        if self.running:
            self.account_manager.response(gtk.RESPONSE_CLOSE)

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
        self.builder.add_from_file(filepath+"/account_manager.ui")#resource_filename(
            #"deluge.ui.gtkui", os.path.join("glade", "connection_manager.ui")
        #))
        # The add host dialog
               ##################################################################################
        self.window = component.get("MainWindow")

        # Setup the ConnectionManager dialog
        self.account_manager = self.builder.get_object("account_manager")
        self.account_manager.set_transient_for(self.window.window)

        self.account_manager.set_icon(get_deluge_icon())

        self.builder.get_object("image1").set_from_pixbuf(get_logo(32))

        #######################################3LISTVIEWSHIT#########################
         #create liststore
        self.liststore = self.builder.get_object("liststore1")
        
        #create treeview using liststore
        #self.treeview  = gtk.TreeView(self.liststore)
        self.treeview = self.builder.get_object("listview_accounts")
        
        #create the columns to display the data
        render = gtk.CellRendererToggle()
        #render.connect("toggled", self._on_file_toggled )
        
        self.col0 = gtk.TreeViewColumn('Name')
        self.col1 = gtk.TreeViewColumn('Level')

        #open file
        fin = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/hashes.txt", 'r')
        for line in fin:
            #print "FILE IO"
            #print line
            line = line.strip()
            line = line.split(':')
            print line[0]
            print line[2]
            self.liststore.append([line[0], line[2]])
       
                #add columns to treeview
        self.treeview.append_column(self.col0)
        self.treeview.append_column(self.col1)
        
        
        #create cellrenderers to render the data
        self.cell1 = gtk.CellRendererText()
        self.cell2 = gtk.CellRendererText()
        
        #add the cells to the columns
        self.col0.pack_start(self.cell1, True)
        self.col1.pack_start(self.cell2, True)
        
        #set the cell attributes to the appropriate liststore column
        self.col0.set_attributes(self.cell1, text=0)
        self.col1.set_attributes(self.cell2, text=1)
        
        self.treeview.set_model(self.liststore)
        
        #allow sorting
        self.col0.set_sort_column_id(0)
        
        #self.treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        
        #self.dialog.show()

      

        # Connect the signals to the handlers
 	self.builder.connect_signals({
            # Torrent Menu
            "on_button_adduser_clicked": self.on_button_adduser_clicked,
            "on_button_removeuser_clicked": self.on_button_removeuser_clicked,
	        "on_button_edituser_clicked": self.on_button_edituser_clicked,
            #"on_hostlist_row_activated": self.on_hostlist_row_activated,
            "on_button_close_clicked": self.on_button_close_clicked
        })
        self.running = True
        # Trigger the on_selection_changed code and select the first host
        # if possible
        '''
        self.hostlist.get_selection().unselect_all()
        if len(self.liststore) > 0:
            self.hostlist.get_selection().select_path("0")
        '''
        # Run the dialog
        self.account_manager.run()
        self.running = False

        # Save the toggle options
       
        self.account_manager.destroy()
        del self.builder
        del self.window
        del self.account_manager

    def get_selected(self):
        """Returns the selected tracker"""
        return self.treeview.get_selection().get_selected()[1]

       
    def on_button_close_clicked(self, widget):
        self.account_manager.response(gtk.RESPONSE_CLOSE)

    def on_button_adduser_clicked(self, data):
        component.get("AddAccount").show()
        
    def on_button_edituser_clicked(self,widget):

        self.treeview = self.builder.get_object("listview_accounts")
        model, pathlist = self.treeview.get_selection().get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 0)
            print "Passing: " + value
        fout = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/ui/gtkui/pass.txt", 'w')
        fout.write(value)
        fout.close()

        component.get("EditAccount").show()
    '''def on_button_adduser_clicked(self,widget):
        print("hhh")
        component.get("AddAccount").show()
    '''
    def on_button_removeuser_clicked(self,widget):
        print "Remove User Clicked"
        #model, row = self.listview_accounts.get_selection().get_selected()
        self.treeview = self.builder.get_object("listview_accounts")
        model, pathlist = self.treeview.get_selection().get_selected_rows()
        for path in pathlist:
            tree_iter = model.get_iter(path)
            value = model.get_value(tree_iter, 0)
            print value

        fin = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/hashes.txt", 'r')
        lines = fin.read()
        fin.close()
       
        fout = open("/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/hashes.txt", 'w')
        lines = lines.split("\n")
        for line in lines:
            if len(line) is not 0:
                print line
                line = line.strip()
                line = line.split(':')
                if line[0] != value:
                    fout.write(line[0] + ':' + line[1] + ':' + line[2] + "\n")
        fout.close()
        print "Exit Remove User"


    def on_hostlist_row_activated(self,widget):
	pass
    
    def on_button_close_clicked(self, widget):
    	
        self.account_manager.response(gtk.RESPONSE_CLOSE)
