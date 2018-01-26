import gi

gi.require_version('Gtk', '3.0')
from Utils import func_once, SettinsManager


class SettingsWindow:
    def __init__(self, app):
        self.app = app
        self.window = app.builder.get_object("WindowwSettings")
        self.window.show_all()
        self.set_values_from_settings()
        self.connect_signals()

    @func_once
    def connect_signals(self):
        self.app.builder.get_object("ButtonSaveSettings").connect("clicked", self.on_save_and_connect)
        self.window.connect('delete_event', self.on_close)

    def set_values_from_settings(self):
        settings = SettinsManager()
        email = settings.get("email")
        passwd = settings.get("pass")
        url = settings.get("url")
        self.app.builder.get_object("InputEmail").set_text(email)
        self.app.builder.get_object("InputPassword").set_text(passwd)
        self.app.builder.get_object("InputServerUrl").set_text(url)

    def on_close(self, widget, event):
        self.window.hide()
        return True

    def on_save_and_connect(self, event):
        email = self.app.builder.get_object("InputEmail").get_text()
        passwd = self.app.builder.get_object("InputPassword").get_text()
        url = self.app.builder.get_object("InputServerUrl").get_text()
        settings = SettinsManager()
        settings.set("email", email)
        settings.set("pass", passwd)
        settings.set("url", url)
        settings.save()
        self.window.hide()
        self.app.reset_connectivity()
