apple_tree_yields = 150, 210, 90, 120, 140, 190, 130, 150, 110, 210, 150

# Объявите функцию reversed_sort(),
# которая вернёт отсортированный по убыванию кортеж.
def reversed_sort(collection):
    return tuple(sorted(collection, reverse=True))

# Присвойте этой переменной значение,
# которое вернёт функция reversed_sort()
result = reversed_sort(apple_tree_yields)
# Напечатайте:
print(result[0])  # наибольшее значение из кортежа result,
print(result[1])  # второй элемент из кортежа result,
print(result[2])  # третий элемент из из кортежа result.
