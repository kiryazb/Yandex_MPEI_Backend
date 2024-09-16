import random as r

answers = ['Норм.', 'Лучше всех :)', 'Ну так', 'Отличненько!', 'Ничего, жить буду']

def how_are_you():
    return answers[r.randint(0, len(answers) - 1)]


print(how_are_you())