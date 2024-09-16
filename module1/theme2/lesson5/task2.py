for current_hour in range(0, 24):
    print("На часах " + str(current_hour) + ":00.")
    # Вместо многоточий напишите код
    if current_hour < 6:
        print('Доброй ночи!')
    elif 6 <= current_hour < 12:
        print('Доброе утро!')
    elif 12 <= current_hour < 18:
        print('Добрый день!')
    elif 18 <= current_hour < 23:
        print('Добрый вечер!')
    else:
        print('Доброй ночи!')
    # Допишите программу