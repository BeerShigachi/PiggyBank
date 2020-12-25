import datetime
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCardSwipe
from db.data_base import db


class HistoryScene(Screen):
    scroll = ObjectProperty(None)
    estimation_bar = ObjectProperty(None)
    estimation_text = ObjectProperty(None)
    term_text = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.show_history()
        self.show_term()

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

    def show_term(self):
        term_info = db.get_term()[0]
        if self._error(term_info[-1]) == 0:
            self.term_text.text = 'Last month!'  # todo make this constant
        else:
            self.term_text.text = str(self._error(term_info[-1])) + "months left!"  # todo make this constant
        self.estimate_deposit_pace(term_info[1])

    def _error(self, date_iso):
        _today = datetime.date.today()  # todo put this in const.py
        return int(_today.isoformat()[5:7]) - int(date_iso[5:7])

    def estimate_deposit_pace(self, term=1):
        """
        :param term: int term of months(or weeks)
        :return: void
        """
        if db.get_objective() is not None:
            goal = db.get_objective()[1]
        else:
            goal = 0

        history = db.get_all_history_logs()
        sum_saving_this_month = 0
        _max_days_in_month = 31
        for i, j, k in history:
            delta = datetime.date.today() - datetime.date.fromisoformat(k)
            if delta.days <= _max_days_in_month and self._error(k) == 0:
                sum_saving_this_month += j
                print(sum_saving_this_month)

        ideal_welfare = round(goal / term, 2)
        real_welfare = round(sum_saving_this_month, 2)
        self.estimation_bar.max = ideal_welfare
        self.estimation_bar.value = real_welfare
        self.estimation_text.text = str(real_welfare) + '/' + str(ideal_welfare)


class ListItemWithCheckbox(MDCardSwipe):
    """Custom list item."""
    text = StringProperty()
    id = NumericProperty(None)
