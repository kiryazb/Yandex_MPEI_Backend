# Функция для вычисления периметра кубов.
def calc_cube_perimeter(side):
    return side * 12


# Функция для вычисления площади кубов.
def calc_cube_area(side):
    one_face = side * side
    cube_area = one_face * 6
    return cube_area


# Дополните объявление функции:
# теперь должна принимать два параметра -
# длину ребра куба и количество кубов.
def calc_cube(side, quantity):
    # Вызываем функцию, рассчитывающую периметр
    # и передаём в неё размер куба
    one_cube_perimeter = calc_cube_perimeter(side)

    # Здесь вместо многоточия должна стоять переменная,
    # хранящая количество кубов, переданное во втором аргументе.
    full_length = one_cube_perimeter * quantity

    # Вызываем функцию, рассчитывающую площадь стекла
    # и передаём в неё размер куба
    one_cube_area = calc_cube_area(side)

    # Здесь вместо многоточия должна стоять переменная,
    # хранящая количество кубов, переданное во втором аргументе.
    full_area = one_cube_area * quantity

    # В этой строке замените многоточие на переменную, хранящую количество кубов
    print('Для', quantity, 'кубов понадобится палок (м):', full_length, 'и стекла (кв.м):', full_area)


# Для проверки работы кода вызываем функцию с двумя аргументами:
# 3 - это размер ребра куба,
# 2 - это необходимое количество кубов
calc_cube(3, 2)