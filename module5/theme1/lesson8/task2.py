import sqlite3


con = sqlite3.connect('db.sqlite')
cur = con.cursor()

results = cur.execute('''
SELECT AVG(price) AS average_price 
FROM ice_cream 
WHERE category = 'Экзотическое';
''')

for result in results:
    print(result)

con.close()
