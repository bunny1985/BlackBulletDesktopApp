import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Notify

from Utils import func_once
from random import randint


class NotificatonFactory:
    title = "Title"
    body = "content"
    type = "information"

    def __init__(self):
        self.init_notifications()
        self.list = []

        def on_notification_closed(notification):
            self.list.remove(notification)

        self.on_notification_closed = on_notification_closed

    def create_notification(self, title, body, icon):
        notification = Notify.Notification.new(title, body, icon)
        notification.id = randint(0, 9999999)
        notification.set_timeout(Notify.EXPIRES_NEVER)
        self.list.append(notification)
        notification.connect('closed', self.on_notification_closed)
        return notification

    def close_all(self):
        for item in self.list:
            item.close()

    def create_info(self, title, body):
        icon = "dialog-info"
        return self.create_notification(title, body, icon)

    def create_warning(self, title, body):
        icon = "dialog-warning"
        return self.create_notification(title, body, icon)

    def create_mobile_notification(self, title, body, icon=None):
        if (icon == None):
            icon = "file:///home/michal/Project/PyGtkBlackBullet/resources/GladeFiles/icons/128x128/phone.png"
        return self.create_notification(title, body, icon)

    @func_once
    def init_notifications(self):
        Notify.init("BlackBulletApp")
