import datetime

from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder

from db.data_base import db
from src.common.utilities import sum_total_saving


class HistoryScene(Screen):
    scroll = ObjectProperty(None)
    estimation_bar = ObjectProperty(None)
    estimation_text = ObjectProperty(None)
    drop_item = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.show_history()
        # todo give self.estimate_deposit_pace the term(int).
        self.estimate_deposit_pace()

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

    def estimate_deposit_pace(self, term=1):
        self.screen = Builder.load_string
        menu_items = [{"text": f"Item {i}"} for i in range(5)]
        self.menu = MDDropdownMenu(
            caller=self.screen.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind(on_release=self.menu_callback)

    def menu_callback(self, instance_menu, instance_menu_item):
        print(instance_menu, instance_menu_item)

    def build(self):
        return self.screen
        """

        :param term: int term of months(or weeks)
        :return: void
        """
        if db.get_objective() is not None:
            goal = db.get_objective()[1]
        else:
            goal = 0
        ideal_welfare = goal / term
        real_welfare = sum_total_saving() / term
        self.estimation_bar.max = ideal_welfare
        self.estimation_bar.value = real_welfare
        self.estimation_text.text = str(real_welfare) + '/' + str(ideal_welfare)


class ListItemWithCheckbox(MDCardSwipe):
    """Custom list item."""
    text = StringProperty()
    id = NumericProperty(None)
