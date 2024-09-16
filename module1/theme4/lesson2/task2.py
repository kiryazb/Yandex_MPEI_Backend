def print_valid_cities(all_cities, used_cities):
    diff = all_cities.difference(used_cities)
    for city in diff:
        print(city)


def add_cities(all_cities, new_cities):
    for city in new_cities:
        all_cities.add(city)


# Анфиса нашла названия нескольких новых городов,
# эти города нужно добавить в множество all_cities
new_cities = [
    'Екатеринбург',
    'Выборг' ,
    'Владивосток',
    'Казань',
    'Why',
    'Йезд'
]

all_cities = {
    'Абакан',
    'Астрахань',
    'Бобруйск',
    'Калуга',
    'Караганда',
    'Кострома',
    'Липецк',
    'Новосибирск'
}

used_cities = {
    'Калуга',
    'Абакан' ,
    'Новосибирск'
}

add_cities(all_cities, new_cities)
print_valid_cities(all_cities, used_cities)
