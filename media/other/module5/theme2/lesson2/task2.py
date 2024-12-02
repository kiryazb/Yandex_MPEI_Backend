import sqlite3

con = sqlite3.connect('db.sqlite')

cur = con.cursor()

results = cur.execute('''
SELECT
    ice_cream.title,
    wrappers.title
FROM
    ice_cream, wrappers
WHERE
    wrappers.id = ice_cream.wrapper_id AND wrappers.title LIKE 'Б%';
''')

for result in results:
    print(result)

con.close()
