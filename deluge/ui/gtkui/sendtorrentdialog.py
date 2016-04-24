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

from deluge.ui.gtkui.dialogs import ErrorDialog
from deluge.ui.gtkui.path_chooser import PathChooser
from deluge.ui.gtkui.torrentview_data_funcs import cell_data_size
from deluge.ui.common import TorrentInfo
import csv
import time
import threading

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
            "on_cancel_clicked": self._on_cancel_clicked,
            "on_button_file_clicked": self._on_button_file_clicked,
            "on_button_url_clicked": self._on_button_url_clicked,
            "on_button_hash_clicked": self._on_button_hash_clicked,
            "on_button_remove_clicked": self._on_button_remove_clicked,
            
        })
        '''
        render = gtk.CellRendererToggle()
        render.connect("toggled", self._on_file_toggled)
        column = gtk.TreeViewColumn(None, render, active=0, inconsistent=4)
        self.listview_files.append_column(column)
        '''

        ########################## File listview #############################
        self.files_treestore = gtk.TreeStore(
            bool, str, gobject.TYPE_UINT64, gobject.TYPE_INT64, bool, str)
        self.files_treestore.set_sort_column_id(1, gtk.SORT_ASCENDING)

        # Holds the files info
        self.files = {}
        self.infos = {}
        self.core_config = {}
        self.options = {}

        self.previous_selected_torrent = None

        self.listview_torrents = self.builder.get_object("listview_torrents")
        render = gtk.CellRendererText()
        render.connect('edited', self._on_torrent_name_edit)
        render.set_property('editable', True)
        column = gtk.TreeViewColumn(_("Torrent"), render, text=1)
        self.listview_torrents.append_column(column)

        render = gtk.CellRendererToggle()
        render.connect("toggled", self._on_file_toggled)
        column = gtk.TreeViewColumn(None, render, active=0, inconsistent=4)
#        self.listview_files.append_column(column)

        column = gtk.TreeViewColumn(_("Filename"))
        render = gtk.CellRendererPixbuf()
        column.pack_start(render, False)
        column.add_attribute(render, "stock-id", 5)
        render = gtk.CellRendererText()
        render.set_property("editable", True)
#        render.connect("edited", self._on_filename_edited)
        column.pack_start(render, True)
        column.add_attribute(render, "text", 1)
        column.set_expand(True)
#        self.listview_files.append_column(column)

        render = gtk.CellRendererText()
        column = gtk.TreeViewColumn(_("Size"))
        column.pack_start(render)
        column.set_cell_data_func(render, cell_data_size, 2)
