import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import sqlite3 as sql
import os.path


class DataBase:
    def __init__(self, db_name):
        self.conn = sql.connect(db_name)
        self.cur = self.conn.cursor()

    def create_new_table(self):
        with self.conn:
            self.cur.execute(""" CREATE TABLE  IF NOT EXISTS user (
                                id integer primary key,
                                objective integer,
                                budget integer
                                )
                                """)

    def insert_objective(self, obj):
        with self.conn:
            self.cur.execute(""" INSERT OR REPLACE INTO user(objective) VALUES (?)""", (int(obj),))

    def get_objective(self):
        self.cur.execute("""SELECT * FROM user WHERE objective""")
        return self.cur.fetchall()



class MainScreen(FloatLayout):
    objective = ObjectProperty(None)
    budget = ObjectProperty(None)
    store = ObjectProperty(None)

    def submit_objective(self):
        self.store.text = "$" + self.objective.text  # todo delete later after implement READ from db

        if len(self.objective.text) > 0:  # todo test this condition.
            db.insert_objective(self.objective.text)
            self.objective.text = ""
            print(db.get_objective())
        else:
            print("something went wrong.")


class MyApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    db_file = 'user_data.db'
    db = DataBase(db_file)
    db.create_new_table()
    MyApp().run()
