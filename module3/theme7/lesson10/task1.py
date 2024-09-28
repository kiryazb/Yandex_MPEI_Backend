    # Импортируйте необходимые модули.
    from datetime import datetime

    # Укажите два параметра функции:
    def validate_record(name, date):
        # Напишите код, верните булево значение.
        try:
            datetime.strptime(date, "%d.%m.%Y")
        except ValueError as e:
            print(f"Некорректный формат даты в записи: {name}, {date}")
            return False
        return True


    # Укажите параметры функции:
    def process_people(data):
        # Объявите счётчики.
        good_count = 0
        bad_count = 0
        for record in data:
            name, date = record[0], record[1]
            if validate_record(name, date):
                good_count += 1
            else:
                bad_count += 1
        
        return {
            "good": good_count,
            "bad": bad_count,
            }



    data = [
        ('Иван Иванов', '10.01.2004'),
        ('Пётр Петров', '15.03.1956'),
        ('Зинаида Зеленая', '6 февраля 1997'),
        ('Елена Ленина', 'Второе мая тысяча девятьсот восемьдесят пятого'),
        ('Кирилл Кириллов', '26/11/2003')
    ]
    statistics = process_people(data)
    # Выведите на экран информацию о корректных и некорректных записях
    # в таком формате:
    # Корректных записей: <число>
    # Некорректных записей: <число>