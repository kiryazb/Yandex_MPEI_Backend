import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

cur.executescript('''
ALTER TABLE ice_cream ADD COLUMN is_published INTEGER NOT NULL;
ALTER TABLE ice_cream ADD COLUMN is_on_main INTEGER NOT NULL;
''')

con.close()
