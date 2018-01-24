
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

import json
from collections import namedtuple
import logging
logging.basicConfig( level=logging.DEBUG)
log = logger = logging.getLogger(__name__)

import webbrowser


class ClipboardHandler():
    can_handle = "clipboard"

    def __init__(self, app):
        self.app = app  # type: Application.BlackBulletApplication

    def handle(self, notification):
        log.debug("Handling cliboard request")

        def clipboard_add(a):
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clipboard.set_text(notification.body, -1)
            notification_factory = self.app.notification_factory  # type : Ui.NotificatonFactory
            notification_factory.CreateInfo("Clipboard From mobile recived", notification.body).show()

        GObject.idle_add(clipboard_add, 1)
class BatteryHandler():
    can_handle = "battery"

    def __init__(self, app):
        self.app = app  # type: Application.BlackBulletApplication

    def handle(self, notification):
        log.debug("Handling Battery status")

        def update_battery_status(a):
            notification_factory = self.app.notification_factory  # type : Ui.NotificatonFactory
            chargingstring = 'charging' if  notification.isCharging == "true" else ''
            notification_factory.CreateInfo("Mobile Battery level:", str(int(float(notification.percent)*100))+"% " + chargingstring   ) .show()

        GObject.idle_add(update_battery_status, 1)

class GenericNotificationHandler():
    can_handle = "notification"

    def __init__(self ,  app):
        self.app = app  # type: Application.BlackBulletApplication

    def handle(self ,notification ):
        log.debug("Handling generic notification")
        desktop_notification  = self.app.notification_factory.CreateMobileNotification(notification.title , notification.body)
        if (notification.package == "com.facebook.katana" or notification.package == "com.facebook.orca"):
            desktop_notification.add_action("open_facebook", "Open Facebook", lambda a , b , c : webbrowser.open('https://facebook.com/', new= 2) , None)
        if(notification.package == "com.whatsapp"): 
            desktop_notification.add_action("open_whatsup", "Whatsup Web", lambda a , b , c: webbrowser.open('https://web.whatsapp.com/', new= 2) , None)
        if(notification.package == "com.instagram.android"): 
            desktop_notification.add_action("open_insta", "Whatsup Web", lambda a , b , c: webbrowser.open('https://www.instagram.com/', new= 2) , None)
        desktop_notification.add_action("dismiss_notification", "Dismiss on mobile", lambda a , b , c: self.app.dismiss_mobile_notification(notification.id) , None)

        desktop_notification.show()

class WebSocketMessageHandler():
    handlers = []
    
    def __init__(self , app):
        self.app = app  # type: Application.BlackBulletApplication
        self.register_handlers(app)

    def register_handlers(self , app):
        self.handlers.append(GenericNotificationHandler(app))
        self.handlers.append(ClipboardHandler(app))
        self.handlers.append(BatteryHandler(app))
    
    def handle(self , message):
        #try:
        msg = json.loads(message , object_hook=lambda d: namedtuple('X', d.keys())(*d.values()) )
        if hasattr(msg, "status"):
            return

        eventType = msg.notificationType
        log.debug(eventType)
        for handler in self.handlers:
            if(handler.can_handle == eventType):
                handler.handle(msg)
            
        # except:
        #     pass
    