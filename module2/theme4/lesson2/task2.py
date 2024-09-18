# Допишите нужные импорты.
from datetime import datetime

date_format = '%Y/%m/%d %H:%M:%S'

def timedelta_days(datetime_str_1, datetime_str_2):
    delta = datetime.strptime(datetime_str_2, date_format) - datetime.strptime(datetime_str_1, date_format)

    return delta.days

difference = timedelta_days('2019/05/10 00:00:00', '2019/10/04 00:00:00')

print('От начала посевной до начала сбора урожая прошло', difference, 'дней.')