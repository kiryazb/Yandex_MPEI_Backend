# Пропишите нужные импорты.
from decimal import Decimal, getcontext

getcontext().prec = 3


# Напишите код функции.
def get_monthly_payment(credit_sum, month_count, procent):
    # Преобразуем входные параметры в Decimal
    credit_sum = Decimal(credit_sum)
    month_count = Decimal(month_count)
    procent = Decimal(procent)

    # Банк делит названную сумму на названное количество месяцев
    # и увеличивает ежемесячный платёж на оговоренный процент.
    month_sum = (credit_sum / month_count) * (1 + procent / Decimal(100))

    # Функция должна вернуть сумму ежемесячного платежа по кредиту.
    return month_sum


print(f"Ежемесячный платёж: {get_monthly_payment(54, 24, 9)} ВтК ")