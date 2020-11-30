import datetime

from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from main import db
from src.common.utilities import valid_user_input


class DepositSheet(BoxLayout):
    deposit = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.binder()

    def binder(self):  # todo rename
        print('binded')
        self.deposit.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )

    def set_error_message(self, instance_textfield):
        if valid_user_input(self.deposit.text):
            self.deposit.error = False
        else:
            self.deposit.error = True

    def update_history(self, false=None):
        print('in update history deposit_sheet.py')
        if valid_user_input(self.deposit.text):
            db.insert_history_log(self.deposit.text, datetime.date.today())
            self.deposit.text = ''
        else:
            print('invalid data')
            self.deposit.text = ''
            self.deposit.error = True
