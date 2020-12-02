from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from main import db
from src.common.utilities import sum_total_saving
from src.common.config import msg_objective, msg_balance
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
        print(self.coin2.color, "display_data")
        self.manager.current = 'Main'
        self.show_objective()
        self.show_total_saving()
        print(self.coin2.color, "display_data__")

    def show_objective(self):
        try:
            store_objective = db.get_objective()[1]
            self.store.text = msg_objective + str(store_objective)

        except TypeError:
            self.store.text = msg_objective + '0'
            print("no data")

    def show_total_saving(self):
        print(self.coin2.color, "show_total_saving")
        self.balance.text = msg_balance + str(sum_total_saving())
        self.set_icon_size_pos()
        print(self.coin2.color, "show_total_saving__")

    def set_icon_size_pos(self):
        data = db.get_objective()
        res = dict_alpha[0]
        saving = sum_total_saving()
        if data is not None:
            b = saving / data[1]
            rate = 1 / (len(dict_alpha) - 1)
            key = ((b + rate / 2) // rate) * rate
            print(key)
            if key in dict_alpha:
                res = dict_alpha[key]
            elif float(saving) >= float(data[1]):
                res = dict_alpha[1]
        print(res[1], "alpha", res)  # todo delete later.
        coins = [self.coin1, self.coin2, self.coin3, self.coin4, self.coin5, self.coin6, self.coin7, self.coin8]  # Add more coins when you have more
        for i, coin in enumerate(coins):
            print(i, coin)
            coin.color = [.6, .6, .6, res[i]]
