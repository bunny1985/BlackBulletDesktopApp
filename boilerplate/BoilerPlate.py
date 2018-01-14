import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk

from gi.repository import Gio
import sys
from TrayIcon import TrayIcon
from SmsWindow import SmsWindow
from SendWindow import SendWindow
from SettingsWindow import SettingsWindow
from Notification import Notification
from ConnectivityManager import ConnectivityManager

class MyApplication(Gtk.Application):
    APPNAME = "boilerplate"
    SETTINGS_KEY = "pl.bmIdeas.blackbullet"
    settings = {}
    def __init__(self):
        Gdk.threads_init()
        Gtk.Application.__init__(self)
        
    def message(self, data=None):
        "Function to display messages to the user."
        msg=Gtk.MessageDialog(None, Gtk.DIALOG_MODAL,
        Gtk.MESSAGE_INFO, Gtk.BUTTONS_OK, data)
        msg.run()
        msg.destroy()

    def show_sms_window(self):
        SmsWindow(self)
    def show_send_window(self):
        SendWindow(self)
    def show_settings_window(self):
        SettingsWindow(self)
    def play_ringtone(self):
        self.notify("Playing ringtone request" , "Sending" , "info")
        self.connectivity.ringtone_request()
    def sms(self, to , text):
        self.notify("Sending Sms via phone" , "" , "info")
        self.connectivity.sms_request(to, text);
    def share(self,  text):
        self.notify("Sending info to phone" ,"", "info")
        self.connectivity.share_request(text);


    def notify(self, title, text ,notificationType):
        Notification(title, text, notificationType).show()
        

    def do_activate(self):
        #window = self.builder.get_object("WindowSms")
        #window.show_all()
        
        self.icon = TrayIcon(self)
        self.notify("Welcome in BlackBullet " , "" , "info")
        
        self.connect()

        Gtk.main()
    def connect(self):
        self.connectivity = ConnectivityManager(self)
        try:
            self.connectivity.authorize()
            self.connectivity.connect()
        except Exception as e:
            print(e)
            self.notify("UNABLE TO AUTHORIZE OR CONNECT"  ,"" , "error")
            self.show_settings_window()
            
        
        
        
        
    def quit(self):
        self.notify("Bye Bye " , "" , "info")
        Gtk.main_quit()
        self.connectivity.ws.close()

        sys.exit(0)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        #self.settings = Gio.Settings.new(self.SETTINGS_KEY)
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../resources/GladeFiles/SmsWindow.glade")
        
        

      
