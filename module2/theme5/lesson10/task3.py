# Овощи, которые растут в каждом из огородов
first_garden = {'помидоры', 'огурцы', 'морковь'}
second_garden = {'перец', 'помидоры', 'лук'}

# 1. Овощи, которые растут и в первом, и во втором огороде
common_vegetables = first_garden & second_garden
print('Овощи, растущие и в первом, и во втором огороде:', common_vegetables)

# 2. Овощи, которые растут только в первом огороде
only_first_garden = first_garden - second_garden
print('Овощи, растущие только в первом огороде:', only_first_garden)

# 3. Овощи, которые растут только во втором огороде
only_second_garden = second_garden - first_garden
print('Овощи, растущие только во втором огороде:', only_second_garden)