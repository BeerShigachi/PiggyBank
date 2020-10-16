import datetime

from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCardSwipe

from main import db
from src.common.utilities import valid_user_input


class HistoryScene(Screen):
    deposit = ObjectProperty(None)
    scroll = ObjectProperty(None)

    def enter(self, *args):
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


class ListItemWithCheckbox(MDCardSwipe):
    """Custom list item."""
    text = StringProperty()
    id = NumericProperty(None)
