import datetime
import functools

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from db.data_base import db
from src.common.utilities import valid_user_input, last_day_of_month

_CALLERS = {'deposit': {'title': 'DEPOSIT', 'input_filter': 'float', 'hint_text': 'Enter amount'},
            'goal': {'title': 'GOAL', 'input_filter': 'float', 'hint_text': 'Enter amount'},
            'deadline': {'title': 'TIME LIMIT', 'input_filter': 'int', 'hint_text': 'months'}}


class PopUpScreen(BoxLayout):
    title = ObjectProperty(None)
    app = App.get_running_app()


class ThemeColorPicker(PopUpScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title.title = 'Theme Color'

    def _dismiss_sheet(self):
        self.app.root.ids['setting'].popup.dismiss()

class PopUpInputField(PopUpScreen):
    text_field = ObjectProperty(None)
    button = ObjectProperty(None)


    def __init__(self, caller, **kwargs):
        super().__init__(**kwargs)
        self.caller = caller
        self.target = _CALLERS[self.caller]
        self.title.title = self.target['title']
        self.text_field.input_filter = self.target['input_filter']
        self.text_field.hint_text = self.target['hint_text']

        self._binder()

    def _text_field_validator(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            self.text_field.error = False
            if valid_user_input(self.text_field.text):
                func(self, *args, **kwargs)
            else:
                self.text_field.error = True

        return inner

    def _binder(self):  # todo rename
        self.text_field.bind(
            on_text_validate=self._dummy_error_toggler,
            on_focus=self._dummy_error_toggler,
        )

    @_text_field_validator
    def _dummy_error_toggler(self, instance_textfield):  # hey it is not typo. dummy.
        pass

    @_text_field_validator
    def store_input_data(self, false=None):
        if self.caller == 'deposit':
            db.insert_history_log(self.text_field.text, datetime.date.today())
            self.app.root.ids['home'].refresh_screen()
            self.app.root.ids['history'].show_history()
            self.app.root.ids['history'].show_term()

        elif self.caller == 'deadline':
            # todo refactor
            deadline_months = datetime.date.today().month + int(self.text_field.text) - 1
            num_month = deadline_months % 12 + 1
            try:
                deadline = datetime.date(datetime.date.today().year + deadline_months // 12, num_month,
                                         datetime.date.today().day)
            except ValueError:
                deadline = last_day_of_month(
                    datetime.date(datetime.date.today().year + deadline_months // 12, num_month, 1))
            db.insert_term(self.text_field.text, deadline)

        elif self.caller == 'goal':
            db.insert_objective(self.text_field.text)
            self.app.root.ids['setting'].show_objective()

        self.text_field.text = ''
