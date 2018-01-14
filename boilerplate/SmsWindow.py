import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

import sys
from Utils import func_once


class SmsWindow:
    
    def __init__(self ,app):
        self.app = app
        
        
        self.window = app.builder.get_object("WindowSms")
        self.window.show_all()
        self.connect_signals()
        #ButtonSendSms
    @func_once
    def connect_signals(self):
        print("Conneting signals")
        self.app.builder.get_object("ButtonSendSms").connect("clicked" ,self.send_sms)
        self.window.connect('delete_event', self.on_close)
    def on_close(self , widget, event):
        self.window.hide()
        return True
    
    def send_sms(self , event):
        phoneNumber  = self.app.builder.get_object("InputPhoneNumber").get_text()
        textbuffer = self.app.builder.get_object("InputSmsText").get_buffer()
        text  =textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter() , False)
        self.app.sms(phoneNumber ,  text)
        self.window.hide()
        