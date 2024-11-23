import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS toppings(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ice_cream(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ice_cream_toppings(
    id INTEGER PRIMARY KEY,
    ice_cream_id INTEGER NOT NULL,
    topping_id INTEGER NOT NULL,
    FOREIGN KEY(ice_cream_id) REFERENCES ice_cream(id),
    FOREIGN KEY(topping_id) REFERENCES toppings(id)
);
''')

con.close()
