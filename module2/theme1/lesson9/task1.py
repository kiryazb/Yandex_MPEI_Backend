bash = 31
c_and_c_plus_plus = 29
c_sharp = 11
html_css = 36
java = 19
javascript = 37
sql = 34

def analyze_skills():
    print(f"Доля питонистов, у которых есть наименее популярный навык (в %): {min(bash, c_and_c_plus_plus, c_sharp, html_css, java, javascript, sql)}")
    print(f"Доля питонистов, у которых есть наиболее популярный навык (в %): {max(bash, c_and_c_plus_plus, c_sharp, html_css, java, javascript, sql)}")

# Не удаляйте вызов функции.
analyze_skills()