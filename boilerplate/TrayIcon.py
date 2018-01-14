import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

import sys



class TrayIcon:

    def __init__(self ,app):
        self.app = app
        self.statusIcon  = app.builder.get_object("StatusIcon")
        self.statusIcon.set_visible(True)
        
        self.statusIcon.connect("popup-menu", self.right_click_event)
        self.menu  = self.app.builder.get_object("TryIconMenu")
        
        quit  = self.app.builder.get_object("MenuItemQuit")
        quit.connect("activate", self.QuitSelected)
        
        settings  = self.app.builder.get_object("MenuItemSettings")
        settings.connect("activate", self.SettingsSelected)

        ringtone  = self.app.builder.get_object("MenuItemRingtone")
        ringtone.connect("activate", self.RingtoneSelected)

        share  = self.app.builder.get_object("MenuItemShare")
        share.connect("activate", self.SendTextSelected)

        sms  = self.app.builder.get_object("MenuItemSms")
        sms.connect("activate", self.SmsSelected)
        
        #.connect("popup-menu", self.OnShowPopupMenu)
        #window = Gtk.Window()
    def QuitSelected(self, widget):
        print("Quit")
        self.app.quit()
    def SettingsSelected(self, widget):
        print("Settings")
        self.app.show_settings_window();
    def SmsSelected(self, widget):
        print("Sms")
        self.app.show_sms_window();
    def RingtoneSelected(self, widget):
        print("Ringtone")
        self.app.play_ringtone();
    def SendTextSelected(self, widget):
        print("Send")
        self.app.show_send_window();


    def right_click_event(self, widget, event, eventTime):
        self.menu.popup(None, None, None, None, event, eventTime)
        
        




    

        