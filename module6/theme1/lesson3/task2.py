class Contact:

    def __init__(self, name, year_birth, is_programmer):
        self.name = name
        self.year_birth = year_birth
        self.is_programmer = is_programmer

    def age_define(self):
        if 1946 < self.year_birth < 1980:
            return 'Олдскул'
        if self.year_birth >= 1980:
            return 'Молодой'
        return 'Старейшина'

    def programmer_define(self):
        if self.is_programmer:
            return 'Программист'
        return 'Нормальный'

    def show_contact(self):
        return (
            f'{self.name}, '
            f'возраст: {self.age_define()}, '
            f'статус: {self.programmer_define()}'
        )


# Тест для старейшины, не программиста
test_old_none_programmer = Contact('Пушкин', 1799, False)
assert test_old_none_programmer.programmer_define() == 'Нормальный', "Ошибка: статус программиста неверен."
assert test_old_none_programmer.age_define() == 'Старейшина', "Ошибка: возраст неверен."

# Тест для олдскула, программиста
test_oldschool_programmer = Contact('Бьёрн Страуструп', 1950, True)
assert test_oldschool_programmer.programmer_define() == 'Программист', "Ошибка: статус программиста неверен."
assert test_oldschool_programmer.age_define() == 'Олдскул', "Ошибка: возраст неверен."

# Тест для молодого, не программиста
test_young_none_programmer = Contact('Иван', 1995, False)
assert test_young_none_programmer.programmer_define() == 'Нормальный', "Ошибка: статус программиста неверен."
assert test_young_none_programmer.age_define() == 'Молодой', "Ошибка: возраст неверен."

# Тест для молодого программиста
test_young_programmer = Contact('Саша', 2000, True)
assert test_young_programmer.programmer_define() == 'Программист', "Ошибка: статус программиста неверен."
assert test_young_programmer.age_define() == 'Молодой', "Ошибка: возраст неверен."

# Тест для олдскула, не программиста
test_oldschool_none_programmer = Contact('Линус', 1969, False)
assert test_oldschool_none_programmer.programmer_define() == 'Нормальный', "Ошибка: статус программиста неверен."
assert test_oldschool_none_programmer.age_define() == 'Олдскул', "Ошибка: возраст неверен."

# Дополнительные тесты для проверки show_contact()
assert (
    test_old_none_programmer.show_contact()
    == 'Пушкин, возраст: Старейшина, статус: Нормальный'
), "Ошибка в методе show_contact для старейшины, не программиста."

assert (
    test_young_programmer.show_contact()
    == 'Саша, возраст: Молодой, статус: Программист'
), "Ошибка в методе show_contact для молодого программиста."
