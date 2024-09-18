# Кидаем игровой кубик, и на нём выпадает...
dice_value = 2

if dice_value < 4:
    print('Выпало 1, 2 или 3!')
    if dice_value < 2:
        print('Выпало 1, точно!')
    else:
        print('Выпало 2 или 3!')
        if dice_value == 2:
            print('Это двойка!')
        else:
            print('Выпало 3!')
else:
    print('Выпало 4, 5 или 6!')
    if dice_value > 5:
        print('Это шесть, большего значения и быть не может!')
    else:
        print('Выпало 4 или 5. Неплохо!')