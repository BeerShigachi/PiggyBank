from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from db.data_base import db
from src.common.utilities import sum_total_saving
from src.common.config import dict_alpha


class MainScene(Screen):
    total_saving = ObjectProperty(None)
    store = ObjectProperty(None)
    balance = ObjectProperty(None)
    coin1 = ObjectProperty(None)
    coin2 = ObjectProperty(None)
    coin3 = ObjectProperty(None)
    coin4 = ObjectProperty(None)
    coin5 = ObjectProperty(None)
    coin6 = ObjectProperty(None)
    coin7 = ObjectProperty(None)
    coin8 = ObjectProperty(None)

    def __init__(self, **kw):
        super(MainScene, self).__init__(**kw)
        Clock.schedule_once(self.display_data, 0)

    def display_data(self, dt):
        self.manager.current = 'Main'
        self.set_icon_size_pos()

    def set_icon_size_pos(self):
        data = db.get_objective()
        res = dict_alpha[0]
        saving = sum_total_saving()
        if data is not None:
            b = saving / data[1]
            rate = 1 / (len(dict_alpha) - 1)
            key = ((b + rate / 2) // rate) * rate
            if key in dict_alpha:
                res = dict_alpha[key]
            elif float(saving) >= float(data[1]):
                res = dict_alpha[1]
        coins = [self.coin1, self.coin2, self.coin3, self.coin4, self.coin5, self.coin6, self.coin7, self.coin8]  # Add more coins when you have more
        for i, coin in enumerate(coins):
            coin.color = [.55, .55, .55, res[i]]
