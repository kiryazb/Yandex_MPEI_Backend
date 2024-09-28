def calculate_sum_and_average(numbers):
    total_sum = 0
    for num in numbers:
        total_sum += num

    average = total_sum // len(numbers)
    return total_sum, average


numbers = [10, 20, 30, 40, 50]
total, avg = calculate_sum_and_average(numbers)
print(f'Сумма чисел: {total}')
print(f'Среднее значение: {avg}')

numbers = [11, 22, 33, 42, 51]
total, avg = calculate_sum_and_average(numbers)
print(f'Сумма чисел: {total}')
print(f'Среднее значение: {avg}')