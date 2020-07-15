import datetime
import sqlite3 as sql

from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

from src.config import msg_balance, msg_objective

message_balance = msg_balance
message_objective = msg_objective


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


def sum_total_saving():  # todo refactor
    total_money = 0
    for i in db.get_history():
        total_money += i[1]
    return total_money


def valid_user_input(user_input):
    validation_bool = True
    if user_input == '' or float(user_input) < 0:
        validation_bool = False
    elif float(user_input) >= 1 and user_input[0] == '0':
        validation_bool = False
    elif 0 < float(user_input) < 1 and user_input[:2] == '00':
        validation_bool = False
    return validation_bool


class Root(BoxLayout):
    pass


class MainScene(Screen):
    total_saving = ObjectProperty(None)
    store = ObjectProperty(None)
    balance = ObjectProperty(None)

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
            self.store.text = message_objective + str(store_objective)
            self.total_saving.max = store_objective

        except TypeError:
            self.store.text = message_objective + '0'
            print("no data")

    def show_total_saving(self):  # todo refactor
        if sum_total_saving() > 0:
            self.balance.text = message_balance + str(sum_total_saving())
            self.total_saving.value = sum_total_saving()
        else:
            self.balance.text = message_balance + str(sum_total_saving())
            self.total_saving.value = 0


some = None


class HistoryScene(Screen):
    deposit = ObjectProperty(None)
    scroll = ObjectProperty(None)

    def on_pre_enter(self, *args):  # todo consider using on_enter instead.
        global some
        some = self.scroll
        self.binder()
        self.show_lists()

    def on_pre_leave(self, *args):  # todo consider using on_leave instead.
        self.clean_lists()

    def binder(self):  # todo rename
        self.deposit.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )

    def set_error_message(self, instance_textfield):  # todo refactor
        if valid_user_input(self.deposit.text):
            self.deposit.error = False
        else:
            self.deposit.error = True

    def update_history(self):
        try:
            if valid_user_input(self.deposit.text):  # todo refactor
                db.insert_history(self.deposit.text, datetime.date.today())
                self.deposit.text = ''
                self.manager.screens[0].total_saving.value = sum_total_saving()
                self.manager.screens[0].balance.text = message_balance + str(sum_total_saving())
                print('saved successfully')
            else:
                self.deposit.text = ''
                self.deposit.error = True
        except ValueError:
            print('ValueError')  # todo delete later

    def show_lists(self):  # todo rename
        for i in range(10):
            self.scroll.add_widget(
                ListItemWithCheckbox(text=f"Single-line item {i}")
            )

    def clean_lists(self):  # todo rename
        self.scroll.clear_widgets(self.children[:])


def clear_lists():
    global some
    some.clear_widgets(some.children[:])


def register_lists():
    for i in range(3):
        global some
        some.add_widget(
            ListItemWithCheckbox(text=f"Single-line item {i}")
        )


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    """Custom list item."""
    disabled = True
    icon = StringProperty('delete')

    def delete_lists(self):
        clear_lists()
        register_lists()


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Custom right container."""


class SettingScene(Screen):
    objective = ObjectProperty(None)
    dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.dialog = MDDialog(
            text="Restore all progress?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.dismiss_dialog
                ),
                MDFlatButton(
                    text="DISCARD",
                    on_release=self.reset
                ),
            ],
        )
        Clock.schedule_once(self.binder, 0)

    def binder(self, dt):  # todo rename
        self.objective.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )

    def set_error_message(self, instance_textfield):  # todo refactor
        if valid_user_input(self.objective.text):
            self.objective.error = False
        else:
            self.objective.error = True

    def submit_objective(self):
        try:
            if valid_user_input(self.objective.text):  # todo test this condition.
                db.insert_objective(self.objective.text)
                self.manager.screens[0].store.text = message_objective + self.objective.text
                self.manager.screens[0].total_saving.max = float(self.objective.text)
                self.objective.text = ""
            else:
                print("something went wrong.")
        except ValueError:
            print('set objective plz')

    def reset(self, *args):
        db.reset_tables()
        self.objective.text = ''
        self.manager.screens[0].store.text = message_objective + '0'
        self.manager.screens[0].balance.text = message_balance + '0'
        self.manager.screens[0].total_saving.value = 0
        self.dismiss_dialog()

    def show_alert_dialog(self):
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()


db_file = 'user_data.db'
db = DataBase(db_file)
db.create_new_tables()


class MyApp(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        self.theme_cls.theme_style = "Light"
        super().__init__(**kwargs)

    def toggle_theme(self, switch, value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


if __name__ == '__main__':
    MyApp().run()
