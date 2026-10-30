import sqlite3

DB_NAME = "expenses.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(date, type, category, amount, description):
    conn = get_connection()
    conn.execute(
        "INSERT INTO transactions (date, type, category, amount, description) VALUES (?, ?, ?, ?, ?)",
        (date, type, category, amount, description)
    )
    conn.commit()
    conn.close()

def get_transactions():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM transactions ORDER BY date DESC"
    ).fetchall()
    conn.close()
    return rows

create_table()