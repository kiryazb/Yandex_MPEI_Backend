# Список для тестирования.
numbers = [1, 3, 4, 6, 9, 11]

# Здесь напишите ваше генераторное выражение.
gen_expr = (number ** 2 for number in numbers if number % 3 == 0)

print(sum(gen_expr))