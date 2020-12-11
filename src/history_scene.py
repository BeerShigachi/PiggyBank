import datetime

from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import OneLineAvatarIconListItem

from main import db
from src.common.utilities import sum_total_saving


class HistoryScene(Screen):
    scroll = ObjectProperty(None)
    estimation_bar = ObjectProperty(None)
    estimation_text = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.show_history()
        self.process_estimation()

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

    def process_estimation(self, term=1):
        all_histories = db.get_all_history_logs()[::-1]
        print(all_histories, type(datetime.date.fromisoformat(all_histories[-1][-1])))
        # d1 = datetime.date(year=2012, month=10, day=12)
        goal = db.get_objective()[1]
        ideal_schedule = goal / term
        for i in all_histories:
            history = datetime.date.fromisoformat(i[-1])
            day_error = abs(datetime.date.today() - history)
            print(type(day_error.days), day_error.days)



class ListItemWithCheckbox(MDCardSwipe):
    """Custom list item."""
    text = StringProperty()
    id = NumericProperty(None)
