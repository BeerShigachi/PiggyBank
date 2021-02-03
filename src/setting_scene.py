import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDThemePicker

from db.data_base import db
from src.common.utilities import get_goal
from src.common.config import msg_objective


class SettingScene(Screen):
    dialog = None
    app = App.get_running_app()
    store = ObjectProperty(None)

    popup = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.dialog = MDDialog(
            auto_dismiss=False,
            size_hint=(.8, None),
            title="Reset all progress?",
            buttons=[
                MDRaisedButton(
                    text="CANCEL",
                    on_release=self.dismiss_dialog,
                    # md_bg_color=[1, 1, 1, 1]  # to change color
                ),
                MDRaisedButton(
                    text="RESET",
                    on_release=self.reset,
                    # md_bg_color=[1, 1, 1, 1]
                ),
            ],
        )
        # Clock.schedule_once(self.binder, 0)
        Clock.schedule_once(self.show_objective, 0)


    def show_objective(self, dt=0):
        self.store.text = msg_objective + str(get_goal())
        print('done')




    def reset(self, *args):
        print('resetting')
        db.erase_all_tables()
        self.dismiss_dialog()
        self.show_objective()

    def show_alert_dialog(self):
        print(self.app.theme_cls.theme_style)
        if self.app.theme_cls.theme_style == 'Light':
            self.dialog.md_bg_color = [.9, .9, .9, 1]
        else:
            self.dialog.md_bg_color = [0.3, 0.3, 0.3, 1]
        self.dialog.open()

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    def _show_deadline_field(self):
        self.popup = MDCustomBottomSheet(screen=Factory.DepositSheet(caller='deadline'))
        self.popup.open()

    def _show_goal_field(self):
        self.popup = MDCustomBottomSheet(screen=Factory.DepositSheet(caller='goal'))
        self.popup.open()