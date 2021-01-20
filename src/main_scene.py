from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


class MainScene(Screen):
    gif = ObjectProperty(None)

    def __init__(self, **kw):
        super(MainScene, self).__init__(**kw)
        Clock.schedule_once(self.display_data, 0)

    def display_data(self, dt):
        self.manager.current = 'Home'

    def set_icon_size_pos(self):
        self.gif.anim_delay = 0.05
        self.gif._coreimage.anim_reset(True)
