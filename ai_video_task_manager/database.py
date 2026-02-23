import sqlite3

DATABASE_NAME = "taskbot.db"

def get_connection():
   
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():

    conn = get_connection()
    c = conn.cursor()

    
    c.execute("""
        CREATE TABLE IF NOT EXISTS USER_TABLE (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS TASK_ITEM_TABLE (
            task_item_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id      TEXT,
            assigned_to    TEXT,
            start_date     TEXT,
            due_date       TEXT,
            status         TEXT DEFAULT 'Pending'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS TASK_STAGE_TABLE (
            stage_id          INTEGER PRIMARY KEY AUTOINCREMENT,
            task_item_id      INTEGER,
            stage_name        TEXT,
            stage_status      TEXT DEFAULT 'Pending',
            last_updated_date TEXT,
            status            TEXT DEFAULT 'Active',
            FOREIGN KEY (task_item_id) REFERENCES TASK_ITEM_TABLE(task_item_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS REMINDER_LOG (
            log_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            task_item_id  INTEGER,
            lesson_id     TEXT,
            reminder_type TEXT,
            logged_date   TEXT
        )
    """)

    
    c.execute("INSERT OR IGNORE INTO USER_TABLE VALUES ('admin',  'admin123')")
    c.execute("INSERT OR IGNORE INTO USER_TABLE VALUES ('bruntha','pass123')")

    conn.commit()
    conn.close()
    print("[DB] Database initialized successfully.")
