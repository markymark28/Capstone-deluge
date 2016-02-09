/*!
 * Deluge.preferences.InterfacePage.js
 *
 * Copyright (c) Damien Churchill 2009-2010 <damoxc@gmail.com>
 *
 * This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
 * the additional special exception to link portions of this program with the OpenSSL library.
 * See LICENSE for more details.
 */
Ext.namespace('Deluge.preferences');

/**
 * @class Deluge.preferences.Interface
 * @extends Ext.form.FormPanel
 */
Deluge.preferences.Interface = Ext.extend(Ext.form.FormPanel, {

    border: false,
    title: _('Interface'),
    layout: 'form',

    initComponent: function() {
        Deluge.preferences.Interface.superclass.initComponent.call(this);

        var om = this.optionsManager = new Deluge.OptionsManager();
        this.on('show', this.onPageShow, this);

        var fieldset = this.add({
            xtype: 'fieldset',
            border: false,
            title: _('Interface'),
            style: 'margin-bottom: 0px; padding-bottom: 5px; padding-top: 5px',
            autoHeight: true,
            labelWidth: 1,
            defaultType: 'checkbox'
        });
        om.bind('show_session_speed', fieldset.add({
            name: 'show_session_speed',
            height: 22,
            fieldLabel: '',
            labelSeparator: '',
            boxLabel: _('Show session speed in titlebar')
        }));
        om.bind('sidebar_show_zero', fieldset.add({
            name: 'sidebar_show_zero',
            height: 22,
            fieldLabel: '',
            labelSeparator: '',
            boxLabel: _('Show filters with zero torrents')
        }));
        om.bind('sidebar_multiple_filters', fieldset.add({
            name: 'sidebar_multiple_filters',
            height: 22,
            fieldLabel: '',
            labelSeparator: '',
            boxLabel: _('Allow the use of multiple filters at once')
        }));

        fieldset = this.add({
            xtype: 'fieldset',
            border: false,
            title: _('Password'),
            style: 'margin-bottom: 0px; padding-bottom: 0px; padding-top: 5px',
            autoHeight: true,
            labelWidth: 110,
            defaultType: 'textfield',
            defaults: {
                width: 180,
                inputType: 'password'
            }
        });

        this.oldPassword = fieldset.add({
            name: 'old_password',
            fieldLabel: _('Old Password:'),
            labelSeparator: ''
        });
        this.newPassword = fieldset.add({
            name: 'new_password',
            fieldLabel: _('New Password:'),
            labelSeparator: ''
        });
        this.confirmPassword = fieldset.add({
            name: 'confirm_password',
            fieldLabel: _('Confirm Password:'),
            labelSeparator: ''
        });

        var panel = fieldset.add({
            xtype: 'panel',
            autoHeight: true,
            border: false,
            width: 320,
            bodyStyle: 'padding-left: 230px'
        })
        panel.add({
            xtype: 'button',
            text: _('Change'),
            listeners: {
                'click': {
                    fn: this.onPasswordChange,
                    scope: this
                }
            }
        });

        fieldset = this.add({
            xtype: 'fieldset',
            border: false,
            title: _('Server'),
            style: 'margin-top: 0px; padding-top: 0px; margin-bottom: 0px; padding-bottom: 0px',
            autoHeight: true,
            labelWidth: 110,
            defaultType: 'spinnerfield',
            defaults: {
                width: 80
            }
        });
        om.bind('session_timeout', fieldset.add({
            name: 'session_timeout',
            fieldLabel: _('Session Timeout:'),
            labelSeparator: '',
            decimalPrecision: 0,
            minValue: -1,
            maxValue: 99999
        }));
        om.bind('port', fieldset.add({
            name: 'port',
            fieldLabel: _('Port:'),
            labelSeparator: '',
            decimalPrecision: 0,
            minValue: -1,
            maxValue: 99999
        }));
        this.httpsField = om.bind('https', fieldset.add({
            xtype: 'checkbox',
            name: 'https',
            hideLabel: true,
            width: 280,
            height: 22,
            boxLabel: _('Use SSL (paths relative to Deluge config folder)')
        }));
        this.httpsField.on('check', this.onSSLCheck, this);
        this.pkeyField = om.bind('pkey', fieldset.add({
            xtype: 'textfield',
            disabled: true,
            name: 'pkey',
            width: 180,
            fieldLabel: _('Private Key:'),
            labelSeparator: ''
        }));
        this.certField = om.bind('cert', fieldset.add({
            xtype: 'textfield',
            disabled: true,
            name: 'cert',
            width: 180,
            fieldLabel: _('Certificate:'),
            labelSeparator: ''
        }));
    },

    onApply: function() {
        var changed = this.optionsManager.getDirty();
        if (!Ext.isObjectEmpty(changed)) {
            deluge.client.web.set_config(changed, {
                success: this.onSetConfig,
                scope: this
            });

            for (var key in deluge.config) {
                deluge.config[key] = this.optionsManager.get(key);
            }
        }
    },

    onGotConfig: function(config) {
        this.optionsManager.set(config);
    },

    onPasswordChange: function() {
        var newPassword = this.newPassword.getValue();
        if (newPassword != this.confirmPassword.getValue()) {
            Ext.MessageBox.show({
                title: _('Invalid Password'),
                msg: _('Your passwords don\'t match!'),
                buttons: Ext.MessageBox.OK,
                modal: false,
                icon: Ext.MessageBox.ERROR,
                iconCls: 'x-deluge-icon-error'
            });
            return;
        }

        var oldPassword = this.oldPassword.getValue();
        deluge.client.auth.change_password(oldPassword, newPassword, {
            success: function(result) {
                if (!result) {
                    Ext.MessageBox.show({
                        title: _('Password'),
                        msg: _('Your old password was incorrect!'),
                        buttons: Ext.MessageBox.OK,
                        modal: false,
                        icon: Ext.MessageBox.ERROR,
                        iconCls: 'x-deluge-icon-error'
                    });
                    this.oldPassword.setValue('');
                } else {
                    Ext.MessageBox.show({
                        title: _('Change Successful'),
                        msg: _('Your password was successfully changed!'),
                        buttons: Ext.MessageBox.OK,
                        modal: false,
                        icon: Ext.MessageBox.INFO,
                        iconCls: 'x-deluge-icon-info'
                    });
                    this.oldPassword.setValue('');
                    this.newPassword.setValue('');
                    this.confirmPassword.setValue('');
                }
            },
            scope: this
        });
    },

    onSetConfig: function() {
        this.optionsManager.commit();
    },

    onPageShow: function() {
        deluge.client.web.get_config({
            success: this.onGotConfig,
            scope: this
        })
    },

    onSSLCheck: function(e, checked) {
        this.pkeyField.setDisabled(!checked);
        this.certField.setDisabled(!checked);
    }
});
