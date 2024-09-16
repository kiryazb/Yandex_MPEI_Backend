import urllib.parse


url = 'https://yandex.ru/search/?text=%D0%BA%D0%B0%D0%BA%20%D0%B1%D0%B5%D1%81%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%BE%20%D0%B5%D0%B7%D0%B4%D0%B8%D1%82%D1%8C%20%D0%BD%D0%B0%20%D1%82%D0%B0%D0%BA%D1%81%D0%B8'

# чтобы вычленить текст вопроса
# разбейте строку по знаку = и возьмите
# второй элемент получившегося списка
question = url.split('=')[1] # сохраните его в переменной question

# напечатайте на экран запрос в расшифрованном виде
print(urllib.parse.unquote(question))  # ваш код здесь