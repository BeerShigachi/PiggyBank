from main import db


def valid_user_input(user_input):
    validation_bool = True
    if user_input == '' or float(user_input) < 0:
        validation_bool = False
    elif float(user_input) >= 1 and user_input[0] == '0':
        validation_bool = False
    elif 0 < float(user_input) < 1 and user_input[:2] == '00':
        validation_bool = False
    elif user_input == "-":
        validation_bool = False
    return validation_bool


def sum_total_saving():
    total_money = 0
    for i in db.get_all_history_logs():
        total_money += i[1]
    return total_money
