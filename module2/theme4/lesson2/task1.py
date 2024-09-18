from datetime import datetime

deadline = datetime(2023, 11, 6, 9, 15, 0)
date_format = "%d.%m"
deadline_as_str = datetime.strftime(deadline, date_format)
print('Ваш дедлайн:', deadline_as_str)