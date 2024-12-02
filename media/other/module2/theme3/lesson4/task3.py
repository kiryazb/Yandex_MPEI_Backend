# Вместо многоточия укажите нужные параметры.
def find_pool_capacity(num_of_people, length, width=None):
    # Опишите условие, когда передано отрицательное значение длины.
    if length < 0:
        length *= -1
    # Опишите условие, когда передано отрицательное значение
    # количества людей.
    if num_of_people < 0:
        num_of_people *= -1

    # Опишите условие, когда ширина бассейна не указана, когда указано
    # отрицательное значение, и когда положительное.
    if not width:
        width = length
    elif width < 0:
        width *= -1

    area = length * width
    if num_of_people <= area * 2:
        print(f'Бассейн площадью {area} кв. м. вмещает {num_of_people} чел.')
    else:
        print(f'Бассейн площадью {area} кв. м. не вмещает {num_of_people} чел.')


# Проверьте работу функции, можете подставить свои значения.
find_pool_capacity(4, 2)
find_pool_capacity(4, 5, 10)
find_pool_capacity(-10, -5, -2)