import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDThemePicker

from db.data_base import db
from src.common.utilities import valid_user_input, get_goal, last_day_of_month
from src.common.config import msg_objective


class SettingScene(Screen):
    objective = ObjectProperty(None)
    dialog = None
    app = App.get_running_app()
    store = ObjectProperty(None)
    term = ObjectProperty(None)
    button_term = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.dialog = MDDialog(
            auto_dismiss=False,
            size_hint=(.8, None),
            title="Reset all progress?",
            buttons=[
                MDRaisedButton(
                    text="CANCEL",
                    on_release=self.dismiss_dialog,
                    # md_bg_color=[1, 1, 1, 1]  # to change color
                ),
                MDRaisedButton(
                    text="RESET",
                    on_release=self.reset,
                    # md_bg_color=[1, 1, 1, 1]
                ),
            ],
        )
        Clock.schedule_once(self.binder, 0)
        Clock.schedule_once(self.display_data, 0)

    def display_data(self, dt):
        self.show_objective()

    def show_objective(self):
        self.store.text = msg_objective + str(get_goal())

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
            self.objective.text = ""
            self.show_objective()
        else:
            print("something went wrong.")

    def submit_term(self):
        if valid_user_input(self.term.text):
            deadline_months = datetime.date.today().month + int(self.term.text) - 1
            num_month = deadline_months % 12 + 1
            try:
                deadline = datetime.date(datetime.date.today().year + deadline_months // 12, num_month,
                                         datetime.date.today().day)
            except ValueError:
                deadline = last_day_of_month(
                    datetime.date(datetime.date.today().year + deadline_months // 12, num_month, 1))

            db.insert_term(self.term.text, deadline)
            self.term.text = ''

    def reset(self, *args):
        print('resetting')
        db.erase_all_tables()
        self.objective.text = ''  # todo delete here
        self.dismiss_dialog()
        self.show_objective()

    def show_alert_dialog(self):
        print(self.app.theme_cls.theme_style)
        if self.app.theme_cls.theme_style == 'Light':
            self.dialog.md_bg_color = [.9, .9, .9, 1]
        else:
            self.dialog.md_bg_color = [0.3, 0.3, 0.3, 1]
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()
