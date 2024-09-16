# Функция для вычисления периметра куба.
def calc_cube_perimeter(side):
    return side * 12

# Присвойте переменной one_cube_perimeter значение,
# которое вернёт функция calc_cube_perimeter() с аргументом 3:
# 3 метра - это длина ребра куба.

one_cube_perimeter = calc_cube_perimeter(3)

# Вычислите общую длину палок, необходимых
# для строительства 8 кубов,
# и сохраните это значение в переменную full_length
full_length = 8 * one_cube_perimeter

# А теперь напечатаем результат (в этой строке ничего изменять не нужно)
print('Необходимый метраж палок для 8 кубов:', full_length)