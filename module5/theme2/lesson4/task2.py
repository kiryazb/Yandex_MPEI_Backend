import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

results = cur.execute('''
SELECT
    ice_cream.title,
    categories.slug,
    wrappers.title,
    MIN(ice_cream.price),
    AVG(ice_cream.price)
FROM ice_cream
LEFT JOIN wrappers ON ice_cream.wrapper_id = wrappers.id
JOIN categories ON ice_cream.category_id = categories.id
GROUP BY categories.id;
''')

for result in results:
    print(result)

con.close()
