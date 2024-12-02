vegetables = ['Помидоры', 'Огурцы', 'Баклажаны', 'Перец', 'Капуста']
vegetable_yields = [6.5, 4.3, 2.8, 2.2, 3.5]

for index in range(len(vegetable_yields)):
    print(f'{vegetables[index]}: урожайность - {int(vegetable_yields[index] * 10000)} кг на гектар.')