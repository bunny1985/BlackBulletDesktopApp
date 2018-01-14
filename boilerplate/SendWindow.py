import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

import sys



class SendWindow:
    def __init__(self ,app):
        self.app = app
        self.window = app.builder.get_object("WindowShare")
        self.window.show_all()
        app.builder.get_object("ButtonSend").connect("clicked" ,self.send)
        self.window.connect('delete_event', self.on_close)
    def on_close(self , widget, event):
        self.window.hide()
        return True
    def send(self , event):
        textbuffer = self.app.builder.get_object("InputTextShare").get_buffer()
        text  =textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter() , False)
        self.app.share(text)
        self.window.hide()
        
