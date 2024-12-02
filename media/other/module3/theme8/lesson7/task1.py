def fibonacci(n):
    first_number, second_number = 0, 1
    for i in range(n):
        yield first_number
        first_number, second_number = second_number, first_number + second_number


sequence = fibonacci(10)
for number in sequence:
    print(number)