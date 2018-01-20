import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
from gi.repository import Notify

from Utils import func_once , SettinsManager
from random import randint


class SendWindow:
    def __init__(self ,app):
        self.app = app
        self.window = app.builder.get_object("WindowShare")
        self.window.show_all()
        self.connect_signals()
    @func_once
    def connect_signals(self):
        self.app.builder.get_object("ButtonSend").connect("clicked" ,self.send)
        self.window.connect('delete_event', self.on_close)
    def on_close(self , widget, event):
        self.window.hide()
        self.app.builder.get_object("ButtonSend").connect("clicked" ,self.send)
        return True
    def send(self , event):
        textbuffer = self.app.builder.get_object("InputTextShare").get_buffer()
        text  =textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter() , False)
        self.app.share(text)
        self.window.hide()
        



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
        

class TrayIcon:

    def __init__(self ,app):
        self.app = app
        self.statusIcon  = app.builder.get_object("StatusIcon")
        self.statusIcon.set_visible(True)
        
        self.statusIcon.connect("popup-menu", self.right_click_event)
        self.menu  = self.app.builder.get_object("TryIconMenu")
        
        quit  = self.app.builder.get_object("MenuItemQuit")
        quit.connect("activate", self.QuitSelected)
        
        settings  = self.app.builder.get_object("MenuItemSettings")
        settings.connect("activate", self.SettingsSelected)

        ringtone  = self.app.builder.get_object("MenuItemRingtone")
        ringtone.connect("activate", self.RingtoneSelected)

        share  = self.app.builder.get_object("MenuItemShare")
        share.connect("activate", self.SendTextSelected)

        sms  = self.app.builder.get_object("MenuItemSms")
        sms.connect("activate", self.SmsSelected)
        clear = self.app.builder.get_object("MenuItemClearAll")
        clear.connect("activate", self.Clear_all_notifications)
        
        #.connect("popup-menu", self.OnShowPopupMenu)
        #window = Gtk.Window()
    def QuitSelected(self, widget):
        print("Quit")
        self.app.quit()
    def SettingsSelected(self, widget):
        print("Settings")
        self.app.show_settings_window();
    def SmsSelected(self, widget):
        print("Sms")
        self.app.show_sms_window();
    def RingtoneSelected(self, widget):
        print("Ringtone")
        self.app.play_ringtone();
    def SendTextSelected(self, widget):
        print("Send")
        self.app.show_send_window();

    def Clear_all_notifications(self, widget):
        print("Clear All Notification")
        self.app.close_all_notifications();


    def right_click_event(self, widget, event, eventTime):
        self.menu.popup(None, None, None, None, event, eventTime)


class SettingsWindow:
    def __init__(self ,app):
        self.app = app
        self.window = app.builder.get_object("WindowwSettings")
        self.window.show_all()
        self.set_values_from_settings()
        self.connect_signals()
    @func_once
    def connect_signals(self):
        self.app.builder.get_object("ButtonSaveSettings").connect("clicked" ,self.save)
        self.window.connect('delete_event', self.on_close)
        

    def set_values_from_settings(self):
        settings = SettinsManager()
        email = settings.get("email" )
        passwd = settings.get("pass" )
        url = settings.get("url" )
        self.app.builder.get_object("InputEmail").set_text(email)
        self.app.builder.get_object("InputPassword").set_text(passwd)
        self.app.builder.get_object("InputServerUrl").set_text(url)

    def on_close(self , widget, event):
        self.window.hide()
        return True
    def save(self , event):
        email  = self.app.builder.get_object("InputEmail").get_text()
        passwd  = self.app.builder.get_object("InputPassword").get_text()
        url  = self.app.builder.get_object("InputServerUrl").get_text()
        settings = SettinsManager()
        settings.set("email" ,email)
        settings.set("pass" ,passwd)
        settings.set("url" ,url)
        settings.save()
        
        self.app.reset_connectivity()
        
        self.window.hide()



class NotificatonFactory:
  title = "Title"
  body = "content"
  type ="information"

  def __init__(self):
    self.init_notifications()
    self.list = []
    def on_notification_closed(notification):
      self.list.remove(notification)
    self.on_notification_closed = on_notification_closed
  def CreateNotification(self, title, body ,icon):
    notification = Notify.Notification.new(title, body , icon)
    notification.id = randint(0, 9999999) 
    notification.set_timeout(Notify.EXPIRES_NEVER)
    self.list.append(notification)
    notification.connect('closed', self.on_notification_closed)
    return notification

  def close_all(self):
      for item in self.list:
          item.close()
  def CreateInfo(self , title , body):
    icon = "dialog-info"
    return self.CreateNotification(title,body , icon)

  def CreateWarning(self , title , body):
    icon = "dialog-warning"
    return self.CreateNotification(title,body , icon)
  def CreateMobileNotification(self , title, body , icon=None):
    if(icon == None):
      icon = "file:///home/michal/Project/PyGtkBlackBullet/resources/GladeFiles/icons/128x128/phone.png"
    return self.CreateNotification(title,body , icon)
  @func_once
  def init_notifications(self):
    Notify.init("BlackBulletApp")