#        self.listview_files.append_column(column)
        
        self.torrent_liststore = gtk.ListStore(str, str, str)
        self.listview_torrents.set_model(self.torrent_liststore)
        self.listview_torrents.set_tooltip_column(2)
        
      
        
        #name, email
        
        #create liststore
        self.liststore = self.builder.get_object("liststore1")
        self.liststore.clear()
        #create treeview using liststore
        #self.treeview  = gtk.TreeView(self.liststore)
        self.treeview = self.builder.get_object("listview_names")
        
        #create the columns to display the data
        render = gtk.CellRendererToggle()
        render.connect("toggled", self._on_file_toggled )
        
        ###
        column = gtk.TreeViewColumn('Send', render, active=0, inconsistent=4)
        self.treeview.append_column(column)
        
        ###
        #self.col0 = gtk.TreeViewColumn('Send',render,active=0, inconsistent=4)
        self.col1 = gtk.TreeViewColumn('Name')
        self.col2 = gtk.TreeViewColumn('Email')
        
        #add a rows
        with open('/home/m160426/Desktop/Capstone/Capstone-deluge/deluge/ui/gtkui/dist_list.csv') as csvfile:
        	reader = csv.DictReader(csvfile)
        	for row in reader:
        		print(row['toggle_box'], row['last_name'], row['email'])
        		self.liststore.append([row['toggle_box'],row['last_name'],row['email']])
        #self.liststore.append([False,"Bayless","yo@ya.com"])
        #self.liststore.append([False,"Gumpert","hey@ya.com"])
        
        #add columns to treeview
        #self.treeview.append_column(self.col0)
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
        #self.col1.set_sort_column_id(0)
        
        self.treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        #self.listview_torrents.get_selection().connect("changed", self._on_torrent_changed)
        
        
        self.core_keys = [
            "pre_allocate_storage",
            "max_connections_per_torrent",
            "max_upload_slots_per_torrent",
            "max_upload_speed_per_torrent",
            "max_download_speed_per_torrent",
            "prioritize_first_last_pieces",
            "sequential_download",
            "add_paused",
            "download_location",
            "download_location_paths_list",
            "move_completed",
            "move_completed_path",
            "move_completed_paths_list",
        ]
       
        self.dialog.set_transient_for(component.get("MainWindow").window)
    	self.dialog.present()
    	

        
    def _on_file_toggled(self, render, path):
        (model, paths) = self.treeview.get_selection().get_selected_rows()
        if len(paths) > 1:
            for path in paths:
                row = model.get_iter(path)
                self.toggle_iter(row)
        else:
            row = model.get_iter(path)
            self.toggle_iter(row)
        self.update_treeview_toggles(self.liststore.get_iter_first())

    def toggle_iter(self, _iter, toggle_to=None):
        if toggle_to is None:
            toggle_to = not self.liststore.get_value(_iter, 0)
        self.liststore.set_value(_iter, 0, toggle_to)
        if self.liststore.iter_has_child(_iter):
            child = self.liststore.iter_children(_iter)
            while child is not None:
                self.toggle_iter(child, toggle_to)
                child = self.liststore.iter_next(child)
    
    def update_treeview_toggles(self, _iter):
        toggle_inconsistent = -1
        this_level_toggle = None
        while _iter is not None:
            if self.liststore.iter_has_child(_iter):
                toggle = self.update_treeview_toggles(self.liststore.iter_children(_iter))
                if toggle == toggle_inconsistent:
                    self.liststore.set_value(_iter, 4, True)
                else:
                    self.liststore.set_value(_iter, 0, toggle)
                    # set inconsistent to false
                    self.liststore.set_value(_iter, 4, False)
            else:
                toggle = self.liststore.get_value(_iter, 0)
            if this_level_toggle is None:
                this_level_toggle = toggle
            elif this_level_toggle != toggle:
                this_level_toggle = toggle_inconsistent
            _iter = self.liststore.iter_next(_iter)
        return this_level_toggle
                    
    def _on_cancel_clicked(self, widget):
        log.debug("_on_button_cancel_clicked")
        self.hide()
    
    def hide(self):
        self.dialog.hide()
        self.files = {}
        self.infos = {}
        self.options = {}
        self.previous_selected_torrent = None
        self.torrent_liststore.clear()
        self.liststore.clear()
        self.dialog.set_transient_for(component.get("MainWindow").window)
        return None

    def _on_send_clicked(self,widget):
    	
    	torrent_list = []
    	email_list   = []
    	
    	item = self.torrent_liststore.get_iter_first()
    	while item != None:
    		print(self.torrent_liststore[item][2])
    		torrent_list.append(self.torrent_liststore[item][2])
    		item = self.torrent_liststore.iter_next(item)
        
        torrent_str = ""
        for i in range(len(torrent_list)):
        	if i < len(torrent_list)-1:
        		torrent_str = torrent_str + str(torrent_list[i]) + ","
    		else:
    			torrent_str = torrent_str + str(torrent_list[i])
    	torrent_str = torrent_str + "'"
        
        emails = self.liststore.get_iter_first()
        while emails != None:
        	if self.liststore.get_value(emails,0) == True:
    			print(self.liststore.get_value(emails,2))
    			email_list.append(self.liststore.get_value(emails,2))
        	emails = self.liststore.iter_next(emails)
        
        email_str = "'"
        for i in range(len(email_list)):
        	if i < len(email_list)-1:
        		email_str = email_str + str(email_list[i]) + ","
    		else:
    			email_str = email_str + str(email_list[i])
    	email_str = email_str + "'"
    		
    	cmd = "thunderbird -compose \"to=" + email_str + ",subject='deluge',body='New Torrents to Download',attachment='" + torrent_str + "\""
        print(cmd)
        self.hide()
        
        #THREADS
        
        thread1 = myThread(1,"Thread-1", 1)
        thread2 = myThread(2,"Thread-2", 2)
        
        thread1.start()
        ##################################
        enig_builder = gtk.Builder()
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
        enig_builder.add_from_file(filepath+"/starting_enigmail.ui")#resource_filename(
        #enig_window = enig_builder.get_object("window1")
        self.dialog = enig_builder.get_object("dialog1")
        self.dialog.set_transient_for(component.get("MainWindow").window)
        self.dialog.present()
        ##################################
        thread2.start()
        startEnig(cmd)
        thread2.join()
        thread1.join()
    	print("Exiting main thread")
        #enig_window.destroy()
    

 
        
    def _on_torrent_changed(self, treeselection):
        (model, row) = treeselection.get_selected()
        if row is None or not model.iter_is_valid(row):
            self.liststore.clear()
            self.previous_selected_torrent = None
            return

        if model[row][0] not in self.files:
            self.liststore.clear()
            self.previous_selected_torrent = None
            return

        # Save the previous torrents options
        self.save_torrent_options()
        # Update files list
        files_list = self.files[model.get_value(row, 0)]

        self.prepare_file_store(files_list)

        if self.core_config == {}:
            self.update_core_config()

        # Update the options frame
        self.update_torrent_options(model.get_value(row, 0))

        self.previous_selected_torrent = row
        
    def _on_torrent_name_edit(self, w, row, new_name):
        # TODO: Update torrent name
        pass
	
    def _on_button_file_clicked(self, widget):
        log.debug("_on_button_file_clicked")
        # Setup the filechooserdialog
        chooser = gtk.FileChooserDialog(
            _("Choose a .torrent file"),
            None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN,
                     gtk.RESPONSE_OK)
        )

        chooser.set_transient_for(self.dialog)
        chooser.set_select_multiple(True)
        chooser.set_property("skip-taskbar-hint", True)
        chooser.set_local_only(False)

        # Add .torrent and * file filters
        file_filter = gtk.FileFilter()
        file_filter.set_name(_("Torrent files"))
        file_filter.add_pattern("*." + "torrent")
        chooser.add_filter(file_filter)
        file_filter = gtk.FileFilter()
        file_filter.set_name(_("All files"))
        file_filter.add_pattern("*")
        chooser.add_filter(file_filter)

        # Load the 'default_load_path' from the config
        self.config = ConfigManager("gtkui.conf")
        if self.config["default_load_path"] is not None:
            chooser.set_current_folder(self.config["default_load_path"])

        # Run the dialog
        response = chooser.run()

        if response == gtk.RESPONSE_OK:
            result = chooser.get_filenames()
            self.config["default_load_path"] = chooser.get_current_folder()
        else:
            chooser.destroy()
            return

        chooser.destroy()
        self.add_from_files(result)
    
    def _on_button_url_clicked(self, widget):
        log.debug("_on_button_url_clicked")
        dialog = self.builder.get_object("url_dialog")
        entry = self.builder.get_object("entry_url")

        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_transient_for(self.dialog)
        entry.grab_focus()

        text = (gtk.clipboard_get(selection='PRIMARY').wait_for_text() or
                gtk.clipboard_get().wait_for_text())
        if text:
            text = text.strip()
            if deluge.common.is_url(text) or deluge.common.is_magnet(text):
                entry.set_text(text)

        dialog.show_all()
        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            url = entry.get_text().decode("utf-8")
        else:
            url = None

        entry.set_text("")
        dialog.hide()

        # This is where we need to fetch the .torrent file from the URL and
        # add it to the list.
        log.debug("url: %s", url)
        if url:
            if deluge.common.is_url(url):
                self.add_from_url(url)
            elif deluge.common.is_magnet(url):
                self.add_from_magnets([url])
            else:
                ErrorDialog(
                    _("Invalid URL"),
                    "%s %s" % (url, _("is not a valid URL.")),
                    self.dialog
                ).run()
                
    def update_core_config(self, show=False, focus=False):
        def _on_config_values(config):
            self.core_config = config
            if self.core_config:
                self.set_default_options()
            if show:
                self._show(focus)

        # Send requests to the core for these config values
        return client.core.get_config_values(self.core_keys).addCallback(_on_config_values)
        
    def save_torrent_options(self, row=None):
        # Keeps the torrent options dictionary up-to-date with what the user has
        # selected.
        pass
        if row is None:
            if self.previous_selected_torrent and \
                    self.torrent_liststore.iter_is_valid(self.previous_selected_torrent):
                row = self.previous_selected_torrent
            else:
                return

        torrent_id = self.torrent_liststore.get_value(row, 0)

        if torrent_id in self.options:
            options = self.options[torrent_id]
        else:
            options = {}

        options["download_location"] = self.download_location_path_chooser.get_text()
        options["move_completed_path"] = self.move_completed_path_chooser.get_text()
        options["pre_allocate_storage"] = self.builder.get_object("chk_pre_alloc").get_active()
        options["move_completed"] = self.builder.get_object("chk_move_completed").get_active()
        options["max_download_speed"] = \
            self.builder.get_object("spin_maxdown").get_value()
        options["max_upload_speed"] = \
            self.builder.get_object("spin_maxup").get_value()
        options["max_connections"] = \
            self.builder.get_object("spin_maxconnections").get_value_as_int()
        options["max_upload_slots"] = \
            self.builder.get_object("spin_maxupslots").get_value_as_int()
        options["add_paused"] = \
            self.builder.get_object("chk_paused").get_active()
        options["prioritize_first_last_pieces"] = \
            self.builder.get_object("chk_prioritize").get_active()
        options["sequential_download"] = \
            self.builder.get_object("chk_sequential_download").get_active() or False
        options["move_completed"] = \
            self.builder.get_object("chk_move_completed").get_active()
        options["seed_mode"] = self.builder.get_object("chk_seed_mode").get_active()

        self.options[torrent_id] = options

        # Save the file priorities
        files_priorities = self.build_priorities(
            self.files_treestore.get_iter_first(), {}
        )

        if len(files_priorities) > 0:
            for i, file_dict in enumerate(self.files[torrent_id]):
                file_dict["download"] = files_priorities[i]
                    
    def set_default_options(self):
        if not self.core_config:
            # update_core_config will call this method again.
            self.update_core_config()
            return

        self.load_path_choosers_data()

        self.builder.get_object("chk_pre_alloc").set_active(
            self.core_config["pre_allocate_storage"])
        self.builder.get_object("spin_maxdown").set_value(
            self.core_config["max_download_speed_per_torrent"])
        self.builder.get_object("spin_maxup").set_value(
            self.core_config["max_upload_speed_per_torrent"])
        self.builder.get_object("spin_maxconnections").set_value(
            self.core_config["max_connections_per_torrent"])
        self.builder.get_object("spin_maxupslots").set_value(
            self.core_config["max_upload_slots_per_torrent"])
        self.builder.get_object("chk_paused").set_active(
            self.core_config["add_paused"])
        self.builder.get_object("chk_prioritize").set_active(
            self.core_config["prioritize_first_last_pieces"])
        self.builder.get_object("chk_sequential_download").set_active(
            self.core_config["sequential_download"])
        self.builder.get_object("chk_move_completed").set_active(
            self.core_config["move_completed"])
        self.builder.get_object("chk_seed_mode").set_active(False)
        
 #   def _on_file_toggled(self, render, path):
