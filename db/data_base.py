import sqlite3 as sql
from src.common.config import init_style, init_currency
from src.common.const import DATABASE_FILENAME


class DataBase:
    def __init__(self, db_name):
        self.conn = sql.connect(db_name)
        self.cur = self.conn.cursor()

    def create_new_tables(self):
        with self.conn:
            self.cur.execute(""" CREATE TABLE  IF NOT EXISTS history (
                                id INTEGER PRIMARY KEY NOT NULL,
                                deposit INTEGER NOT NULL,
                                date timestamp
                                )
                                """)

        with self.conn:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS objective (
                                id INTEGER PRIMARY KEY NOT NULL,
                                objective INTEGER NOT NULL
                                )""")

        with self.conn:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS term (
                                id INTEGER PRIMARY KEY NOT NULL,
                                term INTEGER NOT NULL,
                                date timestamp
                                )""")

        with self.conn:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS config (
                                id INTEGER PRIMARY KEY NOT NULL,
                                theme_style TEXT NOT NULL,
                                currency TEXT NOT NULL
                                )""")
        if self.get_config() is None:
            self.set_config(init_style, init_currency)

    def insert_objective(self, obj):
        with self.conn:
            self.cur.execute(""" INSERT OR REPLACE INTO objective(id, objective) VALUES (?, ?)""", (1, float(obj)))

    def get_objective(self):
        self.cur.execute("""SELECT * FROM objective WHERE objective""")
        return self.cur.fetchone()

    def insert_term(self, term, date):
        with self.conn:
            self.cur.execute(""" INSERT OR REPLACE INTO term(id, term, date) VALUES (?, ?, ?)""", (1, int(term), date))

    def get_term(self):
        self.cur.execute("""SELECT * FROM term""")
        return self.cur.fetchall()

    def get_config(self):
        self.cur.execute("""SELECT * FROM config WHERE id""")
        return self.cur.fetchone()

    def set_config(self, style, currency):
        with self.conn:
            self.cur.execute(""" INSERT OR REPLACE INTO config(id, theme_style, currency) VALUES (?, ?, ?)""",
                             (1, style, currency))

    def insert_history_log(self, deposit, date):
        with self.conn:
            self.cur.execute(""" INSERT OR REPLACE INTO history(deposit, date) VALUES (?, ?)""", (float(deposit), date))

    def get_all_history_logs(self):
        self.cur.execute("""SELECT * FROM history""")
        return self.cur.fetchall()

    def erase_history_log(self, id_num):
        with self.conn:
            self.cur.execute("""DELETE FROM history WHERE id=?""", (id_num,))

    def erase_all_tables(self):
        print('deleting')
        with self.conn:
            self.cur.execute("""DELETE FROM objective""")
            self.cur.execute("""DELETE FROM history""")
        print('deleted')

db = DataBase(DATABASE_FILENAME)
