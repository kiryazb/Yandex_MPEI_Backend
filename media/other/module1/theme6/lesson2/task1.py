import datetime as dt

# Дата выхода первой серии.
start_time = dt.datetime(2011, 4, 17)
# Укажите дату выхода последней серии.
final_time = dt.datetime(2019, 4, 15)

# Вычислите, сколько времени шёл сериал.
duration = final_time - start_time

print(duration)