countdown_str = ''

for number in range(10, -1, -1):
    countdown_str = countdown_str + f'{number}, '

countdown_str = countdown_str + 'поехали!'

print(countdown_str)