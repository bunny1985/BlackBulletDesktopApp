import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import sys
import Ui
import Utils
import Api
import logging
import time

import WebsocketMessageHandler
logging.basicConfig( level=logging.DEBUG)
log = logger = logging.getLogger(__name__)


class BlackBulletApplication(Gtk.Application):

    def __init__(self):

        self.messageHandler = WebsocketMessageHandler.WebSocketMessageHandler(self)
        self.notification_factory = Ui.NotificatonFactory()  # type : Ui.NotificatonFactory
        Gtk.Application.__init__(self)
        Gdk.threads_init()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        #self.settings = Gio.Settings.new(self.SETTINGS_KEY)
        self.builder = Gtk.Builder()
        self.builder.add_from_file("../resources/GladeFiles/SmsWindow.glade")
        if self.is_config_valid() == False: 
            self.show_settings_window()
        self.api = Api.ConnectivityManager(self)
        self.api.connect("authenticated" , self.on_authorized)
        self.api.connect("authenticatation_failed" , self.on_authorization_failed)
        self.api.connect("ws_opened" , self.on_ws_opened)
        self.api.connect("ws_closed" , self.on_ws_closed)
        self.api.connect("ws_message_recived" , self.on_message_recived)
        
        self.api.authorize()
        
    def reset_connectivity(self):
        log.info("Closing Connections")
        self.api.checker_thread_cancelation_token = True
        if self.api.ws!=None:
            self.api.ws.close()
        # Make sure that everything is closed
        time.sleep(5)
        log.info("Opening Connections")
        self.api.checker_thread_cancelation_token = None
        self.api.authorize()
        

    def on_ws_opened(self , event ,msg ):
        log.info("WS OPEN! WE ARE ONLINE NOW")
        self.icon.statusIcon.set_from_file("../resources/GladeFiles/icons/128x128/icon.png")
    def on_ws_closed(self , event ,reason ):
        self.icon.statusIcon.set_from_file("../resources/GladeFiles/icons/128x128/ammunition.png")
        log.info("CONNECTION DOWN")
        self.reset_connectivity();


    def on_message_recived(self, event , raw_mmessage):
        self.messageHandler.handle(raw_mmessage)
        
        
        

    def on_authorized(self , event ,cookie ):
        log.info("Authenticated")
        self.api.connect_web_socket()

    def on_authorization_failed(self, event ,string):
        log.warn("AUTH FAILED")
        self.notification_factory.CreateWarning("Authorization Failed"  , "").show()
        self.show_settings_window()


    def is_config_valid(self):
        config = Utils.SettinsManager().get_config_as_object()
        if config.user_name == "" or config.password == "" or config.address == "":
            return False
        return True


    def show_sms_window(self):
        Ui.SmsWindow(self)
    def show_send_window(self):
        Ui.SendWindow(self)
    def show_settings_window(self):
        Ui.SettingsWindow(self)
    def play_ringtone(self):
        self.notification_factory.CreateInfo("Sending ringtone request", "").show()
        self.api.ringtone_request()
    def sms(self, to , text):
        self.notification_factory.CreateInfo("Sending sms", text).show()
        self.api.sms_request(to, text);
    def share(self,  text):
        self.notification_factory.CreateInfo("Sending notification", text).show()
        self.api.share_request(text);
    def get_battery_status(self):
        self.api.get_battery_status();

    def close_all_notifications(self):
        self.get_battery_status()
        self.notification_factory.close_all();

    def dismiss_mobile_notification(self,  id):
        log.info("Dismissing Notification id: " + id)
        self.api.dismiss_notification(id);

    def do_activate(self):
        self.icon = Ui.TrayIcon(self)
        self.notification_factory.CreateInfo("Blackbullet Started" , "").show()
        Gtk.main()

        
        
        
        
    def quit(self):
        self.api.checker_thread_cancelation_token = True
        self.notification_factory.CreateInfo("Bye Bye" , "").show()
        Gtk.main_quit()
        # self.connectivity.ws.close()

        sys.exit(0)


        

      
