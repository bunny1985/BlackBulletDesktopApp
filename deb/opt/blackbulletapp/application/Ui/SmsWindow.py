import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from Utils import func_once


class SmsWindow:

    def __init__(self, app):
        self.app = app

        self.window = app.builder.get_object("WindowSms")
        self.window.show_all()
        self.connect_signals()
        # ButtonSendSms

    @func_once
    def connect_signals(self):
        print("Conneting signals")
        self.app.builder.get_object("ButtonSendSms").connect("clicked", self.send_sms)
        self.window.connect('delete_event', self.on_close)

    def on_close(self, widget, event):
        self.window.hide()
        return True

    def send_sms(self, event):
        phone_number = self.app.builder.get_object("InputPhoneNumber").get_text()
        text_buffer = self.app.builder.get_object("InputSmsText").get_buffer()
        text = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter(), False)
        self.app.sms(phone_number, text)
        self.window.hide()
