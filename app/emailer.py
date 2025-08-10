# app/emailer.py
from app.config import settings

def send_email(to_email: str, subject: str, body: str):
    # Simulated email sending for demo/deployment on Vercel
    print("=" * 50)
    print("📧 Simulated Email Sent")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print("=" * 50)
    return {"status": "success", "message": "Simulated email sent"}

# Keep the old SMTP function for reference
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_smtp(to_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        if settings.SMTP_USE_TLS:
            server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM, to_email, msg.as_string())
"""
