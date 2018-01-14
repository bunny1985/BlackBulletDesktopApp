import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
import configparser
import sys
from Utils import func_once


class SettingsWindow:
    def __init__(self ,app):
        self.app = app
        self.window = app.builder.get_object("WindowwSettings")
        self.window.show_all()
        self.set_values_from_settings()
        self.connect_signals()
    @func_once
    def connect_signals(self):
        self.app.builder.get_object("ButtonSaveSettings").connect("clicked" ,self.save)
        self.window.connect('delete_event', self.on_close)
        

    def set_values_from_settings(self):
        settings = SettinsManager()
        email = settings.get("email" )
        passwd = settings.get("pass" )
        url = settings.get("url" )
        self.app.builder.get_object("InputEmail").set_text(email)
        self.app.builder.get_object("InputPassword").set_text(passwd)
        self.app.builder.get_object("InputServerUrl").set_text(url)

    def on_close(self , widget, event):
        self.window.hide()
        return True
    def save(self , event):
        email  = self.app.builder.get_object("InputEmail").get_text()
        passwd  = self.app.builder.get_object("InputPassword").get_text()
        url  = self.app.builder.get_object("InputServerUrl").get_text()
        settings = SettinsManager()
        settings.set("email" ,email)
        settings.set("pass" ,passwd)
        settings.set("url" ,url)
        settings.save()
        self.app.notify("Settings saved" , "" , "info")
        self.app.connect()
        
        self.window.hide()
        

class SettinsManager:

    def __init__(self):
        SettinsManager.filename = "preferences.conf"
        SettinsManager.category = "DEFAULT"

        self.config = configparser.ConfigParser()
        self.config.read(SettinsManager.filename)


    def get(self, key):
        return self.config[SettinsManager.category][key]
    def set(self, key , value):
        self.config[SettinsManager.category][key] = value
    def save(self):
        with open(SettinsManager.filename, 'w') as configfile:    # save
            self.config.write(configfile)

