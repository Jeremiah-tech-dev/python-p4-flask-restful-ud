#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('newsletters.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS newsletters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR,
    body VARCHAR,
    published_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    edited_at DATETIME
)
''')

conn.commit()
conn.close()
print("Database created successfully!")
