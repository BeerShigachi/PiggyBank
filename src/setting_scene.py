from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog

from main import db
from src.common.utilities import valid_user_input


class SettingScene(Screen):
    objective = ObjectProperty(None)
    dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.dialog = MDDialog(
            auto_dismiss=False,
            size_hint=(.8, None),
            text="Reset all progress?",
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
            self.manager.screens[0].show_total_saving()
            self.objective.text = ""
        else:
            print("something went wrong.")

    def reset(self, *args):
        print('resetting')
        db.erase_all_tables()
        print('reset complete.')
        self.objective.text = ''
        self.manager.screens[0].show_objective()
        self.manager.screens[0].show_total_saving()
        self.dismiss_dialog()

    def show_alert_dialog(self):
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()
