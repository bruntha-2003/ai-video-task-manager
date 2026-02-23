from database import get_connection
from datetime import date


def validate_user(username, password):
    
    conn = get_connection()
    row  = conn.execute(
        "SELECT * FROM USER_TABLE WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    conn.close()
    return row is not None




def add_task(lesson_id, assigned_to, start_date, due_date, status):
    
    conn = get_connection()
    conn.execute(
        "INSERT INTO TASK_ITEM_TABLE (lesson_id, assigned_to, start_date, due_date, status) VALUES (?,?,?,?,?)",
        (lesson_id, assigned_to, start_date, due_date, status)
    )
    conn.commit()
    conn.close()

def update_task(task_id, lesson_id, assigned_to, start_date, due_date, status):
    
    conn = get_connection()
    conn.execute(
        "UPDATE TASK_ITEM_TABLE SET lesson_id=?, assigned_to=?, start_date=?, due_date=?, status=? WHERE task_item_id=?",
        (lesson_id, assigned_to, start_date, due_date, status, task_id)
    )
    conn.commit()
    conn.close()

def delete_task(task_id):
    
    conn = get_connection()
    conn.execute("DELETE FROM TASK_ITEM_TABLE WHERE task_item_id=?", (task_id,))
    conn.commit()
    conn.close()

def get_all_tasks():
   
    conn = get_connection()
    rows = conn.execute("SELECT * FROM TASK_ITEM_TABLE").fetchall()
    conn.close()
    return rows

def search_task(task_id):
    
    conn = get_connection()
    row  = conn.execute("SELECT * FROM TASK_ITEM_TABLE WHERE task_item_id=?", (task_id,)).fetchone()
    conn.close()
    return row




def add_stage(task_item_id, stage_name, stage_status, last_updated_date, status):
    
    conn = get_connection()
    conn.execute(
        "INSERT INTO TASK_STAGE_TABLE (task_item_id, stage_name, stage_status, last_updated_date, status) VALUES (?,?,?,?,?)",
        (task_item_id, stage_name, stage_status, last_updated_date, status)
    )
    conn.commit()
    conn.close()

def get_all_stages():
    
    conn = get_connection()
    rows = conn.execute(
        "SELECT stage_id, task_item_id, stage_status, last_updated_date, status FROM TASK_STAGE_TABLE"
    ).fetchall()
    conn.close()
    return rows



def get_report():
    
    conn = get_connection()
    rows = conn.execute("""
        SELECT
            ts.stage_id,
            ti.task_item_id,
            ti.due_date,
            ts.last_updated_date,
            ts.stage_status
        FROM TASK_STAGE_TABLE ts
        JOIN TASK_ITEM_TABLE  ti
          ON ts.task_item_id = ti.task_item_id
    """).fetchall()
    conn.close()
    return rows


def log_reminder(task_item_id, lesson_id, reminder_type):
    """Insert a reminder log record."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO REMINDER_LOG (task_item_id, lesson_id, reminder_type, logged_date) VALUES (?,?,?,?)",
        (task_item_id, lesson_id, reminder_type, str(date.today()))
    )
    conn.commit()
    conn.close()

def get_overdue_tasks():
    
    conn = get_connection()
    rows = conn.execute(
        "SELECT task_item_id, lesson_id, due_date, status FROM TASK_ITEM_TABLE"
    ).fetchall()
    conn.close()
    return rows
