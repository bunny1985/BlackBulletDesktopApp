import configparser
from pathlib import Path


def func_once(func):
    "A decorator that runs a function only once."
    def decorated(*args, **kwargs):
        try:
            return decorated._once_result
        except AttributeError:
            decorated._once_result = func(*args, **kwargs)
            return decorated._once_result
    return decorated


class Config:
    user_name = ""
    password = ""
    address = ""


class SettinsManager:
    def __init__(self):
        SettinsManager.filename = str(Path.home()) + "/.blackbullet.conf"
        SettinsManager.category = "DEFAULT"

        self.config = configparser.ConfigParser()
        self.config.read(SettinsManager.filename)
    def get_config_as_object(self):
        config = Config()
        config.user_name = self.get("email")
        config.password = self.get("pass")
        config.address = self.get("url" ,"blackbulletapp.ovh" )
        return config
    def get(self, key , default = ""):
        try:
            return self.config[SettinsManager.category][key]
        except:
            return default;

    def set(self, key , value):
        self.config[SettinsManager.category][key] = value
    def save(self):
        with open(SettinsManager.filename, 'w+') as configfile:    # save
            self.config.write(configfile)