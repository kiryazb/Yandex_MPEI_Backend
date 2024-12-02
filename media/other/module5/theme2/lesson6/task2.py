import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

cur.executescript('''
ALTER TABLE ice_cream RENAME COLUMN description TO specification;
''')

con.close()
