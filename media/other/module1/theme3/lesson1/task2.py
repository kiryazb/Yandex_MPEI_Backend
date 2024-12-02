resorts = ['в Сочи', 'на курорты Краснодарского Края', 'в Санкт-Петербург', 'в Карелию']

def choose_vacation_place(resorts):
 # Стёпа, смотри, мы начнём выбор с Карелии, пусть тебе повезёт!
    destination = 'в Карелию'
    for resort in resorts:
        if resort == 'в Сочи':
            destination = resort
    print('Поехали ' + destination)

choose_vacation_place(resorts)