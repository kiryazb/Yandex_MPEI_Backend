def pay_bills(month, bills):
    if month % 3 == 0:
        return bills[1:-1]
    return bills[0:len(bills):len(bills) - 1]


# Вызов функции:
print(pay_bills(5, ['Интернет', 'Коммуналка', 'Телефон', 'Страховка']))