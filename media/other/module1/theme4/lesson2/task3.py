def get_together_games(games1, games2):
    return set(games1) & set(games2)

anfisa_games = [
    'Online-chess',
    'Города',
    'DOOM',
    'Крестики-нолики'
]
alisa_games = [
    'DOOM',
    'Online-chess',
    'Города',
    'GTA',
    'World of tanks'
]
# Вызовите функцию со списками игр в качестве параметров
together_games = get_together_games(anfisa_games, alisa_games)
# Напечатайте итоговый перечень игр в цикле
for game in together_games:
    print(f"👾 {game}")