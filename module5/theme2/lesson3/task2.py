import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

results = cur.execute('''

''')

for result in results:
    print(result)

con.close()
