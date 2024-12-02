for current_hour in range(0, 24):
    print("На часах " + str(current_hour) + ":00.")

    if current_hour >= 6 and current_hour <= 11:
        print('Доброе утро!')
    elif current_hour >= 12 and current_hour <= 17:
        print('Добрый день!')
    elif current_hour >= 18 and current_hour <= 22:
        print('Добрый вечер!')
    elif current_hour <= 5 or current_hour >= 23:
        print('Доброй ночи!')