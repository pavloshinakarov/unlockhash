import sqlite3
from datetime import datetime

conn = sqlite3.connect('storage.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS work (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mask TEXT NOT NULL,
    hash TEXT NOT NULL,
    algorithm TEXT NOT NULL,
    at TEXT NOT NULL,
    author TEXT NOT NULL,
    password TEXT NOT NULL,
    complexity REAL NOT NULL,
    duration REAL NOT NULL
)
''')
conn.commit()

def store(mask, hash, algorithm, author, password, complexity, duration):
    at = datetime.utcnow().isoformat()
    cursor.execute('''
        INSERT INTO work (mask, hash, algorithm, at, author, password, complexity, duration)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (mask, hash, algorithm, at, author, password, complexity, duration))
    conn.commit()

def exists(mask, hash, algorithm):
    cursor.execute('''
        SELECT 1 FROM work
        WHERE mask = ? AND hash = ? AND algorithm = ?
        LIMIT 1
    ''', (mask, hash, algorithm))
    return cursor.fetchone() is not None    

def estimated_time(author, algorithm, target_complexity):
    cursor.execute('''
        SELECT complexity, duration
        FROM work
        WHERE author = ?
        AND algorithm = ?
        ORDER BY id DESC
        LIMIT 1
    ''', (author,algorithm,))
    
    row = cursor.fetchone()
    if row is None:
        return 0

    base_complexity, base_duration = row  # base_duration should be in seconds
    #print("base_complexity:", base_complexity)
    #print("base_duration:", base_duration)
    #print("target_complexity:", target_complexity)
    return (target_complexity * base_duration) / base_complexity

def get_all_passwords():
    cursor.execute('''
        SELECT password FROM work
        WHERE password != 0
    ''')
    rows = cursor.fetchall()
    passwords = [row[0] for row in rows]
    return ', '.join(passwords)