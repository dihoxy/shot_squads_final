from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.snackbar import Snackbar
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from config import *
import psycopg2 as psy
import datetime

Window.size = (300, 500)

con = psy.connect(
    host=f'{host}',
    database=f'{database}',
    user=f'{user}',
    password=f'{password}'
)

cur = con.cursor()

class LoginScreen(Screen):
    pass

class MainScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class ShotmdApp(MDApp):
    def build(self):
        kv = Builder.load_file("shotMD.kv")  # this must be loaded in the 'App' class to prevent it from being loaded
        # before the main app has a chance to initialize (which returns a ValueError)
        return kv

    def test_function(self):
        print("This is a test")


if __name__ == '__main__':
    ShotmdApp().run()
