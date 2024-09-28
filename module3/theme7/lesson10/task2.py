from datetime import datetime
from random import sample


def choose_days():
    # Определяем диапазон дат первой половины месяца.
    first_month_half = list(range(1, 16))

    # Выбор трёх случайных чисел:
    random_days = sample(first_month_half, k=3)
    # Cортировка этих чисел по возрастанию:
    sorted_days = sorted(random_days)

    # Получаем сегодняшнюю дату.
    # На её основе будут генерироваться даты для занятий:
    now = datetime.now()

    # Чтобы было проще формировать сообщение, начнём цикл с 1.
    for i in range(1, 4):
        # Генерируем дату занятия, подменяя номер дня в сегодняшней дате.
        practice_day = now.replace(day=sorted_days[i - 1]).strftime("%d.%m.%Y")
        print(f'{i}-е занятие: {practice_day}')


choose_days()