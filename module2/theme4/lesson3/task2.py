# Пропишите нужные импорты.
from datetime import datetime

date_format = '%H:%M:%S'

# Напишите код функции, следуя плану из задания.
def get_results(leader_time, member_time):
    leader_time = datetime.strptime(leader_time, date_format)
    member_time = datetime.strptime(member_time, date_format)
    if leader_time == member_time:
        print(f"Вы пробежали за {leader_time.time()} и победили!")
    else:
        print(f"Вы пробежали за {member_time.time()} с отставанием от лидера {(member_time - leader_time)}")


# Проверьте работу программы, можете подставить свои значения.
get_results('02:02:02', '02:02:02')
get_results('02:02:02', '03:04:05')