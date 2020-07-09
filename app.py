import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import sqlite3 as sql
import os.path
import datetime
from kivymd.app import MDApp



class DataBase:
    def __init__(self, db_name):
        self.conn = sql.connect(db_name)
        self.cur = self.conn.cursor()

    def create_new_tables(self):
        with self.conn:
            self.cur.execute(""" CREATE TABLE  IF NOT EXISTS history (
                                id INTEGER PRIMARY KEY NOT NULL,
                                deposit INTEGER NOT NULL,
                                date timestamp
                                )
                                """)

        with self.conn:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS objective(
                                id INTEGER PRIMARY KEY NOT NULL,
                                objective INTEGER NOT NULL
                                )""")

    def insert_objective(self, obj):
        with self.conn:
            self.cur.execute(""" INSERT OR REPLACE INTO objective(id, objective) VALUES (?, ?)""", (1, float(obj)))

    def get_objective(self):
        self.cur.execute("""SELECT * FROM objective WHERE objective""")
        return self.cur.fetchone()

    def insert_history(self, deposit, date):
        with self.conn:
            self.cur.execute(""" INSERT OR REPLACE INTO history(deposit, date) VALUES (?, ?)""", (float(deposit), date))

    def get_history(self):
        self.cur.execute("""SELECT * FROM history""")
        return self.cur.fetchall()

    def reset_tables(self):
        with self.conn:
            self.cur.execute("""DELETE FROM objective""")
            self.cur.execute("""DELETE FROM history""")


class Root(BoxLayout):

    pass


class MainScene(Screen):
    total_saving = ObjectProperty(None)
    store = ObjectProperty(None)

    def __init__(self, **kw):
        super(MainScene, self).__init__(**kw)
        Clock.schedule_once(self.display_data, 0)

    def display_data(self, dt):
        self.manager.current = 'main'
        self.show_objective()
        self.show_total_saving()

    def show_objective(self):  # todo refactor
        try:
            store_objective = db.get_objective()[1]
            print(store_objective)
            self.store.text = str(store_objective)

        except TypeError:
            self.store.text = '$ 0'
            print("no data")

    def show_total_saving(self):  # todo refactor
        if sum_total_saving() > 0:
            self.total_saving.text = str(sum_total_saving())
        else:
            self.total_saving.text = '$ 0'


def sum_total_saving():  # todo refactor
    total_money = 0
    for i in db.get_history():
        total_money += i[1]
    return total_money


class HistoryScene(Screen):
    deposit = ObjectProperty(None)

    def __init__(self, **kw):
        super(HistoryScene, self).__init__(**kw)
        Clock.schedule_once(self.bind_d, 0)

    def validation(self):
        validation = False
        if len(self.deposit.text) > 1 and self.deposit.text[:2] == '00':
            validation = True
        elif self.deposit.text != '' and float(self.deposit.text) < 0:
            validation = True
        return validation

    def bind_d(self, dt):  # todo rename
        self.deposit.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )

    def set_error_message(self, instance_textfield):  # todo refactor
        if self.validation():
            self.deposit.error = True
        else:
            self.deposit.error = False

    def update_history(self):
        try:
            if not self.validation() and self.deposit.text != '':  # todo refactor
                db.insert_history(self.deposit.text, datetime.date.today())
                self.deposit.text = ''
                self.manager.screens[0].total_saving.text = str(sum_total_saving())
                print('saved successfully')
            else:
                self.deposit.text = ''
                self.deposit.error = True
        except ValueError:
            print('no empty')


class SettingScene(Screen):
    objective = ObjectProperty(None)

    def submit_objective(self):
        try:
            if len(self.objective.text) > 0:  # todo test this condition.

                db.insert_objective(self.objective.text)
                self.manager.screens[0].store.text = self.objective.text
                self.objective.text = ""
            else:
                print("something went wrong.")
        except ValueError:
            print('set objective plz')

    def reset(self):
        db.reset_tables()
        self.objective.text = 'set objective'
        self.manager.screens[0].store.text = '$ 0'
        self.manager.screens[0].total_saving.text = '$ 0'


db_file = 'user_data.db'
db = DataBase(db_file)
db.create_new_tables()



class MyApp(MDApp):
    def __init__(self, **kwargs):
        self.theme_cls.theme_style = "Dark"
        super().__init__(**kwargs)

MyApp().run()
