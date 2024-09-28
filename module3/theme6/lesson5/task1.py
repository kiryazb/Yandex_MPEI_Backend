class Product:
    # Опишите инициализатор класса и метод get_info()
    def __init__(self, name, count) -> None:
        self.name = name
        self.count = count
    
    def get_info(self):
        return f"{self.name} (в наличии: {self.count})"
        


class Kettlebell(Product):
    # Опишите инициализитор класса и метод get_weight()
    def __init__(self, name, count, weight) -> None:
        self.weight = weight
        super().__init__(name, count)
    
    def get_weight(self):
        product_info = super().get_info()
        return f"{product_info}. Вес: {self.weight} кг"

class Clothing(Product):
    # Опишите инициализатор класса и метод get_size()
    def __init__(self, name, count, size) -> None:
        self.size = size
        super().__init__(name, count)
    
    def get_size(self):
        product_info = super().get_info()
        return f"{product_info}. Размер: {self.size}"



# Для проверки вашего кода создадим пару объектов
# и вызовем их методы:
small_kettlebell = Kettlebell('Гиря малая', 15, 2)
shirt = Clothing('Футболка', 5, 'L')

print(small_kettlebell.get_weight())
print(shirt.get_size())