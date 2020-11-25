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
        self.theme_cls.theme_style = db.get_config()[1]
        self.currency = db.get_config()[2]
        super().__init__(**kwargs)

    def change_screen(self, screen_name, direction='left'):
        screen_manager = self.root.ids['screen_manager']
        if screen_name == 'main' and screen_manager.current == 'setting':
            direction = 'right'
        screen_manager.transition.direction = direction
        screen_manager.current = screen_name

        db.set_config(self.theme_cls.theme_style, 'usd')  # todo define later


if __name__ == '__main__':
    MyApp().run()

