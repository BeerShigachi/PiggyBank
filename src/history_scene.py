import datetime

from kivy.core.text import Label
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCardSwipe
from db.data_base import db
from src.common.const import TODAY
from src.common.circular_bar import CircularProgressBar  # do not delete this line. using it in .kv

_DEFAULT_LABEL = '{}%'


class HistoryScene(Screen):
    scroll = ObjectProperty(None)
    estimation_bar = ObjectProperty(None)
    estimation_text = ObjectProperty(None)
    term_text = ObjectProperty(None)
    term_bar = ObjectProperty(None)
    _label = Label(text=_DEFAULT_LABEL, font_size=40, color=(0, 0, 0, 1))

    def on_pre_enter(self, *args):
        self.show_history()
        self.show_term()

    def show_history(self):  # todo rename
        self.scroll.clear_widgets(self.scroll.children[:])
        for i in db.get_all_history_logs():
            row_date = i[2]
            date = datetime.date.fromisoformat(row_date)

            self.scroll.add_widget(
                ListItemWithCheckbox(text=f"${i[1]}, " + date.strftime("%A %d. %B %Y"), id=i[0])
            )

    def delete_history_log(self, widget):
        """Delete each history"""
        db.erase_history_log(widget.id)
        self.show_history()
        self.show_term()

    def show_term(self):
        info = db.get_term()
        if not info:
            return
        term_info = info[0]
        deadline = datetime.date.fromisoformat(term_info[-1])
        if TODAY <= deadline:
            error = (deadline.year - TODAY.year) * 12 + (deadline.month - TODAY.month)
            if error == 1:
                self.term_text.text = "LAST MONTH"  # todo make this constant
            else:
                self.term_text.text = str(error) + " months left"  # todo make this constant

            self.term_bar.max = term_info[1]
            self.term_bar.value = term_info[1] - error

            self._estimate_deposit_pace(term_info[1])

    def _format_data_iso(self, date_iso):
        return int(date_iso[5:7])

    def _error(self, date_iso):
        return self._format_data_iso(TODAY.isoformat()) - self._format_data_iso(date_iso)

    def _estimate_deposit_pace(self, term=1):
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
            delta = TODAY - datetime.date.fromisoformat(k)
            if delta.days <= _max_days_in_month and self._error(k) == 0:
                sum_saving_this_month += j

        ideal_welfare = round(goal / term, 2)
        real_welfare = round(sum_saving_this_month, 2)
        if real_welfare >= ideal_welfare:
            self.estimation_bar.value = self.estimation_bar.max
        else:
            self.estimation_bar.value = int((real_welfare / ideal_welfare) * 100)

        # self.estimation_bar.draw()
        self.estimation_text.text = "${}/${}".format(real_welfare, ideal_welfare)


class ListItemWithCheckbox(MDCardSwipe):
    """Custom list item."""
    text = StringProperty()
    id = NumericProperty(None)
