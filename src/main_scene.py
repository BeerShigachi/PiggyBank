from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from app import db
from src.common.utilities import sum_total_saving
from src.common.config import msg_objective, msg_balance
from src.common.config import piggy_size_max, piggy_size_min


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
            self.total_saving.max = store_objective  # todo delete. total_saving.value is not defined anymore
            self.total_saving.value = sum_total_saving()  # todo delete. total_saving.value is not defined anymore

        except TypeError:
            self.store.text = msg_objective + '0'
            print("no data")

    def show_total_saving(self):
        if sum_total_saving() > 0:
            self.balance.text = msg_balance + str(sum_total_saving())
            self.total_saving.value = sum_total_saving()  # todo delete. total_saving.value is not defined anymore
            self.total_saving.font_size = self._normalize_piggy_size()
        else:
            self.balance.text = msg_balance + str(sum_total_saving())
            self.total_saving.value = 0  # todo delete. total_saving.value is not defined anymore
            self.total_saving.font_size = piggy_size_min

    def _normalize_piggy_size(self):
        # todo normalize
        piggy_ratio = piggy_size_max - piggy_size_min
        a = sum_total_saving() / db.get_objective()[1]
        return piggy_ratio * a + piggy_size_min
