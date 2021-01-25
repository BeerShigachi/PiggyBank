from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
import os

os.environ["KIVY_IMAGE"]="pil"

class MainScene(Screen):
    gif = ObjectProperty(None)

    def set_icon_size_pos(self):
        self.gif.anim_delay = 0.05
        self.gif._coreimage.anim_reset(True)
