from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.snackbar import Snackbar
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from config import *
import psycopg2 as psy
import datetime

Window.size = (450, 650)

con = psy.connect(
    host=f'{host}',
    database=f'{database}',
    user=f'{user}',
    password=f'{password}'
)

cur = con.cursor()


class LoginScreen(Screen):
    dialog = None

    # kivy objects
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    # Function that handles password check and navigation to main screen
    def btn(self):
        cur.execute(
            'SELECT "EMP_PASSWORD" FROM dao5ci75ci5u9b.public."LOGIN" WHERE "EMP_USERNAME" = (%s);',
            (self.username.text,))
        pw = cur.fetchall()
        if pw[0][0] == self.password.text:
            print("correct Password")
            return True


class MainScreen(Screen):
    pass


# class WindowManager(ScreenManager):
#     pass


# sm = ScreenManager()
# sm.add_widget(LoginScreen(name='login'))
# sm.add_widget(MainScreen(name='main'))


# class WindowManager(ScreenManager):
#     pass


class ShotmdApp(MDApp):
    # instantiating the dialog variable
    dialog = None

    def build(self):
        kv = Builder.load_file("shotMD.kv")  # this must be loaded in the 'App' class to prevent it from being loaded
        # before the main app has a chance to initialize (which returns a ValueError)

        return kv

    # incorrect password handling
    def incorrect(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text='Incorrect Password',
                buttons=[
                    MDFlatButton( # 'Retry' button
                        text='Retry'
                    ),
                ],

            )
        self.dialog.open()

    def test_function(self):
        print("This is a test")


if __name__ == '__main__':
    ShotmdApp().run()
    cur.close()
    con.close()
