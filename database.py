import sqlite3 as sl

con = sl.connect('user.db')

with con:
    con.execute("DROP TABLE IF EXISTS USER")
    con.execute("""
        CREATE TABLE USER (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            friends TEXT
        )
    """)

sql = 'INSERT INTO USER (id, name, friends) values(?,?,?)'

data = [
    (1, 'Alice', '["Bob", "Jack"]'),
    (2, 'Bob', '["Alice", "Chris"]'),
    (3, 'Chris', '["Bob"]'),
    (4, 'Jack', '["Alice"]'),
]

with con:
    con.executemany(sql, data)