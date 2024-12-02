# Продуктов маловато:
milk = False          # Молока нет.
cereal = True         # Хлопья есть.
eggs = False          # Яиц нет.

# Вставьте логический оператор вместо многоточия.

if milk and cereal or eggs:
    if eggs:
        if milk:
            breakfast = "- омлет"
        else:
            breakfast = "- яичница"
    else:
        breakfast = "- хлопья с молоком"
else:
    if milk:
        breakfast = "- стакан молока"
    elif cereal:
        breakfast = "можно погрызть сухих хлопьев"
    else:
        breakfast = "ничего не будет: разгрузочный день"

print("Сегодня на завтрак", breakfast)