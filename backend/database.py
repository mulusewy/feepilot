import sqlite3

DATABASE_URL = "sqlite:///./feepilot.db"

def create_db_and_tables():
    with sqlite3.connect(DATABASE_URL.replace("sqlite:///./", "")) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracking_scripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                script_name TEXT NOT NULL UNIQUE,
                script_code TEXT NOT NULL
            )
        """)
        conn.commit()

if __name__ == "__main__":
    create_db_and_tables()
