from decimal import Decimal
from datetime import datetime as dt, date, timedelta


def add(items, title, amount, expiration_date=None):
    if title not in items:
        items[title] = []
    if expiration_date and isinstance(expiration_date, str):
        expiration_date = dt.strptime(expiration_date, '%Y-%m-%d').date()
    items[title].append(
        {
            'amount': Decimal(str(amount)),
            'expiration_date': expiration_date,
        }
    )


def add_by_note(items, note):
    parts = note.split()
    try:
        expiration_date = dt.strptime(parts[-1], '%Y-%m-%d').date()
    except Exception as e:
        expiration_date = None
    if expiration_date:
        amount = parts[-2]
        title = ' '.join(parts[:-2])
    else:
        amount = parts[-1]
        title = ' '.join(parts[:-1])
    add(items, title, amount, expiration_date)


def find(items, needle):
    res = list()
    for key in items.keys():
        if needle.lower() in key.lower():
            res.append(key)
    return res


def amount(items, needle):
    suitable = find(items, needle)
    count = Decimal('0')
    for need in suitable:
        for info in items[need]:
            count += info['amount']
    return count


def expire(items, in_advance_days=0):
    res = []
    # Текущая дата с учетом in_advance_days
    date_now = date.today() + timedelta(days=in_advance_days)

    for key, value in items.items():
        total_amount = Decimal('0')  # Суммируем количество для каждого продукта
        for info in value:
            item_date = info['expiration_date']
            if item_date and item_date <= date_now:
                total_amount += info['amount']

        if total_amount > 0:
            res.append((key, total_amount))

    return res


goods = {
    'Хлеб': [
        {'amount': Decimal('1'), 'expiration_date': None},
        {'amount': Decimal('1'), 'expiration_date': date(2024, 9, 16)}
    ],
    'Яйца': [
        {'amount': Decimal('2'), 'expiration_date': date(2024, 9, 19)},
        {'amount': Decimal('3'), 'expiration_date': date(2024, 9, 18)}
    ],
    'Вода': [{'amount': Decimal('100'), 'expiration_date': None}]
}

# Если функция вызвана 10 декабря 2023 года
print(expire(goods))
# Вывод: [('Хлеб', Decimal('1'))]
print(expire(goods, 1))
# Вывод: [('Хлеб', Decimal('1')), ('Яйца', Decimal('3'))]
print(expire(goods, 2))
# Вывод: [('Хлеб', Decimal('1')), ('Яйца', Decimal('5'))]