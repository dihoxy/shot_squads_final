
from kivy.app import App  # base for creating Kivy applications. This is the main entry point into
# the Kivy run loop. Create a subclass that inherits from 'App' and then create an instance of that subclass.
# Call the subclass' 'App.run()' method when launching app
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
import psycopg2
import datetime

# TODO: CONVERT TO KIVY MD (MATERIAL DESIGN)
"""
Filename: new_login.py
Related Files: shot.kv
Description: Basic UI that takes accepts Patient Inbox and a basic patient search query. Connects to PostgreSQL server
TO-DO:
-Needs to accept multiple events
-Needs to display all occurrences of a name in the db that is queried (e.g., search "Tony"; 
returns Tony Barge, and Tony Smith)
-Switch from Gridlayout to FloatLayout to create a more intuitive design
-Explore using KivyMD to recreate applicaiton
-Create more interfaces for business processes (i.e., creating appointments, billing, inventory, etc.)
"""

# instantiating the connection variable
con = psycopg2.connect(
    host='localhost',
    database="shot_squads_3",
    user="postgres",
    password='wiewes88*')

# create the cursor object
cur = con.cursor()


class MainWindow(Screen):  # pass in Screen as the parent class
    pass


# Enter New Patient Info
class SecondWindow(Screen):
    # References corresponding objects in the kv file
    pt_ssn = ObjectProperty(None)
    pt_fname = ObjectProperty(None)
    pt_lname = ObjectProperty(None)
    pt_dob = ObjectProperty(None)
    pt_st_add = ObjectProperty(None)
    pt_zipcode = ObjectProperty(None)
    pt_phone = ObjectProperty(None)
    pt_email = ObjectProperty(None)
    policy_holder = ObjectProperty(None)

    # Reference 'root.btn()' in KV file
    def btn(self):
        # call self because it is a method within the 'SecondWindow' class
        ssn = self.pt_ssn.text
        f_name = self.pt_fname.text
        l_name = self.pt_lname.text
        dob = datetime.datetime.strptime(self.pt_dob.text, "%m/%d/%y")  # converts the string object into a date object
        # using the datetime.datetime module's 'strptime' (converts a string into a date object)
        st_add = self.pt_st_add.text
        zip_code = self.pt_zipcode.text
        phone_num = self.pt_phone.text
        email = self.pt_email.text
        policy_holder = self.policy_holder.text
        cur.execute(
            "INSERT INTO shot_squads_3.public.\"PATIENT\"(\"PT_SSN\",\"PT_FNAME\", \"PT_LNAME\", \"PT_DOB\", \"PT_ST_ADDRESS\", \"PT_ZIPCODE\",\"PT_PHONE_NUMBER\",\"PT_EMAIL\", \"POLICY_HOLDER_SSN\") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (ssn, f_name, l_name, dob, st_add, zip_code, phone_num, email, policy_holder))
        # commit the entry to the db
        # TODO: Instance only allows one event before closing the connection. Needs to accept multiple
        con.commit()

        # Clearing text forms upon submission of the entry
        self.pt_ssn.text = ""
        self.pt_fname.text = ""
        self.pt_lname.text = ""
        self.pt_dob.text = ""
        self.pt_st_add.text = ""
        self.pt_zipcode.text = ""
        self.pt_phone.text = ""
        self.pt_email.text = ""
        self.pt_email.text = ""
        self.policy_holder.text = ""
        # close the cursor object and the connection (best practice)


# Search Patient Window
class ThirdWindow(Screen):
    pt_fir_name: ObjectProperty(None)
    pt_output: ObjectProperty(None)

    def btn_2(self):
        pt_info = self.pt_fir_name.text
        cur.execute(
            "SELECT \"PT_FNAME\", \"PT_LNAME\" FROM shot_squads_3.public.\"PATIENT\" WHERE \"PT_FNAME\" = (%s);",
            (pt_info,))  # for some reason, these types of queries must be structured as a tuple even if there
        # is only one item in the tuple
        patients = cur.fetchall()
        # generates an array of tuples

        # TODO: Loop needs to return each iteration of patient name typed in the search bar
        for row in patients:
            self.ids.pt_output.text = f"{row[1]}, {row[0]}"
        con.commit()


# Querying Patient name and Policy holder name
class FourthWindow(Screen):
    pt_id = ObjectProperty(None)
    pt_display = ObjectProperty(None)

    def btn_3(self):
        patient_id = self.pt_id.text
        cur.execute(
            "SELECT \"PT_LNAME\", \"PT_FNAME\", \"POLICY_HOLDER_LNAME\", \"POLICY_HOLDER_FNAME\",\"POLICY_HOLDER\".\"POLICY_HOLDER_SSN\" FROM shot_squads_3.public.\"PATIENT\" "
            "INNER JOIN shot_squads_3.public.\"POLICY_HOLDER\" ON shot_squads_3.public.\"PATIENT\".\"POLICY_HOLDER_SSN\" "
            "= shot_squads_3.public.\"POLICY_HOLDER\".\"POLICY_HOLDER_SSN\" WHERE \"PT_SSN\" = (%s);", (patient_id,))

        info = cur.fetchall()
        try:
            self.ids.pt_display.text = f"Patient Name: {info[0][0]}, {info[0][1]}  \nPolicy Holder Name: {info[0][2]}, " \
                                       f"{info[0][3]} SSN: {info[0][4]}"
        except IndexError:
            self.ids.pt_display.text = f"{patient_id} is not associated with a record in the database"


class FifthWindow(Screen):
    pass


class WindowManager(ScreenManager):  # acts as screenmanager for all screens
    pass


kv = Builder.load_file("shot.kv")


class ShotApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    ShotApp().run()
    cur.close()
    con.close()