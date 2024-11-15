import sqlite3


con = sqlite3.connect('db.sqlite')
cur = con.cursor()

results = cur.execute('''
SELECT MIN(price) AS cheapest_price 
FROM ice_cream;
''')



for result in results:
    print(result)

con.close()
