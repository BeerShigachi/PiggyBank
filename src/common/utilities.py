import datetime
from db.data_base import db
from src.common.const import DEFAULT_GOAL


def valid_user_input(user_input):
    validation_bool = True
    if user_input == '-':
        validation_bool = False
    elif user_input == '0':
        validation_bool = False
    elif user_input == '' or float(user_input) < 0:
        validation_bool = False
    elif float(user_input) >= 1 and user_input[0] == '0':
        validation_bool = False
    elif 0 < float(user_input) < 1 and user_input[:2] == '00':
        validation_bool = False
    return validation_bool


def sum_total_saving():
    total_money = 0
    for i in db.fetch_all_history_logs():
        total_money += i[1]
    return total_money


def get_goal():
    value = DEFAULT_GOAL
    data = db.fetch_objective()
    if data is not None:
        value = data[1]
    return value


def regularize_num(value):
    if value == int(value):
        return int(value)
    else:
        return value


def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - datetime.timedelta(days=next_month.day)

