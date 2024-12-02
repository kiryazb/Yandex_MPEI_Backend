# Импортировать функцию для получения случайного значения
# и присвоить ей псевдоним rnd
from random import randint as rnd
# Объявить функцию get_dumplings_recommendation(),
# которая вернёт (return) случайное число в диапазоне от 10 до 20.
def get_dumplings_recommendation(min_number, max_number):
    return rnd(min_number, max_number)
# Вызвать функцию get_dumplings_recommendation() и напечатать заданную фразу.
print(f"Оптимальным количеством пельменей на сегодня будет {get_dumplings_recommendation(20, 30)}")