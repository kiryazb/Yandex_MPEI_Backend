def calc_stat(listened):  # От англ. calculate statistics, посчитать статистику
    return f'Вы прослушали {len(listened)} песен общей продолжительностью {sum(listened) // 60} минут.'

print(calc_stat([189, 148, 210, 144, 174, 158, 163, 189, 227, 198]))