# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, 2008 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2011 Pedro Algarvio <pedro@algarvio.me>
#
# This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

import logging
import os
from hashlib import sha1 as sha

import gtk
import pygtk

import deluge.common
import deluge.component as component
from deluge.configmanager import ConfigManager, get_config_dir
from deluge.error import AuthManagerError, NotAuthorizedError
from deluge.ui.client import client
from deluge.ui.gtkui.common import associate_magnet_links, get_deluge_icon
from deluge.ui.gtkui.dialogs import AccountDialog, ErrorDialog, InformationDialog, YesNoDialog
from deluge.ui.gtkui.path_chooser import PathChooser

pygtk.require('2.0')


log = logging.getLogger(__name__)


class AddAccountDialog(component.Component):
    def __init__(self):
        component.Component.__init__(self, "AddAccountDialog")
        self.builder = gtk.Builder()
        ####################################################################
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
            #"deluge.ui.gtkui", os.path.join("glade", "preferences_dialog.ui")
        #))
        ######################################################################
        self.pref_dialog = self.builder.get_object("add_account_dialog")
        self.pref_dialog.set_transient_for(component.get("MainWindow").window)
        self.pref_dialog.set_icon(get_deluge_icon())
        self.gtkui_config = ConfigManager("gtkui.conf")
        self.window_open = False



       

        # Setup the liststore for the categories (tab pages)
        '''
        self.builder.connect_signals({
            "on_pref_dialog_delete_event": self.on_pref_dialog_delete_event,
            "on_button_ok_clicked": self.on_button_ok_clicked,
            "on_button_apply_clicked": self.on_button_apply_clicked,
            "on_button_cancel_clicked": self.on_button_cancel_clicked,
            "on_toggle": self.on_toggle,
            "on_test_port_clicked": self.on_test_port_clicked,
            "on_button_plugin_install_clicked": self._on_button_plugin_install_clicked,
            "on_button_rescan_plugins_clicked": self._on_button_rescan_plugins_clicked,
            "on_button_find_plugins_clicked": self._on_button_find_plugins_clicked,
            "on_button_cache_refresh_clicked": self._on_button_cache_refresh_clicked,
            "on_combo_encryption_changed": self._on_combo_encryption_changed,
            "on_combo_proxy_type_changed": self._on_combo_proxy_type_changed,
            "on_button_associate_magnet_clicked": self._on_button_associate_magnet_clicked,
            "on_accounts_add_clicked": self._on_accounts_add_clicked,
            "on_accounts_delete_clicked": self._on_accounts_delete_clicked,
            "on_accounts_edit_clicked": self._on_accounts_edit_clicked,
            "on_piecesbar_toggle_toggled": self._on_piecesbar_toggle_toggled,
            "on_completed_color_set": self._on_completed_color_set,
            "on_revert_color_completed_clicked": self._on_revert_color_completed_clicked,
            "on_downloading_color_set": self._on_downloading_color_set,
            "on_revert_color_downloading_clicked": self._on_revert_color_downloading_clicked,
            "on_waiting_color_set": self._on_waiting_color_set,
            "on_revert_color_waiting_clicked": self._on_revert_color_waiting_clicked,
            "on_missing_color_set": self._on_missing_color_set,
            "on_revert_color_missing_clicked": self._on_revert_color_missing_clicked,
            "on_pref_dialog_configure_event": self.on_pref_dialog_configure_event,
            "on_checkbutton_language_toggled": self._on_checkbutton_language_toggled,
        })
        '''


    def __del__(self):
        del self.gtkui_config


    def show(self, page=None):
        """Page should be the string in the left list.. ie, 'Network' or
        'Bandwidth'"""
        self.window_open = True
        '''
        # Update the preferences dialog to reflect current config settings
        self.core_config = {}
        if client.connected():
            self._get_accounts_tab_data()

            def _on_get_config(config):
                self.core_config = config
                client.core.get_available_plugins().addCallback(_on_get_available_plugins)

            def _on_get_available_plugins(plugins):
                self.all_plugins = plugins
                client.core.get_enabled_plugins().addCallback(_on_get_enabled_plugins)

            def _on_get_enabled_plugins(plugins):
                self.enabled_plugins = plugins
                client.core.get_listen_port().addCallback(_on_get_listen_port)

            def _on_get_listen_port(port):
                self.active_port = port
                client.core.get_cache_status().addCallback(_on_get_cache_status)

            def _on_get_cache_status(status):
                self.cache_status = status
                self._show()

            # This starts a series of client.core requests prior to showing the window
            client.core.get_config().addCallback(_on_get_config)
        else:
            self._show()
    '''
    def start(self):
        if self.window_open:
            self.show()

    def stop(self):
        self.core_config = None
        if self.window_open:
            self._show()

    def _show(self):
        pass

        '''   def set_config(self, hide=False):
        """
        Sets all altered config values in the core.

        :param hide: bool, if True, will not re-show the dialog and will hide it instead
        """
        classic_mode_was_set = self.gtkui_config["classic_mode"]

        # Get the values from the dialog
        new_core_config = {}
        new_gtkui_config = {}

        # Downloads tab #
        new_gtkui_config["interactive_add"] = \
            self.builder.get_object("chk_show_dialog").get_active()
        new_gtkui_config["focus_add_dialog"] = \
            self.builder.get_object("chk_focus_dialog").get_active()

        for state in ("missing", "waiting", "downloading", "completed"):
            color = self.builder.get_object("%s_color" % state).get_color()
            new_gtkui_config["pieces_color_%s" % state] = [
                color.red, color.green, color.blue
            ]

        new_core_config["copy_torrent_file"] = \
            self.builder.get_object("chk_copy_torrent_file").get_active()
        new_core_config["del_copy_torrent_file"] = \
            self.builder.get_object("chk_del_copy_torrent_file").get_active()
        new_core_config["move_completed"] = \
            self.builder.get_object("chk_move_completed").get_active()

        new_core_config["download_location"] = self.download_location_path_chooser.get_text()
        new_core_config["move_completed_path"] = self.move_completed_path_chooser.get_text()
        new_core_config["torrentfiles_location"] = self.copy_torrent_files_path_chooser.get_text()
        new_core_config["prioritize_first_last_pieces"] = \
            self.builder.get_object("chk_prioritize_first_last_pieces").get_active()
        new_core_config["sequential_download"] = \
            self.builder.get_object("chk_sequential_download").get_active()
        new_core_config["add_paused"] = self.builder.get_object("chk_add_paused").get_active()
        new_core_config["pre_allocate_storage"] = self.builder.get_object("chk_pre_allocation").get_active()

        # Network tab #
        listen_ports = (
            self.builder.get_object("spin_port_min").get_value_as_int(),
            self.builder.get_object("spin_port_max").get_value_as_int()
        )
        new_core_config["listen_ports"] = listen_ports
        new_core_config["random_port"] = \
            self.builder.get_object("chk_random_port").get_active()
        outgoing_ports = (
            self.builder.get_object("spin_outgoing_port_min").get_value_as_int(),
            self.builder.get_object("spin_outgoing_port_max").get_value_as_int()
        )
        new_core_config["outgoing_ports"] = outgoing_ports
        new_core_config["random_outgoing_ports"] = \
            self.builder.get_object("chk_random_outgoing_ports").get_active()
        incoming_address = self.builder.get_object("entry_interface").get_text().strip()
        if deluge.common.is_ip(incoming_address) or not incoming_address:
            new_core_config["listen_interface"] = incoming_address
        new_core_config["peer_tos"] = self.builder.get_object("entry_peer_tos").get_text()
        new_core_config["dht"] = self.builder.get_object("chk_dht").get_active()
        new_core_config["upnp"] = self.builder.get_object("chk_upnp").get_active()
        new_core_config["natpmp"] = \
            self.builder.get_object("chk_natpmp").get_active()
        new_core_config["utpex"] = \
            self.builder.get_object("chk_utpex").get_active()
        new_core_config["lt_tex"] = \
            self.builder.get_object("chk_lt_tex").get_active()
        new_core_config["lsd"] = \
            self.builder.get_object("chk_lsd").get_active()
        new_core_config["enc_in_policy"] = \
            self.builder.get_object("combo_encin").get_active()
        new_core_config["enc_out_policy"] = \
            self.builder.get_object("combo_encout").get_active()
        new_core_config["enc_level"] = \
            self.builder.get_object("combo_enclevel").get_active()

        # Bandwidth tab #
        new_core_config["max_connections_global"] = \
            self.builder.get_object(
                "spin_max_connections_global").get_value_as_int()
        new_core_config["max_download_speed"] = \
            self.builder.get_object("spin_max_download").get_value()
        new_core_config["max_upload_speed"] = \
            self.builder.get_object("spin_max_upload").get_value()
        new_core_config["max_upload_slots_global"] = \
            self.builder.get_object(
                "spin_max_upload_slots_global").get_value_as_int()
        new_core_config["max_half_open_connections"] = \
            self.builder.get_object("spin_max_half_open_connections").get_value_as_int()
        new_core_config["max_connections_per_second"] = \
            self.builder.get_object(
                "spin_max_connections_per_second").get_value_as_int()
        new_core_config["max_connections_per_torrent"] = \
            self.builder.get_object(
                "spin_max_connections_per_torrent").get_value_as_int()
        new_core_config["max_upload_slots_per_torrent"] = \
            self.builder.get_object(
                "spin_max_upload_slots_per_torrent").get_value_as_int()
        new_core_config["max_upload_speed_per_torrent"] = \
            self.builder.get_object(
                "spin_max_upload_per_torrent").get_value()
        new_core_config["max_download_speed_per_torrent"] = \
            self.builder.get_object(
                "spin_max_download_per_torrent").get_value()
        new_core_config["ignore_limits_on_local_network"] = \
            self.builder.get_object("chk_ignore_limits_on_local_network").get_active()
        new_core_config["rate_limit_ip_overhead"] = \
            self.builder.get_object("chk_rate_limit_ip_overhead").get_active()

        # Interface tab #
        new_gtkui_config["enable_system_tray"] = \
            self.builder.get_object("chk_use_tray").get_active()
        new_gtkui_config["close_to_tray"] = \
            self.builder.get_object("chk_min_on_close").get_active()
        new_gtkui_config["start_in_tray"] = \
            self.builder.get_object("chk_start_in_tray").get_active()
        new_gtkui_config["enable_appindicator"] = \
            self.builder.get_object("radio_appind").get_active()
        new_gtkui_config["lock_tray"] = \
            self.builder.get_object("chk_lock_tray").get_active()
        passhex = sha(self.builder.get_object("txt_tray_password").get_text()).hexdigest()
        if passhex != "c07eb5a8c0dc7bb81c217b67f11c3b7a5e95ffd7":
            new_gtkui_config["tray_password"] = passhex

        new_gtkui_in_classic_mode = self.builder.get_object("radio_classic").get_active()
        new_gtkui_config["classic_mode"] = new_gtkui_in_classic_mode

        new_gtkui_config["show_rate_in_title"] = \
            self.builder.get_object("chk_show_rate_in_title").get_active()
        new_gtkui_config["focus_main_window_on_add"] = \
            self.builder.get_object("chk_focus_main_window_on_add").get_active()

        # Other tab #
        new_gtkui_config["show_new_releases"] = \
            self.builder.get_object("chk_show_new_releases").get_active()
        new_core_config["send_info"] = \
            self.builder.get_object("chk_send_info").get_active()
        new_core_config["geoip_db_location"] = \
            self.builder.get_object("entry_geoip").get_text()

        # Daemon tab #
        new_core_config["daemon_port"] = \
            self.builder.get_object("spin_daemon_port").get_value_as_int()
        new_core_config["allow_remote"] = \
            self.builder.get_object("chk_allow_remote_connections").get_active()
        new_core_config["new_release_check"] = \
            self.builder.get_object("chk_new_releases").get_active()

        # Proxy tab #
        new_core_config["proxy"] = {}
        new_core_config["proxy"]["type"] = self.builder.get_object("combo_proxy_type").get_active()
        new_core_config["proxy"]["username"] = self.builder.get_object("entry_proxy_user").get_text()
        new_core_config["proxy"]["password"] = self.builder.get_object("entry_proxy_pass").get_text()
        new_core_config["proxy"]["hostname"] = self.builder.get_object("entry_proxy_host").get_text()
        new_core_config["proxy"]["port"] = self.builder.get_object("spin_proxy_port").get_value_as_int()
        new_core_config["proxy"]["proxy_hostnames"] = self.builder.get_object("chk_proxy_host_resolve").get_active()
        new_core_config["proxy"]["proxy_peer_connections"] = self.builder.get_object(
            "chk_proxy_peer_conn").get_active()
        new_core_config["i2p_proxy"] = {}
        new_core_config["i2p_proxy"]["hostname"] = self.builder.get_object("entry_i2p_host").get_text()
        new_core_config["i2p_proxy"]["port"] = self.builder.get_object("spin_i2p_port").get_value_as_int()
        new_core_config["anonymous_mode"] = self.builder.get_object("chk_anonymous_mode").get_active()

        # Queue tab #
        new_core_config["queue_new_to_top"] = \
            self.builder.get_object("chk_queue_new_top").get_active()
        new_core_config["max_active_seeding"] = \
            self.builder.get_object("spin_seeding").get_value_as_int()
        new_core_config["max_active_downloading"] = \
            self.builder.get_object("spin_downloading").get_value_as_int()
        new_core_config["max_active_limit"] = \
            self.builder.get_object("spin_active").get_value_as_int()
        new_core_config["dont_count_slow_torrents"] = \
            self.builder.get_object("chk_dont_count_slow_torrents").get_active()
        new_core_config["auto_manage_prefer_seeds"] = \
            self.builder.get_object("chk_auto_manage_prefer_seeds").get_active()
        new_core_config["stop_seed_at_ratio"] = \
            self.builder.get_object("chk_seed_ratio").get_active()
        new_core_config["remove_seed_at_ratio"] = \
            self.builder.get_object("chk_remove_ratio").get_active()
        new_core_config["stop_seed_ratio"] = \
            self.builder.get_object("spin_share_ratio").get_value()
        new_core_config["share_ratio_limit"] = \
            self.builder.get_object("spin_share_ratio_limit").get_value()
        new_core_config["seed_time_ratio_limit"] = \
            self.builder.get_object("spin_seed_time_ratio_limit").get_value()
        new_core_config["seed_time_limit"] = \
            self.builder.get_object("spin_seed_time_limit").get_value()

        # Cache tab #
        new_core_config["cache_size"] = \
            self.builder.get_object("spin_cache_size").get_value_as_int()
        new_core_config["cache_expiry"] = \
            self.builder.get_object("spin_cache_expiry").get_value_as_int()

        # Run plugin hook to apply preferences
        component.get("PluginManager").run_on_apply_prefs()

        # Lanuage
        if self.language_checkbox.get_active():
            new_gtkui_config["language"] = None
        else:
            active = self.language_combo.get_active()
            if active == -1:
                dialog = InformationDialog(
                    _("Attention"),
                    _("You must choose a language")
                )
                dialog.run()
                return
            else:
                model = self.language_combo.get_model()
                new_gtkui_config["language"] = model.get(model.get_iter(active), 0)[0]

        if new_gtkui_config["language"] != self.gtkui_config["language"]:
            dialog = InformationDialog(
                _("Attention"),
                _("You must now restart the deluge UI for the changes to take effect.")
            )
            dialog.run()

        # GtkUI
        for key in new_gtkui_config.keys():
            # The values do not match so this needs to be updated
            if self.gtkui_config[key] != new_gtkui_config[key]:
                self.gtkui_config[key] = new_gtkui_config[key]

        # Core
        if client.connected():
            # Only do this if we're connected to a daemon
            config_to_set = {}
            for key in new_core_config.keys():
                # The values do not match so this needs to be updated
                if self.core_config[key] != new_core_config[key]:
                    config_to_set[key] = new_core_config[key]

            if config_to_set:
                # Set each changed config value in the core
                client.core.set_config(config_to_set)
                client.force_call(True)
                # Update the configuration
                self.core_config.update(config_to_set)

        if hide:
            self.hide()
        else:
            # Re-show the dialog to make sure everything has been updated
            self.show()

        if classic_mode_was_set != new_gtkui_in_classic_mode:
            def on_response(response):
                if response == gtk.RESPONSE_YES:
                    shutdown_daemon = (not client.is_classicmode() and
                                       client.connected() and
                                       client.is_localhost())
                    component.get("MainWindow").quit(shutdown=shutdown_daemon)
                else:
                    self.gtkui_config["classic_mode"] = not new_gtkui_in_classic_mode
                    self.builder.get_object("radio_classic").set_active(self.gtkui_config["classic_mode"])
                    self.builder.get_object("radio_thinclient").set_active(not self.gtkui_config["classic_mode"])
            dialog = YesNoDialog(
                _("Switching client mode..."),
                _("Your current session will be stopped. Do you wish to continue?")
            )
            dialog.run().addCallback(on_response)
    '''
    def hide(self):
        self.window_open = False
        self.builder.get_object("port_img").hide()
        self.pref_dialog.hide()
