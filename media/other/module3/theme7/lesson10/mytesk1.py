from datetime import datetime


def validate_record(name, date_str):
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        print(f'Некорректный формат даты в записи: {name}, {date_str}')
        return False

    return True


def process_people(data):
    good_count = 0
    bad_count = 0

    for name, date_str in data:
        if validate_record(name, date_str):
            good_count += 1
        else:
            bad_count += 1
    
    return {'good': good_count, 'bad': bad_count}


data = [
    ('Иван Иванов', '10.01.2004'),
    ('Пётр Петров', '15.03.1956'),
    ('Зинаида Зеленая', '6 февраля 1997'),
    ('Елена Ленина', 'Второе мая тысяча девятьсот восемьдесят пятого'),
    ('Кирилл Кириллов', '26/11/2003')
]

statistics = process_people(data)

print(f"Корректных записей: {statistics['good']}")
print(f"Некорректных записей: {statistics['bad']}")
