import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, Gio
from gi.repository import Notify


class Notification:
  title = "Title"
  body = "content"
  type ="information" 
  def __init__(self, title, body , notificationType):
    self.title = title
    self.body = body
    self.type = notificationType
  def show(self):
    Notify.init(self.title)
    Hello=Notify.Notification.new(self.title, self.body , "dialog-"+ self.type)
    Hello.show()