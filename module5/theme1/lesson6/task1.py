import sqlite3


con = sqlite3.connect('db.sqlite')
cur = con.cursor()

cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table';")

table = cur.fetchall()[0][0]

results = cur.execute(f'''
SELECT title, description
FROM {table};
''')

for result in results:
    print(result)

con.close()
