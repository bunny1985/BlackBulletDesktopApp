import json
from collections import namedtuple
import httplib2
import websocket
from Utils import SettinsManager
import threading
import time
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import  GObject

import logging
logging.basicConfig( level=logging.DEBUG)
log = logger = logging.getLogger(__name__)


class ConnectivityManager(GObject.GObject):
    checker_thread = None
    checker_thread_cancelation_token = None
    ws = None

    __gsignals__ = {
        'authenticated': (GObject.SIGNAL_RUN_LAST, None,(str,)),
        'authenticatation_failed': (GObject.SIGNAL_RUN_LAST, None,(str,)),
        'ws_opened': (GObject.SIGNAL_RUN_LAST, None ,(str,)),
        'ws_error': (GObject.SIGNAL_RUN_LAST, None ,(str,)),
        'ws_closed': (GObject.SIGNAL_RUN_LAST, None  ,(str,)),
        'ws_message_recived': (GObject.SIGNAL_RUN_LAST, None  ,(str,))
    }
    

    def __init__(self , app):
        GObject.GObject.__init__(self)
        self.app = app
        self.http = httplib2.Http(".cache")
        self.config = SettinsManager().get_config_as_object()
        

        


        
        
        
    

    def authorize(self):
        try:
            (resp_headers, content) = self.http.request("http://" +  self.config.address + "/api/Account/Login" , "POST", body = "{'email': '" + self.config.user_name+ "', 'PASSWORD': '" + self.config.password+  "'}", headers = {'Content-type': 'application/json'})
            self.authCookie =  resp_headers["set-cookie"]
            self.app.state.authorized = True
            
            self.emit("authenticated" , self.authCookie)
        except Exception as e:
            print(e)
            self.emit("authenticatation_failed" , "Something went wrong")
            
    

    def connect_web_socket(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(url = "ws://" + self.config.address + "/notificationsSocket" , on_open = self.on_connect_callback()  ,on_close=self.on_disconnect_callback(),  cookie = self.authCookie )
        self.ws.on_message = self.on_message_callback()
        self.ws.isOk = False
        ConnectivityManager.websocketWorker = threading.Thread(name='worker', target=self.ws.run_forever)
        ConnectivityManager.websocketWorker.daemon = True
        ConnectivityManager.websocketWorker.start()
        
    

        
    def on_connect_callback(self):
        def fun(ws):
            log.debug("connected")
            self.ws.isOk = True
            self.emit("ws_opened" , "Ok")
            #GObject.idle_add(lambda :self.emit("ws_opened" , "Closed"))
        return fun

    
        
    def on_disconnect_callback(self):
        
        def fun(ws):
            log.debug("disconnected")
            GObject.idle_add(lambda :self.emit("ws_closed" , "Closed"))
            self.ws.isOk = False
        return fun
    

            

    
    def ringtone_request(self):
        self.ws.send('{"type": "ringtone"}')
    def sms_request(self, to , text):
        self.ws.send("{'type': 'sms' , 'to' : '" + to + "' , 'text': '" + text+ "' }")
    def share_request(self, text):
        self.ws.send("{'type': 'notification' , 'text': '" + text+ "' }")
    def dismiss_notification(self, id):
        self.ws.send("{'type': 'dismiss' , 'id': '" + id+ "' }")
    


    def on_message_callback(self):
        def on_message(ws, message):
            
            try:
                print("Server Said: ")
                print(message)
                #log.debug("WS message:" + message)
                #msg = json.loads(message , object_hook=lambda d: namedtuple('X', d.keys())(*d.values()) )
                #self.app.notify(msg.title , msg.body , "information" )
                self.emit("ws_message_recived" , message)
            except:
                pass

        return on_message
            