# Код этой функции не меняйте.
def count_tiles(depth, length, width=None):
    if width is None:
        width = length

    width_side = 2 * width * depth
    length_side = 2 * length * depth
    bottom_tiles = length * width
    total = width_side + length_side + bottom_tiles

    return total

# Передайте в функцию нужный параметр и напишите её код.
def make_phrase(tiles_count):
    if tiles_count == 11 or tiles_count == 12 or tiles_count == 13 or tiles_count == 14:
        return f'{tiles_count} плиток'
    elif tiles_count % 10 == 1:
        return f'{tiles_count} плитку'
    elif tiles_count % 10 == 2 or tiles_count % 10 == 3 or tiles_count % 10 == 4:
        return f'{tiles_count} плитки'
    else:
        return f'{tiles_count} плиток'


total_tiles = count_tiles(2, 2, 2)
# Выведите на экран нужное сообщение.
print(f"Для строительства бассейна нужно заготовить {make_phrase(total_tiles)}")