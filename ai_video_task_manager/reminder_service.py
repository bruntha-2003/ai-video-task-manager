from datetime import datetime, date
from models import get_overdue_tasks, log_reminder
from email_service import send_task_reminder_email


def check_and_send_reminders(log_callback=None):
    

    def log(msg):
        if log_callback:
            log_callback(msg)
        else:
            print(msg)

    today  = date.today()
    tasks  = get_overdue_tasks()
    found  = False

    log(f"\n{'='*55}")
    log(f"  Reminder Check — {today}")
    log(f"{'='*55}")

    for row in tasks:
        task_id   = row["task_item_id"]
        lesson_id = row["lesson_id"]
        due_str   = row["due_date"]
        status    = row["status"]

        try:
            due = datetime.strptime(due_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            log(f"  [SKIP] Task {task_id} — invalid due date: {due_str}")
            continue

        
        if today <= due or status == "Completed":
            continue

        found      = True
        days_late  = (today - due).days

        log(f"\n  Task ID  : {task_id}")
        log(f"  Lesson   : {lesson_id}")
        log(f"  Due Date : {due}  |  Days Overdue: {days_late}")

       
        log("   Email Reminder — triggered")
        log_reminder(task_id, lesson_id, "EMAIL")
        
        
        if days_late >= 2:
            log("   WhatsApp Reminder — logged in DB")
            log_reminder(task_id, lesson_id, "WHATSAPP")

        if days_late >= 5:
            log("   IVR Call — logged in DB")
            log_reminder(task_id, lesson_id, "IVR")

    if not found:
        log("\n    All tasks are on time. No reminders needed.")

    log(f"\n{'='*55}\n")
