import sqlite3

conn = sqlite3.connect("finance.db")
cur = conn.cursor()

cur.execute("CREATE TABLE user (id integer primary key, google_sheet_id text)")

conn.commit()
