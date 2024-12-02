# Объявите функцию rooms_equal() с параметрами room_size и room_list
...
# Перенесите следующий код в тело функции, которую вы объявили
def rooms_equal(room_size, room_list):
    count = 0

    for room in room_list:
        if room == room_size:
            count = count + 1

    print('Комнат площадью', room_size, 'кв.м:', count)


    # Следующий код не изменяйте и не переносите в тело функции
flat = [
        5.55, 22.19, 7.78, 26.86, 5.55,
        29.84, 22.19, 5.55, 16.85, 4.52
    ]

hut = [9.2, 3.5, 8.1, 2.3, 9.2, 4.2, 6.9]

rooms_equal(5.55, flat)
# Добавьте ещё один вызов функции rooms_equal()
# Передайте в функцию искомую площадь - 9.2 кв.м и список hut
rooms_equal(9.2, hut)