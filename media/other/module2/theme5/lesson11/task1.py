# Объявите функцию check_winners с параметрами scores и student_score.
# Функция должна напечатать результат в заданном формате.
def check_winners(scores, student_score):
    scores_sort = sorted(scores)

    if student_score in scores_sort[-3:]:
        print('Вы в тройке победителей!')
    else:
        print('Вы не попали в тройку победителей.')


# Вызовы для проверки работы функции check_winners().
# Три набора данных - для проверки разных ситуаций.
first_olympiad_scores = [20, 48, 52, 38, 36, 13, 7, 41, 34, 24, 5, 51, 9, 14, 28, 42, 40, 39, 1, 45, 37, 10, 31, 27, 17,
                         46, 2, 22, 35, 55]
check_winners(first_olympiad_scores, 52)

second_olympiad_scores = [22, 4, 42, 5, 54, 28, 19, 33, 8, 16, 23, 40, 39, 58, 9, 13, 48, 2, 51, 41, 21, 36, 55, 25, 31,
                          45, 44, 30, 1, 10]
check_winners(second_olympiad_scores, 4)

third_olympiad_scores = [36, 1, 49, 27, 8, 23, 13, 56, 46, 33, 45, 30, 16, 11, 41, 19, 43, 54, 39, 38, 40, 48, 34, 26,
                         5, 28, 21, 3, 51, 44]
check_winners(third_olympiad_scores, 21)