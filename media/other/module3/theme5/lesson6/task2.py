class MushroomsCollector:
    # Проверьте, нет ли здесь ошибки:
    def __init__(self) -> None:
        self.mushrooms = []

    # Исправьте ошибку в этом методе.
    def is_poisonous(self, mushroom_name):
        if mushroom_name == 'Мухомор' or mushroom_name == 'Поганка':
            return True
        return False

    # Допишите метод.
    def add_mushroom(self, mushroom):
        if not self.is_poisonous(mushroom):
            self.mushrooms.append(mushroom)
        else:
            print("Нельзя добавить ядовитый гриб")

    def __str__(self):
        return ', '.join(self.mushrooms)


# Пример запуска для самопроверки
collector_1 = MushroomsCollector()
collector_1.add_mushroom('Мухомор')
collector_1.add_mushroom('Подосиновик')
collector_1.add_mushroom('Белый')
print(collector_1)

collector_2 = MushroomsCollector()
collector_2.add_mushroom('Лисичка')
print(collector_1)
print(collector_2)
