for current_hour in range(24):
    if current_hour < 12:
        print('Доброе утро!')
    elif current_hour >= 12:
        print('Добрый день!')