import sqlite3

conn = sqlite3.connect('bauru_participa.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE Enquetes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT
    )
''')

conn.commit()

conn.close()
