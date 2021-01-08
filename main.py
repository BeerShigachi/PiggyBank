from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.factory import Factory
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.list import ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.clock import Clock

from src.common.config import msg_balance, INIT_CONFIG
from src.common.utilities import sum_total_saving
from db.data_base import db
import json

Window.keyboard_anim_args = {'d': 0.2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

Factory.register('MainScene', module='src.main_scene')
Factory.register('HistoryScene', module='src.history_scene')
Factory.register('SettingScene', module='src.setting_scene')
Factory.register('DepositSheet', module='src.deposit_sheet')

db.create_new_tables()


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Do not move the class to another file. IleftBodyTouch has a known issue."""


class Root(BoxLayout):
    """Root Widget"""
    label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.display_balance_bar, 0)
        Clock.schedule_once(self.set_label_font_size)

    def display_balance_bar(self, dt=0):
        self.label.title = msg_balance + str(sum_total_saving())

    def set_label_font_size(self, *args):
        self.ids.label.ids.label_title.font_size = '30sp'


class MyApp(MDApp):
    dialog = None
    deposit_sheet = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            with open('theme_config.json', 'r') as f:
                self._store = json.load(f)
        except FileNotFoundError:
            with open('theme_config.json', 'w') as f:
                json.dump(INIT_CONFIG, f)
                self._store = INIT_CONFIG
        self._theme_config = self._store['theme']

    def change_screen(self, screen_name, direction='left'):
        screen_manager = self.root.ids['screen_manager']
        if screen_name == 'History' and screen_manager.current == 'Setting':
            direction = 'right'
        screen_manager.transition.direction = direction
        screen_manager.current = screen_name

    def show_deposit_sheet(self):
        print(self.theme_cls.primary_palette, self.theme_cls.primary_hue, self.theme_cls.accent_palette,
              self.theme_cls.accent_hue)
        self.deposit_sheet = MDCustomBottomSheet(screen=Factory.DepositSheet())
        self.deposit_sheet.open()

    def build(self):
        pass

    def on_start(self):
        # todo set currency
        # todo refactor
        print('read from _theme_config')
        self.theme_cls.theme_style = self._theme_config['style']
        self.theme_cls.primary_palette = self._theme_config['primary_palette']
        self.theme_cls.accent_palette = self._theme_config['accent_palette']

    def on_pause(self):
        # todo refactor
        for key, value in zip(['style', 'primary_palette', 'accent_palette'],
                              [self.theme_cls.theme_style, self.theme_cls.primary_palette,
                               self.theme_cls.accent_palette]):
            self._theme_config[key] = value
        with open('theme_config.json', 'w') as f:
            json.dump(self._store, f)
        print('pausing app')


if __name__ == '__main__':
    MyApp().run()
