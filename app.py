import datetime
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

from src.data_base import DataBase
from src.config import msg_balance, msg_objective

message_balance = msg_balance
message_objective = msg_objective

db_file = 'user_data.db'
db = DataBase(db_file)
db.create_new_tables()


def sum_total_saving():
    total_money = 0
    for i in db.get_all_history_logs():
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

    def show_objective(self):
        try:
            store_objective = db.get_objective()[1]
            self.store.text = message_objective + str(store_objective)
            self.total_saving.max = store_objective
            self.total_saving.value = sum_total_saving()

        except TypeError:
            self.store.text = message_objective + '0'
            print("no data")

    def show_total_saving(self):
        if sum_total_saving() > 0:
            self.balance.text = message_balance + str(sum_total_saving())
            self.total_saving.value = sum_total_saving()
        else:
            self.balance.text = message_balance + str(sum_total_saving())
            self.total_saving.value = 0


class HistoryScene(Screen):
    deposit = ObjectProperty(None)
    scroll = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.binder()
        self.show_history()

    def binder(self):  # todo rename
        self.deposit.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )

    def set_error_message(self, instance_textfield):
        if valid_user_input(self.deposit.text):
            self.deposit.error = False
        else:
            self.deposit.error = True

    def update_history(self):
        if valid_user_input(self.deposit.text):
            db.insert_history_log(self.deposit.text, datetime.date.today())
            self.deposit.text = ''
            self.manager.screens[0].show_total_saving()
            self.show_history()
        else:
            self.deposit.text = ''
            self.deposit.error = True

    def show_history(self):  # todo rename
        self.scroll.clear_widgets(self.scroll.children[:])
        for i in db.get_all_history_logs():
            self.scroll.add_widget(
                ListItemWithCheckbox(text=f"${i[1]}, date {i[2]}", id=i[0])
            )

    def delete_history_log(self, widget):
        """Delete each history"""
        db.erase_history_log(widget.id)
        self.show_history()
        self.manager.screens[0].show_total_saving()


class ListItemWithCheckbox(OneLineAvatarIconListItem):
    """Custom list item."""
    disabled = True
    icon = StringProperty('delete')
    id = NumericProperty(None)


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Custom right container."""


class SettingScene(Screen):
    objective = ObjectProperty(None)
    dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.dialog = MDDialog(
            size_hint=(.5, None),
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
        if valid_user_input(self.objective.text):  # todo test this condition.
            db.insert_objective(self.objective.text)
            self.manager.screens[0].show_objective()
            self.objective.text = ""
        else:
            print("something went wrong.")

    def reset(self, *args):
        db.erase_all_tables()
        self.objective.text = ''
        self.manager.screens[0].store.text = message_objective + '0'
        self.manager.screens[0].balance.text = message_balance + '0'
        self.manager.screens[0].total_saving.value = 0
        self.manager.screens[0].total_saving.max = 0
        self.dismiss_dialog()

    def show_alert_dialog(self):
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()


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
