from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from main import db
from src.common.utilities import sum_total_saving
from src.common.config import msg_objective
from src.common.config import piggy_size


class MainScene(Screen):
    total_saving = ObjectProperty(None)
    store = ObjectProperty(None)
    balance = ObjectProperty(None)

    def __init__(self, **kw):
        super(MainScene, self).__init__(**kw)
        Clock.schedule_once(self.display_data, 0)

    def display_data(self, dt):
        self.manager.current = 'main'
        self.show_objective()
        self.show_total_saving()

    def show_objective(self):
        try:
            store_objective = db.get_objective()[1]
            self.store.text = msg_objective + str(store_objective)

        except TypeError:
            self.store.text = msg_objective + '0'
            print("no data")

    def show_total_saving(self):
        self.balance.text = str(sum_total_saving())
        self.set_icon_size_pos()

    def set_icon_size_pos(self):
        data = db.get_objective()
        res = piggy_size[0]
        saving = sum_total_saving()
        if data is not None:
            b = saving / data[1]
            rate = 1 / (len(piggy_size) - 1)
            key = ((b+rate/2)//rate)*rate
            print(key)
            if key in piggy_size:
                res = piggy_size[key]
        print(res)  # todo delete later.
        self.total_saving.font_size = res[0]
        self.total_saving.pos_hint = res[1]

