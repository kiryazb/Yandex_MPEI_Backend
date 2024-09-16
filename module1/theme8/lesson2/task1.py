import requests


url = 'https://wttr.in'  # не изменяйте значение URL

weather_parameters = {
    '0': '',
    'T': '',
    # добавьте параметр запроса `T`, чтобы вернулся чёрно-белый текст
}

response = requests.get(url, params=weather_parameters)  # передайте параметры в http-запрос

print(response.text)