import sqlite3

con = sqlite3.connect('db.sqlite')

cur = con.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS ice_cream(
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    wrapper_id INTEGER UNIQUE,
    FOREIGN KEY(wrapper_id) REFERENCES wrappers(id)
);

CREATE TABLE IF NOT EXISTS wrappers (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);
''')

con.close()
