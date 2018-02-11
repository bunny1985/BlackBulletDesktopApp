import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from Utils import func_once


class SendWindow:
    def __init__(self, app):
        self.app = app
        self.window = app.builder.get_object("WindowShare")
        self.window.show_all()
        self.connect_signals()

    @func_once
    def connect_signals(self):
        self.app.builder.get_object("ButtonSend").connect("clicked", self.send)
        self.window.connect('delete_event', self.on_close)

    def on_close(self, widget, event):
        self.window.hide()
        self.app.builder.get_object("ButtonSend").connect("clicked", self.send)
        return True

    def send(self, event):
        text_buffer = self.app.builder.get_object("InputTextShare").get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), False)
        self.app.share(text)
        self.window.hide()
