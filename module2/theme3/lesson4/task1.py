# Вместо многоточия укажите необходимые параметры.
def count_tiles(depth, length, width=None):
    # Опишите условие, когда ширина бассейна не указана.
    if not width:
        width = length

    # Посчитайте, сколько понадобится плиток для стенок и дна бассейна.
    ...

    # Верните результат работы функции.
    return depth * length * 2 + depth * width * 2 + width * length


total_tiles = count_tiles(2, 2, 2)
print('Общее количество плиток для строительства бассейна:', total_tiles)