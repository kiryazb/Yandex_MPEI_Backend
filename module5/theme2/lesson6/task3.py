import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

cur.executescript('''
DROP TABLE ice_cream;
''')

con.close()
