def rectangle_area(length, width):
    return length * width

area_1 = rectangle_area(5, 10)
area_2 = rectangle_area(7, 7)

if area_1 < area_2:  # Если area_1 меньше, чем area_2...
    # ...выполнится этот код.
    print('Площадь первой грядки меньше второй!')

print('Сравнение грядок завершено!')