# Получаем данные в секундах
response = 424562

# Переведите полученное значение в необходимые единицы измерения
days = response // (24 * 60 * 60)
hours = (response - days * 60 * 60 * 24) // 3600
minutes = (response - days * 60 * 60 * 24 - hours * 60 * 60) // 60
seconds = (response - days * 60 * 60 * 24 - hours * 60 * 60 - minutes * 60)

print(response, 'секунд - это')
print('Дней:', days)
print('Часов:', hours)
print('Минут:', minutes)
print('Секунд:', seconds)