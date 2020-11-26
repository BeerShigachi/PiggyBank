from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.list import ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.picker import MDThemePicker

from db.data_base import DataBase
from src.common.const import DATABASE_FILENAME

Window.keyboard_anim_args = {'d': 0.2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

Factory.register('MainScene', module='src.main_scene')
Factory.register('HistoryScene', module='src.history_scene')
Factory.register('SettingScene', module='src.setting_scene')
Factory.register('DepositSheet', module='src.deposit_sheet')

db = DataBase(DATABASE_FILENAME)
db.create_new_tables()


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Do not move the class to another file. IleftBodyTouch has a known issue."""


class Root(BoxLayout):
    """Root Widget(Top Tool Bar)"""
    pass


class MyApp(MDApp):
    dialog = None
    deposit_sheet = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = db.get_config()[1]
        self.currency = db.get_config()[2]

    def toggle_theme(self, switch, value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"

        db.set_config(self.theme_cls.theme_style, 'usd')  # todo define later

    def change_screen(self, screen_name, direction='left'):
        screen_manager = self.root.ids['screen_manager']
        if screen_name == 'History' and screen_manager.current == 'Setting':
            direction = 'right'
        screen_manager.transition.direction = direction
        screen_manager.current = screen_name

    def show_deposit_sheet(self):
        self.deposit_sheet = MDCustomBottomSheet(screen=Factory.DepositSheet())
        self.deposit_sheet.open()

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()


if __name__ == '__main__':
    MyApp().run()
