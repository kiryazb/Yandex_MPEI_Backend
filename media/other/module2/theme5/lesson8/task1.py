# Функция для создания словаря информации об овощах

def create_vegetable_info(names, varieties, yields):
    vegetable_info = dict()
    for info in zip(names, varieties, yields):
        name, variety, _yield = zip(info)
        vegetable_info[str(name[0])] = (str(variety[0]), float(_yield[0]))
    return vegetable_info

# Тестовые данные:
vegetables = ['Помидоры', 'Огурцы', 'Баклажаны', 'Перец', 'Капуста']
varieties = ['Красный куб', 'Аллигатор', 'Василёк', 'Тропический закат', 'Арктик']
yields = [6.5, 4.3, 2.8, 2.2, 3.5]

# Вызов функции:
print(create_vegetable_info(vegetables, varieties, yields))