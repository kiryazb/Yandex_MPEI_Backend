def assess_yield(number_of_plants, average_weight):
    total_weight = number_of_plants * average_weight / 1000
    grade = ''
    if total_weight > 100:
        grade = 'Ожидается отличный урожай.'
    elif total_weight > 50:
        grade = 'Ожидается хороший урожай.'
    elif total_weight > 0:
        grade = 'Урожай будет так себе.'
    else:
        grade = 'Урожая не будет.'

    return (total_weight, grade)


# Пример вызова функции
total_weight, rating = assess_yield(50, 200)
print(total_weight, 'кг.', rating)