#		(model, paths) = self.treeview.get_selection().get_selected_rows()
		#print(paths)
		#print(paths[0][0])
		#print(paths[0])
#		treeiter = self.liststore.get_iter(paths[0])
#		if self.liststore.get_value(treeiter,0) == False:
#			self.liststore.set_value(treeiter, 0 , True)
#		else:
#			self.liststore.set_value(treeiter, 0 , False)
    
    def add_from_files(self, filenames):
        new_row = None
        already_added = 0

        for filename in filenames:
            # Get the torrent data from the torrent file
            try:
                info = TorrentInfo(filename)
            except Exception as ex:
                log.debug("Unable to open torrent file: %s", ex)
                ErrorDialog(_("Invalid File"), ex, self.dialog).run()
                continue

            if info.info_hash in self.files:
                already_added += 1
                continue

            new_row = self.torrent_liststore.append([info.info_hash, info.name, filename])
            self.files[info.info_hash] = info.files
            self.infos[info.info_hash] = info.filedata
            self.listview_torrents.get_selection().select_iter(new_row)

            #self.set_default_options()
            #self.save_torrent_options(new_row)

        (model, row) = self.listview_torrents.get_selection().get_selected()
        if not row and new_row:
            self.listview_torrents.get_selection().select_iter(new_row)

        #self.builder.get_object("label_torrent_count").set_text("Torrents (%d)" % len(self.torrent_liststore))

        if already_added:
            log.debug("Tried to add %d duplicate torrents!", already_added)
            ErrorDialog(
                _("Duplicate Torrent(s)"),
                _("You cannot add the same torrent twice. %d torrents were already added." % already_added),
                self.dialog
            ).run()
            
    def _on_button_hash_clicked(self, widget):
        log.debug("_on_button_hash_clicked")
        dialog = self.builder.get_object("dialog_infohash")
        entry = self.builder.get_object("entry_hash")
        textview = self.builder.get_object("text_trackers")

        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.set_transient_for(self.dialog)
        entry.grab_focus()
        dialog.show_all()
        response = dialog.run()
        if response == gtk.RESPONSE_OK and len(entry.get_text()) == 40:
            trackers = []
            b = textview.get_buffer()
            lines = b.get_text(b.get_start_iter(), b.get_end_iter()).strip().split("\n")
            log.debug("lines: %s", lines)
            for l in lines:
                if deluge.common.is_url(l):
                    trackers.append(l)
            # Convert the information to a magnet uri, this is just easier to
            # handle this way.
            log.debug("trackers: %s", trackers)
            magnet = deluge.common.create_magnet_uri(
                infohash=entry.get_text().decode("utf-8"),
                trackers=trackers)
            log.debug("magnet uri: %s", magnet)
            self.add_from_magnets([magnet])

        entry.set_text("")
        textview.get_buffer().set_text("")
        dialog.hide()

    def _on_button_remove_clicked(self, widget):
        log.debug("_on_button_remove_clicked")
        (model, row) = self.listview_torrents.get_selection().get_selected()
        if row is None:
            return

        torrent_id = model.get_value(row, 0)

        model.remove(row)
        del self.files[torrent_id]
        del self.infos[torrent_id]
        
    def load_path_choosers_data(self):
        self.move_completed_path_chooser.set_text(self.core_config["move_completed_path"],
                                                  cursor_end=False, default_text=True)
        self.download_location_path_chooser.set_text(self.core_config["download_location"],
                                                     cursor_end=False, default_text=True)
        self.builder.get_object("chk_move_completed").set_active(self.core_config["move_completed"])

    def setup_move_completed_path_chooser(self):
        self.move_completed_hbox = self.builder.get_object("hbox_move_completed_chooser")
        self.move_completed_path_chooser = PathChooser("move_completed_paths_list")
        self.move_completed_hbox.add(self.move_completed_path_chooser)
        self.move_completed_hbox.show_all()

    def setup_download_location_path_chooser(self):
        self.download_location_hbox = self.builder.get_object("hbox_download_location_chooser")
        self.download_location_path_chooser = PathChooser("download_location_paths_list")
        self.download_location_hbox.add(self.download_location_path_chooser)
        self.download_location_hbox.show_all()
def startEnig(cmd):
	os.system(cmd)
	
	
	
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        # Get lock to synchronize threads


	             	
