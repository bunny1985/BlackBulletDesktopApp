import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')


class TrayIcon:

    def __init__(self, app):
        self.app = app
        self.status_icon = app.builder.get_object("StatusIcon")
        self.status_icon.set_visible(True)
        # icons/128x128/icon.png

        self.status_icon.connect("popup-menu", self.right_click_event)
        self.menu = self.app.builder.get_object("TryIconMenu")

        quit = self.app.builder.get_object("MenuItemQuit")
        quit.connect("activate", self.on_quit_selected)

        settings = self.app.builder.get_object("MenuItemSettings")
        settings.connect("activate", self.on_setting_selected)

        ringtone = self.app.builder.get_object("MenuItemRingtone")
        ringtone.connect("activate", self.on_ringtone_selected)

        share = self.app.builder.get_object("MenuItemShare")
        share.connect("activate", self.on_send_text_selected)

        sms = self.app.builder.get_object("MenuItemSms")
        sms.connect("activate", self.on_sms_selected)

        clear = self.app.builder.get_object("MenuItemClearAll")
        clear.connect("activate", self.Clear_all_notifications)

        battery = self.app.builder.get_object("BatteryStatus")
        battery.connect("activate", self.BatterySelected)

        # .connect("popup-menu", self.OnShowPopupMenu)
        # window = Gtk.Window()

    def on_quit_selected(self, widget):
        print("Quit")
        self.app.quit()

    def on_setting_selected(self, widget):
        print("Settings")
        self.app.show_settings_window();

    def on_sms_selected(self, widget):
        print("Sms")
        self.app.show_sms_window();

    def on_ringtone_selected(self, widget):
        print("Ringtone")
        self.app.play_ringtone();

    def on_send_text_selected(self, widget):
        print("Send")
        self.app.show_send_window();

    def Clear_all_notifications(self, widget):
        print("Clear All Notification")
        self.app.close_all_notifications();

    def BatterySelected(self, widget):
        print("GET BATTERY STATUS")
        self.app.get_battery_status();

    def right_click_event(self, widget, event, eventTime):
        self.menu.popup(None, None, None, None, event, eventTime)
