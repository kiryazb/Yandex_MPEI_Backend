import sqlite3


con = sqlite3.connect('db.sqlite')

cur = con.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS ice_cream (
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL
);
'''

cur.execute(create_table_query)

con.commit()

con.close()

