# -*- coding: utf-8 -*-
#
# Copyright (C) 2008 Andrew Resch <andrewresch@gmail.com>
#
# This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

import base64
import logging
import os.path

import gobject
import gtk
from twisted.internet.threads import deferToThread

import deluge.component as component
from deluge.common import get_path_size, is_url, resource_filename
from deluge.configmanager import ConfigManager
from deluge.ui.client import client
from deluge.ui.gtkui.torrentview_data_funcs import cell_data_size

log = logging.getLogger(__name__)


class SendTorrentDialog:

    def __init__(self):
        pass

    def show(self):
        self.builder = gtk.Builder()

        # The main dialog
        ######################################################################################
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
        self.builder.add_from_file(filepath+"/send_torrent_dialog.ui")#resource_filename(
          
		####################################################################################
        self.config = ConfigManager("gtkui.conf")

        self.dialog = self.builder.get_object("send_torrent_dialog")
        self.dialog.set_transient_for(component.get("MainWindow").window)
        self.dialog.set_size_request(450,500)
        self.builder.connect_signals({
            "on_send_clicked": self._on_send_clicked,
            "on_cancel_clicked": self._on_cancel_clicked
            
        })
        '''
        render = gtk.CellRendererToggle()
        render.connect("toggled", self._on_file_toggled)
        column = gtk.TreeViewColumn(None, render, active=0, inconsistent=4)
        self.listview_files.append_column(column)
        '''
        #name, email
        
        #create liststore
        self.liststore = self.builder.get_object("liststore1")
        
        #create treeview using liststore
        #self.treeview  = gtk.TreeView(self.liststore)
        self.treeview = self.builder.get_object("listview_names")
        
        #create the columns to display the data
        render = gtk.CellRendererToggle()
        render.connect("toggled", self._on_file_toggled )
        
        self.col0 = gtk.TreeViewColumn(None,render,active=0, inconsistent=4)
        self.col1 = gtk.TreeViewColumn('Name')
        self.col2 = gtk.TreeViewColumn('Email')
        
        #add a rows
        self.liststore.append([False,"Bayless","yo@ya.com"])
        self.liststore.append([False,"Gumpert","hey@ya.com"])
        
        #add columns to treeview
        self.treeview.append_column(self.col0)
        self.treeview.append_column(self.col1)
        self.treeview.append_column(self.col2)
        
        #create cellrenderers to render the data
        self.cell1 = gtk.CellRendererText()
        self.cell2 = gtk.CellRendererText()
        
        #add the cells to the columns
        self.col1.pack_start(self.cell1, True)
        self.col2.pack_start(self.cell2, True)
        
        #set the cell attributes to the appropriate liststore column
        self.col1.set_attributes(self.cell1, text=1)
        self.col2.set_attributes(self.cell2, text=2)
        
        self.treeview.set_model(self.liststore)
        
        #allow sorting
        self.col1.set_sort_column_id(0)
        
        self.treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        
        self.dialog.show()
    
    def _on_cancel_clicked(self, widget):
        log.debug("_on_button_cancel_clicked")
        self.dialog.destroy()
    
    def _on_send_clicked(self,widget):
    	print("send")
    	self.liststore.get_iter_first()
    	
    
    def _on_file_toggled(self, render, path):
		(model, paths) = self.treeview.get_selection().get_selected_rows()
		#print(paths)
		#print(paths[0][0])
		#print(paths[0])
		treeiter = self.liststore.get_iter(paths[0])
		if self.liststore.get_value(treeiter,0) == False:
			self.liststore.set_value(treeiter, 0 , True)
		else:
			self.liststore.set_value(treeiter, 0 , False)
