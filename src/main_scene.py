from kivy.app import App
from kivy.clock import Clock

from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from src.common.circular_bar import CircularProgressBar  # do not delete this line. using it in .kv
from src.common.utilities import sum_total_saving, get_goal

import os


_DEFAULT_LABEL = '{}%'

os.environ["KIVY_IMAGE"] = "pil"


class MainScene(Screen):
    gif = ObjectProperty(None)
    circular_bar = CircularProgressBar()
    _label = Label(text=_DEFAULT_LABEL, font_size=40, color=(0.2, 0.2, 0.2, 1))
    app = App.get_running_app()
    label = ObjectProperty(None)

    def on_enter(self, *args):
        Clock.schedule_once(self._draw_circular_bar, 0)
        Clock.schedule_once(self._set_saving_label, 0)

    def _set_saving_label(self, dt=0):
        self.label.text = "$ " + str(sum_total_saving())

    def refresh_screen(self):
        self._draw_circular_bar()
        self._set_saving_label()
        self._play_gif()

    def _draw_circular_bar(self, dt=0):

        self._set_color_circular_bar()
        self._set_param_circular_bar()
        self.circular_bar.draw()

    def _set_color_circular_bar(self):
        # todo adapt self.circular_bar.color from self.app.theme_cls.accent_color
        if self.app.theme_cls.theme_style == 'Light':
            self.circular_bar.background_colour = (0.26, 0.26, 0.26, 1)
            self._label.color = (0.1, 0.1, 0.1, 1)
        else:
            self.circular_bar.background_colour = (0.26, 0.26, 0.26, 1)  # todo change color
            self._label.color = (0.9, 0.9, 0.9, 1)

    def _set_param_circular_bar(self):
        goal = get_goal()
        saving = sum_total_saving()
        self.circular_bar.max = goal
        if goal >= saving:
            self.circular_bar.value = saving
        else:
            self.circular_bar.value = goal

    def _play_gif(self):
        self.gif.anim_delay = 0.01
        self.gif._coreimage.anim_reset(True)
