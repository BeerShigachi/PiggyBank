from kivymd.app import MDApp
from kivy.factory import Factory
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.list import ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

from db.data_base import DataBase
from src.common.const import DATABASE_FILENAME

Factory.register('MainScene', module='src.main_scene')
Factory.register('HistoryScene', module='src.history_scene')
Factory.register('SettingScene', module='src.setting_scene')

db = DataBase(DATABASE_FILENAME)
db.create_new_tables()


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Do not move the class to another file. IleftBodyTouch has a known issue."""


class Root(MDBottomNavigation):
    """Root Widget(Bottom Tool Bar)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change_screen(self, screen_name):
        screen_manager = self.ids['tab_manager']
        screen_manager.current = screen_name


class MyApp(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        # todo read theme_style setting from db.

        print(db.get_config(), 'here')
        self.theme_cls.theme_style = db.get_config()[1]
        self.currency = db.get_config()[2]
        super().__init__(**kwargs)

    def toggle_theme(self, switch, value):
        # todo store theme_style setting into db.
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
        print(switch.active)
        db.set_config(self.theme_cls.theme_style, 'usd')  # todo define later

    def select_currency(self, value):
        self.currency = value
        pass


if __name__ == '__main__':
    MyApp().run()
