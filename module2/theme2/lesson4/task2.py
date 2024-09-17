def find_answer():
    number = 3
    # Далее проводите операции над number отдельно по шагам
    number *= 100
    number /= 5
    number -= 20
    number += 2
    # Верните результат:
    return int(number)


# Вызовите функцию find_answer() и напечатайте результат.
print(f'Ответ на главный вопрос жизни, Вселенной и всего такого: {find_answer()}')