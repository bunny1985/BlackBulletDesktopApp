import json
from collections import namedtuple
import httplib2
import websocket
from SettingsWindow import SettinsManager
import threading
import time
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import  GObject


class ConnectivityManager():
    def __init__(self , app):
        self.app = app
        settings = SettinsManager()
        self.mail = settings.get("email")
        self.passwd = settings.get("pass")
        self.url = settings.get("url")
        self.http = httplib2.Http(".cache")
        


    def authorize(self):
        print(self.url + "/api/Account/Login")
        print(self.mail)
        print(self.passwd)
        (resp_headers, content) = self.http.request("http://" +  self.url + "/api/Account/Login" , "POST", body = "{'email': '" + self.mail+ "', 'PASSWORD': '" + self.passwd+  "'}", headers = {'Content-type': 'application/json'})
        self.authCookie =  resp_headers["set-cookie"]
        print("AUTHENTICATED")
    

    def connect(self):
        self.ws = websocket.WebSocketApp(url = "ws://" + self.url + "/notificationsSocket" , on_open = self.on_connect_callback()  ,on_close=self.on_disconnect_callback(),  cookie = self.authCookie )
        self.ws.on_message = self.on_message_callback()
        ConnectivityManager.websocketWorker = threading.Thread(name='worker', target=self.ws.run_forever)
        ConnectivityManager.websocketWorker.daemon = True
        ConnectivityManager.websocketWorker.start()
    

        
    def on_connect_callback(self):
        def fun(ws):
            print("WS OPEN")
            self.app.notify("BlackBullet connection established", "" , "info")
        return fun

    def on_disconnect_callback(self):
        def fun(ws):
            print("WS Closed!")
            self.app.notify("BlackBullet connection lost", "" , "warning")
            def restart(a, b):
                    self.ws.close()
                    self.authorize()
                    ConnectivityManager.websocketWorker = threading.Thread(name='worker', target=self.ws.run_forever)
                    ConnectivityManager.websocketWorker.daemon = True
                    ConnectivityManager.websocketWorker.start()
            time.sleep(5)
            GObject.idle_add(restart, 0,2)    
        return fun
    

            

    
    def ringtone_request(self):
        self.ws.send('{"type": "ringtone"}')
    def sms_request(self, to , text):
        self.ws.send("{'type': 'sms' , 'to' : '" + to + "' , 'text': '" + text+ "' }")
    def share_request(self, text):
        self.ws.send("{'type': 'notification' , 'text': '" + text+ "' }")
    


    def on_message_callback(self):
        def on_message(ws, message):
            try:
                print("Server Said: ")
                print(message)
                msg = json.loads(message , object_hook=lambda d: namedtuple('X', d.keys())(*d.values()) )
                self.app.notify(msg.title , msg.body , "information" )
            except:
                pass

        return on_message
            