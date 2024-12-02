fruit_yields = [164.8, 105.0, 124.3, 113.8]  # Урожайность, кг на дерево.

# Вместо всего этого кода нужно написать единственную строчку,
# которая выполнит те же действия.
# corrected_fruit_yields = []

# for yield_value in fruit_yields:
#     yield_value += 1.2
#     list.append(corrected_fruit_yields, yield_value)

corrected_fruit_yields = [yield_value + 1.2 for yield_value in fruit_yields]  # Ваш код - здесь.


print(corrected_fruit_yields)