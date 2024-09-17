from random import randint

# Начальная температура чая
current_temperature = 85

# Объявите цикл while
# В теле цикла получите случайное значение температуры,
# на которое остыл чай в этой итерации (в диапазоне от 1 до 3).
# Уменьшите температуру чая на полученное значение.
# Напечатайте нужные сообщения.
while current_temperature > 60:
    delta = randint(1, 3)
    current_temperature -= delta
    print("Прошла минута.")
    print(f"Чай остыл ещё на {delta} °C. Текущая температура: {current_temperature} °C")

print("Время пить чай!")