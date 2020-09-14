from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from app import db
from src.common.utilities import valid_user_input
from src.common.config import msg_objective, msg_balance


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
        self.manager.screens[0].store.text = msg_objective + '0'
        self.manager.screens[0].balance.text = msg_balance + '0'
        self.manager.screens[0].total_saving.value = 0
        self.manager.screens[0].total_saving.max = 0
        self.dismiss_dialog()

    def show_alert_dialog(self):
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()