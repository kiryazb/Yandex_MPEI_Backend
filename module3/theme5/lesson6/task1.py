class BacteriaProducer:

    def __init__(self, max_bacteria):
        self.max_bacteria = max_bacteria
        self.bacteria_count = 0

    # Допишите метод
    def create_new(self):
        if self.bacteria_count + 1 > self.max_bacteria:
            print("Нет места под новую бактерию")
        else:
            self.bacteria_count += 1
            print(f"Добавлена одна бактерия. "
                  f"Количество бактерий в популяции: {self.bacteria_count}")

    # Допишите метод
    def remove_one(self):
        if self.bacteria_count <= 0:
            print("В популяции нет бактерий, удалять нечего")
        else:
            self.bacteria_count -= 1
            print(f"Одна бактерия удалена. "
                  f"Количество бактерий в популяции: {self.bacteria_count}")


# Пример запуска для самопроверки
bacteria_producer = BacteriaProducer(max_bacteria=3)
bacteria_producer.remove_one()
bacteria_producer.create_new()
bacteria_producer.create_new()
bacteria_producer.create_new()
bacteria_producer.create_new()
bacteria_producer.remove_one()
