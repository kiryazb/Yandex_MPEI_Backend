DATABASE = {
    'Серёга': 'Омск',
    'Соня': 'Москва',
    'Миша': 'Москва',
    'Дима': 'Челябинск',
    'Алина': 'Красноярск',
    'Егор': 'Пермь',
    'Коля': 'Красноярск'
}

def process_anfisa(query):
    if query == 'Сколько у меня друзей?':
        count = len(DATABASE)
        # В следующей строке замените конкатенацию на f-строку
        return f'У тебя {str(count)} друзей.'
    elif query == 'Кто все мои друзья?':
        friends_string = ', '.join(DATABASE)
        # В следующей строке замените конкатенацию на f-строку
        return f'Твои друзья: {friends_string}'
    elif query == 'Где все мои друзья?':
        unique_cities = set(DATABASE.values())
        cities_string = ', '.join(unique_cities)
        # В следующей строке замените конкатенацию на f-строку
        return f'Твои друзья в городах: {cities_string}'
    else:
        return '<неизвестный запрос>'


print('Привет, я Анфиса!')
print(process_anfisa('Сколько у меня друзей?'))
print(process_anfisa('Кто все мои друзья?'))
print(process_anfisa('Где все мои друзья?'))