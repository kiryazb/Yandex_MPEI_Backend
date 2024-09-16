import requests


cities = [
    'Омск',
    'Калининград',
    'Челябинск',
    'Владивосток',
    'Красноярск',
    'Москва',
    'Екатеринбург'
]


def make_url(city):
    # в URL задаём город, в котором узнаем погоду
    return f'http://wttr.in/{city}'


def make_parameters():
    params = {
        'format': 2,  # погода одной строкой
        'M': ''  # скорость ветра в "м/с"
    }
    return params


def what_weather(city):
    try:
        response = requests.get(make_url(city), params=make_parameters())
        if response.status_code == 200:
            return response.text
        else:
            return '<ошибка на сервере погоды>'
    except requests.ConnectionError as e:
        return '<сетевая ошибка>'

print('Погода в городах:')
for city in cities:
    print(city, what_weather(city))
