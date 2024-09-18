# Напишите функцию get_competition_data().
def get_competition_data(races_data):
    print(f"Команды, участвовавшие в гонке: {', '.join(sorted(races_data[0].keys()))}")
    team_info = {}

    for match in races_data:
        for key, value in match.items():
            team_info[key] = team_info.get(key, 0) + value

    mx_ball, team = 0, ""
    for key, value in team_info.items():
        if value > mx_ball:
            mx_ball = value
            team = key

    print(f"В гонке победила команда {team} с результатом {mx_ball} баллов")


races_data = [
    {'Ferrari': 20, 'Mercedes': 5, 'Aston Martin': 10, 'Williams': 15},
    {'Mercedes': 15, 'Aston Martin': 20, 'Ferrari': 10, 'Williams': 0},
    {'Ferrari': 20, 'Williams': 15, 'Aston Martin': 10, 'Mercedes': 5}
]

get_competition_data(races_data)