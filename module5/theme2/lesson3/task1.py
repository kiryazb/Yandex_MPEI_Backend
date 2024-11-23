import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

results = cur.execute('''
SELECT
    ice_cream.title,
    categories.slug,
    MAX(ice_cream.price)
FROM
    ice_cream, categories
WHERE
    ice_cream.category_id = categories.id
GROUP BY
    categories.slug
ORDER BY
    ice_cream.price DESC;
''')

for result in results:
    print(result)

con.close()
