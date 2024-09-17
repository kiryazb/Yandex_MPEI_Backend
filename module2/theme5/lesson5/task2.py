# Количество корзин с овощами, шт.
baskets = 462
# Средний вес овощей в одной корзине, кг.
average_weight = 25
# Стоимость одного килограмма урожая, в монетах.
price_per_kg = 175


# Допишите функцию, которая рассчитывает вес и стоимость урожая.
def calc(basket_count, weight, price):
    return basket_count * weight, basket_count * weight * price
    ...

weight, price = calc(baskets, average_weight, price_per_kg)
...
# Составьте f-строку и напечатайте её.
print(f"Общий вес урожая: {weight} кг. Оценённая стоимость урожая: {price}.")