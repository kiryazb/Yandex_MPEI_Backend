import sqlite3


con = sqlite3.connect('db.sqlite')
cur = con.cursor()

results = cur.execute('''
SELECT title, description 
FROM ice_cream 
WHERE is_published = 1 
ORDER BY title DESC 
LIMIT 2 OFFSET 1;
''')

for result in results:
    print(result)

con.close()
