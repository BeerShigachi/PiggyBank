from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.factory import Factory
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


class Root(BoxLayout):
    """Root Widget(Top Tool Bar)"""
    pass


class MyApp(MDApp):
    dialog = None

    def __init__(self, **kwargs):
        self.theme_cls.theme_style = "Light"
        super().__init__(**kwargs)

    def toggle_theme(self, switch, value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


if __name__ == '__main__':
    MyApp().run()
