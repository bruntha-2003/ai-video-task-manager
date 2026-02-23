import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


SENDER_EMAIL    = "yourmail@gmail.com"
SENDER_PASSWORD = "your_app_password"
SMTP_HOST       = "smtp.gmail.com"
SMTP_PORT       = 587


def send_email(to_email, subject, body):
    
    try:
        msg = MIMEMultipart()
        msg["From"]    = SENDER_EMAIL
        msg["To"]      = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()

        print(f"[EMAIL] Sent to {to_email} — Subject: {subject}")
        return True

    except Exception as e:
        print(f"[EMAIL] Failed to send: {e}")
        return False


def send_task_reminder_email(to_email, task_id, lesson_id, days_overdue):
    
    subject = f"[TrackBot] Task Reminder — Task ID {task_id}"
    body    = f"""
Dear Content Creator,

This is an automated reminder from TrackBot.

Your assigned AI video task is overdue.

  Task ID   : {task_id}
  Lesson ID : {lesson_id}
  Days Late : {days_overdue} day(s)

Please update your task status as soon as possible.

Regards,
TrackBot — AI Video Task Management System
"""
    return send_email(to_email, subject, body)
